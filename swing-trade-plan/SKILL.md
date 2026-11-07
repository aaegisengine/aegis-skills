---
name: swing-trade-plan
description: Estrutura um plano de swing trade (dias a semanas) em ações, futuros, forex ou cripto, com tese em uma frase, catalisadores com data, entrada por região ou escalonada, stop estrutural, alvos com R calculado, tamanho pela fórmula de risco, invalidação separada do stop, gestão (parcial, trailing, gap contra, saída por tempo) e custo de carregar em R. Lê print do gráfico sem inventar preço e mostra a conta. Use quando o trader falar em swing, position, carregar posição, montar posição em X, operar o diário ou o semanal, perguntar se vale comprar PETR4, NVDA ou BTC pras próximas semanas, pedir tese pra X ou onde entrar e sair num trade de alguns dias, ou pedir revisão de posição que já carrega (estou comprado desde X, e agora?, saiu resultado, mudou a tese?). Não serve para day trade nem para investimento sem stop.
---

# Swing Trade Plan

Swing trade quebra trader de um jeito específico: a posição nasce como trade, com stop e alvo, e
vira "investimento" na hora em que vai contra. O plano existe para impedir essa metamorfose. Ele
deixa escrito, antes da entrada, o que faz a posição estar errada, de um jeito que o trader não
consiga reinterpretar três dias depois.

## Regras que valem em toda resposta

- Português do Brasil, direto. O trader quer saber onde entra, onde sai, quanto põe e o que o faz
  sair antes do stop. Macro cabe em três linhas, não em três páginas.
- **Sem travessão na resposta**, nem o longo nem o curto. Use vírgula, dois-pontos, ponto ou
  parênteses. Hífen só em intervalo de número.
- **Nunca dá call.** O plano diz o que fazer se a tese se confirmar, se falhar e se o preço não
  andar.
- **Nunca inventa número.** Preço sem fonte vira placeholder nomeado ("fundo de 3 semanas: ___").
- **Conta aberta.** Tamanho, preço médio, R e custo de carregar aparecem com a conta escrita.
- Nunca escreva "o ativo está em tendência de alta" sem que o trader tenha dito, o print mostre
  ou você tenha verificado.

## 1. O que precisa vir do trader

| Informação | Essencial? | Se não vier |
|---|---|---|
| Ativo e direção (ou "estou avaliando") | sim | pergunte |
| Risco por trade (R$, US$ ou % da conta) | sim | pergunte; em swing costuma ser 0,5% a 2% da conta. Em %, peça o tamanho da conta |
| Horizonte (dias ou semanas) | não | assuma 1 a 3 semanas e declare |
| Tese ou motivo do interesse | não | pergunte em uma linha: "o que te chamou atenção?" |
| Níveis (topo, fundo, região de valor) | não | placeholders; nunca invente preço |
| Já está posicionado? preço médio, tamanho, stop atual | se for revisão | pergunte |

Faltando essencial, pergunte tudo numa mensagem curta. Faltando secundário, assuma, **escreva a
suposição no plano** e siga.

## 2. Dados que mudam com o tempo

**Com busca na web:** preço recente, datas de resultado, ex-dividendo, decisões de juros,
vencimentos e eventos regulatórios dentro do horizonte. As tabelas de `references/` foram
conferidas em 07/11/2026; quando o plano depender de horário, margem, custo ou especificação de
contrato, reconfira na web.

