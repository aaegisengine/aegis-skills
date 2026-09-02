#!/usr/bin/env python3
"""Métricas de uma lista de trades + simulação de Monte Carlo.

Entrada: CSV com uma linha por trade. Colunas aceitas (case-insensitive):
  - `r`        → resultado em múltiplos de R (preferido)
  - `pnl`      → resultado em dinheiro; use --risco para converter em R
  - `data` ou `date` (opcional) → para agrupar por mês e ordenar
  - qualquer outra coluna é ignorada (setup, ativo, obs...)

Uso:
  python backtest_metrics.py trades.csv
  python backtest_metrics.py trades.csv --risco 150          # pnl em R$ com risco fixo de 150
  python backtest_metrics.py trades.csv --custo 0.05         # desconta 0,05R por trade (custos/slippage)
  python backtest_metrics.py trades.csv --mc 5000 --ruina -20 # Monte Carlo, ruína em -20R
  python backtest_metrics.py trades.csv --json               # saída em JSON

Só depende da biblioteca padrão.
"""
import argparse
import csv
import json
import math
import random
import statistics
import sys
from collections import defaultdict

# Console do Windows usa cp1252 por padrao; forca UTF-8 pra nao quebrar em "->"/acentos.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def carregar(path, risco, custo):
    trades = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = {c.lower().strip(): c for c in reader.fieldnames or []}
        col_r = cols.get("r")
        col_pnl = cols.get("pnl")
        col_data = cols.get("data") or cols.get("date")
        if not col_r and not col_pnl:
            sys.exit("CSV precisa de coluna `r` (resultado em R) ou `pnl` (dinheiro, com --risco)")
        if col_pnl and not col_r and not risco:
            sys.exit("coluna `pnl` sem --risco: não dá para converter em R")
        for row in reader:
            raw = row[col_r] if col_r else row[col_pnl]
            raw = (raw or "").strip().replace(",", ".")
            if raw == "":
                continue
            try:
                v = float(raw)
            except ValueError:
                continue
            if not col_r:
                v = v / risco
            v -= custo
            trades.append({"r": v, "data": (row.get(col_data) or "").strip() if col_data else ""})
    if not trades:
        sys.exit("nenhum trade válido no arquivo")
    return trades


def drawdown(seq):
    pico = 0.0
    eq = 0.0
    max_dd = 0.0
    dur = 0
    max_dur = 0
    for r in seq:
        eq += r
        if eq > pico:
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
    wr = len(ganhos) / n
    avg_w = statistics.mean(ganhos) if ganhos else 0.0
    avg_l = statistics.mean(perdas) if perdas else 0.0
    exp = statistics.mean(rs)
    sd = statistics.pstdev(rs) if n > 1 else 0.0
    pf = (sum(ganhos) / abs(sum(perdas))) if perdas else float("inf")
    max_dd, dd_dur = drawdown(rs)
    bw, bl = streaks(rs)
    sqn = (math.sqrt(n) * exp / sd) if sd else 0.0
    return {
        "trades": n,
        "win_rate": wr,
        "ganho_medio_R": avg_w,
        "perda_media_R": avg_l,
        "payoff": (avg_w / abs(avg_l)) if avg_l else float("inf"),
        "expectancia_R": exp,
        "desvio_padrao_R": sd,
        "profit_factor": pf,
        "resultado_total_R": sum(rs),
        "max_drawdown_R": max_dd,
        "max_trades_em_drawdown": dd_dur,
        "maior_sequencia_ganhos": bw,
        "maior_sequencia_perdas": bl,
        "sqn": sqn,
    }


