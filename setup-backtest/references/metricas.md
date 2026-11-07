# Métricas: o que cada uma diz e o que é "bom"

Tudo em R (múltiplo do risco inicial de cada trade). Backtest em dinheiro esconde o que importa:
um setup com 60% de acerto e payoff 0,5 perde dinheiro, e a curva em R$ só mostra isso depois de
muito tempo.

## O que é 1R

R é o risco inicial planejado do trade: a distância da entrada ao **stop inicial**, vezes o
tamanho. O resultado do trade em R é:

`R = (saída - entrada) ÷ (entrada - stop inicial)`

Funciona pros dois lados (na venda o denominador fica negativo e o sinal se acerta). Stop movido
depois não muda o R: vale o inicial. Parcial: use o preço médio ponderado das saídas. Trade sem
stop inicial não tem R; registre à parte e diga que o risco era indefinido. Se o registro está
em dinheiro, `R = resultado em R$ ÷ risco em R$ daquele trade`.

## As métricas

Notação: n = trades; G = trades com ganho; P = trades com perda; zerados não entram em G nem em P.

| Métrica | Fórmula | Leitura | Referência (day trade discricionário) |
|---|---|---|---|
| **Win rate** | G ÷ n | Sozinha não diz nada. 35% com payoff 3 é ótimo; 70% com payoff 0,3 quebra. | irrelevante isolada |
| **Payoff** | ganho médio ÷ \|perda média\| | Quanto cada acerto paga em relação a cada erro. | depende do win rate (ver empate) |
| **Win rate de empate** | 1 ÷ (1 + payoff) | O acerto mínimo pra não perder com esse payoff. Payoff 2 empata com 33%; payoff 0,5 precisa de 67%. | win rate real bem acima disso |
| **Expectância** | Σ R ÷ n (igual a G/n × ganho médio - P/n × \|perda média\|) | Quanto o setup rende por trade, em média. **É a métrica.** | ≥ 0,2R depois de custo já é operável; > 0,5R é raro e merece desconfiança |
| **Profit factor** | Σ ganhos ÷ \|Σ perdas\| | Robustez. | 1,3 a 2,5 saudável; > 3 em amostra pequena é quase sempre overfitting |
| **Max drawdown** | maior queda da curva acumulada, do pico ao vale | O que o trader vai ter que aguentar. Se ele não aguenta -15R na prática, um setup com DD histórico de -12R vai quebrá-lo na primeira fase ruim. | compare com a tolerância real dele |
| **Trades abaixo do pico** | maior número de trades entre um pico e a recuperação dele | Quanto tempo ele fica no vermelho. Semanas em DD é o que faz abandonar setup bom. | dizer o número a ele |
| **Maior sequência de perdas** | contagem direta | Se 8 perdas seguidas aconteceram no histórico, vão acontecer ao vivo. | compare com a do acaso (abaixo) |
| **SQN** (Van Tharp) | √n × expectância ÷ desvio padrão dos R | Qualidade ajustada pela variância. Cresce com √n, então pra comparar sistemas Van Tharp limita n a 100 no cálculo. | faixas dele, aproximadas: < 1,6 difícil; 1,6 a 2 abaixo da média; 2 a 2,5 média; 2,5 a 3 bom; 3 a 5 excelente. Acima de 5 em backtest: desconfie antes de comemorar |
| **Meses positivos** | meses com soma de R > 0 ÷ meses | Consistência. Ganhar tudo em 2 meses e perder nos outros 10 é setup de regime. | > 60%, e só vale com ~10+ trades por mês |

Desvio padrão: use o amostral (divide por n - 1).

## Sequência de perdas que o acaso já produz

Com taxa de perda q (P ÷ n) e n trades, a maior sequência de perdas esperada só por acaso é
aproximadamente:

`L ≈ log(n × (1 - q)) ÷ log(1 ÷ q)`

