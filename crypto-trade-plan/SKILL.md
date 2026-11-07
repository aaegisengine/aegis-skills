---
name: crypto-trade-plan
description: Plano de trade em cripto (BTC, ETH, altcoins, spot e perpétuos) com a camada que só existe ali (funding, open interest, liquidações, fluxo de ETF, mercado 24/7 com fim de semana fino, alavancagem, preço de liquidação em margem isolada e cruzada e risco de exchange). Três cenários com gatilho, stop, alvo com R e invalidação, e tamanho pelo risco (nunca pela alavancagem) com a conta aberta, via script ou passo a passo na conversa quando não der para rodar código. Use quando o trader citar bitcoin, ETH, solana, altcoin, perp, funding, liquidação, alavancagem, Binance, Bybit, OKX ou Hyperliquid, perguntar como fica o BTC hoje ou na semana, se vale entrar em X, qual o preço de liquidação, ou disser que está alavancado e quer revisar a posição. Para ativos tradicionais, o certo é um plano de day trade ou de swing.
---

# Crypto Trade Plan

Cripto pune dois tipos de trader: o que trata como ação (ignora funding, liquidação e o domingo) e
o que trata como cassino (alavanca porque a exchange deixa). O plano serve para os dois: traz as
variáveis que só existem aqui e força o tamanho a ser definido pelo risco, não pela alavancagem
disponível.

## Regras que valem em toda resposta

- Português do Brasil, direto, sem "to the moon" nem "vai zerar".
- **Sem travessão na resposta**, nem o longo nem o curto. Use vírgula, dois-pontos, ponto ou
  parênteses. Hífen só em intervalo de número.
- **Nunca dá call.** Três cenários com gatilho e invalidação; a decisão é do trader.
- **Nunca inventa número.** Preço, funding, OI e liquidação mudam a cada minuto: sem fonte, vira
  "n/d, confira antes de entrar" ou placeholder nomeado. "Funding está alto" sem número e fonte
  não entra.
- **Conta aberta.** Tamanho, margem, liquidação, folga, funding e R aparecem com a conta escrita.

## 1. O que precisa vir do trader

| Informação | Essencial? | Se não vier |
|---|---|---|
| Ativo (BTC, ETH, SOL, par específico) | sim | pergunte; "cripto" sozinho, assuma BTC e diga |
| Risco por trade (USD ou % da conta) | sim | pergunte; em %, peça o tamanho da conta |
| Spot ou perpétuo? Exchange? | não | assuma perpétuo linear em USDT e diga |
| Margem isolada ou cruzada | não | assuma isolada e diga; na cruzada, peça o saldo da conta de futuros |
| Horizonte (horas, dias, semanas) | não | pergunte em uma linha: define quanto o funding pesa |
| Alavancagem pretendida | não | calcule a necessária, não a máxima |
| Taxa da exchange (taker) | não | sem taxa na conta e avise; ou peça o valor |
| Níveis ou print | não | placeholders |
| Já está posicionado? | se for revisão | preço médio, tamanho, alavancagem, modo de margem, liquidação na tela |

## 2. Dados que mudam com o tempo

