# Especificações dos ativos mais operados

Use esta tabela para transformar "risco em R$" em "pontos" e "contratos" sem errar a conta. Quando o trader operar um ativo que não está aqui, pergunte o valor do ponto e do tick em vez de chutar.

## Futuros B3

| Ativo | Valor do ponto (1 contrato) | Tick mínimo | Observações |
|---|---|---|---|
| WIN (mini índice) | R$ 0,20 | 5 pontos = R$ 1,00 | Vence bimestral (meses pares), 3ª quarta-feira útil. Rolagem concentra volume nos 2–3 dias antes. |
| IND (índice cheio) | R$ 1,00 | 5 pontos = R$ 5,00 | 1 IND ≈ 5 WIN. |
| WDO (mini dólar) | R$ 10,00 | 0,5 ponto = R$ 5,00 | Cotado em R$ por US$ 1.000. Vence todo mês, 1º dia útil. Rolagem no último dia útil do mês anterior. |
| DOL (dólar cheio) | R$ 50,00 | 0,5 ponto = R$ 25,00 | 1 DOL = 5 WDO. |
| BIT (bitcoin futuro B3) | varia | — | Baixa liquidez; prefira a referência de cripto da skill `crypto-trade-plan`. |

Custo típico por contrato de WIN/WDO (corretagem + emolumentos + slippage de 1 tick): entre R$ 0,50 e R$ 2,00 por lado, dependendo da corretora. Em scalp isso come metade da expectativa — sempre inclua no cálculo.

## Futuros CME (EUA)

| Ativo | Valor do ponto | Tick mínimo | Micro equivalente |
|---|---|---|---|
| NQ (E-mini Nasdaq 100) | US$ 20 | 0,25 = US$ 5 | MNQ = US$ 2/ponto (1/10) |
| ES (E-mini S&P 500) | US$ 50 | 0,25 = US$ 12,50 | MES = US$ 5/ponto |
| YM (E-mini Dow) | US$ 5 | 1,0 = US$ 5 | MYM = US$ 0,50/ponto |
| GC (ouro) | US$ 100 | 0,10 = US$ 10 | MGC = US$ 10/ponto |
| CL (petróleo WTI) | US$ 1.000 | 0,01 = US$ 10 | MCL = US$ 100/ponto |
| 6E (euro) | US$ 125.000 × variação | 0,00005 = US$ 6,25 | M6E = 1/10 |

Vencimentos trimestrais (março, junho, setembro, dezembro) na 3ª sexta-feira. Na semana da rolagem, o contrato "front" muda e o volume migra — confirme qual vencimento o trader está olhando.

## CFDs e forex (varia por corretora)

| Ativo | Lote padrão | Valor aproximado de 1 pip / 1 ponto por lote |
|---|---|---|
| XAUUSD (ouro spot) | 100 oz | US$ 1,00 de variação no preço = US$ 100 por lote |
| EURUSD, GBPUSD, AUDUSD | 100.000 | 1 pip (0,0001) ≈ US$ 10 |
| USDJPY | 100.000 | 1 pip (0,01) ≈ US$ 6–7 (varia com a cotação) |
| US100 / NAS100 (CFD) | 1 contrato | geralmente US$ 1 por ponto (confirme na corretora) |
| Mini lote | 10.000 | ÷10 |
| Micro lote | 1.000 | ÷100 |

CFDs têm spread variável e alargam brutalmente em notícia. Se o trader opera XAUUSD em CFD e o plano tem entrada a 5 minutos do payroll, avise que o spread naquele momento pode ser 3–5x o normal.

## Cripto (perpétuos)

| Ativo | Tamanho de contrato típico | Observação |
|---|---|---|
| BTCUSDT perp | 1 contrato = 1 BTC ou 0,001 BTC (varia por exchange) | Confirme o `contract size` da exchange antes de dimensionar. |
| ETHUSDT perp | idem | |

Funding rate a cada 8h (na maioria das exchanges) é custo ou receita de carregar posição. A skill `crypto-trade-plan` cobre isso.

## Fórmula de posição (vale para tudo)

```
contratos = risco_em_dinheiro / (distância_do_stop_em_pontos × valor_do_ponto)
```

Arredonde sempre **para baixo**. Se der zero contrato, o stop está largo demais para o risco definido — ou o trade não cabe, ou o risco tem que subir (e aí a decisão é do trader, não da conta).

Exemplo: risco R$ 150, stop de 150 pontos no WIN → 150 / (150 × 0,20) = 5 contratos.
Exemplo: risco US$ 200, stop de 40 pontos no MNQ → 200 / (40 × 2) = 2,5 → 2 contratos.
