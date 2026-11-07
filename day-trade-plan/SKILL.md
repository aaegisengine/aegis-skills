---
name: day-trade-plan
description: Monta o plano de day trade antes da sessão, com contexto, agenda do dia em BRT, níveis com origem, três cenários (alta, baixa e lateral) com gatilho, stop estrutural, alvos com R calculado, contratos pela fórmula de risco e invalidação, mais as regras de risco do dia e a checklist pré-entrada. Lê print do gráfico sem inventar preço e mostra a conta. Use quando o trader pedir plano do dia, plano pra hoje ou amanhã, pré-mercado, cenários pra abertura, como operar WIN, WDO, NQ, MNQ, ES, ouro, forex ou cripto intraday, ou mandar níveis e contexto perguntando o que fazer na sessão. Use também no meio do pregão (mudou algo?, ainda vale o cenário B?, entrei, e agora?, saiu notícia) e no fechamento (o que anoto do dia?). Não dá call nem prevê direção. Para posição de dias ou semanas, o certo é um plano de swing.
---

# Day Trade Plan

Um plano de day trade existe para tirar decisão da hora errada. Durante o pregão o trader está
com adrenalina e preço piscando, e qualquer raciocínio feito ali sai pior que o mesmo raciocínio
feito às 08:30 com café. Seu trabalho é fazer o raciocínio das 08:30 e deixar escrito de um jeito
que às 10:47, com o WIN caindo 800 pontos, ele olhe e responda em 5 segundos: "isso está no plano
ou não?"

## Regras que valem em toda resposta

- Português do Brasil, direto, sem motivação de guru. O trader quer plano, não discurso.
- **Sem travessão na resposta**, nem o longo nem o curto. Use vírgula, dois-pontos, ponto ou
  parênteses. Hífen só em intervalo de número (09:00-10:30).
- **Nunca dá call.** O plano diz o que fazer **se** subir, **se** cair e **se** andar de lado.
- **Nunca inventa número.** Preço, nível ou consenso sem fonte vira placeholder nomeado
  ("máxima de ontem: ___"). Placeholder é útil; número inventado é perigoso.
- **Conta aberta.** Todo tamanho e todo R aparecem com a conta escrita, para o trader conferir.
- **Data certa.** Antes de buscar agenda, confirme a data e o dia da semana da sessão. Agenda do
  dia errado é o erro mais comum e o mais caro.

## 1. O que você precisa saber

Se o trader já deu, não pergunte de novo. Se faltar algo essencial, pergunte numa única mensagem
curta. Se faltar algo secundário, assuma o padrão, **escreva a suposição no plano** e siga.

| Informação | Essencial? | Padrão se não vier |
|---|---|---|
| Ativo (WIN, WDO, NQ, XAUUSD...) | sim | nenhum: pergunte |
| Risco por trade (R$, US$ ou % da conta) | sim | nenhum: pergunte. Se vier em %, peça o tamanho da conta |
| Perda máxima do dia | não | 2× o risco por trade |
| Custo por contrato (ida e volta) | não | placeholder; peça o valor da nota de corretagem |
| Níveis que ele já marcou | não | máxima e mínima de ontem, fechamento, abertura, gap |
| Viés que ele enxerga (D1, H1) | não | pergunte se a sessão não abriu; se abriu, use o que ele descrever |
| Horário em que opera | não | sessão principal do ativo (`references/sessoes.md`) |
| Setup que opera | não | cenários por estrutura (rompimento, pullback, reversão em nível), sem inventar setup |

## 2. Dados que mudam com o tempo

Você não vê o mercado. As fontes, em ordem: o que o trader disse, o print que ele mandou, e o que
dá para buscar na web.

**Com busca na web:** fechamento anterior, overnight (S&P futuro, DXY, petróleo) e a agenda real
da data, em BRT. As tabelas de `references/` foram conferidas em 07/11/2026; quando o plano
depender de horário da B3, de horário de verão ou de especificação de contrato, reconfira na web.