Exemplo: q = 0,6 e n = 100 dá log(40) ÷ log(1,667) ≈ 7. Ou seja, um setup com 40% de acerto
vai ter 7 perdas seguidas em 100 trades sem nada estar quebrado. Se a sequência real for bem
maior que L, pode ser regime (perdas agrupadas) e o Monte Carlo vai subestimar o risco.

## Tamanho de amostra

O erro padrão da expectância é `desvio ÷ √n`. Com desvio típico de 1,5R e 30 trades, o erro é
±0,27R: maior que a expectância de quase todo setup real. **30 trades não distinguem um setup
bom de um aleatório.**

A conta que decide quantos trades precisa: pra afirmar expectância acima de zero com ~95% de
confiança, **n ≈ (2 × desvio ÷ expectância)²**. Desvio 1,2R e expectância 0,2R pedem 144
trades; expectância 0,1R pede 576.

| Trades | O que dá para concluir |
|---|---|
| < 30 | nada; serve para achar erro na regra |
| 30 a 100 | direção da expectância, com erro grande |
| 100 a 300 | expectância com erro razoável; DD ainda subestimado |
| > 300 | dá para confiar nas métricas, se o período cobriu mais de um regime |

Regime importa tanto quanto quantidade: 300 trades em 2 meses de tendência forte valem menos que
150 trades espalhados por um ano com alta, baixa e lateral.

## Custos

Inclua sempre: corretagem, emolumentos e slippage (pelo menos 1 tick por ponta em ordem a
mercado ou stop, mais em notícia). Em R, isso costuma ficar entre 0,03R e 0,15R por trade, e
pesa mais quanto mais curto o stop.

Exemplo (números hipotéticos; confira os da sua corretora e da bolsa): no mini índice, 1 ponto
vale R$ 0,20 por contrato e o tick é de 5 pontos. Stop de 30 pontos = R$ 6,00 de risco. Custo
fixo de R$ 1,50 ida e volta = 0,25R. Somando 1 tick de slippage em cada ponta (R$ 2,00), o custo
vai a R$ 3,50 = 0,58R por trade. A maioria dos setups de scalp morre aqui, e o backtest sem custo
não mostra.

## Monte Carlo (o que o script faz)

Dois métodos, porque respondem perguntas diferentes:

- **Ordem embaralhada:** os MESMOS trades em outra ordem. O resultado final é igual em todas as
  simulações; o que muda é o drawdown. Responde: "e se a sequência ruim viesse primeiro?".
- **Reamostragem com reposição (bootstrap):** sorteia n trades da amostra, podendo repetir. Mede
  também a incerteza da própria amostra: a faixa do resultado, o intervalo da expectância e a
  chance de o resultado ser negativo. Costuma dar drawdown pior que o embaralhamento.

Use o drawdown dos **5% piores** cenários como o DD pra se preparar, e a chance de tocar o limite
de ruína como critério: acima de 5% é alto demais pro tamanho atual; reduza o risco por trade.

Limites honestos: os dois supõem trades independentes e risco fixo em R. Se as perdas vêm em
grupo (regime), o drawdown real pode ser pior que o dos 5% piores. E nenhum Monte Carlo conserta
amostra viciada: ele embaralha o que você deu.

**Tamanho da mão a partir do DD:** risco máximo por trade em R$ ≈ drawdown tolerável em R$ ÷
|DD dos 5% piores em R|. Ex.: tolera perder R$ 3.000 e o DD dos 5% piores é -15R: risco de até
R$ 200 por trade. É conta de dimensionamento, não recomendação.

## Fora da amostra e walk-forward

Divida o período por data: ~70% para desenvolver (dentro da amostra), ~30% para validar (fora),
**sem olhar a parte de fora até fechar as regras**. Se a expectância cai mais da metade fora da
amostra, as regras estão ajustadas ao passado. A parte de fora só vale uma vez: ajustou depois
de ver, ela virou dentro.

Walk-forward é a versão rolante: otimiza na janela 1, testa na 2; otimiza em 1+2, testa na 3; e
assim por diante. Só vale a pena para setups com parâmetros numéricos; setup discricionário faz
o equivalente com o forward test (demo ou tamanho mínimo).
