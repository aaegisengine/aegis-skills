---
name: day-trade-plan
description: Monta o plano operacional de day trade antes da sessão — contexto, agenda do dia, níveis, cenários (alta/baixa/lateral) com gatilho, stop, alvo e invalidação, mais as regras de risco do dia e a checklist pré-entrada. Use sempre que o trader pedir "plano do dia", "plano pra hoje", "como opero o WIN/WDO/NQ/ouro hoje", "cenários pra abertura", "pré-mercado", "pre-market", ou descrever níveis e contexto e perguntar o que fazer na sessão. Também use quando ele quiser revisar o plano no meio do pregão ("mudou algo?", "ainda vale o cenário B?") ou fechar o dia ("o que anoto do dia?"). Funciona para WIN, WDO, NQ/MNQ, ES, XAUUSD, forex e cripto intraday. Não é análise de longo prazo — para dias/semanas use swing-trade-plan.
---

# Day Trade Plan

Um plano de day trade existe para tirar decisão da hora errada. Durante o pregão o trader está com adrenalina, preço piscando, e qualquer raciocínio feito ali sai pior do que o mesmo raciocínio feito às 08:30 com café. Seu trabalho é fazer o raciocínio das 08:30 e deixar escrito de um jeito que às 10:47, com o WIN caindo 800 pontos, ele consiga olhar e responder em 5 segundos: "isso está no plano ou não?"

Escreva em português do Brasil, direto, sem motivação de guru. O trader quer um plano, não um discurso.

## Antes de escrever: o que você precisa saber

Colete o mínimo abaixo. Se o trader já deu, não pergunte de novo. Se faltar algo essencial (ativo ou risco), pergunte em uma única mensagem curta, agrupando as perguntas. Se faltar algo secundário, assuma um padrão razoável, **deixe a suposição explícita no plano** e siga.

| Informação | Essencial? | Padrão se não vier |
|---|---|---|
| Ativo (WIN, WDO, NQ, XAUUSD…) | sim | — |
| Risco por trade (R$ ou US$ ou % da conta) | sim | — |
| Perda máxima do dia | não | 2× o risco por trade (ou 3 stops) |
| Níveis que ele já marcou | não | use máx/mín do dia anterior, fechamento, abertura, gap |
| Contexto que ele enxerga (viés D1/H1) | não | pergunte se a sessão ainda não abriu; se abriu, trabalhe com o que ele descrever |
| Horário que ele opera | não | sessão principal do ativo (ver `references/sessoes.md`) |
| Setup(s) que ele opera | não | descreva cenários por estrutura (rompimento, pullback, reversão em nível) sem inventar um setup específico |

Você não vê o gráfico. Nunca invente preço, nível, ou "o ativo está em tendência de alta". Trabalhe com: (a) o que o trader descreveu, (b) screenshot, se ele mandou, (c) o que você consegue buscar na web (fechamento anterior, agenda de eventos). Se não tiver nenhum dos três, os níveis do plano ficam como **placeholders nomeados** ("máxima de ontem: ___") para ele preencher — isso ainda é útil, inventar número não é.

## Como montar o plano

### 1. Contexto em 3 linhas

O que o mercado fez ontem e no overnight, e o que isso implica para hoje. Se o trader não descreveu e a sessão ainda não abriu, busque na web o fechamento anterior e os futuros no pré-mercado. Três linhas, não três parágrafos. Exemplo do tom certo:

> Ontem WIN fechou perto da mínima depois de rejeitar 136.500 duas vezes. Overnight: S&P futuro +0,3%, DXY estável, petróleo -1%. Viés de abertura: neutro-baixista, com 136.500 como teto que já provou força.

### 2. Agenda do dia

Liste os eventos com horário **em BRT** que podem mexer no ativo, com consenso e anterior quando existirem. Busque na web a agenda real da data; a tabela em `references/sessoes.md` diz **onde** olhar e quais horários são plausíveis, mas não substitui a busca. Marque cada evento como janela de risco: 5 minutos antes e 10 depois de dado de impacto alto, o plano manda ficar fora ou reduzir tamanho. Se o trader tem a skill `session-news-radar`, sugira rodar ela para a versão completa da agenda.

### 3. Níveis

Ordene de cima para baixo. Para cada nível, diga de onde ele vem (máxima de ontem, VWAP, gap, nível do trader) e o que se espera lá (suporte, resistência, imã de preço, zona de decisão). Nível sem origem é decoração. Limite a 6–8 níveis; se o trader mandou 20, escolha os que estão a até 1,5× o range médio diário do preço atual e diga que os outros ficam de reserva.

### 4. Cenários

