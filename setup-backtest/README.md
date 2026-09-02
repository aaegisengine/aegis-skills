# 🔬 Setup Backtest: do "eu vejo no gráfico" ao número reproduzível

A maioria dos setups nunca é testada porque a regra não está escrita de um jeito testável.
"Compro pullback em tendência" não é regra, é uma memória dos pullbacks que deram certo. O
primeiro trabalho da skill, e o mais valioso, é tirar o setup da sua cabeça e colocá-lo em
regras que **duas pessoas aplicariam igual no mesmo gráfico**. Só depois vem o número.

## O fluxo

1. **Formalizar as regras**, contexto, gatilho, entrada, stop, saída e o "o que NÃO é sinal", cada um respondendo a uma pergunta objetiva. Mais de 4–5 parâmetros? Alerta de overfitting antes de qualquer teste
2. **Critério de aprovação ANTES do teste**, expectância, profit factor, drawdown tolerável, mínimo de trades. Definido depois, o critério sempre se ajusta ao resultado
3. **Método**, replay manual na planilha, código (template pronto de estratégia sobre candles OHLC) ou híbrido, medindo o quanto o seu filtro discricionário adiciona (ou tira)
4. **Medir**, `scripts/backtest_metrics.py` lê o CSV de trades e devolve expectância, PF, drawdown, SQN, resultado por mês e **Monte Carlo** (drawdown p95, probabilidade de ruína). Nada calculado de cabeça: reproduzibilidade é o ponto
5. **Caçar vieses**, look-ahead, sobrevivência, overfitting, execução idealizada, regime único, contagem seletiva. Um "não" na checklist invalida a conclusão até ser corrigido
6. **Veredito**, **aprovado / reprovado / inconclusivo**. Não existe "quase aprovado". E aprovado ≠ tamanho cheio: o plano de forward test vem junto, com critério de continuidade já escrito

## O que vem na pasta

- [`scripts/backtest_metrics.py`](scripts/backtest_metrics.py): métricas + Monte Carlo de um CSV de trades (só biblioteca padrão)
- [`scripts/strategy_template.py`](scripts/strategy_template.py): backtest por regras sobre candles; troque a função `sinal()` pela sua
- [`assets/trades_template.csv`](assets/trades_template.csv): o formato do registro, pro replay manual e pro forward test

## Como ativar

> *"meu setup funciona?"* · *"analisa minha planilha de trades"* · *"quantos trades preciso pra saber?"* · *"posso aumentar a mão?"*

## O que ela nunca faz

Não aceita "funciona, eu vejo no gráfico" como dado (o olho vê os que funcionaram). Não otimiza parâmetro e devolve "o melhor é 23" (devolve a vizinhança e avisa que o "melhor" é o mais suspeito. E fala o que você não quer ouvir) *"sua amostra não prova nada"*, com respeito e com o motivo, sem suavizar a conclusão.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · 📚 [`references/metricas.md`](references/metricas.md) · [`references/vieses.md`](references/vieses.md) · ⬅️ [Voltar ao pacote](../README.md)
