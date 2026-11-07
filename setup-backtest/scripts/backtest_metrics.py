#!/usr/bin/env python3
"""Métricas de uma lista de trades + Monte Carlo (ordem embaralhada e reamostragem).

Entrada: CSV com uma linha por trade. Separador vírgula, ponto e vírgula ou tab
(detectado pelo cabeçalho); texto em UTF-8 ou Windows-1252 (Excel em português).

O resultado de cada trade sai da primeira opção disponível na linha:
  1. coluna `r`: resultado em múltiplos de R. Aceita 2 | 2,0 | -1R | 1.5r
  2. colunas `entrada`, `stop` e `saida`: r = (saida - entrada) / (entrada - stop)
     Vale para compra e venda sem coluna `lado` (o stop diz o lado).
  3. coluna `pnl` (dinheiro) dividida pela coluna `risco` da linha, ou por --risco
Coluna opcional `data`: ordena os trades e agrupa por mês. Aceita 2026-08-03,
03/08/2026 e 03/08/26 (com barra, sempre dia/mês/ano), com ou sem hora.
Nomes em português e variações comuns são reconhecidos (ex.: "Resultado (R)",
"Lucro", "Saída", "P&L"). Qualquer outra coluna é ignorada.

Uso:
  python backtest_metrics.py trades.csv
  python backtest_metrics.py trades.csv --custo 0.05 --ruina 20
  python backtest_metrics.py trades.csv --risco 150             # pnl em R$, risco fixo de 150
  python backtest_metrics.py trades.csv --fora-da-amostra 0.3   # últimos 30% como validação
  python backtest_metrics.py trades.csv --col-r "Resultado em R" # aponta a coluna na mão
  python backtest_metrics.py trades.csv --json

Só depende da biblioteca padrão.
"""
import argparse
import csv
import json
import math
import random
import re
import statistics
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime

# Console do Windows usa cp1252 por padrao; forca UTF-8 pra nao quebrar acentos.
for _fluxo in (sys.stdout, sys.stderr):
    if hasattr(_fluxo, "reconfigure"):
        _fluxo.reconfigure(encoding="utf-8", errors="replace")

# Nomes aceitos por coluna, já normalizados (sem acento, minúsculo, só letras e números).
# A ordem da lista é a prioridade quando o CSV tem mais de um nome parecido.
ALIASES = {
    "r": ["r", "resultador", "resultadoemr", "rmultiplo", "rmultiple", "multiplor", "resultadoemmultiplosder"],
    "entrada": ["entrada", "precoentrada", "precodeentrada", "entry", "entryprice"],
    "stop": ["stop", "stopinicial", "stoploss", "precostop", "sl", "initialstop"],
    "saida": ["saida", "precosaida", "precodesaida", "saidamedia", "exit", "exitprice"],
    "pnl": ["pnl", "pl", "lucro", "lucroprejuizo", "resultadors", "resultadoemrs", "resultadoreais",
            "resultadofinanceiro", "financeiro", "rs", "profit"],
    "risco": ["risco", "riscors", "riscoemrs", "riscoinicial", "riscoreais", "risk"],
    "data": ["data", "date", "datahora", "datetime", "dataentrada", "datadeentrada"],
}

# "1.250" ou "R$ 12.500": ponto como separador de milhar, comum em planilha brasileira.
MILHAR = re.compile(r"^\(?-?\s*(R\$)?\s*\d{1,3}(\.\d{3})+\)?$", re.IGNORECASE)

FORMATOS_DATA = ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%Y/%m/%d", "%d-%m-%Y", "%d.%m.%Y")


def norm(nome):
    s = unicodedata.normalize("NFKD", nome or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower().replace("r$", "rs")  # "R$" é dinheiro: não pode virar a coluna `r`
    return re.sub(r"[^a-z0-9]", "", s)


def numero(txt):
    """Texto de planilha -> float, ou None se vazio/ilegível."""
    s = (txt or "").strip()
    if not s:
        return None
    negativo = False
    if s.startswith("(") and s.endswith(")"):  # formato contábil: (150,00) = -150
        negativo, s = True, s[1:-1]
    s = s.replace("−", "-").replace(" ", "").replace(" ", "")
    s = re.sub(r"(?i)r\$", "", s)
    if s[-1:] in ("R", "r"):  # "2R", "-1r"
        s = s[:-1]
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):  # 1.250,50 (Brasil)
            s = s.replace(".", "").replace(",", ".")
        else:  # 1,250.50 (EUA)
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        v = float(s)
    except ValueError:
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return -v if negativo else v