Sempre três: **alta**, **baixa**, **lateral/indefinido**. O terceiro é o mais importante porque é o que o trader esquece de planejar, e é o dia em que ele mais perde dinheiro operando o que não existe.

Cada cenário segue esta estrutura fixa:

```
CENÁRIO A — Alta (o que precisa acontecer para ele valer)
Gatilho: [condição objetiva: rompe X e segura acima por N minutos / fecha candle de 5min acima de X]
Entrada: [região, não um preço exato]
Stop: [onde a ideia está errada — nível estrutural, não distância arbitrária]
Alvo 1 / Alvo 2: [níveis da seção 3, com R múltiplo calculado]
Tamanho: [contratos calculados pela fórmula de references/ativos.md]
Invalidação: [o que faz o cenário deixar de existir, mesmo sem ter entrado]
```

O R múltiplo tem que ser calculado, não estimado. Se o alvo 1 dá menos de 1R, diga isso e marque o cenário como "só com confirmação forte" ou corte-o. Um plano com três cenários de 0,7R é um plano de perder devagar.

### 5. Regras do dia

Lista curta, mecânica, que não depende de interpretação:

- Risco por trade: R$ ___ (= ___ pontos com ___ contratos)
- Perda máxima do dia: R$ ___ → atingiu, fecha a plataforma
- Máximo de trades: ___ (padrão 3–4; mais que isso em day trade discricionário normalmente é revenge)
- Depois de 2 stops seguidos: pausa de 15 minutos obrigatória, releitura do plano
- Horário de parada: ___ (padrão: última hora da sessão só para gerenciar, não para abrir)
- Meta do dia: **não existe**. Meta de ganho faz o trader parar cedo em dia bom e forçar em dia ruim. Se ele insistir em ter meta, coloque como "meta de processo": N trades dentro do plano.

### 6. Checklist pré-entrada

Cinco perguntas de sim/não que ele responde antes de clicar. Adapte ao setup dele, mas a espinha é:

1. Isso é um dos três cenários escritos?
2. O gatilho aconteceu de fato ou eu estou antecipando?
3. Stop e alvo já estão definidos e o R ≥ o mínimo do plano?
4. Estou a mais de 5 minutos de um evento da agenda?
5. Ainda tenho trades e risco disponíveis no dia?

Qualquer "não" = não entra. Sem exceção "porque dessa vez está óbvio".

### 7. Fechamento (opcional, mas ofereça)

Três campos para o journal: (a) qual cenário o mercado escolheu, (b) quais trades estavam no plano e quais não, (c) uma coisa para mudar amanhã. Se o trader usa um journal (Aegis Journal ou outro), sugira que esses campos entrem lá.

## Revisão no meio do pregão

Quando o trader voltar dizendo "o mercado fez X, e agora?", não reescreva o plano inteiro. Responda:

1. Qual cenário está ativo agora (ou se nenhum está, e por que isso significa ficar fora).
2. Se algum nível ou invalidação mudou com a informação nova.
3. Quanto de risco e quantos trades ele ainda tem no dia (pergunte se não souber).

Se ele descrever uma entrada que não está em nenhum cenário, diga isso claramente antes de qualquer outra coisa. O plano só funciona se alguém defender o plano — e nesse momento esse alguém é você.

## Coisas que degradam o plano (evite)

- Preço exato de entrada ("compra em 136.230"). Mercado não respeita centavo; use regiões.
- Stop por distância fixa ("100 pontos") sem relação com a estrutura. Se a estrutura pede 180 pontos e o risco só cabe 100, a resposta é reduzir contratos, não apertar o stop.
- Cenário sem invalidação. Se nada invalida, não é cenário, é esperança.
- Previsão disfarçada de plano ("hoje vai subir"). O plano diz o que fazer **se** subir, **se** cair, **se** não fizer nada.
- Alvos otimistas para o R parecer bom. Alvo é nível real da seção 3, não "topo histórico".
- Adjetivos. "Forte resistência", "grande suporte" — o nível é ou não é. Diga quantas vezes foi testado, se tem dado.

## Formato de saída

Use os títulos numerados acima (1 a 7) na ordem. Tabelas para agenda e níveis, blocos de texto curtos para cenários, lista para regras e checklist. O plano inteiro deve caber numa tela de celular com scroll — se passou de ~60 linhas, cortou pouco.

Termine com uma linha: *Plano é hipótese, não previsão. Nada aqui é recomendação de investimento.*

## Referências

- `references/sessoes.md` — janelas de cada sessão em BRT, sobreposições, horários fixos de dados. Leia quando montar a agenda ou quando o trader opera ativo estrangeiro.
- `references/ativos.md` — valor do ponto, tick, custos e a fórmula de posição por ativo. Leia sempre que calcular contratos.
