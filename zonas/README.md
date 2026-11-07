# 📏 Zonas de Suporte e Resistência: o mapa que um trader olharia

A primeira coisa que separa este mapa do mapa amador: **suporte e resistência são ZONAS, não
linhas.** O preço não respeita um número exato, respeita uma região onde ordens se acumularam.
Linha fina cria uma precisão que o mercado não tem.

## O que ela faz

- **Âncoras de verdade:** extremos revisitados, origem de movimento forte, acúmulo de fechamentos,
  pavios longos repetidos no mesmo nível.
- **Zona como banda,** com largura calibrada pela volatilidade da própria tela (entre meio e um
  candle médio).
- **Toque com critério:** só conta quando o preço chega e se afasta de forma visível. Atravessar a
  banda sem reagir não é toque.
- **Flip de verdade:** suporte que vira resistência (e o contrário) só é chamado de flip quando
  houve rompimento por fechamento **e** reteste pelo outro lado.
- **Frescor:** toques espaçados dão força; toques em sequência com reação encolhendo gastam a zona,
  e ela marca `gasta`.
- **Teto de 6 zonas.** Cortar é parte do trabalho.
- **Na zona que importa agora, os dois cenários:** o que a reação confirmaria, o que o rompimento
  confirmaria e o sinal de rompimento falso, sem escolher um.

## O que há de novo

- **Número com origem.** Cada ponta da zona vem marcada `(lido)` (rótulo do eixo) ou `(aprox.)`
  (interpolada), sem mais precisão do que o eixo permite.
- **Print ruim é dito como ruim.** Foto da tela com celular, print borrado ou cortado: ela diz o que
  continua confiável (a ordem das zonas) e o que não (o preço fino).
- **Vários prints:** lê do tempo gráfico maior pro menor, marca o TF de cada zona e funde
  confluências, sem passar de 6 no total.
- **Feita pra ler no celular:** RESUMO de até 3 linhas e seções fixas.
- **Conversa que continua:** print novo atualiza o mapa em vez de refazer; "só os suportes" entrega
  só os suportes; "essa resistência segura?" recebe os dois cenários, nunca um sim ou não.
- **Funciona sozinha,** inclusive com print de renko, mesmo sem as outras skills instaladas.

## Como ativar

> *"marca os suportes e resistências"* · *"onde o preço pode reagir?"* · *"quais os níveis importantes?"*

## O que ela nunca faz

Não risca linha exata como verdade, não diz que zona "vai segurar" (zona concentra probabilidade
de reação, não garante nada) e não recomenda entrada, stop ou alvo.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · ⬅️ [Voltar ao pacote](../README.md)
