# Métricas: o que cada uma diz e o que é "bom"

Tudo em R (múltiplo do risco inicial por trade). Backtest em dinheiro esconde o que importa: um setup com 60% de acerto e payoff 0,5 perde dinheiro, e a curva em R$ só mostra isso depois de muito tempo.

| Métrica | Fórmula | Leitura | Referência (day trade discricionário) |
|---|---|---|---|
| **Win rate** | ganhos / total | Sozinha não diz nada. 35% com payoff 3 é ótimo; 70% com payoff 0,3 quebra. | irrelevante isolada |
| **Payoff** | ganho médio / perda média | Quanto cada acerto paga em relação a cada erro. | > 1,5 para WR < 50%; > 0,8 para WR > 60% |
| **Expectância** | WR × ganho médio − (1−WR) × perda média | Quanto o setup rende por trade, em média. **É a métrica.** | > 0,2R já é operável; > 0,4R é raro e merece desconfiança |
| **Profit factor** | Σ ganhos / |Σ perdas| | Robustez. | 1,3–2,0 saudável; > 3 em amostra pequena é quase sempre overfitting |
| **Max drawdown** | maior queda do pico ao vale da curva de equity | O que o trader vai ter que aguentar. Se ele não aguenta −15R na prática, um setup com DD histórico de −12R vai quebrá-lo na primeira sequência ruim. | compare com a tolerância real do trader |
| **Trades em drawdown** | candles/trades entre um pico e o próximo | Quanto tempo ele fica abaixo do pico. Semanas em DD é o que faz abandonar setup bom. | — |
| **Maior sequência de perdas** | — | Se 8 perdas seguidas aconteceram no backtest, vão acontecer ao vivo. Ele precisa saber antes. | — |
| **SQN** | √n × expectância / desvio padrão | Qualidade ajustada pela variância (Van Tharp). | 1,6–2,0 pobre mas operável; 2–3 bom; > 3 excelente; > 5 desconfie |
| **Meses positivos** | — | Consistência. Um setup que ganha tudo em 2 meses e perde nos outros 10 é um setup de regime, não um setup. | > 60% dos meses |

## Tamanho de amostra

A expectância medida em 30 trades tem erro padrão de `desvio / √30`. Com desvio típico de 1,5R, o erro é ±0,27R — maior do que a expectância de quase todo setup real. Ou seja: **30 trades não distinguem um setup bom de um aleatório.**

| Trades | O que dá para concluir |
|---|---|
| < 30 | nada; serve para achar bug na regra |
| 30–100 | direção da expectância, com erro grande |
| 100–300 | expectância com erro razoável; DD ainda subestimado |
| > 300 | dá para confiar nas métricas, se o período cobriu mais de um regime |

Regime importa tanto quanto quantidade: 300 trades em 2 meses de tendência forte valem menos que 150 trades espalhados por um ano com alta, baixa e lateral.

## Custos

Inclua sempre: corretagem + emolumentos + slippage (mínimo 1 tick por lado em futuros líquidos, mais em notícia). Em R, isso costuma ficar entre 0,03R e 0,15R por trade dependendo da distância do stop. Setup de scalp com stop de 30 pontos no WIN e custo de R$ 1,50 ida e volta por contrato tem 0,25R de custo — a maioria dos setups de scalp morre aqui, e o backtest sem custo não mostra.

## Monte Carlo (o que o script faz)

Embaralha a ordem dos trades milhares de vezes e mede o drawdown em cada ordem. A ordem histórica é **uma** das possíveis; a sequência ruim pode vir primeiro ao vivo. Use o drawdown do percentil 95 (os 5% piores cenários) como o DD que o trader precisa estar preparado para tolerar, e a probabilidade de ruína (tocar o limite que ele definiu) como critério de go/no-go: acima de 5% é alto demais para o tamanho atual — reduza o risco por trade.

## Fora da amostra e walk-forward

Divida o período: 70% para desenvolver (in-sample), 30% para validar (out-of-sample), **sem olhar o out-of-sample até fechar as regras**. Se a expectância cai mais de metade no out-of-sample, as regras estão ajustadas ao passado.

Walk-forward é a versão rolante: otimiza em janela 1, testa em janela 2, otimiza em 1+2, testa em 3, e assim por diante. Só vale a pena para setups com parâmetros numéricos; setup discricionário faz o equivalente com o forward test (seção 6 da skill).