def ler_data(txt):
    s = (txt or "").strip().replace("T", " ")
    if not s:
        return None
    pedacos = s.split()
    dia = pedacos[0]
    hora = pedacos[1][:8] if len(pedacos) > 1 else ""
    for f in FORMATOS_DATA:
        try:
            d = datetime.strptime(dia, f)
        except ValueError:
            continue
        for fh in ("%H:%M:%S", "%H:%M"):
            try:
                t = datetime.strptime(hora, fh)
                return d.replace(hour=t.hour, minute=t.minute, second=t.second)
            except ValueError:
                pass
        return d
    return None


def ler_tabela(path):
    """Devolve (DictReader, quantas linhas do topo do arquivo foram puladas)."""
    with open(path, "rb") as f:
        bruto = f.read()
    texto = None
    for enc in ("utf-8-sig", "cp1252", "latin-1"):  # latin-1 nunca falha
        try:
            texto = bruto.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    linhas = texto.splitlines()
    pulados = 0
    while linhas and not linhas[0].strip():
        linhas.pop(0)
        pulados += 1
    if not linhas:
        sys.exit("arquivo vazio")
    sep = None
    if linhas[0].lower().startswith("sep="):  # dica que o Excel às vezes grava na 1ª linha
        sep = linhas[0][4:5] or ","
        linhas.pop(0)
        pulados += 1
    if sep is None:
        cab = linhas[0]
        if cab.count(";") > cab.count(","):
            sep = ";"
        elif cab.count("\t") > cab.count(","):
            sep = "\t"
        else:
            sep = ","
    return csv.DictReader(linhas, delimiter=sep), pulados


def achar_colunas(campos, forcadas):
    normais = {}
    for c in campos:
        normais.setdefault(norm(c), c)
    mapa = {}
    for chave, nomes in ALIASES.items():
        if forcadas.get(chave):
            alvo = norm(forcadas[chave])
            if alvo not in normais:
                sys.exit(f"coluna `{forcadas[chave]}` não existe no CSV. Colunas lidas: {', '.join(campos)}")
            mapa[chave] = normais[alvo]
            continue
        for n in nomes:
            if n in normais:
                mapa[chave] = normais[n]
                break
    return mapa


def resumo_linhas(nums, limite=12):
    txt = ", ".join(str(n) for n in nums[:limite])
    return txt + (f" e mais {len(nums) - limite}" if len(nums) > limite else "")


