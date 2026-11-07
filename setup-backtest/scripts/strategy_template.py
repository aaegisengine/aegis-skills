#!/usr/bin/env python3
"""Template de backtest por regras sobre candles OHLC.

Este arquivo é um PONTO DE PARTIDA, não um motor genérico. A regra de
exemplo é um rompimento de canal (compra quando o fechamento supera a máxima
dos últimos N candles) com stop e alvo por ATR e saída por tempo. Troque a
função `sinal()` e os parâmetros pela regra do trader. A estrutura em volta
(loop candle a candle, preenchimento conservador, custos, geração do CSV de
trades) fica.

Entrada: CSV com data, open, high, low, close (volume opcional), um candle por
linha. Aceita também os nomes em português (abertura, maxima, minima,
fechamento) e o formato do Excel brasileiro (ponto e vírgula, vírgula decimal).
Se os candles vierem do mais novo para o mais antigo, a ordem é invertida.

Saída: CSV de trades no formato que `backtest_metrics.py` lê (coluna `r`).

Uso:
  python strategy_template.py candles.csv --out trades.csv
  python strategy_template.py candles.csv --n 20 --atr-stop 1.5 --atr-alvo 3 --max-barras 10 --custo-r 0.05 --tick 5
  python strategy_template.py candles.csv --sep ";" --decimal ","

Depende de pandas.
"""
import argparse
import re
import sys
import unicodedata

# Console do Windows usa cp1252 por padrao; forca UTF-8 pra nao quebrar acentos.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pandas as pd
except ImportError:
    sys.exit("instale pandas: pip install pandas")

# ---------------------------------------------------------------------------
# PARÂMETROS: tudo que é número da regra fica aqui, nunca espalhado no código.
# Cada parâmetro da REGRA é um grau de liberdade para overfitting; quanto menos, melhor.
# `tick` e `custo_r` são de EXECUÇÃO (realismo), não da regra.
# ---------------------------------------------------------------------------
PADRAO = {
    "n": 20,          # janela do canal (candles)
    "atr_n": 14,      # período do ATR (média simples do true range; o ATR de Wilder suaviza diferente)
    "atr_stop": 1.5,  # stop = entrada - atr_stop * ATR (na compra)
    "atr_alvo": 3.0,  # alvo = entrada + atr_alvo * ATR (na compra)
    "max_barras": 10, # saída por tempo: fecha no fechamento do último candle permitido
    "custo_r": 0.0,   # custo + slippage por trade, em R (ex.: 0.05)
    "tick": 0.0,      # tamanho do tick: o alvo só conta se o preço passar 1 tick além dele
}

# Nomes de coluna aceitos (normalizados: sem acento, minúsculo, só letras e números).
COLUNAS = {
    "date": ["date", "data", "datahora", "datetime", "time", "timestamp"],
    "open": ["open", "abertura"],
    "high": ["high", "maxima", "max"],
    "low": ["low", "minima", "min"],
    "close": ["close", "fechamento", "ultimo"],
}