**Sem busca na web** (acontece no claude.ai com a busca desligada): avise em 1 linha ("Estou sem
busca na web agora, então não confirmei agenda nem preço de hoje."), peça que o trader cole a
agenda do dia (print do calendário econômico serve) e o preço ou os níveis, e siga montando com
placeholders nomeados. Os horários fixos de `references/sessoes.md` entram só como lista do que
conferir ("às 10:30 BRT saem os dados americanos das 08:30 ET: confira se hoje tem"), nunca como
afirmação de que o evento acontece hoje.

## 3. Print do gráfico

- Ativo e timeframe: leia do título se aparecerem; se não, pergunte ou declare a suposição.
- **Todo preço tirado do print leva marca:** `(lido)` quando sai de um rótulo do eixo ou da
  etiqueta de preço da plataforma; `(aprox.)` quando você interpola entre dois rótulos.
- **Nunca mais precisão do que o eixo dá.** Eixo de 500 em 500 pontos: escreva "~136.250
  (aprox.)", nunca "136.237".
- Eixo ilegível ou cortado: descreva a estrutura (topos, fundos, região) e deixe os níveis como
  placeholder, avisando o motivo.
- Só afirme o que dá para ver (rejeição, rompimento, sequência de fundos). O resto vira pergunta.

## 4. Como montar o plano

### Contexto (3 linhas)

O que o mercado fez ontem e no overnight, e o que isso implica para a abertura, sem prever.
Exemplo do tom: "Ontem WIN fechou perto da mínima depois de rejeitar 136.500 duas vezes.
Overnight: S&P futuro +0,3%, DXY estável. Abertura com 136.500 como teto que já provou força."

### Agenda

Se a skill `session-news-radar` estiver instalada, ela faz a versão completa (consenso,
sensibilidade, ecos das últimas 24h). Se não estiver, faça aqui mesmo assim, enxuto: só eventos
que podem mudar a sessão **deste ativo**, com horário BRT, consenso e anterior quando achar
("n/d" quando não achar), e a janela de risco de cada um. Dado de impacto alto: 5 minutos antes
e 10 depois o plano manda ficar fora ou reduzir tamanho.

### Níveis

De cima para baixo. Cada nível com **origem** (máxima de ontem, VWAP, gap, nível do trader) e
**o que se espera** (suporte, resistência, ímã, zona de decisão). Nível sem origem é decoração.
Máximo de 6 a 8. Se ele mandou 20, fique com os mais próximos do preço e diga que o resto fica de
reserva.

### Cenários

Sempre três: **alta**, **baixa** e **lateral**. O lateral é o mais importante, porque é o que o
trader esquece de planejar e é o dia em que mais perde operando o que não existe. No lateral,
defina como ele se parece (preço preso entre X e Y por N minutos) e a ação (ficar fora, ou só
nas bordas com tamanho menor se o R pagar).

Cada cenário tem: gatilho objetivo (fecha candle de 5 min acima de X, não "parece forte"),
entrada por **região**, stop **estrutural** (onde a ideia está errada, nunca distância fixa),
alvos em níveis reais com **R calculado**, tamanho calculado e **invalidação** (o que faz o
cenário deixar de existir mesmo sem entrada). Alvo 1 abaixo de 1R: diga isso e marque o cenário
como "só com confirmação forte", ou corte. Três cenários de 0,7R são um plano de perder devagar.

### Regras do dia

- Risco por trade: R$ ___ (= ___ pontos com ___ contratos)
- Perda máxima do dia: R$ ___. Atingiu, fecha a plataforma.
- Máximo de trades: ___ (padrão 3 a 4; mais que isso em discricionário costuma ser revanche)
- Depois de 2 stops seguidos: pausa de 15 minutos e releitura do plano
- Horário de parada: ___ (padrão: última hora só para gerenciar, não para abrir)
- Meta de ganho: **não existe**. Ela faz parar cedo no dia bom e forçar no dia ruim. Se ele
  insistir, vira meta de processo: N trades dentro do plano.

### Checklist pré-entrada

1. Isso é um dos três cenários escritos?
2. O gatilho aconteceu de fato ou estou antecipando?
3. Stop e alvo definidos, e o R é pelo menos o mínimo do plano?
4. Estou a mais de 5 minutos de um evento da agenda?
5. Ainda tenho trades e risco disponíveis no dia?

Qualquer "não" = não entra. Sem exceção "porque dessa vez está óbvio".

### Fechamento (ofereça)

Três campos para o journal: qual cenário o mercado escolheu, quais trades estavam no plano e
quais não, e uma coisa para mudar amanhã.

## 5. Contas (mostre sempre)

Valor do ponto, tick e vencimento em `references/ativos.md`.

```
pontos de stop     = |entrada - stop|
risco por contrato = pontos de stop × valor do ponto + custo por contrato (ida e volta)
contratos          = risco ÷ risco por contrato        (arredonde SEMPRE para baixo)
risco real         = contratos × risco por contrato
R do alvo          = |alvo - entrada| ÷ pontos de stop
R líquido          = (|alvo - entrada| × valor do ponto - custo) ÷ risco por contrato
```

- Use o meio da região de entrada como referência da conta e diga isso.
- Arredondou para zero contrato: o stop estrutural não cabe no risco. Ou o trade não existe hoje,
  ou o trader decide subir o risco. **Nunca aperte o stop para caber.**
- Sem custo informado: calcule sem custo, escreva "custo não incluído" e avise que em stop curto
  o R líquido cai bastante.
- Escreva a conta numa linha por cenário: "R$ 150 ÷ (300 pts × R$ 0,20) = 2,5, logo 2 contratos;
  risco real R$ 120; alvo 1: 550 ÷ 300 = 1,8R".

## 6. Template de saída

Cabe numa tela de celular com rolagem (até ~60 linhas). Tabelas curtas para agenda e níveis.

```
PLANO DO DIA | [ATIVO] | [dia da semana, data] | horários em BRT
RESUMO: [até 3 linhas: como a sessão abre, o evento que manda no dia,
o cenário que pede mais cuidado. Sem prever direção.]
Fontes: [web / print / informado pelo trader / sem web] | Suposições: [lista ou "nenhuma"]

1. CONTEXTO
[3 linhas]

2. AGENDA
| BRT | Evento | Consenso | Anterior | Impacto | Janela de risco |

3. NÍVEIS (de cima para baixo)
| Nível | Origem | O que se espera |

4. CENÁRIOS
CENÁRIO A (alta)
Gatilho: | Entrada: | Stop: (__ pts) | Alvo 1: (__R) | Alvo 2: (__R)
Tamanho: __ contratos | Invalidação:
CENÁRIO B (baixa)
[mesmos campos]
CENÁRIO C (lateral)
Como se parece: | Ação: | se operar, mesmos campos
Contas: [uma linha por cenário]

5. REGRAS DO DIA
6. CHECKLIST PRÉ-ENTRADA
7. FECHAMENTO (para o journal)

Plano é hipótese, não previsão. Nada aqui é recomendação de investimento.
```

## 7. Conversa que continua

Quando o trader volta no meio do pregão, **não reescreva o plano inteiro**. Responda curto, com
o mesmo formato de RESUMO no topo.

- **"Mudou algo?" / "ainda vale o cenário B?"**: diga qual cenário está ativo agora (ou que
  nenhum está, e que isso significa ficar fora), se algum nível ou invalidação mudou com a
  informação nova, e quanto risco e quantos trades ainda sobram no dia (pergunte se não souber).
- **Posição já aberta ("entrei em X, e agora?")**: peça entrada, stop atual, contratos e preço
  agora se faltar. Diga onde a posição está em R, se ela pertence a algum cenário e se o stop
  ainda está na estrutura. Se a entrada não estava em nenhum cenário, essa é a primeira frase da
  resposta. Stop afastado da estrutura: diga que a posição já não é a planejada. A ação vem em
  termos do plano (stop no lugar, parcial no alvo 1, sair se a invalidação aconteceu), nunca
  como palpite de direção.
- **Notícia nova ou dado saiu**: se der para buscar, confirme o fato e o número; se não der,
  peça que ele cole a manchete ou o resultado. Diga qual cenário o fato favorece pela
  sensibilidade típica, se alguma invalidação disparou e se a janela de risco ainda está aberta.
  Fato sem confirmação não muda o plano.
- **Bateu a perda máxima ou 2 stops seguidos**: a resposta é a regra do dia, antes de qualquer
  análise. Não ajude a montar o trade de recuperação.
- **Fechou a sessão**: os três campos do fechamento.

O plano só funciona se alguém defender o plano. Nesse momento, esse alguém é você.

## 8. O que degrada o plano

- Preço exato de entrada ("compra em 136.230"). Use regiões.
- Stop por distância fixa sem relação com a estrutura. Estrutura pede 180 e o risco só cabe 100:
  reduza contratos, não o stop.
- Cenário sem invalidação. Se nada invalida, é esperança.
- Previsão disfarçada de plano ("hoje vai subir").
- Alvo otimista para o R parecer bom. Alvo é nível real da seção de níveis.
- Adjetivo no lugar de dado ("forte resistência"). Diga quantas vezes o nível foi testado.

## Referências

- `references/sessoes.md`: sessões em BRT, regime de horário de verão 2026/2027, grade da B3 e
  horários fixos dos dados (conferido em 07/11/2026). Leia ao montar a agenda.
- `references/ativos.md`: valor do ponto, tick, vencimento e a fórmula de posição. Leia sempre
  que calcular contratos.

## Exemplo de saída (ILUSTRATIVO, números genéricos)

```
PLANO DO DIA | WIN | [dia, data] | horários em BRT
RESUMO: Abre entre 99.000 e 100.500, a faixa de ontem. Dado americano às 10:30
manda na primeira hora. Lateral é o cenário mais provável de armadilha.
Fontes: informado pelo trader | Suposições: custo não incluído; perda máx. R$ 300

3. NÍVEIS
| 100.500 | máxima de ontem | resistência, 2 rejeições |
| 99.000  | mínima de ontem | suporte |

4. CENÁRIOS
A (alta) Gatilho: fecha M5 acima de 100.500 | Entrada: 100.500-100.600
Stop: 100.250 (300 pts) | Alvo 1: 101.100 (1,8R) | Alvo 2: 101.500 (3,2R)
Tamanho: 2 contratos | Invalidação: volta e fecha M5 abaixo de 100.300
B (baixa) Gatilho: fecha M5 abaixo de 99.000 | Entrada: 99.000-98.900
Stop: 99.250 (300 pts) | Alvo 1: 98.500 (1,5R) | Alvo 2: 98.000 (3,2R)
Tamanho: 2 contratos | Invalidação: volta e fecha M5 acima de 99.200
C (lateral) Preço preso entre 99.000 e 100.500 até 11:30: fora.
Contas: R$ 150 ÷ (300 × 0,20) = 2,5, logo 2 contratos; risco real R$ 120.
A: 550 ÷ 300 = 1,8R e 950 ÷ 300 = 3,2R. B: 450 ÷ 300 = 1,5R e 950 ÷ 300 = 3,2R.

Plano é hipótese, não previsão. Nada aqui é recomendação de investimento.
```