def carregar(path, a):
    leitor, pulados = ler_tabela(path)
    campos = [c for c in (leitor.fieldnames or []) if c is not None]
    col = achar_colunas(campos, {"r": a.col_r, "pnl": a.col_pnl, "data": a.col_data})
    tem_precos = all(k in col for k in ("entrada", "stop", "saida"))
    if "r" not in col and not tem_precos and "pnl" not in col:
        sys.exit(
            "não achei o resultado dos trades. O CSV precisa de uma destas opções:\n"
            "  coluna `r` (resultado em R), ou\n"
            "  colunas `entrada`, `stop` e `saida`, ou\n"
            "  coluna `pnl` (dinheiro) com coluna `risco` ou o parâmetro --risco.\n"
            f"Colunas lidas: {', '.join(campos) or '(nenhuma)'}\n"
            "Se o nome for outro, aponte com --col-r ou --col-pnl."
        )
    if "pnl" in col and "r" not in col and not tem_precos and "risco" not in col and not a.risco:
        sys.exit("coluna `pnl` sem coluna `risco` e sem --risco: não dá para converter dinheiro em R")

    trades, ignoradas, suspeitas = [], [], 0
    origem = defaultdict(int)
    for row in leitor:
        num = leitor.line_num + pulados  # linha real no arquivo, mesmo com linhas em branco no meio
        v = None
        if "r" in col:
            v = numero(row.get(col["r"]))
            if v is not None:
                origem["coluna r"] += 1
        if v is None and tem_precos:
            e, s, x = (numero(row.get(col[k])) for k in ("entrada", "stop", "saida"))
            if None not in (e, s, x) and e != s:
                v = (x - e) / (e - s)
                origem["entrada/stop/saida"] += 1
        if v is None and "pnl" in col:
            txt_pnl = row.get(col["pnl"])
            p = numero(txt_pnl)
            risco = numero(row.get(col["risco"])) if "risco" in col else None
            if not risco:
                risco = a.risco
            if p is not None and risco:
                v = p / abs(risco)
                origem["pnl/risco"] += 1
                if MILHAR.match((txt_pnl or "").strip()):
                    suspeitas += 1
        if v is None:
            if any(isinstance(val, str) and val.strip() for val in row.values()):
                ignoradas.append(num)
            continue
        v -= a.custo
        d_txt = (row.get(col["data"]) or "").strip() if "data" in col else ""
        trades.append({"r": v, "data": ler_data(d_txt), "linha": num})

    if not trades:
        sys.exit("nenhum trade válido no arquivo")

    avisos = []
    if ignoradas:
        avisos.append(f"{len(ignoradas)} linha(s) ignorada(s) por resultado vazio ou ilegível (linhas {resumo_linhas(ignoradas)})")
    if suspeitas:
        avisos.append(
            f"{suspeitas} valor(es) de pnl parecem usar ponto como milhar (ex.: 1.250). "
            "Se for R$ 1.250, grave como 1250 ou 1.250,00 e rode de novo"
        )
    datas = [t["data"] for t in trades]
    if "data" not in col:
        avisos.append("sem coluna de data: a ordem do arquivo foi tratada como a ordem real dos trades")
    elif all(d is not None for d in datas):
        pares = list(zip(datas, datas[1:]))
        crescente = all(x <= y for x, y in pares)
        decrescente = all(x >= y for x, y in pares)
        if decrescente and not crescente:
            trades.reverse()
            avisos.append("o arquivo estava do mais novo para o mais antigo; a ordem foi invertida")
        elif not crescente:
            trades.sort(key=lambda t: t["data"])  # sort estável: mantém a ordem do arquivo no mesmo dia
            avisos.append("datas fora de ordem: os trades foram ordenados por data (a ordem muda o drawdown)")
    else:
        faltam = sum(1 for d in datas if d is None)
        avisos.append(f"{faltam} data(s) vazia(s) ou ilegível(is): a ordem do arquivo foi mantida e o resultado por mês fica incompleto")
    return trades, avisos, dict(origem)


def drawdown(seq):
    """Maior queda da curva acumulada (em R, negativa) e maior número de trades abaixo do pico."""
    pico = eq = max_dd = 0.0
    dur = max_dur = 0
    for r in seq:
        eq += r
        if eq >= pico:
            pico = eq
            dur = 0
        else:
            dur += 1
            max_dur = max(max_dur, dur)
        max_dd = min(max_dd, eq - pico)
    return max_dd, max_dur


def streaks(seq):
    best_w = best_l = cur_w = cur_l = 0
    for r in seq:
        if r > 0:
            cur_w += 1
            cur_l = 0
        elif r < 0:
            cur_l += 1
            cur_w = 0
        best_w = max(best_w, cur_w)
        best_l = max(best_l, cur_l)
    return best_w, best_l


