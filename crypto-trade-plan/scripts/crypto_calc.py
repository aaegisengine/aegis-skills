#!/usr/bin/env python3
"""Calculadora de posição para perpétuos lineares de cripto (margem em USDT, USDC ou USD).

Dado risco, entrada e stop, devolve, com cada conta escrita:
  - tamanho da posição pelo risco (com taxa de corretagem, se informada)
  - margem usada e alavancagem mínima para a margem disponível
  - preço de liquidação estimado, em margem isolada ou cruzada
  - folga entre stop e liquidação
  - custo de funding pelo prazo estimado, em dinheiro e em R
  - R dos alvos (bruto e líquido de taxa)

Uso:
  python crypto_calc.py --risco 200 --entrada 60000 --stop 58500 --alav 5 --alvo 63000 --alvo 65500
  python crypto_calc.py --risco 200 --entrada 60000 --stop 61200 --lado short --alav 5 --funding 0.03 --horas 72
  python crypto_calc.py --risco 200 --entrada 60000 --stop 58500 --modo cruzada --saldo 3000 --taxa 0.05

Valores na moeda de cotação do par. Funding e taxa em % (0.01 = 0,01%).
Funding negativo: --funding=-0.01

Não cobre contrato inverso (margem em moeda, ex.: BTCUSD coin-margined): use a
calculadora da exchange. Os números são estimativa: a exchange usa mark price,
faixas de margem de manutenção e às vezes reserva taxa de liquidação. O preço de
liquidação que vale é o da tela da posição.
"""
import argparse
import math
import sys

# Console do Windows usa cp1252 por padrão; força UTF-8 para não quebrar acentos e setas.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EPS = 1e-9


def br(valor, casas=2):
    """Número no padrão brasileiro: 60000.5 vira 60.000,50."""
    s = f"{valor:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(valor, casas=2):
    return br(valor, casas) + "%"


def erro(msg):
    sys.exit("ERRO: " + msg)


def preco_liquidacao(lado, entrada, qtd, margem, mmr):
    """Preço em que patrimônio da posição = margem de manutenção (mmr x qtd x preço).

    margem: o que sustenta a posição (margem isolada, ou saldo da conta na cruzada).
    Devolve None quando não há liquidação (long coberto até o preço zero).
    """
    por_moeda = margem / qtd
    if lado == "long":
        liq = (entrada - por_moeda) / (1 - mmr)
        return liq if liq > 0 else None
    return (entrada + por_moeda) / (1 + mmr)


def validar(a):
    if a.risco <= 0 or a.entrada <= 0 or a.stop <= 0:
        erro("risco, entrada e stop precisam ser maiores que zero")
    if a.entrada == a.stop:
        erro("stop igual à entrada, nada a calcular")
    if a.lado == "long" and a.stop > a.entrada:
        erro("long com stop acima da entrada; confira os valores")
    if a.lado == "short" and a.stop < a.entrada:
        erro("short com stop abaixo da entrada; confira os valores")
    if not 0 <= a.mmr < 0.5:
        erro("--mmr é fração (0.005 = 0,5%); confira o valor")
    if a.alav is not None and a.alav < 1:
        erro("--alav precisa ser 1 ou mais")
    if a.taxa < 0:
        erro("--taxa não pode ser negativa")
    if a.intervalo <= 0:
        erro("--intervalo precisa ser maior que zero (horas entre cobranças de funding)")
    if a.contrato is not None and a.contrato <= 0:
        erro("--contrato precisa ser maior que zero")
    if a.modo == "cruzada" and (a.saldo is None or a.saldo <= 0):
        erro("modo cruzada precisa de --saldo (o saldo que sustenta a posição)")


