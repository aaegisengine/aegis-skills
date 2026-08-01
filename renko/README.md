# 🧱 Leitura Renko — a gramática do tijolo

Renko não é candle sem pavio — **é outra linguagem.** Não existe eixo de tempo, o tijolo já é
um filtro, e a reversão CUSTA (2 tijolos contra pra pintar 1 de cor oposta). Esta skill lê a
tela com a gramática certa, em vez de aplicar conceito de candle onde ele não existe.

## O que ela faz

- **Leitura de sequência:** tendência (tijolos consecutivos), congestão (alternância na mesma
  faixa — o range do renko), reversão em curso (2+ contra após sequência; 1 tijolo isolado em
  tendência forte é normal, e ela não chama de reversão).
- **Zonas por FLIPS, não por toques:** suporte/resistência em renko é a faixa onde a **cor
  virou** repetidas vezes — pilha de reversões, bordas de caixa de congestão, flip de papel.
- **Rompimento medido em tijolos:** 2-3 consecutivos além da borda = força; 1 tijolo além e a
  cor virando de volta = rompimento falho (o spring do renko — e costuma valer mais que o
  rompimento em si).
- **A parte que ninguém entrega — crítica da calibração:** tijolo pequeno demais deixa o ruído
  passar (a tela inteira parece congestão); grande demais come a estrutura. Ela diagnostica o
  SEU print — e nunca receita número mágico, porque calibração se testa no seu ativo.
- **Cenários na moeda do renko:** *"se imprimir o 2º tijolo de baixa abaixo do piso da caixa,
  a congestão resolveu — e o cenário morre se a cor virar de volta pra dentro"*.

## Como ativar

> *"lê esse renko"* · *"suportes e resistências no renko"* · *"o que esse renko tá dizendo?"*

## O que ela nunca faz

Não aplica figura de candle em tijolo, não infere tempo (renko esconde o tempo — ela declara),
não receita tamanho de tijolo, não dá call.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · ⬅️ [Voltar ao pacote](../README.md)