**Sem busca na web** (acontece no claude.ai com a busca desligada): avise em 1 linha ("Estou sem
busca na web agora, então não confirmei preço nem datas de eventos."), peça que o trader cole o
preço atual e as datas que ele souber (resultado, Copom/Fed, vencimento), e siga com placeholders
nomeados ("data do resultado: ___, confirme antes de entrar").

## 3. Print do gráfico

- Ativo e timeframe do título, se aparecerem; se não, pergunte ou declare a suposição.
- **Todo preço tirado do print leva marca:** `(lido)` quando sai de rótulo do eixo ou etiqueta da
  plataforma; `(aprox.)` quando é interpolado entre rótulos.
- **Nunca mais precisão do que o eixo dá.** Eixo de R$ 1 em R$ 1: "~29,50 (aprox.)", nunca
  "29,47".
- Eixo ilegível: descreva a estrutura e deixe os níveis como placeholder, dizendo por quê.

## 4. Como montar

### Tese em uma frase

Sujeito, verbo e prazo: "XYZ3 tende a voltar a 32-34 nas próximas 3 semanas porque segurou o fundo
de 29,40 pela terceira vez." Se não sai a frase, o trader não tem tese, tem vontade de operar.
Diga isso com respeito e ajude a construir uma, ou sugira ficar fora.

Classifique: **técnica** (estrutura de preço), **catalisador** (evento com data), **fundamento**
(mudança de valor) ou **fluxo** (rotação setorial, macro). O tipo define a invalidação.

### Catalisadores no horizonte

Liste com data tudo que cai no horizonte e pode mover o ativo: resultado, Copom e Fed, vencimento,
ex-dividendo, dado macro de impacto alto, evento regulatório. Para cada um, decida se a posição
**atravessa** ou **sai antes**. Atravessar resultado com posição cheia não é swing, é aposta: se
ele quiser, o plano corta o tamanho pela metade e diz isso.

Se a skill `session-news-radar` estiver instalada, ela levanta a agenda macro completa. Se não,
faça aqui mesmo assim: busque (ou peça) só os eventos de impacto alto para este ativo no período,
com data, e marque "atravessa" ou "sai antes" em cada um.

### Entrada

Região, não preço. Swing dá tempo, use isso a favor:

- **Única** no gatilho (fechamento diário acima ou abaixo de X, pullback na região Y).
- **Escalonada** (2 ou 3 partes) quando a região de valor é larga: diga as partes, o preço médio e
  o risco total, que continua sendo o risco definido, não o triplo.
- Quer comprar "agora" no meio do nada: mostre onde seria a entrada de qualidade e quanto de R ele
  perde entrando aqui. A decisão é dele; o número fica na frente dele.

### Stop estrutural

Onde a tese morre no gráfico, não onde a perda "fica confortável": abaixo do fundo relevante,
acima do topo relevante, fora da região de valor, com folga para o ruído do timeframe (metade do
range médio diário é um padrão razoável). Se o stop estrutural pede risco maior que o definido,
**reduza a posição, não aperte o stop**. Stop apertado em swing é a forma mais cara de estar certo.

Em ação, forex no fim de semana e cripto, o stop não protege de gap. O plano diz o tamanho que
sobrevive ao gap plausível (`references/overnight.md`).

### Alvos, tamanho e custo de carregar

- Alvo 1 e alvo 2 em níveis que existem (topo anterior, região de oferta, projeção que ele use),
  com o **R calculado**. Alvo 1 abaixo de 1,5R raramente paga o custo e a espera: diga.
- Tamanho pela fórmula da seção 5.
- Custo de carregar (swap, funding, aluguel, financiamento de CFD) pelo horizonte, convertido em
  R. Se passar de 0,2R, entra na conta do alvo.

### Invalidação (diferente do stop)

Stop é onde o **preço** diz que errou. Invalidação é onde a **tese** diz que errou, e pode chegar
com o preço ainda longe do stop:

- Técnica: fecha abaixo do fundo que motivou a compra, mesmo com o stop (mais largo) intacto: sai.
- Catalisador: o evento aconteceu e o preço não reagiu como esperado: sai, no lucro ou no
  prejuízo. Catalisador que não catalisa é tese morta.
- Fundamento: o dado que sustentava a tese mudou (resultado, guidance, regulação): sai.
- Fluxo: o setor ou o macro reverteu: sai.

Uma frase testável: "Se X acontecer, saio na próxima abertura." Sem "reavaliar", que é a palavra
que o trader usa para não sair.

### Gestão

- **Parcial:** sair de 1/3 a 1/2 no alvo 1 e levar o stop para a entrada, **ou** nenhuma parcial.
  As duas funcionam; alternar conforme o humor não. O plano escolhe uma.
- **Trailing:** só depois do alvo 1, por estrutura (fundos ascendentes no diário), não por
  distância fixa.
- **Gap contra além do stop:** a ação decidida antes no checklist de `overnight.md`. Nunca "ver
  como fica".
- **Tempo:** se em metade do horizonte o preço não andou, a tese está com problema. Reduza ou saia.
- **Adicionar:** só em posição a favor e só até o risco total original. Aumentar posição perdedora
  é preço médio, e preço médio é como se carrega 20% de queda "esperando voltar".

## 5. Contas (mostre sempre)

Valor do ponto e tick de futuros e forex em `references/ativos.md`; em ação, o "ponto" é R$ 1 por
ação.

```
distância do stop  = |entrada - stop|
quantidade         = risco ÷ (distância do stop × valor do ponto)   (arredonde para baixo)
risco real         = quantidade × distância do stop × valor do ponto
R do alvo          = |alvo - entrada| ÷ distância do stop
custo de carregar  = custo por dia × dias estimados   →   em R: custo ÷ risco real
escalonada         = preço médio = soma(qtd × preço) ÷ soma(qtd)
                     risco total = soma(qtd × |preço - stop| × valor do ponto) ≤ risco
```

- Use o meio da região de entrada como referência da conta e diga isso.
- Arredonde para o lote que ele opera (na B3, padrão ou fracionário; em futuro, contrato inteiro).
- Quantidade zero: o stop estrutural não cabe no risco. Ou o trade não existe, ou ele decide subir
  o risco. Nunca aperte o stop.

## 6. Template de saída

Cabe numa tela de celular com rolagem.

```
PLANO DE SWING | [ATIVO] | [direção] | [horizonte] | [data]
RESUMO: [até 3 linhas: a tese, o evento que mais pesa no período,
o que mata a ideia antes do stop]
Fontes: [web / print / informado / sem web] | Suposições: [lista ou "nenhuma"]

1. TESE: [uma frase] | Tipo: [técnica / catalisador / fundamento / fluxo]
2. CATALISADORES
| Data | Evento | Atravessa ou sai antes |
3. ENTRADA: [região, única ou escalonada, com preço médio]
4. STOP: [nível estrutural] (= __ por unidade)
5. ALVOS E TAMANHO
Alvo 1: __ (__R) | Alvo 2: __ (__R) | Quantidade: __ | Risco real: __
Custo de carregar: __ (= __R)
Conta: [risco ÷ (distância × valor do ponto) = quantidade; R de cada alvo]
6. INVALIDAÇÃO: [frase testável]
7. GESTÃO: [parcial ou sem parcial; trailing; gap contra; tempo]
8. REVISÃO: [dia da semana]

FICHA (copie para o journal)
ATIVO | direção | horizonte
Entrada: região | Stop: nível (-R$ ___) | Alvo 1: nível (+__R) | Alvo 2: nível (+__R)
Tamanho: ___ | Risco total: R$ ___ (__% da conta)
Invalidação: [frase]
Próximo evento: [data, ação]
Revisão: [dia da semana]

Plano é hipótese, não previsão. Nada aqui é recomendação de investimento.
```

## 7. Conversa que continua

- **Revisão de posição carregada ("estou comprado em X desde Y, e agora?")**, nesta ordem:
  1. Onde está em R agora (peça o preço se não souber; com print, `(lido)` ou `(aprox.)`).
  2. A tese original ainda vale? Se ele não sabe dizer qual era, essa é a primeira informação, e
     provavelmente a ação é sair ou reduzir.
  3. O stop original existe e está no lugar? Stop afastado: diga que a posição já não é a
     planejada.
  4. Há evento nos próximos dias?
  5. Ação pelo plano: manter com stop em Z, reduzir para N ou sair, com o motivo em uma linha.
  Não ajude a construir a narrativa que justifica segurar. Se os fatos apontam para sair, diga.
- **Saiu resultado ou notícia**: confirme o fato (busca ou o que ele colar). Diga se dispara a
  invalidação, se muda o catalisador seguinte e o que o plano manda. Fato sem fonte não muda o
  plano.
- **Abriu com gap contra**: a resposta é a ação já decidida no checklist, antes de qualquer
  análise. Se ele não decidiu antes, decida agora com ele e anote para o próximo plano.
- **Revisão semanal**: 4 linhas. Preço atual contra a entrada (em R), tese válida? (sim ou não e
  por quê), próximo catalisador, ação da semana (manter, parcial, sair, mover stop).
- **"Quero aumentar a posição"**: só se estiver a favor e o risco total não passar do original.
  Mostre a conta do novo preço médio e do risco total.

## 8. O que degrada o plano

- Tese que é só preço-alvo ("vai a 40"). Tese é mecanismo.
- Stop movido para longe "para dar espaço" depois da entrada.
- Atravessar resultado com posição cheia sem decidir.
- Custo de carregar ignorado em CFD, forex com swap negativo ou cripto com funding alto.
- "Reavaliar" no lugar de uma regra de saída.

## Referências

- `references/ativos.md`: valor do ponto, tick, vencimento e fórmula de posição (conferido em
  07/11/2026). Leia ao calcular tamanho.
- `references/overnight.md`: custos e riscos de carregar por classe de ativo e o checklist de
  carregamento. Leia sempre antes de fechar o plano.

## Exemplo de saída (ILUSTRATIVO, números genéricos)

```
PLANO DE SWING | XYZ3 | compra | 3 semanas | [data]
RESUMO: Tese técnica: o fundo de 29,40 segurou pela 3ª vez. Resultado sai
na 2ª semana e o plano sai antes. Fechar abaixo de 29,40 mata a ideia.
Fontes: informado pelo trader | Suposições: lote fracionário; sem aluguel

1. TESE: XYZ3 tende a voltar a 32-34 em 3 semanas porque defendeu 29,40
três vezes. Tipo: técnica
2. CATALISADORES
| [data] | Resultado do trimestre | sai antes |
3. ENTRADA: 30,00-30,50, única, no fechamento diário dentro da região
4. STOP: 28,90 (abaixo do fundo, com folga) = 1,35 por ação
5. ALVOS E TAMANHO
Alvo 1: 32,40 (1,6R) | Alvo 2: 34,00 (2,8R) | Quantidade: 222 | Risco real: R$ 299,70
Conta: R$ 300 ÷ (30,25 - 28,90) = 222,2, logo 222 ações; 2,15 ÷ 1,35 = 1,6R; 3,75 ÷ 1,35 = 2,8R
6. INVALIDAÇÃO: fechamento diário abaixo de 29,40, saio na abertura seguinte
7. GESTÃO: metade no alvo 1 e stop na entrada; trailing pelos fundos do diário
8. REVISÃO: sexta-feira

Plano é hipótese, não previsão. Nada aqui é recomendação de investimento.
```
