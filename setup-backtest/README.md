# 🔬 Setup Backtest: os números do seu setup

Você envia os trades, ela devolve os números que importam, em R e reproduzíveis, e um veredito
**aprovado / reprovado / inconclusivo** contra um critério escrito ANTES do resultado. Sem
"quase aprovado" e sem suavizar: *"sua amostra não prova nada"*, com respeito e com o motivo.

**Ela cuida dos NÚMEROS.** Desenhar o protocolo e auditar o método em conversa é da
**[Backtest Honesto](../backtest/)**. Se você só tiver esta instalada, ela faz a versão enxuta
do protocolo mesmo assim.

## Como enviar os trades

- **CSV ou planilha anexada**, **tabela colada** como texto ou **print da planilha** (ela
  transcreve, diz quantas linhas leu e pede confirmação; célula ilegível não é adivinhada).
- **Colunas mínimas** (uma das três): resultado em R; ou entrada, stop inicial e saída; ou
  resultado em R$ com o risco em R$. Data é recomendada. Modelo em
  [`assets/trades_template.csv`](assets/trades_template.csv).
- Planilha do Excel em português funciona: ponto e vírgula, vírgula decimal, "R$", "-1R",
  datas dd/mm/aaaa.

## O que ela calcula

Expectância com faixa de 95%, win rate com o acerto de empate, payoff, profit factor, drawdown e
tempo abaixo do pico, sequências (e a que o acaso já produz), SQN, resultado por mês, expectância
sem os 3 melhores trades, dentro × fora da amostra e **Monte Carlo** de dois jeitos: ordem
embaralhada e reamostragem com reposição (faixa do resultado, chance de terminar negativo, chance
de tocar o seu limite de ruína). E a conta de quantos trades você precisa: n ≈ (2 × desvio ÷
expectância)².

## No claude.ai, com ou sem código

- **Com a execução de código ativada**, ela roda o script da pasta e o número é reproduzível.
- **Sem execução de código**, ela calcula passo a passo na conversa, com a fórmula à vista, pra
  você conferir na calculadora. Monte Carlo não se faz à mão: ela avisa e não inventa.

## O que vem na pasta

- [`scripts/backtest_metrics.py`](scripts/backtest_metrics.py): métricas + Monte Carlo de um CSV
  de trades (só biblioteca padrão do Python).
- [`scripts/strategy_template.py`](scripts/strategy_template.py): backtest por regras sobre
  candles OHLC; troque a função `sinal()` pela sua. Preenchimento conservador (gap no stop,
  1 tick além do alvo) e custo por trade.
- [`references/`](references/): métricas, vieses e o roteiro de cálculo manual.

## Resposta pensada pra celular

RESUMO de até 3 linhas no topo, seções fixas, 40 a 60 linhas. Tabela por mês só se você pedir.

## Como ativar

> *"analisa minha planilha de trades"* · *"qual a minha expectância?"* · *"quantos trades
> preciso pra saber?"* · *"roda um Monte Carlo"* · *"posso aumentar a mão?"*

## O que ela nunca faz

Não aceita "funciona, eu vejo no gráfico" como dado, não deixa o critério ser escrito depois do
resultado, não devolve "o melhor parâmetro é 23" (devolve a vizinhança e avisa que o "melhor" é
o mais suspeito) e não promete que aprovado vai funcionar.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · 📚 [`references/metricas.md`](references/metricas.md) · [`references/vieses.md`](references/vieses.md) · [`references/calculo-manual.md`](references/calculo-manual.md) · ⬅️ [Voltar ao pacote](../README.md)
