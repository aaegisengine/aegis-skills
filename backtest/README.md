# 🧪 Backtest Honesto: o teste que tenta se derrubar

A verdade desconfortável: **a maioria dos backtests não testa a estratégia, confirma o
desejo.** Esta skill monta (ou ataca) o teste do jeito que um adversário montaria. Se a ideia
sobreviver, merece consideração; se não, você economizou meses e capital.

Ela não executa o teste com dados de mercado (não tem feed, e **não finge ter**). Ela entrega
o protocolo que você executa no replay/planilha, e depois audita o que você trouxer.

## Modo PROJETAR: da ideia ao protocolo

- **Teste dos dois traders:** a regra é reescrita até que duas pessoas com o mesmo gráfico
  encontrem OS MESMOS trades. "Entro quando mostra força" reprova; enquanto houver palavra
  subjetiva, volta pra reescrita.
- **Amostra:** 30 trades é o mínimo absoluto (abaixo é ruído com cara de padrão); 100+ pra
  confiar. Período cobrindo tendência E range.
- **Out-of-sample de uso ÚNICO:** calibrou na primeira janela, validou na segunda: se voltar
  pra ajustar, a segunda janela morreu e o teste precisa de dados novos.
- **Custos desde o 1º trade:** corretagem + slippage realista em cada linha da planilha.
  Backtest sem custo é ficção, melhor o setup morrer na planilha que na conta.
- **Métricas que importam:** expectância (média de R por trade: O número), profit factor,
  drawdown máximo e maior sequência de perdas ("você aguentaria X stops seguidos?").
  **Taxa de acerto é a métrica-isca**, sozinha não diz nada.

## Modo AUDITAR: o ataque aos resultados

Checklist de 9 ataques sobre o que você trouxer: amostra, regra objetiva, **overfitting**
(teste do vizinho: mudou pouco um parâmetro e o resultado desabou? curva ajustada), janela
escolhida a dedo, look-ahead, sobrevivência, custos, out-of-sample, consistência interna
(tira os 3 melhores trades, a expectância sobrevive?). Veredito em três blocos: **o que este
teste PROVA · o que NÃO prova · o próximo teste.**

## Como ativar

> *"quero testar esse setup"* · *"monta um protocolo de backtest"* · *"audita esses resultados"* + os números

## O que ela nunca faz

Não promete que setup aprovado "vai funcionar" (backtest reduz autoengano, não garante futuro),
não fabrica estatística de mercado, não aprova amostra pequena "porque a ideia parece boa".

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · ⬅️ [Voltar ao pacote](../README.md)
