# Custos e riscos de carregar posição

Swing trade é day trade com uma variável a mais: o tempo entre o fechamento e a abertura, em que o trader não pode fazer nada e o mercado pode. Antes de fechar um plano de swing, passe por estes pontos para o ativo em questão. O que não se aplica, ignore; o que se aplica, entra no plano com número.

## Por classe de ativo

### Ações (B3 e EUA)

- **Gap de abertura** é o risco principal. Stop em ação não protege contra gap: se a ação fecha a R$ 20,10 com stop em 20,00 e abre a 18,50, a saída é 18,50. Dimensione a posição pelo gap plausível, não pelo stop. Regra prática: em semana de resultado, assuma gap de 2× o range médio diário.
- **Resultado trimestral**: descubra a data antes de montar a posição. Carregar posição por resultado é uma decisão explícita (com tamanho reduzido), nunca um acidente.
- **Dividendos / JCP**: a ação abre "ex" descontada — não é queda, mas o stop pode ser acionado se estiver justo. Ajuste.
- **Custos**: corretagem (muitas vezes zero), emolumentos B3, e no caso de vendido: aluguel (taxa anual, cobrada por dia) + risco de recall. Nos EUA: custo de borrow pode ser proibitivo em ações "hard to borrow".
- **Liquidez**: ação que negocia R$ 5 milhões/dia não comporta posição de R$ 500 mil sem mover o preço na saída.

### Futuros (WIN, WDO, NQ, ES, GC, CL)

- **Margem overnight** é muito maior que a intraday (na B3, WIN e WDO passam de centenas de reais intraday para milhares por contrato overnight). Confirme que a conta comporta — corretora zera posição sem margem no fechamento.
- **Vencimento e rolagem**: WDO vence todo mês, WIN a cada dois, CME a cada três. Um swing de 3 semanas pode atravessar o vencimento; o plano precisa dizer se rola e quando (idealmente 2–3 dias antes, quando a liquidez migra).
- **Ajuste diário**: em futuros da B3 o resultado é liquidado todo dia em dinheiro. Posição perdedora consome caixa **antes** do stop ser acionado.
- **Limite de oscilação / circuit breaker**: em dia de estresse, o ativo pode travar e o stop não executa.
- **Gaps** existem mas são menores que em ações, porque o mercado é quase 24h (CME) ou tem after (B3 não; WIN/WDO abrem com gap em relação ao fechamento das 18:25).

### Forex e CFDs

- **Swap / rollover**: cobrado ou pago todo dia às 17:00 NY (18:00/19:00 BRT), triplo na quarta-feira (cobre o fim de semana). Em par com diferencial de juros grande (ex.: comprado em USDJPY recebe, vendido paga), o swap muda o resultado de um swing de 3 semanas em dezenas de pips. Coloque no cálculo do R.
- **Gap de fim de semana**: forex fecha sexta 17:00 NY e abre domingo 17:00 NY. Notícia no fim de semana (eleição, geopolítica, decisão surpresa) vira gap. Stop não protege.
- **Spread alargado** em abertura de domingo e em notícia: stop justo é executado em nível pior.
- **CFD de índice** tem custo de financiamento diário (juro + taxa da corretora) que corrói posição longa.

### Cripto

- **Funding rate** a cada 8h em perpétuos: com funding positivo alto (+0,05% a cada 8h = ~55% ao ano), carregar comprado é caro; vendido recebe. Calcule o custo do período estimado da posição.
- **Liquidação** em vez de stop: com alavancagem, o preço de liquidação é o stop de verdade. Nunca deixe a liquidação mais próxima que o stop.
- **Fim de semana**: liquidez fina, movimentos de 5–10% sem notícia. O swing de cripto precisa de tamanho que sobreviva ao domingo.
- **Risco de exchange**: posição em corretora é passivo da corretora. Não concentre.

A skill `crypto-trade-plan` cobre isso em profundidade.

## Checklist de carregamento

Responda antes de fechar o plano:

1. Há resultado, decisão de juros, vencimento, ou evento binário dentro do horizonte da posição? Data e hora.
2. Qual é o gap plausível contra a posição, e o tamanho sobrevive a ele?
3. Qual é o custo de carregar (swap, funding, aluguel, financiamento) pelo prazo estimado, em R múltiplo?
4. A margem overnight cabe na conta com folga de 30%?
5. Se o ativo abrir com gap além do stop, qual é a ação: sair no primeiro minuto, esperar 15 minutos, ou reavaliar? Decida agora.
