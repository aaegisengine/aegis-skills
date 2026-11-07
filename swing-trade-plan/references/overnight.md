# Custos e riscos de carregar posição

Swing trade é day trade com uma variável a mais: o tempo entre o fechamento e a abertura, em que o
trader não pode fazer nada e o mercado pode. Antes de fechar um plano de swing, passe por estes
pontos para o ativo em questão. O que não se aplica, ignore; o que se aplica entra no plano com
número.

**Conferido em 07/11/2026.** Horários, margens, custos e intervalos de funding mudam. Quando o
plano depender de um deles, reconfira na web (ou peça ao trader o número da corretora/exchange).

## Por classe de ativo

### Ações (B3 e EUA)

- **Gap de abertura** é o risco principal. Stop em ação não protege contra gap: fecha a R$ 20,10
  com stop em 20,00 e abre a 18,50, a saída é 18,50. Dimensione pelo gap plausível, não só pelo
  stop. Regra prática: em semana de resultado, assuma gap de 2× o range médio diário.
- **Sem after-market na B3** na grade em vigor desde 03/11/2026 (OC 055/2026-VNC), exceto no
  vencimento de opções: tudo o que sai entre o call de fechamento e a abertura vira gap.
  Nos EUA existe pré e pós-mercado, com liquidez menor; resultado sai muito nesse horário.
- **Resultado trimestral:** descubra a data antes de montar. Carregar por resultado é decisão
  explícita, com tamanho reduzido, nunca acidente.
- **Dividendos e JCP:** a ação abre "ex" descontada. Não é queda, mas aciona stop justo. Ajuste.
- **Custos:** corretagem, emolumentos e, no vendido, aluguel (taxa anual cobrada por dia) com
  risco de recall. Nos EUA, ação difícil de alugar pode ter custo proibitivo.
- **Liquidez:** ação que negocia pouco não comporta posição grande sem mexer no preço na saída.

### Futuros (WIN, WDO, NQ, ES, GC, CL)

- **Margem para carregar** é a margem de garantia da bolsa, muito maior que a margem de day trade
  que a corretora oferece. Confirme na corretora que a conta comporta com folga: sem margem no
  fim do dia, a corretora zera a posição.
- **Vencimento e rolagem:** WDO vence todo mês (1º dia útil; o último pregão é o dia anterior),
  WIN nos meses pares (quarta-feira mais próxima do dia 15), NQ e ES em março, junho, setembro e
  dezembro (3ª sexta-feira). Ouro e petróleo têm ciclo próprio. Um swing de 3 semanas pode
  atravessar o vencimento: o plano diz se rola e quando (em geral uns dias antes, quando a
  liquidez migra). Especificações em `ativos.md`.
- **Ajuste diário na B3:** o resultado é liquidado todo dia em dinheiro. Posição perdedora consome
  caixa **antes** de o stop ser acionado.
- **Limite de oscilação:** em dia de estresse o contrato pode travar no limite e o stop não
  executa. A B3 também muda o limite quando quer (exemplo: em 26/10/2026 ampliou o limite de baixa
  de IND/WIN de 10% para 15% e o de alta de DOL/WDO de 6% para 8,4%).
- **Gap:** WIN fecha às 18:25 e WDO às 18:30 e só voltam às 09:00, então o noturno vira gap. NQ,
  ES e GC negociam quase 24h na CME, e o gap aparece mais na volta do fim de semana.

### Forex e CFDs

- **Swap (rollover):** cobrado ou pago todo dia na virada das 17:00 de Nova York (19:00 BRT no
  horário padrão americano, 18:00 no verão de lá), em geral triplo na quarta-feira para forex à
  vista; em CFD de índice e commodity o dia triplo pode ser outro. Confira a tabela da corretora.
  Em par com diferencial de juros grande, o swap muda o resultado de 3 semanas em dezenas de pips.
  Coloque no R.
- **Gap de fim de semana:** forex fecha na sexta à tarde de Nova York e volta no domingo à tarde.
  Notícia no fim de semana (eleição, geopolítica, decisão surpresa) vira gap. Stop não protege.
- **Spread alargado** na abertura de domingo e em notícia: stop justo executa pior.
- **CFD de índice** tem financiamento diário (juro + taxa da corretora) que corrói posição longa.

### Cripto

- **Funding:** cobrado no intervalo da exchange (8h na maioria dos pares grandes, 4h ou 1h em
  alguns; a Hyperliquid cobra de hora em hora). Funding de +0,05% a cada 8h é cerca de 55% ao ano
  (0,05% × 3 × 365): carregar comprado fica caro e o vendido recebe. Calcule pelo prazo estimado:
  custo ≈ notional × taxa × número de cobranças.
- **Liquidação no lugar do stop:** com alavancagem, o preço de liquidação é o stop de verdade.
  Ele nunca pode ficar mais perto que o stop.
- **Fim de semana:** liquidez fina e movimentos de vários por cento sem notícia. O tamanho precisa
  sobreviver ao domingo. (Os futuros de cripto da CME negociam 24/7 desde 29/05/2026, então o
  "gap da CME" de fim de semana deixou de se formar nesses contratos.)
- **Risco de exchange:** posição na exchange é crédito contra a exchange. Não concentre.

Se a skill `crypto-trade-plan` estiver instalada, ela faz a camada completa (liquidação isolada e
cruzada, calculadora). Se não, use a conta acima e a regra: liquidação além do stop com folga de
pelo menos metade da distância do stop.

## Checklist de carregamento

Responda antes de fechar o plano:

1. Há resultado, decisão de juros, vencimento ou evento binário dentro do horizonte? Data e hora.
2. Qual é o gap plausível contra a posição, e o tamanho sobrevive a ele?
3. Qual é o custo de carregar (swap, funding, aluguel, financiamento) pelo prazo, em R?
4. A margem para carregar cabe na conta com folga de pelo menos 30%?
5. Se abrir com gap além do stop, qual é a ação: sair no primeiro minuto ou esperar 15 minutos e
   sair se não recuperar o nível? Decida agora, não na hora.
