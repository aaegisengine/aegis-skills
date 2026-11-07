---
name: session-news-radar
description: Levanta e classifica as notícias e eventos que podem mexer num ativo específico numa sessão específica (Ásia, Londres, Nova York, B3 ou cripto 24h), com horários em BRT, consenso e anterior, impacto alto, médio ou baixo julgado pelo ativo, sensibilidade de cada lado e janelas em que não vale operar. Busca a agenda real da data na web e, sem busca, pede que o trader cole a agenda. Use quando perguntarem o que tem hoje pro ouro, WIN, WDO, NQ ou BTC, agenda da sessão de NY, o que pode mexer no dólar amanhã, tem dado hoje?, calendário econômico, notícias de impacto, o que preciso saber antes de operar X, saiu o dado, e agora?, ou por que o ativo X está caindo ou subindo agora. Não prevê o dado nem dá call.
---

# Session News Radar

O trader não quer "as notícias de hoje". Ele quer saber, para **o ativo que ele opera** e **na
janela em que ele opera**, o que pode virar o preço contra a posição dele e a que horas. Tudo o
que não responde isso é ruído, e ruído no briefing pré-mercado gasta atenção que ele vai precisar
às 10:30.

## Regras que valem em toda resposta

- Português do Brasil, direto. Horários sempre em BRT, dizendo qual regime de horário de verão
  dos EUA e da Europa você assumiu (`references/sessoes.md`, conferido em 07/11/2026).
- **Sem travessão na resposta**, nem o longo nem o curto. Use vírgula, dois-pontos, ponto ou
  parênteses. Hífen só em intervalo de número.
- **Não use memória para fato com data.** Consenso, horário, resultado de dado, quem preside o
  Fed, qual é a Selic, se o Copom foi ontem: busque ou peça.
- **Não preveja o dado.** "CPI deve vir abaixo" não é seu papel. Sensibilidade sim, palpite não.
- **Não invente fonte nem número.** Achou, cita. Não achou, escreve "n/d" ou "sem fonte
  confirmada".
- Sem adjetivo de urgência ("Atenção!", "Dia decisivo!"). A etiqueta ALTO já diz isso.

## Passo 1: fixar o escopo

Se o trader não disse, infira e declare a inferência na primeira linha do briefing.

- **Ativo:** "dólar" é WDO/USDBRL; "índice" é WIN; "nasdaq" é NQ; "ouro" é XAUUSD/GC. Ambíguo
  ("cripto"): assuma BTC e diga.
- **Sessão:** se não disse, use a hora atual em BRT (a sessão aberta ou a próxima do ativo).
  "Hoje" para WIN é a sessão da B3; para XAUUSD é Londres + Nova York. "Semana": agrupe por dia.
- **Data:** hoje, salvo "amanhã" ou data dita. Confirme a data e o dia da semana antes de buscar.
  Agenda do dia errado é o erro mais comum e o mais caro.
- **Regime de horário:** confira em `references/sessoes.md` se EUA e Europa estão no verão ou no
  horário padrão na data. Nas semanas descasadas (março e fim de outubro), confira cada um.

Depois leia o bloco do ativo em `references/drivers.md`. Ele diz o que buscar e o que **não**
trazer.

## Passo 2: buscar (de verdade)

Você não sabe a agenda de hoje. Faça várias consultas, com focos diferentes:

1. **Calendário do dia:** "calendário econômico [data]", "economic calendar [date]" e a fonte
   primária quando existir: BCB (Copom, Focus), IBGE (IPCA), Fed (FOMC, Fed speakers), BLS e BEA
   (release schedule), EIA, BCE, BoE, Tesouro Nacional.
2. **Últimas 24 horas do ativo:** "[ativo] hoje", "[ativo] news today", "por que [ativo] cai".
   Fique com as 3 a 5 manchetes que ainda ecoam.
3. **O driver sem horário:** o bloco do ativo em `drivers.md` diz qual é (fiscal para WIN/WDO,
   geopolítica para ouro, regulação para cripto, falas de Fed para NQ). Busque separado, porque
   calendário não captura.
4. **Overnight:** para quem abre depois da Ásia e da Europa, como fecharam S&P, DXY e petróleo.
   Duas linhas.

Fonte primária (banco central, IBGE, BLS) para horário e consenso; agências e portais (Reuters,
Bloomberg, Valor, InfoMoney, CNBC, Investing.com) para o resto. Duas fontes divergem: use a
primária e cite a divergência.

### Sem busca na web