def metricas(rs):
    n = len(rs)
    ganhos = [r for r in rs if r > 0]
    perdas = [r for r in rs if r < 0]
    exp = statistics.mean(rs)
    sd = statistics.stdev(rs) if n > 1 else 0.0  # desvio amostral
    avg_w = statistics.mean(ganhos) if ganhos else 0.0
    avg_l = statistics.mean(perdas) if perdas else 0.0
    payoff = (avg_w / abs(avg_l)) if avg_l else float("inf")
    pf = (sum(ganhos) / abs(sum(perdas))) if perdas else float("inf")
    max_dd, dd_dur = drawdown(rs)
    bw, bl = streaks(rs)
    ep = sd / math.sqrt(n) if n > 1 else None
    taxa_perda = len(perdas) / n
    # Maior sequência de perdas que o acaso já produz (aprox. de Schilling): log_{1/q}(n(1-q))
    seq_acaso = None
    if 0 < taxa_perda < 1 and n * (1 - taxa_perda) > 1:
        seq_acaso = math.log(n * (1 - taxa_perda)) / math.log(1 / taxa_perda)
    ordenados = sorted(rs, reverse=True)
    return {
        "trades": n,
        "win_rate": len(ganhos) / n,
        "taxa_perda": taxa_perda,
        "zerados": n - len(ganhos) - len(perdas),
        "ganho_medio_R": avg_w,
        "perda_media_R": avg_l,
        "payoff": payoff,
        "win_rate_empate": 1 / (1 + payoff),  # acerto mínimo pra empatar com este payoff
        "expectancia_R": exp,
        "desvio_padrao_R": sd,
        "erro_padrao_R": ep,
        "expectancia_ic95_aprox_R": [exp - 1.96 * ep, exp + 1.96 * ep] if ep else None,
        "trades_para_ic95_acima_de_zero": math.ceil((1.96 * sd / exp) ** 2) if (sd and exp > 0) else None,
        "profit_factor": pf,
        "resultado_total_R": sum(rs),
        "expectancia_sem_3_melhores_R": statistics.mean(ordenados[3:]) if n > 3 else None,
        "max_drawdown_R": max_dd,
        "max_trades_em_drawdown": dd_dur,
        "maior_sequencia_ganhos": bw,
        "maior_sequencia_perdas": bl,
        "sequencia_perdas_do_acaso": seq_acaso,
        "sqn": (math.sqrt(n) * exp / sd) if sd else None,
        "sqn_n_ate_100": (math.sqrt(min(n, 100)) * exp / sd) if sd else None,
    }


def percentil(ordenados, p):
    if not ordenados:
        return None
    i = int(round(p * (len(ordenados) - 1)))
    return ordenados[max(0, min(len(ordenados) - 1, i))]


def monte_carlo(rs, n_sim, ruina, rng):
    """Dois métodos, ambos supondo trades independentes e risco fixo em R por trade.

    ordem: embaralha os MESMOS trades. Resultado final igual em toda simulação;
           mede só o risco da sequência ruim vir primeiro (drawdown).
    reamostragem: sorteia n trades COM reposição (bootstrap). Mede também a incerteza
           da própria amostra: faixa do resultado e da expectância.
    """
    n = len(rs)
    seq = list(rs)
    dd_ordem, dd_boot, finais, medias = [], [], [], []
    ruina_ordem = ruina_boot = 0
    for _ in range(n_sim):
        rng.shuffle(seq)
        dd, _ = drawdown(seq)
        dd_ordem.append(dd)
        if ruina is not None and dd <= ruina:
            ruina_ordem += 1
        amostra = rng.choices(rs, k=n)
        dd2, _ = drawdown(amostra)
        dd_boot.append(dd2)
        tot = sum(amostra)
        finais.append(tot)
        medias.append(tot / n)
        if ruina is not None and dd2 <= ruina:
            ruina_boot += 1
    dd_ordem.sort()
    dd_boot.sort()
    finais.sort()
    medias.sort()
    return {
        "simulacoes": n_sim,
        "limite_ruina_R": ruina,
        "ordem": {
            "drawdown_mediano_R": percentil(dd_ordem, 0.5),
            "drawdown_5pct_piores_R": percentil(dd_ordem, 0.05),
            "drawdown_pior_R": dd_ordem[0],
            "prob_ruina": (ruina_ordem / n_sim) if ruina is not None else None,
        },
        "reamostragem": {
            "drawdown_mediano_R": percentil(dd_boot, 0.5),
            "drawdown_5pct_piores_R": percentil(dd_boot, 0.05),
            "resultado_p5_R": percentil(finais, 0.05),
            "resultado_mediano_R": percentil(finais, 0.5),
            "resultado_p95_R": percentil(finais, 0.95),
            "expectancia_ic95_R": [percentil(medias, 0.025), percentil(medias, 0.975)],
            "prob_resultado_negativo": sum(1 for f in finais if f <= 0) / n_sim,
            "prob_ruina": (ruina_boot / n_sim) if ruina is not None else None,
        },
    }


def por_mes(trades):
    grupos = defaultdict(list)
    for t in trades:
        chave = t["data"].strftime("%Y-%m") if t["data"] else "sem data"
        grupos[chave].append(t["r"])
    linhas = []
    for k in sorted(grupos):
        rs = grupos[k]
        linhas.append((k, len(rs), sum(rs), sum(1 for r in rs if r > 0) / len(rs)))
    return linhas


