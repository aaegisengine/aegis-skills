# 🧱 Leitura Renko: a gramática do tijolo

Renko não é candle sem pavio, **é outra linguagem.** Não existe eixo de tempo, o tijolo já é
um filtro, e a reversão custa caro (no renko clássico, o preço anda 2 tijolos contra pra pintar
1 de cor oposta). Esta skill lê a tela com a gramática certa, em vez de aplicar conceito de
candle onde ele não existe.

## O que ela faz

- **Lê o print com honestidade:** confere escala e último preço do eixo; todo preço sai marcado
  `(lido)` ou `(aprox.)`, sem mais precisão do que o eixo dá. Sem eixo, a leitura é em tijolos.
  Foto de tela, print cortado ou borrado: ela avisa o que isso limita.
- **Descobre o tijolo:** lê o tamanho no print, usa o que você informar ou estima pela escala.
  E diz quando a conclusão depende do tipo (pontos fixos ou ATR, reversão de 2 tijolos ou de 1,
  construção por fechamento ou por máxima e mínima, com ou sem pavio).
- **Sequências e congestão:** tendência (tijolos consecutivos), caixas de congestão (o range do
  renko), reversão em curso (2+ contra após perna longa; 1 tijolo isolado é normal).
- **Zonas por FLIPS, não por toques:** a faixa onde a cor virou repetidas vezes, bordas de caixa,
  flip de papel. Largura mínima de 1 tijolo.
- **Rompimento medido em tijolos:** 2-3 consecutivos além da borda = força; 1 tijolo além e a cor
  voltando = rompimento falho.
- **Crítica da calibração:** tijolo pequeno demais deixa o ruído passar; grande demais come a
  estrutura. Diagnóstico do SEU print, nunca número mágico.
- **Conversa que continua:** print novo vira ATUALIZAÇÃO (o que mudou, qual cenário avançou ou
  morreu). Tijolo diferente: ela avisa que não dá pra comparar e refaz.

## Resposta pensada pra celular

RESUMO de até 3 linhas no topo, seções fixas (leitura do print, calibração, sequências, zonas,
cenários, o que observar), 40 a 60 linhas. Versão longa só se você pedir.

## Como ativar

> *"lê esse renko"* · *"suportes e resistências no renko"* · *"meu tijolo está bom?"* ·
> *"o que esse renko tá dizendo?"* · *"e agora?"* + print novo

**Dica:** envie o print com o eixo de preço visível e diga o tamanho e o tipo do tijolo. Se não
souber, ela estima e avisa.

## O que ela nunca faz

Não aplica figura de candle em tijolo, não infere tempo, não receita tamanho de tijolo, não
inventa preço e não dá call. Funciona sozinha: se outra skill do pacote não estiver instalada,
ela faz a versão enxuta da tarefa.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · ⬅️ [Voltar ao pacote](../README.md)
