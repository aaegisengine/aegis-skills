---
name: crypto-trade-plan
description: Plano de trade para cripto (BTC, ETH, altcoins, perpétuos e spot) que incorpora o que o mercado de cripto tem de diferente — funding rate, open interest, clusters de liquidação, fluxo de ETFs, mercado 24/7 com fim de semana ilíquido, alavancagem e preço de liquidação, risco de exchange. Cobre intraday e swing em cripto. Use sempre que o trader mencionar bitcoin, BTC, ETH, ethereum, solana, altcoin, perp, perpétuo, funding, liquidação, alavancagem em cripto, "opero na Binance/Bybit/OKX/Hyperliquid", "como fica o BTC hoje/essa semana", "vale entrar em X", "estou alavancado 10x em...", ou pedir tamanho de posição e preço de liquidação. Inclui calculadora (scripts/crypto_calc.py) de tamanho, liquidação e custo de funding. Para ativos tradicionais use day-trade-plan ou swing-trade-plan.
---

# Crypto Trade Plan

Cripto pune dois tipos de trader: o que trata como ação (ignora funding, liquidação e o domingo) e o que trata como cassino (alavanca porque a exchange deixa). O plano serve para os dois: traz as variáveis que só existem aqui e força o tamanho a ser definido pelo risco, não pela alavancagem disponível.

Escreva em português do Brasil, direto, sem "to the moon" nem "vai zerar". Um plano de cripto tem os mesmos ossos de qualquer plano — tese, entrada, stop, alvo, tamanho, invalidação — mais uma camada de derivativos e de horário que você precisa cobrir.

## O que precisa vir do trader

| Informação | Essencial? | Se não vier |
|---|---|---|
| Ativo (BTC, ETH, SOL, par específico) | sim | pergunte; se disser só "cripto", assuma BTC e diga |
| Spot ou perpétuo? Exchange? | não | assuma perpétuo USDT-margined e diga |
| Risco por trade (USD ou % da conta) | sim | pergunte |
| Horizonte (horas / dias / semanas) | não | pergunte em uma linha — define quanto funding pesa |
| Alavancagem que pretende usar | não | calcule a necessária, não a máxima |
| Níveis que ele vê / screenshot | não | placeholders; nunca invente preço |
| Já está posicionado? | se for revisão | preço médio, tamanho, alavancagem, liquidação atual |

Você não vê o gráfico nem o livro. Preço, funding, OI e liquidações mudam a cada minuto: busque na web ("BTC funding rate", "BTC open interest", "BTC liquidations today", "bitcoin ETF flows") ou peça ao trader que cole os números do Coinglass/exchange. Não escreva "funding está alto" sem número e fonte. Se não achou, escreva "funding: n/d — confira antes de entrar" e siga.

## Como montar

### 1. Contexto em 3 linhas

O que o BTC (e o ativo, se não for BTC) fez nas últimas 24h e na semana; o que o NQ e o DXY estão fazendo (cripto anda com risco global na maioria dos regimes); se houve liquidação grande recente (mercado "limpo" ou "lotado"). Para altcoin: a dominância do BTC está subindo ou caindo — isso define se a alt tem vento a favor.

### 2. Camada de derivativos

Tabela curta com o que você achou. Leia `references/derivativos.md` para interpretar cada linha.

```
| Métrica | Valor | Leitura |
| Funding (8h) | +0,04% | comprados pagando; mercado inclinado long |
| OI | US$ 18,2 bi (↑ 6% em 24h) | dinheiro novo entrando na alta — sustento, mas alavancado |
| Liquidações 24h | US$ 240 mi (80% shorts) | vendidos já limpos acima de 61k |
| Clusters de liquidação | 58,8k (longs) / 62,5k (shorts) | imãs de pavio nos dois lados |
| Basis perp/spot | +0,08% | normal |
| Fluxo ETF (ontem) | +US$ 310 mi | demanda spot confirmando |
```

Conclua em uma frase: qual lado está vulnerável a squeeze. Isso não decide a direção do trade; decide onde o stop **não** pode ficar e qual cenário tem cascata a favor.

### 3. Agenda e horário

Cripto não fecha, mas tem relógio:

- **Dados dos EUA (09:30 BRT) e FOMC** movem BTC como movem o NQ. Liste os da janela do trade (busque; `references/sessoes.md` tem os horários).
- **Abertura de NY (10:30/11:30 BRT)** e **fechamento da CME de BTC (sexta 17:00 NY)** concentram volume; o gap da CME entre sexta e domingo é um imã conhecido.
- **Fim de semana**: liquidez fina, spread aberto, movimento de 5–10% sem notícia. Se o trade atravessa o fim de semana, o tamanho precisa sobreviver a isso — diga o número.
- **Funding settlement** (00:00, 08:00, 16:00 UTC = 21:00, 05:00, 13:00 BRT): preço costuma oscilar perto do horário quando o funding está extremo.
- **Eventos do ativo**: desbloqueio de tokens, upgrade de rede, decisão regulatória, audiência, lançamento de ETF. Busque.

