---
name: session-news-radar
description: Levanta e classifica as notícias e eventos de impacto para um ativo específico numa sessão específica (Ásia, Londres, Nova York, B3 ou cripto 24h), com horários convertidos para BRT, consenso vs. anterior, escala de impacto (alto/médio/baixo), como o ativo costuma reagir e as janelas em que não vale operar. Use sempre que o trader perguntar "o que tem hoje pro ouro/WIN/WDO/NQ/BTC", "agenda da sessão de NY", "o que pode mexer no dólar amanhã", "tem dado hoje?", "por que o ativo X está caindo", "notícias de impacto", "calendário econômico" ou qualquer variação de "o que eu preciso saber antes de operar X". Busca na web a agenda real da data — não use memória para consenso, horário ou resultado de dado.
---

# Session News Radar

O trader não quer "as notícias de hoje". Ele quer saber, para **o ativo que ele opera** e **na janela em que ele opera**, o que pode virar o preço contra a posição dele e a que horas. Tudo o que não responde isso é ruído, e ruído em briefing pré-mercado custa atenção que ele vai precisar às 10:30.

Escreva em português do Brasil. Horários sempre em BRT (e diga qual regime de horário de verão dos EUA/Europa você assumiu — está em `references/sessoes.md`).

## Passo 1: fixar o escopo

Antes de buscar, defina três coisas. Se o trader não disse, infira e declare a inferência na primeira linha do briefing.

- **Ativo** — se ele disse "dólar", entenda WDO/USDBRL; "índice" é WIN; "nasdaq" é NQ; "ouro" é XAUUSD/GC. Se for ambíguo (ex.: "cripto"), assuma BTC e diga.
- **Sessão / horizonte** — se não disse, use a hora atual em BRT: a sessão que está aberta ou a próxima a abrir para aquele ativo. "Hoje" para WIN é a sessão da B3; "hoje" para XAUUSD é Londres + NY. Se ele pediu "semana", agrupe por dia.
- **Data** — hoje, a menos que ele diga "amanhã" ou uma data. Confira a data real antes de buscar: agenda do dia errado é o erro mais comum e o mais caro.

Depois abra `references/drivers.md` e leia o bloco do ativo. Ele diz o que buscar e, mais importante, o que **não** trazer.

## Passo 2: buscar (de verdade)

Você não sabe a agenda de hoje. Nem o consenso do CPI, nem se o Copom é esta semana, nem se houve um ataque de madrugada. Busque. Faça várias consultas paralelas, com foco diferente:

1. **Calendário do dia** — "calendário econômico [data]", "economic calendar [date]", e o calendário oficial da fonte primária quando existir: BCB (agenda do Copom, IPCA no IBGE), Fed (FOMC calendar, Fed speakers), BLS/BEA (release schedule), BCE, Tesouro Nacional (leilões).
2. **Últimas 24 horas para o ativo** — "[ativo] hoje", "[ativo] notícias", "[ativo] news today", "por que [ativo] cai/sobe". Pegue as 3–5 manchetes que ainda ecoam.
3. **O driver sem horário** — o bloco do ativo em `drivers.md` diz qual é (fiscal para WIN/WDO, geopolítica para ouro, regulação para cripto, falas de Fed para NQ). Busque isso separadamente, porque calendário não captura.
4. **Overnight** — para ativos que abrem em BRT depois da Ásia/Europa: como fechou o S&P, DXY, petróleo, e o que Ásia/Europa fizeram. Duas linhas.

Prefira fontes primárias (site do banco central, IBGE, BLS) para horário e consenso, e agências (Reuters, Bloomberg, Valor, InfoMoney, CNBC, Investing.com) para o resto. Se duas fontes divergem no horário ou no consenso, use a primária e cite a divergência.

## Passo 3: classificar

Para cada item, decida a etiqueta de impacto usando a escala em `drivers.md` (ALTO / MÉDIO / BAIXO) — pela pergunta "pode mudar o cenário da sessão **deste ativo**?", não pela estrela do calendário genérico. Depois escreva a **sensibilidade**: como o ativo costuma reagir a uma surpresa para cada lado. Isso não é previsão do dado; é o mapa de "se vier acima → tende a X, se vier abaixo → tende a Y", que é o que o trader precisa para não ficar paralisado às 09:30.

