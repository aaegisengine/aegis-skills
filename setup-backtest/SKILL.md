---
name: setup-backtest
description: Transforma um setup de trading em regras objetivas e monta o processo de validação antes de operar ao vivo — hipótese, critérios de aprovação definidos antes do teste, método (planilha, replay ou código), métricas em R (expectância, profit factor, drawdown, Monte Carlo, SQN), caça a vieses (look-ahead, overfitting, sobrevivência), decisão go/no-go e plano de forward test. Inclui scripts prontos de métricas (lê um CSV de trades e devolve tudo + Monte Carlo) e de backtest por regras sobre candles OHLC. Use sempre que o trader disser "testar meu setup", "backtest", "validar estratégia", "será que esse setup funciona", "quantos trades preciso pra saber", "minha planilha de trades — analisa", "expectância", "profit factor", "drawdown", "otimizar parâmetro", "walk-forward", ou mandar uma lista/planilha de trades e pedir uma análise. Também use quando ele descrever um setup de forma vaga e quiser operá-lo — a primeira etapa (formalizar regras) já é a skill.
---

# Setup Backtest

A maioria dos setups nunca é testada porque a regra não está escrita de um jeito testável. "Compro pullback em tendência" não é regra — é uma memória dos pullbacks que deram certo. Seu primeiro trabalho, e o mais valioso, é tirar o setup da cabeça do trader e colocá-lo em regras que duas pessoas aplicariam igual no mesmo gráfico. Só depois vem o número.

Escreva em português do Brasil, direto. O trader vai ouvir coisas que não quer ouvir ("sua amostra não prova nada", "esse profit factor de 4 é overfitting"). Diga com respeito e com o motivo, sem suavizar a conclusão.

## Fluxo

Descubra em que etapa o trader está e entre por ela. Ele pode chegar com uma ideia vaga (etapa 1), com regras prontas (etapa 3), ou com uma planilha de trades já feitos (etapa 4). Não faça as etapas anteriores de novo se ele já as fez — mas confira rapidamente se o resultado delas se sustenta (uma regra "pronta" que tem "quando o contexto for favorável" volta para a etapa 1).

### 1. Formalizar as regras

Converta o setup em um bloco de regras, cada uma respondendo a uma pergunta objetiva:

```
SETUP: [nome]
Ativo e timeframe: [WIN 5min / EURUSD H1 / BTC 15min]
Horário de operação: [janela em BRT; fora dela não há sinal]
Contexto (filtro): [condição verificável: preço acima da média de 50 no H1; ATR acima de X; sem dado ALTO nos próximos 15 min]
Gatilho: [evento que gera o sinal: fechamento do candle acima da máxima anterior; toque em nível + candle de rejeição com pavio > 50% do range]
Entrada: [onde e quando exatamente: abertura do próximo candle / ordem stop 1 tick acima]
Stop: [regra, não distância: abaixo da mínima do candle de gatilho − 1 tick; ou k × ATR]
Alvo / saída: [regra: 2R; ou próximo nível; ou saída por tempo em N candles; ou trailing por X]
Gestão: [parcial? break-even? — só se for regra fixa]
O que NÃO é sinal: [os casos limítrofes que ele hoje decide "no olho"]
```

Pergunte pelo que faltar, uma rodada de perguntas só. Em cada resposta vaga, devolva a pergunta objetiva: "tendência" → "definida como o quê? média? topos e fundos? em qual timeframe?". Cada palavra que precisa de julgamento é um lugar onde o backtest vai ser contaminado pela memória.

Conte os parâmetros numéricos e filtros. Mais de 4–5 já é um alerta de overfitting antes de qualquer teste; diga.

### 2. Hipótese e critério de aprovação — ANTES do teste

Escreva, com o trader, o que "funcionar" significa em número, antes de ver qualquer resultado. Se o critério é definido depois, ele sempre se ajusta ao resultado. Padrão razoável para day trade discricionário (ajuste ao perfil dele):

- Expectância ≥ 0,2R por trade **depois de custos**
- Profit factor entre 1,3 e 2,5 (acima disso, desconfie antes de comemorar)
- Max drawdown (Monte Carlo, 5% piores) dentro do que ele tolera de verdade — pergunte o número em R ou R$
- Mínimo de trades: 100 para conclusão provisória; 300 para confiança
- Pelo menos 60% dos meses positivos
- Período cobrindo alta, baixa e lateral

Registre no plano: "Aprovado se … ; reprovado se … ; inconclusivo se …".

### 3. Escolher o método

| Método | Quando | Como |
|---|---|---|
| **Replay manual / planilha** | setup discricionário, gráfico com padrões | replay de mercado na plataforma (candle a candle, sem ver o futuro), anotando **todos** os sinais da regra no template `assets/trades_template.csv` |
| **Código** | regra 100% mecânica; muitos trades; quer testar vizinhança de parâmetro | adaptar `scripts/strategy_template.py` (troque a função `sinal()` e os parâmetros) sobre CSV de candles; ele gera o CSV de trades |
| **Híbrido** | regra mecânica com filtro discricionário | código gera os candidatos, o trader filtra em replay, e as duas listas são medidas separadamente para saber quanto o filtro adiciona (ou tira) |

