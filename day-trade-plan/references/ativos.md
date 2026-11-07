# Especificações dos ativos mais operados

Use esta tabela para transformar "risco em dinheiro" em "pontos" e "contratos" sem errar a conta.

**Conferido em 07/11/2026.** Valor do ponto e tick de futuro listado mudam pouco, mas mudam (o
futuro de bitcoin da B3 encolheu 10 vezes em 2025). Horário, margem e custo mudam muito mais.
Quando a resposta depender de um desses números, reconfira na web na hora. Ativo que não está
aqui, ou CFD de corretora: pergunte o valor do ponto e do tick ao trader em vez de chutar.

Fontes: páginas de produto da B3 (WIN, WDO, BIT) e Ofício Circular 055/2026-VNC; páginas de
produto e educação da CME Group (NQ, MNQ, ES, MES, GC, MGC, CL).

## Futuros B3

| Ativo | Tamanho | Valor do ponto (1 contrato) | Tick mínimo | Vencimento |
|---|---|---|---|---|
| WIN (mini índice) | Ibovespa × R$ 0,20 | R$ 0,20 | 5 pontos = R$ 1,00 | meses pares, na quarta-feira mais próxima do dia 15 (feriado: próximo dia útil) |
| IND (índice cheio) | Ibovespa × R$ 1,00 | R$ 1,00 | 5 pontos = R$ 5,00 | igual ao WIN; 1 IND = 5 WIN |
| WDO (mini dólar) | US$ 10.000, cotado em R$ por US$ 1.000 | R$ 10,00 | 0,5 ponto = R$ 5,00 | todo mês, no 1º dia útil; o último pregão é o dia útil anterior |
| DOL (dólar cheio) | US$ 50.000 | R$ 50,00 | 0,5 ponto = R$ 25,00 | igual ao WDO; 1 DOL = 5 WDO |
| BIT (bitcoin futuro B3) | 0,01 BTC, cotado em R$ por 1 BTC | R$ 0,01 por R$ 1 de variação no BTC | R$ 20 por BTC = R$ 0,20 por contrato | todo mês, na última sexta-feira |

O BIT tinha 0,1 BTC por contrato até 16/06/2025. Liquidez menor que a do cripto global: para o
plano de cripto vale a camada de funding e liquidação de perpétuos, não esta tabela.

Horário de negociação B3: ver `sessoes.md`.

**Custos (corretagem, emolumentos e taxa de registro):** variam por corretora, por faixa de
volume da B3 e por day trade ou posição. Não use número de memória. O custo real por contrato
está na nota de corretagem do trader: peça esse valor (ida e volta). Sem ele, deixe o
placeholder "custo por contrato (ida e volta): ___" e avise que, em scalp de poucos pontos, o
custo pode comer boa parte da expectativa. Some 1 tick de slippage por lado quando o plano
operar a mercado.

## Futuros CME (EUA)

| Ativo | Valor do ponto | Tick mínimo | Micro |
|---|---|---|---|
| NQ (E-mini Nasdaq-100) | US$ 20 | 0,25 = US$ 5,00 | MNQ: US$ 2 por ponto, tick 0,25 = US$ 0,50 |
| ES (E-mini S&P 500) | US$ 50 | 0,25 = US$ 12,50 | MES: US$ 5 por ponto, tick 0,25 = US$ 1,25 |
| GC (ouro, 100 onças) | US$ 100 por US$ 1 | 0,10 = US$ 10,00 | MGC (10 onças): US$ 10 por US$ 1, tick 0,10 = US$ 1,00 |
| CL (petróleo WTI, 1.000 barris) | US$ 1.000 por US$ 1 | 0,01 = US$ 10,00 | MCL existe (1/10 do CL): confira a ficha |

**Vencimento:** NQ, ES e micros de índice vencem em março, junho, setembro e dezembro, na 3ª
sexta-feira; o volume migra para o próximo vencimento uns dias antes. Ouro e petróleo têm ciclo
próprio (não é trimestral): confira na ficha da CME qual contrato é o "front" na data. Sempre
confirme qual vencimento o trader está olhando.

**Horário:** domingo 18:00 a sexta 17:00 ET, com pausa diária de 1 hora (ver `sessoes.md`).
**Margem:** muda com a volatilidade e por corretora; confira na corretora.

## CFDs e forex (varia por corretora)

| Ativo | Convenção mais comum | Valor de 1 pip ou 1 ponto por lote |
|---|---|---|
| XAUUSD (ouro spot) | 1 lote = 100 onças | US$ 1,00 de variação no preço = US$ 100 por lote |
| EURUSD, GBPUSD, AUDUSD | 1 lote = 100.000 da moeda base | 1 pip (0,0001) = US$ 10 |
| USDJPY | 1 lote = 100.000 USD | 1 pip (0,01) = 1.000 ienes = 1.000 ÷ cotação do USDJPY em dólares |
| US100 / NAS100 (CFD) | depende da corretora | pergunte; muitas usam US$ 1 por ponto por lote, mas não assuma |
| Mini lote / micro lote | 10.000 / 1.000 | divida por 10 / por 100 |

O tamanho do lote é da corretora, não de uma bolsa. Peça ao trader a especificação do símbolo
(no MetaTrader: botão direito no símbolo, "Especificação"). CFD tem spread variável que alarga
muito em notícia: entrada a 5 minutos do payroll pode pagar um spread várias vezes o normal.

## Cripto (perpétuos)

| Ativo | Tamanho de contrato | Observação |
|---|---|---|
| BTCUSDT, ETHUSDT perp | 1 contrato = 1 moeda, ou fração dela, conforme a exchange | Confirme o `contract size` e o passo mínimo antes de dimensionar |

Funding, liquidação e margem cruzada: se a skill `crypto-trade-plan` estiver instalada, ela faz
essa camada completa. Se não, o mínimo: funding é cobrado no intervalo da exchange (8h na maioria
dos pares grandes, 4h ou 1h em alguns), custo ≈ notional × taxa × número de cobranças, e o preço
de liquidação tem que ficar além do stop com folga.

## Fórmula de posição (vale para tudo)

```
risco por contrato = distância do stop em pontos × valor do ponto + custo por contrato (ida e volta)
contratos          = risco em dinheiro ÷ risco por contrato   (arredonde SEMPRE para baixo)
risco real         = contratos × risco por contrato
R do alvo (bruto)  = distância do alvo em pontos ÷ distância do stop em pontos
R do alvo (líquido)= (distância do alvo × valor do ponto - custo) ÷ risco por contrato
```

Se der zero contrato, o stop está largo demais para o risco definido: ou o trade não cabe, ou o
risco tem que subir, e aí a decisão é do trader, não da conta. Nunca aperte o stop para caber.

Exemplos (custo ignorado para deixar a conta limpa):
- Risco R$ 150, stop de 150 pontos no WIN: 150 × 0,20 = R$ 30 por contrato. 150 ÷ 30 = 5 contratos.
- Risco US$ 200, stop de 40 pontos no MNQ: 40 × 2 = US$ 80 por contrato. 200 ÷ 80 = 2,5, arredonda para 2 contratos. Risco real: 2 × 80 = US$ 160.
- Risco R$ 200, stop de 6 pontos no WDO: 6 × 10 = R$ 60 por contrato. 200 ÷ 60 = 3,33, arredonda para 3. Risco real: R$ 180.
