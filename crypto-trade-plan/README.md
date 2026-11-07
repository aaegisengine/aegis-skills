# 🪙 Crypto Trade Plan: o plano com a camada que só existe em cripto

Cripto pune dois tipos de trader: o que trata como ação (ignora funding, liquidação e o domingo) e
o que trata como cassino (alavanca porque a exchange deixa). O plano serve para os dois e força o
tamanho a ser definido **pelo risco**, não pela alavancagem disponível.

## O que ela entrega

Os ossos de qualquer plano (três cenários com gatilho, stop, alvo com R e invalidação), com
**RESUMO de até 3 linhas no topo**, **mais** a camada que os planos genéricos ignoram:

- **Derivativos lidos em tabela**: funding, open interest, liquidações, clusters, basis, fluxo de ETF, com a leitura de qual lado está vulnerável. Isso não escolhe direção; escolhe **onde o stop não pode ficar**
- **O relógio do 24/7**: dados dos EUA, abertura de NY, horários de cobrança de funding, fim de semana fino, desbloqueio de token
- **A ordem certa do tamanho**: risco, distância do stop, tamanho, *só então* alavancagem e **preço de liquidação com folga além do stop**
- **Margem isolada e cruzada**: na cruzada ela mostra que quem decide a liquidação é o saldo, e que se liquidar vai o saldo inteiro

## O que mudou nesta versão

- **Calculadora revisada** (`scripts/crypto_calc.py`): liquidação pela fórmula de equilíbrio (isolada e cruzada), taxa da exchange no tamanho, intervalo de funding configurável (8h, 4h, 1h), R correto mesmo com arredondamento de quantidade, números no padrão brasileiro e cada conta impressa
- **Sem execução de código**, ela faz a mesma conta passo a passo na conversa
- Dados conferidos em 07/11/2026: os futuros de cripto da CME negociam 24/7 desde 29/05/2026, então o "gap da CME" de fim de semana deixou de se formar; intervalos de funding variam por par e por exchange
- **Sem busca na web**, ela avisa e pede os números do Coinglass ou da exchange
- **Print**: todo preço sai marcado `(lido)` ou `(aprox.)`; a liquidação da tela vale mais que a estimativa
- **Conversa que continua**: posição aberta, notícia nova, funding que virou, liquidação ou stop tomado

Se você disser "vou de 20x", ela não faz sermão: mostra a liquidação a 20x ao lado do stop.
**O número convence mais que o sermão.**

## Posição aberta

*"tô long 10x desde 61k"*: se você está a menos de 3% da liquidação sem stop, **essa é a primeira
frase da resposta**, antes de qualquer análise.

## Como ativar

> *"vale entrar em ETH essa semana?"* · *"estou alavancado 10x em BTC"* · *"qual meu preço de liquidação na cruzada?"* · *"monta o plano do BTC pro fim de semana"*

## O que ela nunca faz

Não inventa preço, funding nem OI: busca na hora ou pede pra você colar, e "n/d, confira antes de
entrar" é resposta válida. Não aceita "BTC vai bater 100k" como tese (tese é mecanismo, não
manchete) e não trabalha com posição copiada de influenciador.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · 📚 [`references/derivativos.md`](references/derivativos.md) · [`references/sessoes.md`](references/sessoes.md) · 🧮 [`scripts/crypto_calc.py`](scripts/crypto_calc.py) · ⬅️ [Voltar ao pacote](../README.md)
