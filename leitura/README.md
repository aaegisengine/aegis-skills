# 🏆 Leitura de Gráfico: print, análise e cobrança

**A carro-chefe do pacote.** Não é uma análise avulsa: é um ciclo em dois tempos que treina o seu
olho, porque análise que nunca é cobrada não ensina nada.

## Como funciona

**Modo ANTES.** Cole o print e receba a leitura: estrutura (topos e fundos), 3 ou 4 zonas-chave, o
que o preço está fazendo agora e 2 ou 3 cenários *se/então*, cada um com invalidação. A leitura
fecha com um bloco **REGISTRO** em bloco de código, pronto pra copiar: os cenários viram compromisso.

**Modo DEPOIS.** A sessão terminou: volte com o print do desfecho. A skill confere qual cenário
rodou, onde o outro morreu e dá nota na **leitura, não no resultado**, em uma palavra:

- `CUMPRIU`: cenários bem construídos e invalidação no lugar, qualquer que tenha sido a porta.
- `FURO`: havia informação na tela que passou batido (ela diz qual).
- `SORTE`: o desfecho bateu com um cenário mal fundamentado. O resultado mais perigoso que existe.

Cada ciclo termina com **UMA lição portátil**. A cada ~10 ciclos, cole o seu log e a skill procura
o padrão do seu olho.

## O que há de novo

- **Número com origem.** Todo preço vem marcado `(lido)` (saiu de um rótulo do eixo) ou `(aprox.)`
  (interpolado). Sem eixo legível, a leitura é por posição e ela avisa.
- **Print ruim é dito como ruim.** Foto da tela tirada com celular, print borrado ou cortado: ela
  diz o que dá e o que não dá pra afirmar. Candle em formação é tratado como provisório.
- **Vários prints.** Identifica o tempo gráfico de cada um e lê do maior pro menor.
- **Feita pra ler no celular.** Abre com um RESUMO de até 3 linhas e segue em seções fixas.
- **Conversa que continua.** Print novo no meio do movimento vira ATUALIZAÇÃO sem apagar o REGISTRO
  original (leitura nova sai como `v2`). "E agora?" sem print novo não vira chute. Peça só um pedaço
  ("só as zonas") e receba só ele.
- **Funciona sozinha.** Não depende das outras skills do pacote: se elas estiverem instaladas, são
  usadas pra aprofundar; se não, a versão enxuta é feita aqui mesmo.
- **DEPOIS mais justo.** Se o preço passou perto da invalidação dentro da margem do print, o
  veredito é "inconclusivo", não um "tocou" inventado.

## Como ativar

Cole um print de gráfico e diga algo como:

> *"faz a leitura desse gráfico"* · *"analisa essa tela"* · *"como tá o WIN no M5?"*

E depois, com o print do desfecho:

> *"deu nisso"* · *"fechou assim"* · *"bateu?"*

## O que ela nunca faz

Não dá call, não escolhe "o cenário que vai rodar", não julga pelo lucro (julga pelo processo) e
não inventa número que o eixo não mostra.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · ⬅️ [Voltar ao pacote](../README.md)