**Com busca na web:** preço, funding, OI, liquidações e fluxo de ETF ("BTC funding rate", "BTC
open interest", "BTC liquidations today", "bitcoin ETF flows"), e a agenda macro da janela do
trade. As referências foram conferidas em 07/11/2026; intervalo de funding, faixa de margem de
manutenção e horários mudam por exchange, então reconfira quando o plano depender deles.

**Sem busca na web** (acontece no claude.ai com a busca desligada): avise em 1 linha ("Estou sem
busca na web agora, então não confirmei preço, funding nem OI."), peça que o trader cole o preço
e os números do Coinglass ou da exchange (print serve), e siga com "n/d" e placeholders.

## 3. Print do gráfico (ou da tela da exchange)

- **Todo preço tirado do print leva marca:** `(lido)` quando sai de rótulo do eixo ou de etiqueta
  da plataforma; `(aprox.)` quando é interpolado entre rótulos.
- **Nunca mais precisão do que o eixo dá.** Eixo de 1.000 em 1.000: "~61.500 (aprox.)", nunca
  "61.487".
- Número lido da tela da posição (liquidação, margem, funding) também leva `(lido)`, e vale mais
  que a sua estimativa.
- Eixo ilegível: descreva a estrutura e deixe níveis como placeholder.

## 4. Como montar

### Contexto (3 linhas)

O que o BTC (e o ativo, se não for BTC) fez em 24h e na semana; o que NQ e DXY estão fazendo
(cripto anda com risco global na maioria dos regimes); se houve liquidação grande recente
(mercado "limpo" ou "lotado"). Altcoin: a dominância do BTC sobe ou cai.

### Camada de derivativos

Tabela curta com o que você achou (leitura de cada linha em `references/derivativos.md`):

```
| Métrica | Valor | Leitura |
| Funding (por cobrança, intervalo) | ... | ... |
| OI (variação 24h) | ... | ... |
| Liquidações 24h (lado) | ... | ... |
| Clusters de liquidação | ... | ... |
| Basis perp/spot | ... | ... |
| Fluxo de ETF (último dia) | ... | ... |
```

Feche em uma frase: qual lado está vulnerável a cascata. Isso não escolhe direção; diz onde o stop
**não** pode ficar e qual cenário tem combustível a favor.

### Agenda e relógio

Cripto não fecha, mas tem relógio:

- **Dados dos EUA e FOMC** mexem no BTC como no NQ. Se a skill `session-news-radar` estiver
  instalada, ela faz a agenda completa. Se não, faça aqui mesmo assim: busque (ou peça) só os
  eventos de impacto alto na janela do trade, com horário BRT (`references/sessoes.md`), e marque
  a janela de risco de cada um.
- **Abertura de Nova York** concentra volume (11:30 BRT no horário padrão americano, 10:30 no
  verão de lá).
- **CME:** os futuros de cripto da CME negociam 24/7 desde 29/05/2026. O "gap da CME" de fim de
  semana deixou de se formar; gap antigo no gráfico é histórico, não ímã novo.
- **Fim de semana:** liquidez fina, spread aberto, movimentos de vários por cento sem notícia. Se o
  trade atravessa o fim de semana, o tamanho precisa sobreviver a isso: diga o número.
- **Cobrança de funding:** em pares de 8h, 21:00, 05:00 e 13:00 BRT; alguns pares cobram a cada 4h
  ou 1h, e a Hyperliquid de hora em hora. Com funding extremo o preço costuma oscilar perto do
  horário.
- **Eventos do ativo:** desbloqueio de tokens, upgrade de rede, decisão regulatória. Busque.

### Cenários

Três, sempre: alta, baixa e lateral.

```
CENÁRIO A (alta)
Gatilho: [fechamento H4/D1 acima de X; ou retomada de nível com OI subindo]
Entrada: [região]
Stop: [além do cluster de liquidação, não dentro dele]
Alvo 1 / Alvo 2: [níveis reais; cluster do lado oposto é alvo legítimo] (com R)
Invalidação: [ex.: fluxo de ETF negativo 3 dias seguidos; NQ perde suporte;
funding vira negativo com OI subindo]
```

Em cripto o gatilho vale dobrado: rompimento falso e caça de stop são frequentes. Prefira
fechamento de candle (H1, H4, D1) a toque de preço. No lateral, diga como ele se parece e a ação
(ficar fora, ou só nas bordas com tamanho menor).

### Tamanho, alavancagem e liquidação

Ordem obrigatória, porque a maioria faz ao contrário:

1. **Risco** em dinheiro (definido pelo trader).
2. **Distância do stop** → **quantidade** = risco ÷ (distância + taxa de ida e volta por moeda).
   Isso define o notional. A posição está definida.
3. **Alavancagem** é só quanta margem esse notional consome. A menor que cabe com folga; 2x a 5x
   cobre quase todo trade sensato.
4. **Liquidação** para essa alavancagem (isolada) ou para o saldo (cruzada). Tem que ficar **além
   do stop**, com folga de pelo menos metade da distância do stop. Se não fica, a alavancagem está
   alta (ou o saldo curto). **Nunca aperte o stop para resolver.**
5. **Funding** pelo horizonte, em R.

Fórmulas completas em `references/derivativos.md`. Na cruzada, deixe claro: a alavancagem quase
não muda a liquidação, quem muda é o saldo, e se liquidar vai o saldo inteiro.

**Com execução de código:** rode o script da pasta `scripts/` desta skill e copie a saída para o
plano:

```
python scripts/crypto_calc.py --risco 200 --entrada 60000 --stop 58500 --alav 5 \
  --funding 0.04 --horas 48 --alvo 63000 --alvo 65500
```

Opções: `--lado short`, `--modo cruzada --saldo 3000`, `--taxa 0.05` (taker por lado, em %),
`--intervalo 4` (horas entre cobranças de funding), `--mmr 0.005` (margem de manutenção da faixa),
`--margem 2000` (margem disponível), `--contrato 0.001` (passo mínimo), `--funding=-0.01`
(negativo).

**Sem execução de código** (ou se o script falhar): faça a mesma conta na conversa, uma linha por
passo, no formato abaixo, para o trader conferir:

```
Distância: |entrada - stop| = __ (__% da entrada)
Quantidade: risco ÷ (distância + taxa × (entrada + stop)) = __ moedas (arredondado no passo: __)
Notional: quantidade × entrada = __
Margem usada (isolada): notional ÷ alavancagem = __
Liquidação long: (entrada - margem ÷ quantidade) ÷ (1 - mmr) = __
Liquidação short: (entrada + margem ÷ quantidade) ÷ (1 + mmr) = __
Folga: |stop - liquidação| ÷ entrada = __% (mínimo: metade de __%)
Funding: notional × taxa × (horas ÷ intervalo) = __ (= __R)
Alvo: |alvo - entrada| ÷ distância = __R
```

Se o trader disser "vou de 20x", não discuta: mostre a liquidação a 20x ao lado do stop. O número
convence mais que o sermão. E diga que a estimativa é aproximada: **o preço de liquidação que vale
é o da tela da posição**.

### Regras de cripto para o plano

- Stop **fora** de cluster de liquidação óbvio; se não der, aceite que pode ser pescado e reduza.
- Ordem de stop na exchange, não mental. Cripto anda de madrugada.
- Atravessa fim de semana: tamanho pela volatilidade do domingo, não da terça.
- Exchange não é cofre. Se a posição é grande em relação ao patrimônio, o risco de contraparte
  entra na conta.
- Altcoin: stop mais largo e tamanho menor. Se o BTC virar, a alt costuma cair mais. O plano de
  altcoin sempre inclui "o que faço se o BTC perder X".
- Sem revanche depois de liquidação. Liquidação mostra que o tamanho estava errado, não que o
  mercado "deve" uma.

## 5. Template de saída

Cabe numa tela de celular com rolagem.

```
PLANO CRIPTO | [ATIVO] | [lado ou "avaliando"] | [perp/spot] | [exchange] | [horizonte]
RESUMO: [até 3 linhas: o contexto, o lado vulnerável nos derivativos,
o evento ou horário que pede cuidado]
Fontes: [web / print / informado / sem web] | Suposições: [lista ou "nenhuma"]

1. CONTEXTO
2. DERIVATIVOS (tabela + 1 frase)
3. AGENDA E RELÓGIO (BRT)
4. CENÁRIOS (A alta, B baixa, C lateral)
5. TAMANHO, ALAVANCAGEM E LIQUIDAÇÃO (conta passo a passo)
6. FICHA
ATIVO | lado | perp/spot | exchange | margem isolada/cruzada | horizonte
Entrada: região | Stop: nível (-__%) | Liquidação @ __x: nível (folga __%)
Tamanho: __ moedas ≈ __ notional | Margem: __ | Risco: __ (__% da conta)
Alvo 1: __ (+__R) | Alvo 2: __ (+__R) | Funding estimado: __R
Invalidação: [frase]
Próximo evento: [data e hora BRT]

Plano é hipótese, não previsão. Nada aqui é recomendação de investimento.
```

## 6. Conversa que continua

- **Posição aberta ("estou long 10x desde 61k")**: peça (ou busque) preço atual, liquidação na
  tela, modo de margem, funding e se existe stop de verdade. Responda nesta ordem: onde está em R;
  distância até a liquidação em %; se a tese ainda vale (e qual era); ação pelo plano (reduzir para
  N para afastar a liquidação, pôr o stop que falta, sair). **Se está a menos de 3% da liquidação
  sem stop, essa é a primeira frase da resposta**, antes de qualquer análise.
- **Notícia nova ou movimento brusco**: confirme o fato (busca ou o que ele colar). Diga se
  dispara alguma invalidação, se a cascata de liquidação mudou de lado e o que o plano manda. Fato
  sem fonte não muda o plano.
- **Funding virou ou disparou**: refaça só a linha do funding em R e diga se o custo passou de
  0,2R para o horizonte que resta.
- **"Mudou algo?" no meio do dia**: qual cenário está ativo, o que mudou nos derivativos e quanto
  risco sobra. Não reescreva o plano inteiro.
- **Foi liquidado ou tomou stop**: sem trade de recuperação. Ofereça olhar o que estava errado no
  tamanho ou no stop.

## 7. O que degrada o plano

- Tamanho definido pela alavancagem ("a corretora deixa 50x").
- Stop em número redondo ou logo abaixo do fundo óbvio, onde todo mundo está.
- Funding ignorado em swing de mais de 3 dias.
- "BTC vai bater 100k" como tese. Tese é mecanismo (fluxo, liquidez, estrutura), não manchete.
- Copiar posição de influenciador. Se a tese é "fulano disse", não existe invalidação possível.

## Referências

- `references/derivativos.md`: funding, OI, liquidações, basis, ETF, dominância e as fórmulas de
  tamanho, liquidação isolada e cruzada e funding (conferido em 07/11/2026). Leia nas seções de
  derivativos e de tamanho.
- `references/sessoes.md`: horários em BRT dos dados e sessões que mexem em cripto via risco
  global (conferido em 07/11/2026).
- `scripts/crypto_calc.py`: calculadora de tamanho, liquidação (isolada e cruzada), folga, funding
  e R, com cada conta impressa. Rode sempre que a execução de código estiver disponível.

## Exemplo de saída (ILUSTRATIVO, números genéricos)

```
PLANO CRIPTO | BTC | avaliando long | perp USDT | [exchange] | 2 dias
RESUMO: Preço preso entre 58.500 e 61.000 há 3 dias. Funding positivo e OI
subindo: longs lotados, então o stop do long não fica colado no fundo óbvio.
CPI americano amanhã às 10:30 BRT pede tamanho que aguente a janela.
Fontes: informado pelo trader | Suposições: margem isolada, sem taxa

5. TAMANHO, ALAVANCAGEM E LIQUIDAÇÃO (cenário A, long)
Distância: |60.000 - 58.500| = 1.500 (2,50% da entrada)
Quantidade: 200 ÷ 1.500 = 0,1333 BTC | Notional: 0,1333 × 60.000 = 8.000
Margem usada a 5x: 8.000 ÷ 5 = 1.600
Liquidação: (60.000 - 1.600 ÷ 0,1333) ÷ (1 - 0,005) = 48.000 ÷ 0,995 = 48.241
Folga: (58.500 - 48.241) ÷ 60.000 = 17,1% (mínimo: 1,25%) ok
Funding: 8.000 × 0,04% × (48 ÷ 8) = 19,20 (= 0,10R)
Alvo 1: 63.000 (3.000 ÷ 1.500 = 2,0R) | Alvo 2: 65.500 (5.500 ÷ 1.500 = 3,7R)

6. FICHA
BTC | long | perp | [exchange] | isolada | 2 dias
Entrada: 59.800-60.200 | Stop: 58.500 (-2,5%) | Liquidação @ 5x: ~48.241 (folga 17,1%)
Tamanho: 0,1333 BTC ≈ 8.000 | Margem: 1.600 | Risco: 200 (2% da conta)
Alvo 1: 63.000 (+2,0R) | Alvo 2: 65.500 (+3,7R) | Funding estimado: 0,10R
Invalidação: funding vira negativo com OI subindo, ou ETF com saída 3 dias seguidos

Plano é hipótese, não previsão. Nada aqui é recomendação de investimento.
```