Rebaixe o que já está precificado. Uma decisão de juros com 100% de probabilidade no mercado futuro e comunicado sem mudança esperada é MÉDIO, não ALTO. Diga isso explicitamente — é uma das informações mais úteis do briefing.

## Passo 4: escrever o briefing

Formato fixo, nesta ordem. Cabe numa tela de celular com scroll.

```
RADAR — [ATIVO] — [SESSÃO], [dia da semana, data]
Horários em BRT (assumindo [verão/inverno] nos EUA/Europa)

RESUMO (3 linhas)
[O que importa hoje, em ordem de peso. Se não há nada de impacto alto, diga: "Dia sem dado de impacto alto para X — o driver é fluxo/técnico."]

OVERNIGHT (2 linhas, se aplicável)
[O que Ásia/Europa/futuros fizeram e o que o ativo já precificou]

AGENDA (cronológica)
| BRT | Evento | Consenso | Anterior | Impacto | Sensibilidade |
|-----|--------|----------|----------|---------|---------------|
| 09:30 | CPI EUA (a/a) | 3,1% | 3,2% | ALTO | acima → DXY sobe, ouro/NQ caem; abaixo → oposto |

SEM HORÁRIO (o que pode aparecer a qualquer momento)
- [driver de risco sem agenda: ex. votação no Congresso, fala de ministro, escalada geopolítica, decisão regulatória]

ECOS DAS ÚLTIMAS 24H
- [manchete + por que ainda importa hoje, 1 linha cada, no máximo 5]

JANELAS DE RISCO
- [horário] ± [minutos]: [motivo]. [Ficar fora / reduzir tamanho / só gerenciar]

FONTES
- [título — link], um por linha, só o que você realmente usou
```

Regras para a tabela:

- Consenso e anterior só entram se você **achou** o número. Se não achou, escreva "n/d" — nunca preencha com um valor "provável".
- Se um dado já saiu (você está montando o radar com a sessão em andamento), coloque o **resultado** no lugar do consenso e marque "(saiu)".
- Evento com horário incerto ou "a confirmar" na fonte: escreva "~" antes do horário e diga que está sem confirmação.

## O que não fazer

- **Não preveja o dado.** "CPI deve vir abaixo" não é seu papel. Sensibilidade sim, palpite não.
- **Não misture ativos.** Se o trader pediu ouro, o CPI da zona do euro entra só se você conseguir explicar em uma linha por que move ouro. Se não consegue, corta.
- **Não repita o calendário genérico.** Vinte linhas de eventos de impacto baixo escondem as duas que importam. Corte tudo que é BAIXO a menos que o dia esteja vazio.
- **Não use memória para fatos com data.** Você não sabe quem é o presidente do Fed hoje, qual é a Selic, ou se o Copom foi ontem. Busque.
- **Não invente fonte.** Se a busca não trouxe link, o item não tem link — e diga que está "sem fonte confirmada".
- **Não use adjetivos de urgência.** "Atenção!", "Crucial!", "Dia decisivo!" — a etiqueta ALTO já diz isso.

## Quando o trader pergunta "por que X está caindo agora"

Modo reativo. Pule o formato completo. Busque as últimas 1–3 horas ("[ativo] cai", "[ativo] drops", "breaking"), cruze com a agenda (saiu dado nos últimos 30 minutos?), e responda em 3–5 linhas: causa mais provável, evidência (link), se é movimento de notícia (tende a estender) ou de fluxo/liquidação (tende a devolver parte), e o que na agenda ainda vem hoje. Se não achar causa clara, diga "sem catalisador identificado — provável fluxo/técnico" em vez de inventar uma narrativa. Mercado cai sem motivo o tempo todo.

## Referências

- `references/drivers.md` — o que move cada ativo, sensibilidade típica, e a escala de impacto. Leia sempre, no passo 1.
- `references/sessoes.md` — janelas de cada sessão em BRT, horários fixos de dados, regime de horário de verão. Leia quando converter horário ou quando não souber qual sessão está aberta.

Termine o briefing com: *Radar informativo. Não é recomendação de investimento.*