def dividir(rs, frac):
    k = int(round(len(rs) * (1 - frac)))
    dentro, fora = rs[:k], rs[k:]
    if len(dentro) < 2 or len(fora) < 2:
        return None
    return {"dentro": metricas(dentro), "fora": metricas(fora)}


def fmt(x, casas=2):
    if x is None:
        return "n/d"
    if isinstance(x, float):
        if math.isinf(x):
            return "inf (sem perdas)"
        return f"{x:.{casas}f}"
    return str(x)


def pct(x):
    return "n/d" if x is None else f"{x * 100:.1f}%"


def imprimir(m, mc, meses, avisos, origem, custo, div):
    print(f"TRADES: {m['trades']}  (origem: {', '.join(f'{k} {v}' for k, v in origem.items())})")
    print(f"Custo descontado: {fmt(custo, 3)}R por trade" if custo else "Custo descontado: nenhum (se os R vieram sem custo, use --custo)")
    if avisos:
        print("Avisos:")
        for av in avisos:
            print(f"  - {av}")
    if m["trades"] < 30:
        print(f"  - amostra de {m['trades']} trades: não conclui nada, serve para achar erro na regra")
    elif m["trades"] < 100:
        print(f"  - amostra de {m['trades']} trades: dá a direção, com erro grande; trate como indicativo")

    print("\nRESULTADO (em R)")
    ic = m["expectancia_ic95_aprox_R"]
    ic_txt = f"  (IC 95% aprox.: {fmt(ic[0], 3)} a {fmt(ic[1], 3)})" if ic else ""
    print(f"  Expectância: {fmt(m['expectancia_R'], 3)}R por trade{ic_txt}")
    print(f"  Win rate: {pct(m['win_rate'])}  (empata com {pct(m['win_rate_empate'])} neste payoff)  zerados: {m['zerados']}")
    print(f"  Payoff: {fmt(m['payoff'])}   Profit factor: {fmt(m['profit_factor'])}")
    print(f"  Ganho médio: {fmt(m['ganho_medio_R'])}R   Perda média: {fmt(m['perda_media_R'])}R   Desvio: {fmt(m['desvio_padrao_R'])}R")
    print(f"  Resultado total: {fmt(m['resultado_total_R'])}R   Expectância sem os 3 melhores: {fmt(m['expectancia_sem_3_melhores_R'], 3)}R")
    print(f"  SQN: {fmt(m['sqn'])}   SQN com n limitado a 100 (para comparar): {fmt(m['sqn_n_ate_100'])}")
    if m["trades_para_ic95_acima_de_zero"]:
        print(f"  Trades para afirmar expectância > 0 com ~95%: cerca de {m['trades_para_ic95_acima_de_zero']}")

    print("\nRISCO")
    print(f"  Max drawdown: {fmt(m['max_drawdown_R'])}R  ({m['max_trades_em_drawdown']} trades abaixo do pico, no pior trecho)")
    acaso = m["sequencia_perdas_do_acaso"]
    acaso_txt = f"  (o acaso sozinho já daria cerca de {acaso:.0f})" if acaso else ""
    print(f"  Sequências: {m['maior_sequencia_ganhos']} ganhos / {m['maior_sequencia_perdas']} perdas seguidas{acaso_txt}")

    if mc:
        o, b = mc["ordem"], mc["reamostragem"]
        print(f"\nMONTE CARLO ({mc['simulacoes']} simulações; supõe trades independentes e risco fixo em R)")
        print(f"  Ordem embaralhada (mesmos trades): DD mediano {fmt(o['drawdown_mediano_R'])}R | 5% piores {fmt(o['drawdown_5pct_piores_R'])}R | pior {fmt(o['drawdown_pior_R'])}R")
        print(f"  Reamostragem com reposição: DD mediano {fmt(b['drawdown_mediano_R'])}R | 5% piores {fmt(b['drawdown_5pct_piores_R'])}R")
        print(f"    resultado p5 / mediano / p95: {fmt(b['resultado_p5_R'])} / {fmt(b['resultado_mediano_R'])} / {fmt(b['resultado_p95_R'])}R")
        print(f"    expectância IC 95%: {fmt(b['expectancia_ic95_R'][0], 3)} a {fmt(b['expectancia_ic95_R'][1], 3)}R   resultado <= 0 em {pct(b['prob_resultado_negativo'])}")
        if mc["limite_ruina_R"] is not None:
            print(f"  Chance de tocar {fmt(mc['limite_ruina_R'])}R: ordem {pct(o['prob_ruina'])} | reamostragem {pct(b['prob_ruina'])}")

    if meses and len(meses) > 1:
        print("\nPOR MÊS")
        for k, n, tot, wr in meses:
            print(f"  {k}: {n:3d} trades  {tot:+7.2f}R  wr {wr * 100:.0f}%")
        validos = [x for x in meses if x[0] != "sem data"]
        positivos = sum(1 for _, _, tot, _ in validos if tot > 0)
        print(f"  meses positivos: {positivos}/{len(validos)}")
        if validos and min(x[1] for x in validos) < 10:
            print("  (há mês com menos de 10 trades: a contagem de meses positivos fica frágil)")

    if div:
        d, f = div["dentro"], div["fora"]
        print("\nDENTRO x FORA DA AMOSTRA (só vale se as regras foram fechadas olhando só a 1ª parte)")
        print(f"  dentro: {d['trades']} trades, expectância {fmt(d['expectancia_R'], 3)}R, PF {fmt(d['profit_factor'])}, DD {fmt(d['max_drawdown_R'])}R")
        print(f"  fora:   {f['trades']} trades, expectância {fmt(f['expectancia_R'], 3)}R, PF {fmt(f['profit_factor'])}, DD {fmt(f['max_drawdown_R'])}R")
        if d["expectancia_R"] > 0 and f["expectancia_R"] < d["expectancia_R"] / 2:
            print("  alerta: fora da amostra a expectância caiu mais da metade (sinal de ajuste ao passado)")