def monte_carlo(rs, n_sim, ruina):
    dds = []
    finais = []
    ruinas = 0
    seq = list(rs)
    for _ in range(n_sim):
        random.shuffle(seq)
        dd, _ = drawdown(seq)
        dds.append(dd)
        finais.append(sum(seq))
        if ruina is not None and dd <= ruina:
            ruinas += 1
    dds.sort()
    def pct(p):
        return dds[min(len(dds) - 1, int(p * len(dds)))]
    return {
        "simulacoes": n_sim,
        "drawdown_mediano_R": pct(0.5),
        "drawdown_p95_R": pct(0.05),  # 5% piores
        "drawdown_pior_R": dds[0],
        "prob_ruina": (ruinas / n_sim) if ruina is not None else None,
        "limite_ruina_R": ruina,
    }


def por_mes(trades):
    grupos = defaultdict(list)
    for t in trades:
        chave = t["data"][:7] if t["data"] else "sem data"
        grupos[chave].append(t["r"])
    linhas = []
    for k in sorted(grupos):
        rs = grupos[k]
        linhas.append((k, len(rs), sum(rs), sum(1 for r in rs if r > 0) / len(rs)))
    return linhas


def fmt(x, casas=2):
    if isinstance(x, float):
        if math.isinf(x):
            return "∞"
        return f"{x:.{casas}f}"
    return str(x)


def imprimir(m, mc, meses):
    print(f"Trades: {m['trades']}")
    if m["trades"] < 100:
        print(f"  (amostra pequena: com {m['trades']} trades o intervalo de confiança da expectância é largo — trate como indicativo)")
    print(f"Win rate: {m['win_rate'] * 100:.1f}%   Payoff: {fmt(m['payoff'])}   Profit factor: {fmt(m['profit_factor'])}")
    print(f"Ganho médio: {fmt(m['ganho_medio_R'])}R   Perda média: {fmt(m['perda_media_R'])}R")
    print(f"Expectância: {fmt(m['expectancia_R'], 3)}R por trade   Desvio: {fmt(m['desvio_padrao_R'])}R   SQN: {fmt(m['sqn'])}")
    print(f"Resultado total: {fmt(m['resultado_total_R'])}R")
    print(f"Max drawdown: {fmt(m['max_drawdown_R'])}R  ({m['max_trades_em_drawdown']} trades até novo pico)")
    print(f"Sequências: {m['maior_sequencia_ganhos']} ganhos / {m['maior_sequencia_perdas']} perdas seguidas")
    if mc:
        print(f"\nMonte Carlo ({mc['simulacoes']} embaralhamentos da mesma amostra):")
        print(f"  drawdown mediano: {fmt(mc['drawdown_mediano_R'])}R   5% piores: {fmt(mc['drawdown_p95_R'])}R   pior: {fmt(mc['drawdown_pior_R'])}R")
        if mc["prob_ruina"] is not None:
            print(f"  probabilidade de tocar {mc['limite_ruina_R']}R: {mc['prob_ruina'] * 100:.1f}%")
    if meses and len(meses) > 1:
        print("\nPor mês:")
        for k, n, tot, wr in meses:
            print(f"  {k}: {n:3d} trades  {tot:+7.2f}R  wr {wr * 100:.0f}%")
        positivos = sum(1 for _, _, tot, _ in meses if tot > 0)
        print(f"  meses positivos: {positivos}/{len(meses)}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--risco", type=float, help="risco fixo por trade, para converter pnl em R")
    p.add_argument("--custo", type=float, default=0.0, help="custo por trade em R a descontar (ex.: 0.05)")
    p.add_argument("--mc", type=int, default=2000, help="simulações de Monte Carlo (0 desliga)")
    p.add_argument("--ruina", type=float, help="drawdown em R que o trader considera ruína (ex.: -20)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    random.seed(a.seed)
    trades = carregar(a.csv, a.risco, a.custo)
    rs = [t["r"] for t in trades]
    m = metricas(rs)
    mc = monte_carlo(rs, a.mc, a.ruina) if a.mc and len(rs) > 1 else None
    meses = por_mes(trades)

    if a.json:
        print(json.dumps({"metricas": m, "monte_carlo": mc, "por_mes": meses}, ensure_ascii=False, indent=2, default=str))
    else:
        imprimir(m, mc, meses)


if __name__ == "__main__":
    main()
