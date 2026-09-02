#!/usr/bin/env python3
"""Calculadora de posição para perpétuos de cripto.

Dado risco, entrada e stop, devolve: tamanho da posição (em moeda e em USD),
alavancagem mínima para a margem disponível, preço de liquidação para a
alavancagem escolhida, distância entre stop e liquidação, custo de funding
para o prazo estimado e R múltiplo dos alvos.

Uso:
  python crypto_calc.py --risco 200 --entrada 60000 --stop 58500 --alvo 63000 --alvo 65000
  python crypto_calc.py --risco 200 --entrada 60000 --stop 61200 --lado short --alav 5 --funding 0.03 --horas 72

Todos os valores em USD (ou na moeda de cotação do par). Funding em % por
período de 8h (0.01 = 0,01%).
"""
import argparse
import math
import sys

# Console do Windows usa cp1252 por padrao; forca UTF-8 pra nao quebrar em "->"/acentos.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def calc(risco, entrada, stop, lado, alav, mmr, funding_pct, horas, margem, alvos, contrato):
    dist = abs(entrada - stop)
    if dist == 0:
        sys.exit("stop igual à entrada — nada a calcular")
    if lado == "long" and stop >= entrada:
        sys.exit("long com stop acima da entrada; confira os valores")
    if lado == "short" and stop <= entrada:
        sys.exit("short com stop abaixo da entrada; confira os valores")

    qtd = risco / dist  # unidades da moeda base
    if contrato:
        qtd = math.floor(qtd / contrato) * contrato
    notional = qtd * entrada
    stop_pct = dist / entrada * 100

    out = []
    out.append(f"Lado: {lado}   Entrada: {entrada:,.2f}   Stop: {stop:,.2f}  ({stop_pct:.2f}% de distância)")
    out.append(f"Risco: {risco:,.2f}  →  Tamanho: {qtd:.6f} moedas  ≈ {notional:,.2f} notional")

    if margem:
        alav_min = notional / margem
        out.append(f"Margem disponível {margem:,.2f} → alavancagem mínima necessária: {alav_min:.1f}x")

    if alav:
        if lado == "long":
            liq = entrada * (1 - 1 / alav + mmr)
            folga = (stop - liq) / entrada * 100
        else:
            liq = entrada * (1 + 1 / alav - mmr)
            folga = (liq - stop) / entrada * 100
        margem_usada = notional / alav
        out.append(f"Alavancagem {alav}x → margem usada {margem_usada:,.2f}; liquidação ≈ {liq:,.2f}")
        if folga <= 0:
            out.append("  AVISO: liquidação vem ANTES do stop. Reduza a alavancagem ou aproxime o stop.")
        elif folga < stop_pct * 0.5:
            out.append(f"  atenção: folga entre stop e liquidação é só {folga:.2f}% — pavio pode liquidar.")
        else:
            out.append(f"  folga entre stop e liquidação: {folga:.2f}% (ok)")

    if funding_pct and horas:
        periodos = horas / 8
        custo = notional * (funding_pct / 100) * periodos
        sinal = 1 if lado == "long" else -1
        custo_lado = custo * sinal
        verbo = "paga" if custo_lado > 0 else "recebe"
        out.append(
            f"Funding {funding_pct}%/8h por {horas}h ({periodos:.1f} períodos): {verbo} ≈ {abs(custo_lado):,.2f}"
            f"  (= {abs(custo_lado) / risco:.2f}R)"
        )

    for i, alvo in enumerate(alvos, 1):
        ganho = (alvo - entrada) * qtd if lado == "long" else (entrada - alvo) * qtd
        out.append(f"Alvo {i}: {alvo:,.2f} → {ganho:,.2f}  ({ganho / risco:.2f}R)")

    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--risco", type=float, required=True, help="perda máxima aceita no trade (USD)")
    p.add_argument("--entrada", type=float, required=True)
    p.add_argument("--stop", type=float, required=True)
    p.add_argument("--lado", choices=["long", "short"], default="long")
    p.add_argument("--alav", type=float, help="alavancagem que será usada (ex.: 5)")
    p.add_argument("--mmr", type=float, default=0.005, help="margem de manutenção (fração, padrão 0.005)")
    p.add_argument("--funding", type=float, default=0.0, help="funding em %% por 8h (ex.: 0.01)")
    p.add_argument("--horas", type=float, default=0.0, help="tempo estimado em posição (horas)")
    p.add_argument("--margem", type=float, help="margem disponível na conta (USD)")
    p.add_argument("--alvo", type=float, action="append", default=[], help="pode repetir")
    p.add_argument("--contrato", type=float, help="tamanho mínimo do contrato (ex.: 0.001)")
    a = p.parse_args()
    print(calc(a.risco, a.entrada, a.stop, a.lado, a.alav, a.mmr, a.funding, a.horas, a.margem, a.alvo, a.contrato))


if __name__ == "__main__":
    main()