### 4. Cenários

Três, como sempre: alta, baixa, lateral. Estrutura por cenário:

```
CENÁRIO A — Alta
Gatilho: [fechamento H4/D1 acima de X; ou reclaim de nível com OI subindo]
Entrada: [região]
Stop: [além do cluster de liquidação, não dentro dele]
Alvo 1 / Alvo 2: [níveis reais; cluster de liquidação do lado oposto é alvo legítimo]
Invalidação: [o que mata a ideia: ex. fluxo de ETF vira negativo 3 dias seguidos; NQ perde suporte; funding vira negativo com OI subindo]
```

Em cripto, "gatilho" vale dobrado: o mercado pesca stops e rompimentos falsos com frequência maior que em ativos regulados. Prefira confirmação por fechamento de candle (H1/H4/D1) a toque de preço.

### 5. Tamanho, alavancagem e liquidação

Ordem obrigatória do raciocínio, porque a maioria faz ao contrário:

1. **Risco** em USD (definido pelo trader).
2. **Distância do stop** em % → **tamanho** da posição (`risco ÷ distância`). Isso é o notional. Pronto — a posição está definida.
3. **Alavancagem** é só quanto de margem esse notional vai consumir. Escolha a menor que cabe na conta com folga; 2–5x cobre quase todo trade sensato.
4. **Preço de liquidação** para essa alavancagem. Ele tem que ficar **além do stop com folga** (pelo menos metade da distância do stop). Se não fica, a alavancagem está alta demais — não o stop apertado demais.
5. **Custo de funding** pelo horizonte, em R.

Rode `scripts/crypto_calc.py` com os números — ele devolve tamanho, liquidação, folga, funding e R dos alvos, e avisa quando a liquidação vem antes do stop. Copie a saída para o plano:

```
python scripts/crypto_calc.py --risco 200 --entrada 60000 --stop 58500 --alav 5 --funding 0.04 --horas 48 --alvo 63000 --alvo 65500
```

Se o trader disser "vou de 20x", não discuta a alavancagem; mostre a liquidação a 20x ao lado do stop. O número convence mais que o sermão.

### 6. Regras específicas de cripto para o plano

- Stop **fora** de cluster de liquidação óbvio; se não der, aceite que ele será pescado e reduza o tamanho.
- Ordem de stop na exchange (não mental) — cripto anda de madrugada.
- Posição que atravessa fim de semana: tamanho pela volatilidade do domingo, não da terça.
- Risco de exchange: não é o lugar para guardar o que não está em posição. Se a posição é grande em relação ao patrimônio, diga que o risco de contraparte entra na conta.
- Altcoin: stop mais largo (volatilidade) e tamanho menor; se o BTC virar, a alt cai o dobro. O plano de altcoin sempre inclui "o que faço se o BTC perder X".
- Sem revenge depois de liquidação. Liquidação é sinal de que o tamanho estava errado, não de que o mercado "deve" uma.

### 7. Ficha final

```
ATIVO | lado | perp/spot | exchange | horizonte
Entrada: região | Stop: nível (−__%) | Liquidação @ __x: nível (folga __%)
Tamanho: __ moedas ≈ US$ __ notional | Margem: US$ __ | Risco: US$ __ (__% da conta)
Alvo 1: __ (+__R) | Alvo 2: __ (+__R) | Funding estimado: __R
Invalidação: [frase]
Próximo evento: [data/hora BRT]
```

## Revisão de posição aberta

Quando ele chega com "estou long 10x desde 61k": pergunte (ou busque) preço atual, liquidação atual, funding, e se há stop de verdade. Responda na ordem: onde está em R; a distância até a liquidação em %; se a tese ainda vale (e qual era); ação concreta (reduzir para N para afastar a liquidação, mover stop, sair). Se ele está a menos de 3% da liquidação sem stop, isso é a primeira frase da resposta, antes de qualquer análise.

## O que degrada o plano

- Tamanho definido pela alavancagem ("a corretora deixa 50x").
- Stop em número redondo ou logo abaixo do fundo óbvio — é onde todo mundo está e onde a liquidez é caçada.
- Ignorar funding em swing de mais de 3 dias.
- "BTC vai bater 100k" como tese. Tese é mecanismo (fluxo, liquidez, estrutura), não preço-alvo de manchete.
- Copiar posição de influenciador. Se a tese é "fulano disse", não há invalidação possível.

Termine com: *Plano é hipótese, não previsão. Nada aqui é recomendação de investimento.*

## Referências

- `references/derivativos.md` — como ler funding, OI, liquidações, basis, ETF flows, dominância; fórmula de liquidação. Leia ao montar a seção 2 e a seção 5.
- `references/sessoes.md` — horários em BRT dos dados e sessões que movem cripto via risco global.
- `scripts/crypto_calc.py` — calculadora de tamanho, liquidação, folga e funding. Rode sempre na seção 5.
