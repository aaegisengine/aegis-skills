# 🪙 Crypto Trade Plan — o plano com a camada que só existe em cripto

Cripto pune dois tipos de trader: o que trata como ação (ignora funding, liquidação e o domingo)
e o que trata como cassino (alavanca porque a exchange deixa). O plano serve para os dois — e
força o tamanho a ser definido **pelo risco**, não pela alavancagem disponível.

## O que ela entrega

Os ossos de qualquer plano (tese, entrada, stop, alvo, invalidação) **mais** a camada que os
planos genéricos ignoram:

- **Derivativos lidos em tabela** — funding, open interest, liquidações 24h, clusters de liquidação, basis, fluxo de ETF, dominância — com a leitura de qual lado está vulnerável a squeeze. Isso não escolhe direção; escolhe **onde o stop não pode ficar**
- **O relógio do 24/7** — dados dos EUA, abertura de NY, fechamento da CME (e o gap de fim de semana que vira imã), settlements de funding, desbloqueio de token
- **A ordem certa do tamanho** — risco → distância do stop → tamanho → *só então* alavancagem (a menor que cabe) → **preço de liquidação com folga além do stop**. A maioria faz ao contrário, e é por isso que liquida
- **Calculadora de verdade** — `scripts/crypto_calc.py` devolve tamanho, liquidação, folga, custo de funding e R dos alvos, e **avisa quando a liquidação vem antes do stop**

Se você disser "vou de 20x", ela não faz sermão: mostra a liquidação a 20x ao lado do stop.
**O número convence mais que o sermão.**

## Posição aberta

*"tô long 10x desde 61k"* — se você está a menos de 3% da liquidação sem stop, **essa é a primeira frase da resposta**, antes de qualquer análise.

## Como ativar

> *"vale entrar em ETH essa semana?"* · *"estou alavancado 10x em BTC"* · *"qual meu preço de liquidação?"* · *"monta o plano do BTC pro fim de semana"*

## O que ela nunca faz

Não inventa preço, funding nem OI — busca na hora ou pede pra você colar do Coinglass, e "n/d — confira antes de entrar" é resposta válida. Não aceita "BTC vai bater 100k" como tese (tese é mecanismo, não manchete) e não trabalha com posição copiada de influenciador: se a tese é "fulano disse", não existe invalidação possível.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · 📚 [`references/derivativos.md`](references/derivativos.md) · [`references/sessoes.md`](references/sessoes.md) · 🧮 [`scripts/crypto_calc.py`](scripts/crypto_calc.py) · ⬅️ [Voltar ao pacote](../README.md)