def calc(a):
    validar(a)
    entrada, stop, risco, lado = a.entrada, a.stop, a.risco, a.lado
    taxa = a.taxa / 100  # fração por lado
    dist = abs(entrada - stop)
    stop_pct = dist / entrada * 100
    taxa_por_moeda = taxa * (entrada + stop)  # entrada + saída no stop
    perda_por_moeda = dist + taxa_por_moeda

    out = ["TAMANHO"]
    out.append(f"  Distância do stop: |{br(entrada)} - {br(stop)}| = {br(dist)} ({pct(stop_pct)} da entrada)")
    if taxa:
        out.append(
            f"  Taxa ida e volta por moeda: {pct(a.taxa, 3)} x ({br(entrada)} + {br(stop)}) = {br(taxa_por_moeda)}"
        )
        out.append(f"  Perda por moeda no stop: {br(dist)} + {br(taxa_por_moeda)} = {br(perda_por_moeda)}")
    qtd_bruta = risco / perda_por_moeda
    out.append(
        f"  Quantidade = risco / perda por moeda = {br(risco)} / {br(perda_por_moeda)} = {br(qtd_bruta, 6)} moedas"
    )
    qtd = qtd_bruta
    if a.contrato:
        qtd = math.floor(qtd_bruta / a.contrato + EPS) * a.contrato
        out.append(f"  Arredondado para baixo no passo {br(a.contrato, 6)}: {br(qtd, 6)} moedas")
        if qtd <= 0:
            out.append("  AVISO: o risco não paga nem 1 passo mínimo com esse stop. O trade não cabe nesse risco.")
            return "\n".join(out)
    notional = qtd * entrada
    risco_real = qtd * perda_por_moeda
    out.append(f"  Notional: {br(qtd, 6)} x {br(entrada)} = {br(notional)}")
    out.append(f"  Risco real no stop: {br(risco_real)}" + (" (taxa incluída)" if taxa else " (sem taxa)"))

    out.append("")
    out.append("MARGEM E LIQUIDAÇÃO")
    if a.alav:
        margem_usada = notional / a.alav
        out.append(f"  Margem usada: {br(notional)} / {br(a.alav, 1)}x = {br(margem_usada)}")
    if a.margem:
        alav_min = notional / a.margem
        out.append(f"  Alavancagem mínima para caber na margem: {br(notional)} / {br(a.margem)} = {br(alav_min, 2)}x")
        if a.alav and a.alav + EPS < alav_min:
            out.append(
                f"  AVISO: com {br(a.alav, 1)}x a margem exigida ({br(notional / a.alav)}) passa da margem disponível."
            )

    margem_pos = None
    if a.modo == "isolada":
        if a.alav:
            margem_pos = notional / a.alav
            out.append("  Modo isolado: a margem da posição é a margem usada.")
        else:
            out.append("  Sem --alav: liquidação não calculada (spot sem alavancagem não tem liquidação).")
    else:
        margem_pos = a.saldo
        out.append(
            f"  Modo cruzado: quem sustenta a posição é o saldo ({br(a.saldo)}). A alavancagem escolhida não muda a liquidação."
        )

    if margem_pos is not None:
        por_moeda = margem_pos / qtd
        liq = preco_liquidacao(lado, entrada, qtd, margem_pos, a.mmr)
        if lado == "long":
            out.append(f"  Liquidação = (entrada - margem/qtd) / (1 - mmr), mmr = {pct(a.mmr * 100)}")
            conta = f"({br(entrada)} - {br(por_moeda)}) / {br(1 - a.mmr, 4)}"
        else:
            out.append(f"  Liquidação = (entrada + margem/qtd) / (1 + mmr), mmr = {pct(a.mmr * 100)}")
            conta = f"({br(entrada)} + {br(por_moeda)}) / {br(1 + a.mmr, 4)}"
        if liq is None:
            out.append(f"             = {conta} <= 0: sem preço de liquidação (a margem cobre a queda até zero)")
        else:
            out.append(f"             = {conta} = {br(liq)}")
            if lado == "long":
                folga = (stop - liq) / entrada * 100
            else:
                folga = (liq - stop) / entrada * 100
            if folga <= 0:
                out.append(
                    "  AVISO: a liquidação vem ANTES do stop. Reduza a alavancagem (isolada) ou aumente o saldo"
                    " (cruzada). Não aperte o stop: ele fica na estrutura."
                )
            elif folga < stop_pct * 0.5:
                out.append(
                    f"  ATENÇÃO: folga entre stop e liquidação de só {pct(folga)} da entrada, menos da metade"
                    f" da distância do stop ({pct(stop_pct)}). Um pavio pode liquidar. Reduza a alavancagem."
                )
            else:
                out.append(f"  Folga entre stop e liquidação: {pct(folga)} da entrada (ok: pelo menos metade da distância do stop)")
        if a.modo == "cruzada":
            out.append(f"  Na cruzada, se liquidar, a perda é o saldo inteiro ({br(a.saldo)}), não só o risco do plano.")

    if a.funding and a.horas:
        cobrancas = a.horas / a.intervalo
        custo = abs(notional * (a.funding / 100) * cobrancas)
        paga = (a.funding > 0 and lado == "long") or (a.funding < 0 and lado == "short")
        verbo = "paga" if paga else "recebe"
        out.append("")
        out.append("FUNDING (estimativa: a taxa muda a cada cobrança)")
        out.append(f"  Cobranças: {br(a.horas, 1)}h / {br(a.intervalo, 1)}h = {br(cobrancas, 1)}")
        out.append(
            f"  Custo = notional x taxa x cobranças = {br(notional)} x {pct(abs(a.funding), 4)} x {br(cobrancas, 1)} = {br(custo)}"
        )
        out.append(f"  Você {verbo} cerca de {br(custo)} = {br(custo / risco_real)}R")

    if a.alvo:
        out.append("")
        out.append("ALVOS")
    for i, alvo in enumerate(a.alvo, 1):
        ganho_por_moeda = (alvo - entrada) if lado == "long" else (entrada - alvo)
        if ganho_por_moeda <= 0:
            out.append(f"  Alvo {i}: {br(alvo)} está do lado errado da entrada; confira.")
            continue
        r_bruto = ganho_por_moeda / dist
        linha = f"  Alvo {i}: {br(alvo)} | R = {br(ganho_por_moeda)} / {br(dist)} = {br(r_bruto)}R"
        liquido_por_moeda = ganho_por_moeda - taxa * (entrada + alvo)
        if taxa:
            linha += f" | líquido de taxa: {br(liquido_por_moeda / perda_por_moeda)}R"
        linha += f" | resultado ~ {br(liquido_por_moeda * qtd)}"
        out.append(linha)

    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--risco", type=float, required=True, help="perda máxima aceita no trade, na moeda de cotação")
    p.add_argument("--entrada", type=float, required=True)
    p.add_argument("--stop", type=float, required=True)
    p.add_argument("--lado", choices=["long", "short"], default="long")
    p.add_argument("--modo", choices=["isolada", "cruzada"], default="isolada", help="tipo de margem (padrão isolada)")
    p.add_argument("--alav", type=float, help="alavancagem que será usada (ex.: 5)")
    p.add_argument("--saldo", type=float, help="na cruzada: saldo da conta que sustenta a posição")
    p.add_argument("--mmr", type=float, default=0.005,
                   help="margem de manutenção em fração (padrão 0.005 = 0,5%%; confira a faixa na exchange)")
    p.add_argument("--taxa", type=float, default=0.0, help="taxa por lado em %% (ex.: 0.05 = 0,05%% taker)")
    p.add_argument("--funding", type=float, default=0.0, help="funding em %% por cobrança (ex.: 0.01)")
    p.add_argument("--intervalo", type=float, default=8.0,
                   help="horas entre cobranças de funding (8 na maioria; 4 ou 1 em alguns pares)")
    p.add_argument("--horas", type=float, default=0.0, help="tempo estimado em posição, em horas")
    p.add_argument("--margem", type=float, help="margem disponível na conta (para a alavancagem mínima)")
    p.add_argument("--alvo", type=float, action="append", default=[], help="pode repetir")
    p.add_argument("--contrato", type=float, help="passo mínimo de quantidade da exchange (ex.: 0.001)")
    print(calc(p.parse_args()))


if __name__ == "__main__":
    main()