def limpar(x):
    """Deixa o JSON válido: inf vira texto, NaN vira null."""
    if isinstance(x, float):
        if math.isnan(x):
            return None
        if math.isinf(x):
            return "inf" if x > 0 else "-inf"
        return x
    if isinstance(x, dict):
        return {k: limpar(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [limpar(v) for v in x]
    return x


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--risco", type=float, help="risco fixo por trade em dinheiro, para converter pnl em R")
    p.add_argument("--custo", type=float, default=0.0, help="custo + slippage por trade, em R, a descontar (ex.: 0.05)")
    p.add_argument("--mc", type=int, default=2000, help="simulações de Monte Carlo (0 desliga)")
    p.add_argument("--ruina", type=float, help="drawdown em R que o trader considera intolerável (ex.: 20 ou -20)")
    p.add_argument("--fora-da-amostra", type=float, default=0.0, help="fração final dos trades usada como validação (ex.: 0.3)")
    p.add_argument("--col-r", help="nome da coluna com o resultado em R, se não for reconhecida")
    p.add_argument("--col-pnl", help="nome da coluna com o resultado em dinheiro, se não for reconhecida")
    p.add_argument("--col-data", help="nome da coluna de data, se não for reconhecida")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.custo < 0:
        sys.exit("--custo é o custo por trade em R e é positivo (ex.: 0.05)")
    if not 0 <= a.fora_da_amostra < 1:
        sys.exit("--fora-da-amostra é uma fração entre 0 e 1 (ex.: 0.3)")
    ruina = -abs(a.ruina) if a.ruina is not None else None  # aceita 20 ou -20

    rng = random.Random(a.seed)
    trades, avisos, origem = carregar(a.csv, a)
    rs = [t["r"] for t in trades]
    m = metricas(rs)
    mc = monte_carlo(rs, a.mc, ruina, rng) if a.mc > 0 and len(rs) > 1 else None
    meses = por_mes(trades)
    div = dividir(rs, a.fora_da_amostra) if a.fora_da_amostra else None

    if a.json:
        saida = {"avisos": avisos, "origem": origem, "custo_R": a.custo, "metricas": m,
                 "monte_carlo": mc, "por_mes": meses, "dentro_fora": div}
        print(json.dumps(limpar(saida), ensure_ascii=False, indent=2, default=str))
    else:
        imprimir(m, mc, meses, avisos, origem, a.custo, div)


if __name__ == "__main__":
    main()