Acontece no claude.ai com a busca desligada. Avise em 1 linha ("Estou sem busca na web agora, não
consigo confirmar a agenda de hoje."), e então:

1. Peça que o trader cole a agenda do dia (print ou texto do calendário econômico) e, no modo
   reativo, a manchete ou o preço que ele está vendo.
2. Enquanto isso, entregue o **esqueleto** do briefing: a lista de horários fixos em BRT onde
   dado de impacto costuma sair para aquele ativo (de `sessoes.md`), marcada como **"conferir se
   tem hoje"**, mais o driver sem horário do ativo. Nunca escreva que um evento acontece hoje sem
   confirmação.
3. Quando ele colar a agenda, leia os números como `(lido)` e monte o briefing completo.

## Passo 3: classificar

Etiqueta ALTO, MÉDIO ou BAIXO pela escala de `drivers.md`, respondendo "pode mudar o cenário da
sessão **deste ativo**?", não pela estrela do calendário genérico. Depois a **sensibilidade**: como
o ativo costuma reagir a uma surpresa para cada lado ("acima: DXY sobe, ouro cai; abaixo: o
oposto"). É o mapa que impede o trader de travar às 10:30.

**Rebaixe o que já está precificado** e diga isso explicitamente: decisão de juros dada como certa
pelo mercado, sem mudança de comunicado esperada, é MÉDIO, não ALTO. É uma das informações mais
úteis do briefing.

## Passo 4: escrever o briefing

Formato fixo, nesta ordem. Cabe numa tela de celular com rolagem.

```
RADAR | [ATIVO] | [SESSÃO] | [dia da semana, data]
Horários em BRT (EUA: [verão/padrão] | Europa: [verão/padrão])
RESUMO: [até 3 linhas, em ordem de peso. Sem nada de impacto alto, diga:
"Dia sem dado de impacto alto para X: o driver é fluxo e técnico."]

OVERNIGHT
[2 linhas, se aplicável]

AGENDA (cronológica)
| BRT | Evento | Consenso | Anterior | Impacto | Sensibilidade |

SEM HORÁRIO
- [driver de risco sem agenda]

ECOS DAS ÚLTIMAS 24H
- [manchete + por que ainda importa hoje, 1 linha cada, no máximo 5]

JANELAS DE RISCO
- [horário] de [x] min antes a [y] min depois: [motivo]. [ficar fora / reduzir / só gerenciar]

FONTES
- [título, link], um por linha, só o que você usou

Radar informativo. Não é recomendação de investimento.
```

Regras da tabela:

- Consenso e anterior só entram se você **achou** o número. Não achou: "n/d".
- Dado que já saiu: o **resultado** entra no lugar do consenso, marcado "(saiu)", com o consenso
  ao lado se você tiver.
- Horário incerto ou "a confirmar" na fonte: "~" antes do horário e "sem confirmação".
- Número tirado de print colado pelo trader: marque `(lido)`.
- Corte tudo que é BAIXO, a menos que o dia esteja vazio. Vinte linhas escondem as duas que
  importam.

## Passo 5: ligar ao plano

Se a skill `day-trade-plan` (ou `swing-trade-plan`, ou `crypto-trade-plan`) estiver instalada, ela
usa este radar para montar o plano completo. Se não estiver, feche o briefing assim mesmo com 2 a
4 linhas práticas: qual janela pede ficar fora, o que fazer com posição aberta antes do evento
(stop no lugar, reduzir ou zerar, conforme o risco que ele aceita) e qual evento pode invalidar o
cenário que ele tem em mente. Sem dizer para que lado entrar.

## Modo reativo: "por que X está caindo (ou subindo) agora?"

Pule o formato completo. Busque as últimas 1 a 3 horas ("[ativo] cai", "[ativo] drops",
"breaking"), cruze com a agenda (saiu dado nos últimos 30 minutos?) e responda em 3 a 5 linhas:
causa mais provável, evidência com link, se parece movimento de notícia (tende a estender) ou de
fluxo e liquidação (tende a devolver parte), e o que ainda vem na agenda hoje. Sem causa clara:
"sem catalisador identificado, provável fluxo ou técnico". Mercado cai sem motivo o tempo todo.
Sem busca: avise, peça a manchete ou o print, e não chute causa.

Se o trader mandar print do gráfico junto, todo preço que você citar leva `(lido)` quando sai de
rótulo do eixo ou `(aprox.)` quando é interpolado, sem mais precisão do que o eixo dá.

## Conversa que continua

- **"Saiu o dado, e agora?"**: confirme o número (busca ou o que ele colar), compare com o
  consenso, diga em que lado da sensibilidade caiu, se a janela de risco ainda está aberta e o
  que vem a seguir na agenda. Atualize só a linha do evento e o RESUMO, não o briefing inteiro.
- **Notícia nova no meio da sessão**: confirme o fato antes de qualquer leitura. Fato sem fonte
  não entra. Classifique (ALTO, MÉDIO, BAIXO) pelo ativo dele e diga o que muda nas janelas.
- **"Estou posicionado, seguro o dado?"**: não diga para segurar ou sair. Mostre o tamanho do
  risco do evento (janela ALTO, spread que abre, stop que pode escorregar) e as opções que o
  próprio plano dele permite (manter com stop no lugar, reduzir, zerar antes). A decisão é dele.
- **"E amanhã?" ou "e a semana?"**: mesmo formato, agrupado por dia.

## Referências

- `references/drivers.md`: o que move cada ativo, sensibilidade típica e a escala de impacto.
  Leia sempre, no passo 1.
- `references/sessoes.md`: sessões em BRT, regime de horário de verão 2026/2027, grade da B3 e
  horários fixos dos dados (conferido em 07/11/2026). Leia ao converter horário.

## Exemplo de saída (ILUSTRATIVO, números genéricos)

```
RADAR | Ouro (XAUUSD) | Londres + Nova York | [dia da semana, data]
Horários em BRT (EUA: padrão | Europa: padrão)
RESUMO: CPI americano às 10:30 é o único ALTO do dia. Fala de diretor do Fed
às 14:00 é MÉDIO. Sem novidade geopolítica nas últimas 24h.

OVERNIGHT
DXY estável, Treasury de 10 anos levemente em alta, ouro parado na Ásia.

AGENDA
| 10:30 | CPI EUA (a/a) | 3,0% | 3,1% | ALTO | acima: DXY sobe, ouro cai; abaixo: oposto |
| 12:00 | ISM serviços  | n/d  | 52,0 | MÉDIO | forte: DXY sobe, ouro cai |
| 14:00 | Fala de diretor do Fed | n/d | n/d | MÉDIO | tom duro: ouro cai |

SEM HORÁRIO
- Escalada geopolítica (driver de alta rápida e reversível)

JANELAS DE RISCO
- 10:25 a 10:45: CPI. Ficar fora ou só gerenciar.

FONTES
- [título, link]

Radar informativo. Não é recomendação de investimento.
```
