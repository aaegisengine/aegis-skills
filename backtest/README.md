# 🧪 Backtest Honesto: o método que tenta se derrubar

A verdade desconfortável: **a maioria dos backtests não testa a estratégia, confirma o
desejo.** Esta skill monta (ou ataca) o teste do jeito que um adversário montaria. Se a ideia
sobreviver, merece consideração; se não, você economizou meses e capital.

**Ela cuida do MÉTODO.** Não tem feed de mercado (e não finge ter) e não calcula planilha de
trades: os números ficam com a **[Setup Backtest](../setup-backtest/)**. Se você só tiver esta
instalada, ela faz uma conta enxuta mesmo assim, mostrando a fórmula.

## Modo PROJETAR: da ideia ao protocolo

- **Teste dos dois traders:** a regra é reescrita até que duas pessoas com o mesmo gráfico
  encontrem OS MESMOS trades.
- **Critério de aprovação escrito ANTES do teste.** Escrito depois, ele sempre se ajusta.
- **Amostra pela conta, não pelo chute:** n ≈ (2 × desvio ÷ expectância)². Edge pequeno pede
  amostra grande. Período cobrindo tendência E range.
- **Fora da amostra de uso ÚNICO**, walk-forward pra regra com parâmetro e forward test no fim.
- **Custos e preenchimento realista:** slippage, stop no toque, alvo só se passar 1 tick, gap
  sai no preço do gap.
- **Executar sem se enganar:** replay com data sorteada, `shift(1)` no código, e o aviso de que
  backtest automático em renko ou Heikin Ashi costuma sair irreal.

## Modo AUDITAR: o ataque aos resultados

Checklist de 10 ataques: amostra, regra objetiva, **overfitting** (teste do vizinho), **data
snooping** (quantas versões você testou antes?), janela e regime, look-ahead e repintura,
sobrevivência e dado, custos, fora da amostra, concentração (tirando os 3 melhores trades, a
expectância sobrevive?). E os sinais de alerta de robô e curso: acerto altíssimo com perda média
gigante é desenho de preço médio ou martingale.

Veredito em três blocos: **o que este teste PROVA · o que NÃO prova · o próximo teste.**

## Resposta pensada pra celular

RESUMO de até 3 linhas no topo, seções fixas, 40 a 60 linhas. Versão longa só se você pedir.

## Como ativar

> *"como faço backtest disso?"* · *"monta um protocolo pro meu setup"* · *"esse resultado é
> confiável?"* · *"audita esse relatório"* · *"esse robô de 90% de acerto é real?"* ·
> *"o que é overfitting?"*

## O que ela nunca faz

Não promete que setup aprovado "vai funcionar" (backtest reduz autoengano, não garante futuro),
não fabrica estatística de mercado, não aprova amostra pequena "porque a ideia parece boa".

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · ⬅️ [Voltar ao pacote](../README.md)