def norm(nome):
    s = unicodedata.normalize("NFKD", str(nome))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def detectar_sep(path):
    """Separador pelo cabeçalho + quantas linhas pular (dica `sep=` do Excel)."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        cab = f.readline()
        pular = 0
        if cab.lower().startswith("sep="):
            sep = cab[4:5] or ","
            return sep, 1
    if cab.count(";") > cab.count(","):
        return ";", pular
    if cab.count("\t") > cab.count(","):
        return "\t", pular
    return ",", pular


def ler_candles(a):
    sep, pular = detectar_sep(a.csv)
    if a.sep:
        sep = "\t" if a.sep in ("\\t", "tab") else a.sep
    dec = a.decimal or ("," if sep == ";" else ".")
    kwargs = {"sep": sep, "decimal": dec, "skiprows": pular}
    if dec == ",":
        kwargs["thousands"] = "."
    try:
        return pd.read_csv(a.csv, encoding="utf-8-sig", **kwargs)
    except UnicodeDecodeError:
        return pd.read_csv(a.csv, encoding="latin-1", **kwargs)


def padronizar(df):
    normais = {}
    for c in df.columns:
        normais.setdefault(norm(c), c)
    renomear = {}
    for alvo, nomes in COLUNAS.items():
        for n in nomes:
            if n in normais:
                renomear[normais[n]] = alvo
                break
    df = df.rename(columns=renomear)
    for c in ("open", "high", "low", "close"):
        if c not in df.columns:
            sys.exit(f"coluna `{c}` ausente (aceito também abertura, maxima, minima, fechamento). Colunas lidas: {list(df.columns)}")
        if not pd.api.types.is_numeric_dtype(df[c]):
            sys.exit(f"coluna `{c}` não é numérica. Confira o separador decimal com --decimal \",\" ou --decimal \".\"")
    df = df.dropna(subset=["open", "high", "low", "close"]).reset_index(drop=True)
    if "date" in df.columns:
        datas = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
        if datas.notna().all() and len(datas) > 1:
            if datas.is_monotonic_decreasing and not datas.is_monotonic_increasing:
                df = df.iloc[::-1].reset_index(drop=True)
                print("aviso: candles do mais novo para o mais antigo; a ordem foi invertida")
            elif not datas.is_monotonic_increasing:
                ordem = datas.sort_values(kind="mergesort").index
                df = df.loc[ordem].reset_index(drop=True)
                print("aviso: candles fora de ordem; foram ordenados por data")
        elif datas.isna().any():
            print("aviso: há datas ilegíveis; a ordem do arquivo foi tratada como cronológica")
    return df


def preparar(df, p):
    df = padronizar(df.copy())
    tr = pd.concat(
        [df["high"] - df["low"], (df["high"] - df["close"].shift()).abs(), (df["low"] - df["close"].shift()).abs()],
        axis=1,
    ).max(axis=1)
    df["atr"] = tr.rolling(p["atr_n"]).mean()
    # máxima dos N candles ANTERIORES (shift para não olhar o candle atual = sem look-ahead)
    df["canal_max"] = df["high"].rolling(p["n"]).max().shift(1)
    return df


def sinal(df, i, p):
    """Devolve 'compra', 'venda' ou None para o candle i, usando SÓ informação até o fechamento de i.

    Troque esta função pela regra do trader. Regra de exemplo: rompimento de canal para cima.
    Para uma regra de venda, devolva 'venda' com a lógica espelhada.
    """
    row = df.iloc[i]
    if pd.isna(row["canal_max"]) or pd.isna(row["atr"]):
        return None
    if row["close"] > row["canal_max"]:
        return "compra"
    return None


def simular(df, p):
    trades = []
    n = len(df)
    tick = p["tick"]
    i = 0
    while i < n - 1:
        s = sinal(df, i, p)
        if s is None:
            i += 1
            continue
        # entrada na ABERTURA do candle seguinte (o sinal só é conhecido no fechamento de i)
        ent_idx = i + 1
        entrada = float(df.iloc[ent_idx]["open"])
        atr = float(df.iloc[i]["atr"])
        if s == "compra":
            stop = entrada - p["atr_stop"] * atr
            alvo = entrada + p["atr_alvo"] * atr
        else:
            stop = entrada + p["atr_stop"] * atr
            alvo = entrada - p["atr_alvo"] * atr
        risco = abs(entrada - stop)
        if not risco > 0:
            i += 1
            continue
        saida = motivo = None
        ultimo = min(n - 1, ent_idx + p["max_barras"] - 1)  # último candle em que a posição pode estar aberta
        j_saida = ultimo
        for j in range(ent_idx, ultimo + 1):
            bar = df.iloc[j]
            abertura, maxima, minima = float(bar["open"]), float(bar["high"]), float(bar["low"])
            # Conservador: gap através do stop sai na abertura (pior que o stop); se o mesmo
            # candle toca stop e alvo, assume que o stop veio primeiro; alvo exige 1 tick além.
            if s == "compra":
                if j > ent_idx and abertura <= stop:
                    saida, motivo = abertura, "stop (gap)"
                elif minima <= stop:
                    saida, motivo = stop, "stop"
                elif maxima >= alvo + tick:
                    saida, motivo = alvo, "alvo"
            else:
                if j > ent_idx and abertura >= stop:
                    saida, motivo = abertura, "stop (gap)"
                elif maxima >= stop:
                    saida, motivo = stop, "stop"
                elif minima <= alvo - tick:
                    saida, motivo = alvo, "alvo"
            if saida is not None:
                j_saida = j
                break
        if saida is None:
            # saída por tempo no fechamento do último candle permitido (que já foi conferido acima)
            saida = float(df.iloc[j_saida]["close"])
            motivo = "fim dos dados" if ent_idx + p["max_barras"] - 1 > n - 1 else "tempo"
        r = (saida - entrada) / risco if s == "compra" else (entrada - saida) / risco
        r -= p["custo_r"]
        trades.append(
            {
                "data": df.iloc[ent_idx]["date"] if "date" in df.columns else ent_idx,
                "lado": s,
                "entrada": round(entrada, 4),
                "stop": round(stop, 4),
                "saida": round(saida, 4),
                "r": round(r, 3),
                "obs": motivo,
            }
        )
        i = j_saida + 1  # não abre novo trade enquanto há posição
    return pd.DataFrame(trades)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--out", default="trades.csv")
    ap.add_argument("--sep", help="separador do CSV de candles (padrão: detecta pelo cabeçalho)")
    ap.add_argument("--decimal", help="separador decimal (padrão: vírgula se o CSV usar ponto e vírgula)")
    for k, v in PADRAO.items():
        ap.add_argument(f"--{k.replace('_', '-')}", type=type(v), default=v)
    a = ap.parse_args()
    p = {k: getattr(a, k) for k in PADRAO}
    if p["max_barras"] < 1 or p["n"] < 1 or p["atr_n"] < 1:
        sys.exit("--max-barras, --n e --atr-n precisam ser 1 ou mais")

    df = preparar(ler_candles(a), p)
    trades = simular(df, p)
    if trades.empty:
        print("nenhum trade gerado: confira a regra e o período")
        return
    trades.to_csv(a.out, index=False)
    print(f"{len(trades)} trades gravados em {a.out}")
    print(f"agora rode: python backtest_metrics.py {a.out}")


if __name__ == "__main__":
    main()
