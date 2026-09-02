# Sessões e horários (referência em BRT)

O Brasil não tem horário de verão desde 2019, então BRT = UTC-3 o ano inteiro. Quem muda é o resto do mundo: EUA (março–novembro) e Europa (fim de março–fim de outubro) adiantam o relógio, e isso desloca a sessão deles em 1 hora **no relógio do trader brasileiro**. Antes de escrever horário no plano, confira qual regime está valendo na data.

## Janelas por sessão

| Sessão | Horário local | BRT (verão deles) | BRT (inverno deles) |
|---|---|---|---|
| Tóquio (Ásia) | 09:00–18:00 JST | 21:00–06:00 | 21:00–06:00 (Japão não muda) |
| Londres | 08:00–16:30 (BST/GMT) | 04:00–12:30 | 05:00–13:30 |
| Nova York (NYSE) | 09:30–16:00 ET | 10:30–17:00 | 11:30–18:00 |
| Futuros CME (NQ, ES, GC) | quase 23h/dia | pausa diária 18:00–19:00 BRT (verão) / 19:00–20:00 (inverno) | — |
| B3 (WIN, WDO) | 09:00–18:25 BRT | fixo | fixo |
| Cripto | 24/7 | — | — |

Os horários da B3 mudam ocasionalmente (a B3 já ajustou o fechamento de WIN/WDO mais de uma vez). Trate a tabela como ponto de partida e confirme no site da B3 quando a precisão importar.

## Sobreposições que concentram volume

- **Londres + NY (BRT ~10:30–12:30 no verão deles)**: maior liquidez em forex, ouro e índices americanos. É onde os movimentos direcionais do dia costumam nascer.
- **Abertura da B3 (09:00–10:30)**: WIN e WDO reagem ao overnight, ao dado das 09:30 BRT dos EUA e ao fluxo estrangeiro. Primeira hora tem amplitude alta e leilões frequentes.
- **Abertura de NY (10:30 BRT no verão / 11:30 no inverno)**: segunda onda de volatilidade em WIN/WDO, NQ, XAUUSD.
- **Fim de Londres (12:30–13:30 BRT)**: reversões comuns em forex e ouro quando o fluxo europeu fecha posição.
- **Tarde americana pós 15:00 BRT**: FOMC, discursos de Fed, e o "power hour" da NYSE (última hora).

## Horários fixos dos dados mais relevantes (BRT)

| Evento | Horário (verão EUA / inverno EUA) | Mexe em |
|---|---|---|
| Payroll, CPI, PCE, PIB, vendas no varejo (EUA) | 09:30 / 10:30 | tudo: DXY, ouro, NQ, WDO, WIN |
| FOMC (decisão) | 15:00 / 16:00 + coletiva 15:30 / 16:30 | tudo |
| Ata do FOMC | 15:00 / 16:00 | DXY, ouro, NQ |
| ISM, confiança do consumidor (EUA) | 11:00 / 12:00 | NQ, DXY |
| Estoques de petróleo (EIA, quarta) | 11:30 / 12:30 | WIN (via Petrobras), petróleo |
| IPCA (IBGE) | 09:00 | WDO, WIN, DI |
| Copom (decisão) | ~18:30, quarta-feira, após o pregão | WDO, WIN (gap no dia seguinte) |
| Ata do Copom | 08:00 terça-feira seguinte | WDO, WIN |
| Boletim Focus | 08:25 segunda-feira | juros, WDO (impacto baixo) |
| BCE (decisão) | 09:15 BRT (verão Europa) / 10:15 | EURUSD, DXY, ouro |
| BoE (decisão) | 08:00 BRT (verão) / 09:00 | GBPUSD |
| BoJ (decisão) | madrugada BRT, sem hora fixa | USDJPY, NQ (carry) |
| PMI China (Caixin/NBS) | 22:30–22:45 BRT | commodities, WIN (via Vale), AUD |
| Leilão de fechamento B3 | 17:55–18:00 | WIN (fechamento à vista) |

Datas exatas variam a cada mês. A skill `session-news-radar` busca a agenda real do dia; esta tabela serve para você saber **onde** olhar e o que é plausível.