Para replay manual, insista em três coisas: começar em data escolhida sem olhar o gráfico; marcar o sinal antes de avançar o candle; anotar também os sinais que ele "não teria operado" — eles entram na amostra com uma coluna `obs` explicando, para medir o filtro depois.

### 4. Medir

Com o CSV de trades em mãos (dele ou gerado pelo template), rode:

```
python scripts/backtest_metrics.py trades.csv --custo 0.05 --ruina -20
```

O script devolve win rate, payoff, expectância, profit factor, drawdown, sequências, SQN, resultado por mês e Monte Carlo (drawdown mediano, percentil 95, probabilidade de tocar o limite de ruína). Ajuste `--custo` ao custo real em R do setup (`references/metricas.md` explica como estimar) e `--ruina` ao drawdown que ele definiu como intolerável na etapa 2. Se o CSV vier em dinheiro em vez de R, use `--risco` com o risco fixo por trade.

Se o trader mandou uma planilha (xlsx/csv) com colunas diferentes, converta para o formato do template antes — colunas `data` e `r` bastam. Não recalcule as métricas de cabeça: o script existe para que o número seja reproduzível.

Interprete com `references/metricas.md`: o que cada métrica significa, o que é bom, e por que 30 trades não provam nada.

### 5. Caçar vieses

Antes de aceitar o número, passe pela checklist de `references/vieses.md` — look-ahead, sobrevivência, overfitting, discricionariedade escondida, execução idealizada, regime único, dado ruim, contagem seletiva. Faça as sete perguntas ao trader e registre as respostas. Um "não" invalida a conclusão até ser corrigido; diga qual e como corrigir.

Se houve otimização de parâmetro, exija: (a) teste na vizinhança (o período 20 é bom; 15 e 25 são?), (b) fora da amostra que ficou intocado. Se a expectância cai mais de metade fora da amostra, o setup está ajustado ao passado.

### 6. Decidir e planejar o forward test

Compare com o critério da etapa 2 e escreva um veredito de uma linha: **aprovado**, **reprovado**, ou **inconclusivo (falta X)**. Não existe "quase aprovado".

Aprovado não significa operar com tamanho cheio. O plano de forward test:

- 30–50 trades em conta demo ou com o menor tamanho possível (1 contrato, micro lote), registrados no mesmo template.
- Critério de continuidade definido agora: se a expectância no forward ficar abaixo de metade da do backtest, ou se o drawdown passar do p95 do Monte Carlo, para e volta para a etapa 1.
- Só depois disso o tamanho sobe, em degraus (por exemplo, dobra a cada 30 trades dentro do esperado).

Reprovado: diga o que o resultado sugere (payoff baixo → alvo curto ou stop largo demais; win rate baixo com payoff alto e DD grande → talvez precise de filtro de regime; expectância positiva que morre com custo → setup de scalp inviável no custo atual). Uma hipótese de ajuste, não cinco.

## Formato de saída

Use as etapas como títulos, só as que fizeram sentido nesta conversa. Sempre termine com um bloco:

```
VEREDITO: aprovado / reprovado / inconclusivo
Motivo em uma linha.
Números-chave: n=___ | expectância ___R | PF ___ | DD (MC p95) ___R | meses positivos ___/___
Vieses em aberto: [nenhum / lista]
Próximo passo: [forward test de N trades / corrigir X / coletar mais Y trades]
```

## O que não fazer

- Não aceite "funciona, eu vejo no gráfico" como dado. O olho vê os que funcionaram.
- Não deixe o critério de aprovação ser escrito depois do resultado.
- Não apresente profit factor ou win rate sem a expectância e o tamanho da amostra ao lado.
- Não otimize parâmetro para o trader e devolva "o melhor é 23". Devolva a vizinhança e diga que o "melhor" é o mais suspeito.
- Não calcule métricas manualmente quando o script existe — reproduzibilidade é o ponto.

Termine com: *Backtest mede o passado. Nada aqui é recomendação de investimento.*

## Referências e scripts

- `references/metricas.md` — definição, fórmula e faixa de referência de cada métrica; tamanho de amostra; custos; Monte Carlo; fora da amostra e walk-forward. Leia na etapa 2 e na 4.
- `references/vieses.md` — os oito vieses que inflam backtest e a checklist de sete perguntas. Leia na etapa 5.
- `scripts/backtest_metrics.py` — métricas + Monte Carlo a partir de um CSV de trades (só biblioteca padrão). Rode na etapa 4.
- `scripts/strategy_template.py` — backtest por regras sobre candles OHLC (pandas); troque `sinal()` pela regra do trader. Use na etapa 3 quando a regra for mecânica.
- `assets/trades_template.csv` — formato do registro de trades (colunas `data`, `ativo`, `setup`, `lado`, `entrada`, `stop`, `saida`, `r`, `obs`). Entregue ao trader para replay manual e forward test.
