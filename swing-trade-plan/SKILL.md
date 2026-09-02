---
name: swing-trade-plan
description: Estrutura um plano de swing trade (posição de dias a semanas) em ações, futuros, forex ou cripto — tese em uma frase, catalisadores no horizonte, região de entrada (inclusive escalonada), stop estrutural, alvos com R calculado, tamanho pela fórmula de risco, gestão da posição (parciais, trailing, gap contra), custos de carregar overnight e o que invalida a tese. Use sempre que o trader falar em "swing", "position", "carregar posição", "montar posição em X", "operar o gráfico diário/semanal", "vale comprar PETR4/NVDA/BTC pras próximas semanas?", "tese pra X", "onde entro e onde saio num trade de alguns dias", ou pedir para revisar uma posição que ele já está carregando. Não é para day trade (use day-trade-plan) nem para investimento de longo prazo sem stop.
---

# Swing Trade Plan

Swing trade quebra trader de um jeito específico: a posição começa como trade, com stop e alvo, e vira "investimento" na hora em que vai contra. O plano existe para impedir essa metamorfose. Ele precisa deixar escrito, antes da entrada, o que faz a posição estar errada — de um jeito que o trader não consiga reinterpretar três dias depois.

Escreva em português do Brasil, direto. O trader quer saber onde entra, onde sai, quanto põe e o que o faz sair antes do stop. Análise de cenário macro tem lugar, mas em três linhas, não em três páginas.

## O que precisa vir do trader

| Informação | Essencial? | Se não vier |
|---|---|---|
| Ativo e direção (ou "estou avaliando") | sim | pergunte |
| Risco por trade (R$, US$ ou % da conta) | sim | pergunte — em swing costuma ser 0,5–2% da conta |
| Horizonte (dias / semanas) | não | assuma 1–3 semanas e declare |
| Tese ou motivo do interesse | não | pergunte em uma linha: "o que te chamou atenção?" — a resposta define se é tese técnica, fundamentalista ou de evento |
| Níveis que ele vê (topo, fundo, região de valor) | não | placeholders nomeados; nunca invente preço |
| Já está posicionado? preço médio, tamanho, stop atual | se for revisão | pergunte |

Você não vê o gráfico. Trabalhe com o que ele descreve, com screenshot se mandar, e com o que você busca na web (preço recente, datas de eventos, resultados). Nunca escreva "o ativo está em tendência de alta" sem que ele tenha dito ou você tenha verificado. Se não tiver informação de preço, os níveis ficam como "___" para ele preencher.

## Como montar

### 1. Tese em uma frase

Uma frase, com sujeito, verbo e prazo: "PETR4 tende a recuperar 38–40 nas próximas 3 semanas porque o Brent segurou 80 e o resultado do trimestre vem forte." Se você não consegue escrever a frase, o trader não tem tese — tem vontade de operar. Diga isso com respeito e ajude a construir uma, ou sugira ficar fora.

Classifique a tese: **técnica** (estrutura de preço), **catalisador** (evento com data), **fundamento** (mudança de valor), ou **fluxo** (rotação setorial, macro). O tipo define o que invalida (seção 6).

### 2. Catalisadores no horizonte

Busque na web e liste, com data, tudo que cai dentro do horizonte e pode mover o ativo: resultado trimestral, decisão de juros (Copom, Fed), vencimento de futuro/opções, ex-dividendo, dado macro de impacto alto, evento regulatório. Para cada um, decida se a posição **atravessa** o evento ou **sai antes**. Atravessar resultado com posição cheia não é swing, é aposta — se ele quiser fazer, o plano reduz o tamanho para metade e diz isso.

### 3. Entrada

Região, não preço. Swing dá tempo — usar isso a favor:

- **Entrada única** no gatilho (fechamento diário acima/abaixo de X, pullback em região Y).
- **Entrada escalonada** (2–3 partes) quando a região de valor é larga: diga as partes, o preço médio resultante e o risco total — que continua sendo o risco definido, não o triplo.
- Se ele quer comprar "agora" no meio de nada: diga onde seria a entrada de qualidade e o que ele perde entrando aqui (R pior). A decisão é dele; o número tem que estar na frente dele.

### 4. Stop estrutural

Stop de swing fica onde a tese morre no gráfico, não onde a perda "fica confortável". Abaixo do fundo relevante, acima do topo relevante, fora da região de valor — com folga para o ruído do timeframe (metade do range médio diário é um padrão razoável). Se o stop estrutural implica risco maior do que o definido, **reduz-se a posição**, não se aperta o stop. Stop apertado em swing é a forma mais cara de estar certo.

