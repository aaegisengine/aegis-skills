# Ler o mercado de derivativos de cripto

Em cripto, o preço à vista é metade da história. A outra metade está nos perpétuos: quem está
alavancado, para que lado, e quanto custa ficar ali. As métricas abaixo são públicas (Coinglass,
Velo, as próprias exchanges) e o trader ou você consegue buscá-las. Use para qualificar o cenário,
nunca para gerar sinal sozinho: nenhuma prevê direção, elas dizem **quem fica vulnerável** se a
direção vier.

**Conferido em 07/11/2026.** Intervalo de funding, faixas de margem de manutenção e horários
mudam por exchange e por par. Quando o plano depender disso, reconfira na exchange (ou peça ao
trader o print da tela do contrato).

## Funding rate

Taxa que os comprados pagam aos vendidos (positiva) ou os vendidos pagam aos comprados
(negativa), cobrada no intervalo da exchange:

- **8h** na maioria dos pares grandes (Binance, Bybit, OKX): 00:00, 08:00 e 16:00 UTC, que são
  21:00, 05:00 e 13:00 BRT.
- **4h ou 1h** em alguns pares, e a exchange pode mudar o intervalo em volatilidade extrema. Desde
  18/09/2025 a Binance ajusta a fórmula ao intervalo (a parte de juros continua 0,01% por 8h).
- **Hyperliquid:** cobra de hora em hora, 1/8 da taxa de 8h por hora. A taxa que a API e a tela
  mostram já é a horária: não divida de novo.

| Funding por 8h | Anualizado (× 3 × 365) | Leitura |
|---|---|---|
| ~0,01% | ~11% | neutro (é o piso de juros padrão de muitas exchanges) |
| 0,03% a 0,05% | 33% a 55% | comprados pagando caro; mercado inclinado para o long |
| acima de 0,1% | acima de 100% | euforia; longs alavancados demais, combustível para queda em cascata |
| negativo persistente | n/a | vendidos pagando; mercado pessimista, combustível para alta em cascata |

**Custo de carregar:**

```
número de cobranças = horas em posição ÷ intervalo de cobrança (h)
custo ≈ notional × taxa por cobrança × número de cobranças
sinal: taxa positiva → long paga, short recebe; taxa negativa → o contrário
em R  = custo ÷ risco real do trade
```

Exemplo: US$ 10.000 comprado, funding 0,05% a cada 8h, 5 dias = 15 cobranças:
10.000 × 0,0005 × 15 = US$ 75. Com risco de US$ 200, são 0,375R.

A taxa muda a cada cobrança, então o resultado é estimativa. O número real de cobranças depende
de quantos horários de cobrança a posição atravessa.

Funding extremo, sozinho, não reverte o mercado: pode ficar extremo por semanas em tendência. O
que ele diz é "se vier um choque contra o lado lotado, a cascata será grande".

## Open interest (OI)

Total de contratos abertos. Leia junto com o preço:

| Preço | OI | Leitura |
|---|---|---|
| sobe | sobe | dinheiro novo entrando comprado: tendência com sustento |
| sobe | cai | vendidos zerando (short squeeze): movimento pode ser curto |
| cai | sobe | dinheiro novo entrando vendido: pressão |
| cai | cai | longs liquidados ou desalavancando: pode limpar e formar fundo |

OI na máxima + funding alto = mercado muito alavancado, amplitude tende a subir. Depois de uma
liquidação grande (OI cai muito em horas), o mercado costuma ficar mais "limpo" por um tempo.

## Liquidações

Clusters de liquidação (mapas de calor no Coinglass, Hyblock) são onde o preço tende a ser puxado
em movimento de pouca liquidez, porque liquidação é ordem a mercado forçada. Cluster grande logo
acima = ímã para cima; logo abaixo = ímã para baixo. É probabilidade de pavio, não garantia.

Para o plano: **nunca ponha stop dentro de um cluster óbvio**. Ponha além dele, ou aceite que o
stop pode ser pescado e reduza o tamanho.

## Basis e contango

Perp acima do spot (basis positivo) confirma demanda alavancada. Futuro trimestral em contango
forte indica otimismo e atrai carry trade (compra spot, vende futuro), que estabiliza. Basis
negativo persistente é sinal de estresse.

## Outros dados que valem uma busca

- **Fluxo de ETFs spot** (BTC e ETH nos EUA): sai depois do fechamento de Nova York. Vários dias
  seguidos de saída pesada costumam pesar.
