#!/usr/bin/env python3
"""Template de backtest por regras sobre candles OHLC.

Este arquivo é um PONTO DE PARTIDA, não um motor genérico. A regra de
exemplo é um rompimento de canal (compra quando o fechamento supera a máxima
dos últimos N candles) com stop e alvo por ATR e saída por tempo. Troque a
função `sinal()` e os parâmetros pela regra do trader — a estrutura em volta
(loop candle a candle, stop/alvo conservadores, custos, geração do CSV de
trades) fica.

Entrada: CSV com colunas date/data, open, high, low, close (volume opcional),
um candle por linha, em ordem cronológica. Qualquer timeframe.

Saída: CSV de trades no formato que `backtest_metrics.py` lê (coluna `r`).

Uso:
  python strategy_template.py candles.csv --out trades.csv
  python strategy_template.py candles.csv --n 20 --atr-stop 1.5 --atr-alvo 3 --max-barras 10 --custo-r 0.05

Depende de pandas.
"""
import argparse
import sys

# Console do Windows usa cp1252 por padrao; forca UTF-8 pra nao quebrar em "->"/acentos.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pandas as pd
except ImportError:
    sys.exit("instale pandas: pip install pandas")

# ---------------------------------------------------------------------------
# PARÂMETROS — tudo que é número da regra fica aqui, nunca espalhado no código.
# Cada parâmetro é um grau de liberdade para overfitting; quanto menos, melhor.
# ---------------------------------------------------------------------------
PADRAO = {
    "n": 20,          # janela do canal (candles)
    "atr_n": 14,      # período do ATR
    "atr_stop": 1.5,  # stop = entrada − atr_stop × ATR
    "atr_alvo": 3.0,  # alvo = entrada + atr_alvo × ATR
    "max_barras": 10, # saída por tempo se nem stop nem alvo
    "custo_r": 0.0,   # custo + slippage por trade, em R (ex.: 0.05)
}


def preparar(df, p):
    df = df.copy()
    df.columns = [c.lower().strip() for c in df.columns]
    if "data" in df.columns and "date" not in df.columns:
        df = df.rename(columns={"data": "date"})
    for c in ("open", "high", "low", "close"):
        if c not in df.columns:
            sys.exit(f"coluna `{c}` ausente no CSV")
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
    i = 0
    n = len(df)
    while i < n - 1:
        s = sinal(df, i, p)
        if s is None:
            i += 1
            continue
        # entrada na ABERTURA do candle seguinte (o sinal só é conhecido no fechamento de i)
        ent_idx = i + 1
        entrada = df.iloc[ent_idx]["open"]
        atr = df.iloc[i]["atr"]
        if s == "compra":
            stop = entrada - p["atr_stop"] * atr
            alvo = entrada + p["atr_alvo"] * atr
        else:
            stop = entrada + p["atr_stop"] * atr
            alvo = entrada - p["atr_alvo"] * atr
        risco = abs(entrada - stop)
        saida = None
        motivo = None
        j = ent_idx
        while j < n and j < ent_idx + p["max_barras"]:
            bar = df.iloc[j]
            if s == "compra":
                tocou_stop = bar["low"] <= stop
                tocou_alvo = bar["high"] >= alvo
            else:
                tocou_stop = bar["high"] >= stop
                tocou_alvo = bar["low"] <= alvo
            # Conservador: se o mesmo candle toca stop e alvo, assume que o stop veio primeiro.
            if tocou_stop:
                saida, motivo = stop, "stop"
                break
            if tocou_alvo:
                saida, motivo = alvo, "alvo"
                break
            j += 1
        if saida is None:
            j = min(j, n - 1)
            saida, motivo = df.iloc[j]["close"], "tempo"
        r = (saida - entrada) / risco if s == "compra" else (entrada - saida) / risco
        r -= p["custo_r"]
        trades.append(
            {
                "data": df.iloc[ent_idx].get("date", ent_idx),
                "lado": s,
                "entrada": round(entrada, 4),
                "stop": round(stop, 4),
                "saida": round(saida, 4),
                "r": round(r, 3),
                "obs": motivo,
            }
        )
        i = j + 1  # não abre novo trade enquanto há posição
    return pd.DataFrame(trades)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--out", default="trades.csv")
    for k, v in PADRAO.items():
        ap.add_argument(f"--{k.replace('_', '-')}", type=type(v), default=v)
    a = ap.parse_args()
    p = {k: getattr(a, k) for k in PADRAO}

    df = pd.read_csv(a.csv)
    df = preparar(df, p)
    trades = simular(df, p)
    if trades.empty:
        print("nenhum trade gerado — confira a regra e o período")
        return
    trades.to_csv(a.out, index=False)
    print(f"{len(trades)} trades → {a.out}")
    print(f"agora rode: python backtest_metrics.py {a.out}")


if __name__ == "__main__":
    main()