Lembre o trader: em ação, forex de fim de semana e cripto, o stop não protege de gap. `references/overnight.md` tem o checklist; o plano precisa dizer o tamanho que sobrevive ao gap plausível.

### 5. Alvos e tamanho

- Alvo 1 e alvo 2 em níveis que existem (topo anterior, região de oferta, projeção que ele use), com o **R múltiplo calculado** de cada um. Swing com alvo 1 abaixo de 1,5R raramente compensa o custo e a espera; diga.
- Tamanho pela fórmula: `quantidade = risco / (distância_do_stop × valor_do_ponto ou preço unitário)`. Arredonde para baixo. `references/ativos.md` tem o valor do ponto de futuros e forex; para ação, é o próprio preço.
- Custo de carregar (swap, funding, aluguel, financiamento de CFD) pelo horizonte estimado, convertido em R. Se comer mais de 0,2R, entra no cálculo do alvo.

### 6. Invalidação (diferente do stop)

Stop é onde o **preço** diz que errou. Invalidação é onde a **tese** diz que errou — e pode acontecer com o preço ainda longe do stop. Exemplos por tipo de tese:

- Técnica: perde a estrutura (fecha abaixo do fundo que motivou a compra) mesmo que o stop, mais largo, ainda não tenha sido tocado → sai.
- Catalisador: o evento aconteceu e o preço não reagiu como esperado → sai, independentemente de estar no lucro ou no prejuízo. Catalisador que não catalisa é tese morta.
- Fundamento: o dado que sustentava a tese muda (resultado, guidance, decisão regulatória) → sai.
- Fluxo: o setor/macro reverte (ex.: a rotação para commodities parou) → sai.

Escreva a invalidação em uma frase testável. "Se X acontecer, saio na próxima abertura" — sem "reavaliar", que é a palavra que o trader usa para não sair.

### 7. Gestão

Regras mecânicas para o tempo em posição:

- **Parcial**: sair de 1/3 a 1/2 no alvo 1 e mover o stop para o preço de entrada — ou não fazer parcial nenhuma. Ambas funcionam; alternar entre elas conforme o humor não. O plano escolhe uma.
- **Trailing**: só depois do alvo 1, e por estrutura (fundos ascendentes no diário), não por distância fixa.
- **Gap contra além do stop**: a ação já decidida em `overnight.md` (sair na abertura / esperar N minutos). Nunca "ver como fica".
- **Tempo**: se em X dias (padrão: metade do horizonte) o preço não andou, a tese está com problema. Reduzir ou sair — swing que não anda vira capital parado com risco aberto.
- **Adicionar**: só em posição que já está a favor e só até o risco total original. Aumentar em posição perdedora é a definição de preço médio, e preço médio é como se carrega 20% de queda "esperando voltar".

### 8. Revisão semanal

Ofereça um formato de 4 linhas para ele voltar toda semana (ou no fim do dia, se ele preferir): preço atual vs. entrada (em R), tese ainda válida? (sim/não e por quê em uma linha), próximo catalisador, ação para a semana (manter / parcial / sair / mover stop).

## Revisão de posição que ele já carrega

Quando o trader chegar com "estou comprado em X desde Y, e agora?", faça na ordem:

1. Onde está em R agora (peça o preço se não souber).
2. A tese original ainda vale? Se ele não sabe dizer qual era a tese, essa é a primeira informação — e provavelmente a resposta é sair ou reduzir.
3. O stop original existe e está no lugar? Se ele moveu o stop para longe, diga que a posição já não é a que foi planejada.
4. Há evento nos próximos dias?
5. Recomendação concreta: manter com stop em Z, reduzir para N, ou sair — com o motivo em uma linha.

Não ajude a construir a narrativa que justifica segurar a posição. Se os fatos apontam para sair, diga.

## Formato de saída

Títulos 1–8 na ordem. Tabela para catalisadores. Blocos curtos para o resto. No fim, uma "ficha" de 6 linhas que ele pode copiar para o journal ou para a plataforma:

```
ATIVO | direção | horizonte
Entrada: região | Stop: nível (−R$ ___) | Alvo 1: nível (+__R) | Alvo 2: nível (+__R)
Tamanho: ___ | Risco total: R$ ___ (__% da conta)
Invalidação: [frase]
Próximo evento: [data — ação]
Revisão: [dia da semana]
```

Termine com: *Plano é hipótese, não previsão. Nada aqui é recomendação de investimento.*

## Referências

- `references/ativos.md` — valor do ponto, tick, custos e fórmula de posição para futuros, forex, CFD e cripto. Leia ao calcular tamanho.
- `references/overnight.md` — custos e riscos de carregar posição por classe de ativo (gap, margem, swap, funding, resultado, vencimento) e o checklist de carregamento. Leia sempre antes de fechar o plano.
