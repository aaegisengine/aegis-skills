# 📋 Day Trade Plan: o raciocínio das 08:30, escrito pra valer às 10:47

Um plano de day trade existe para **tirar decisão da hora errada**. A skill faz o raciocínio
pré-sessão e deixa escrito de um jeito que, com o WIN caindo 800 pontos, você olha e responde em
5 segundos: *"isso está no plano ou não?"*

## O que ela entrega

Um plano de formato fixo, com **RESUMO de até 3 linhas no topo**, que cabe numa tela de celular:

1. **Contexto em 3 linhas**: ontem, overnight e o que isso implica pra abertura
2. **Agenda do dia em BRT** com janela de risco nos dados de impacto alto
3. **Níveis com origem**, no máximo 6 a 8; nível sem origem não entra
4. **Três cenários sempre**: alta, baixa e **lateral**, cada um com gatilho, entrada por região, stop estrutural, alvos com **R calculado**, contratos calculados e invalidação
5. **Regras do dia**: risco por trade, perda máxima que fecha a plataforma, teto de trades, pausa após 2 stops. Meta de ganho **não existe**
6. **Checklist pré-entrada**: 5 perguntas de sim ou não; qualquer "não" = não entra
7. **Fechamento**: 3 campos pro journal

**A conta aparece sempre**, com custo por contrato quando você informar, pra você conferir cada
número.

## O que mudou nesta versão

- Horários de sessões, grade da B3 e regime de horário de verão **conferidos em 07/11/2026**, com
  fonte e data; a skill reconfere na web quando a resposta depende disso
- **Sem busca na web**, ela avisa em 1 linha, pede a agenda e o preço colados e segue com
  placeholders
- **Print do gráfico**: todo preço sai marcado `(lido)` ou `(aprox.)`, sem precisão inventada
- **Conversa que continua**: revisão no meio do pregão, posição já aberta, notícia nova, perda máxima batida
- Funciona sozinha: se a `session-news-radar` estiver instalada, a agenda sai completa; se não, sai enxuta aqui mesmo

## O que precisa vir de você

Só **ativo** e **risco por trade**. O resto ela assume um padrão razoável e **declara a
suposição no plano**. Funciona pra WIN, WDO, NQ/MNQ, ES/MES, ouro, forex e cripto intraday.

## Como ativar

> *"plano pra amanhã no WIN, risco de 100 por trade"* · *"como opero o ouro hoje?"* · *"mudou algo? ainda vale o cenário B?"* · *"entrei vendido em 99.800, e agora?"* · *"fechou a sessão, o que anoto?"*

## O que ela nunca faz

Não vê o mercado e **não inventa preço**: sem informação, o nível vira placeholder nomeado
("máxima de ontem: ___"). Não dá call, não prevê direção. O plano diz o que fazer **se** subir,
**se** cair, **se** não fizer nada.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · 📚 [`references/sessoes.md`](references/sessoes.md) · [`references/ativos.md`](references/ativos.md) · ⬅️ [Voltar ao pacote](../README.md)