- **Reservas em exchanges:** saída para carteira própria lê como retenção; entrada grande na
  exchange costuma anteceder venda.
- **Dominância do BTC:** subindo = dinheiro se protegendo em BTC (altcoins sofrem mais); caindo em
  alta = "alt season", risco maior.
- **Stablecoins (oferta de USDT e USDC):** crescendo = munição; encolhendo = saída do ecossistema.
- **Desbloqueio de tokens** (altcoins): data pública; oferta nova pressiona.
- **CME:** os futuros de cripto da CME negociam 24/7 desde 29/05/2026 (com manutenção semanal
  curta). O "gap da CME" de fim de semana deixou de se formar; gaps antigos no gráfico são
  histórico, não ímã novo.

## Tamanho, alavancagem e liquidação (perpétuo linear, margem em USDT ou USDC)

**A ordem certa:** risco → distância do stop → tamanho → alavancagem (só margem) → liquidação →
funding.

```
distância      = |entrada - stop|
perda por moeda = distância + taxa por lado × (entrada + stop)     (sem taxa: só a distância)
quantidade     = risco ÷ perda por moeda          (arredonde para baixo no passo da exchange)
notional       = quantidade × entrada
risco real     = quantidade × perda por moeda
margem usada   = notional ÷ alavancagem
alav. mínima   = notional ÷ margem disponível
R do alvo      = |alvo - entrada| ÷ distância
R líquido      = (|alvo - entrada| - taxa × (entrada + alvo)) ÷ perda por moeda
```

**Preço de liquidação.** A posição é liquidada quando o patrimônio dela cai até a margem de
manutenção (mmr × quantidade × preço). Chame de **M** a margem que sustenta a posição:

- margem **isolada**: M = margem usada = notional ÷ alavancagem
- margem **cruzada**: M = saldo da conta disponível para a posição (saldo da carteira de futuros,
  mais ou menos o resultado aberto das outras posições, menos a margem de manutenção delas)

```
long:  liquidação = (entrada - M ÷ quantidade) ÷ (1 - mmr)
short: liquidação = (entrada + M ÷ quantidade) ÷ (1 + mmr)
```

Na isolada isso vira: long = entrada × (1 - 1/alav) ÷ (1 - mmr); short = entrada × (1 + 1/alav) ÷
(1 + mmr). Algumas exchanges publicam o atalho entrada × (1 - 1/alav + mmr) para long e entrada ×
(1 + 1/alav - mmr) para short; a diferença é pequena.

Long com resultado menor ou igual a zero: não há preço de liquidação (a margem cobre a queda até
zero, ou seja, alavancagem efetiva de 1x ou menos).

**Isolada × cruzada, o que o trader precisa entender:**

- Na **isolada**, a alavancagem decide a liquidação e a perda máxima é a margem daquela posição.
- Na **cruzada**, a alavancagem escolhida quase não importa para a liquidação: quem decide é o
  saldo. A liquidação fica mais longe, mas quando vem leva a conta de futuros inteira. Outra
  posição perdendo também aproxima a liquidação desta.

**Margem de manutenção (mmr):** sobe por faixa de notional e muda com o tempo. Exemplo: a
Binance publicou 0,40% para a primeira faixa do BTCUSDT em dezembro de 2023 e já alterou as
faixas depois. Confira a tabela "leverage and margin" da exchange na data; altcoins costumam ter
mmr maior. O script usa 0,5% como padrão porque mmr maior deixa a estimativa mais
conservadora. Exchanges também usam o mark price e algumas reservam taxa de liquidação, o que
aproxima um pouco a liquidação da entrada. **O número que vale é o da tela da posição na
exchange.** A regra de folga abaixo absorve essas diferenças.

**Contrato inverso** (margem em moeda, como BTCUSD coin-margined): a conta é outra e o script não
cobre. Use a calculadora da exchange.

**Spot sem alavancagem:** não existe liquidação. Tamanho = risco ÷ distância, limitado ao caixa.

**A regra que sustenta tudo:** o stop é acionado **antes** da liquidação, com folga de pelo menos
metade da distância do stop. Se não fica, a alavancagem (isolada) está alta demais ou o saldo
(cruzada) está curto demais. **Nunca aperte o stop para afastar a liquidação.** Alavancagem não
deveria mudar o tamanho da posição, que é definido pelo risco. Se 10x "permite" uma posição maior,
a conta está sendo feita de trás para frente.

O script `scripts/crypto_calc.py` faz todas essas contas e imprime cada passo. Sem execução de
código, faça na conversa com as fórmulas acima, mostrando cada linha.
