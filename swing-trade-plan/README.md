# 🗓️ Swing Trade Plan: o plano que impede o trade de virar "investimento"

Swing quebra trader de um jeito específico: a posição nasce com stop e alvo e, na hora em que vai
contra, vira "investimento de longo prazo". A skill deixa escrito, **antes da entrada**, o que faz
a posição estar errada, de um jeito que você não consegue reinterpretar três dias depois.

## O que ela entrega

Um plano com **RESUMO de até 3 linhas no topo** e seções fixas:

- **Tese em uma frase**: sujeito, verbo e prazo. Se a frase não sai, você não tem tese, tem vontade de operar
- **Catalisadores com data**, cada um marcado "atravessa" ou "sai antes"
- **Entrada por região**, única ou escalonada, com preço médio e risco total calculados
- **Stop estrutural**: se o risco não cabe, **reduz a posição, não aperta o stop**
- **Invalidação separada do stop**: o stop é onde o *preço* diz que errou; a invalidação é onde a *tese* diz que errou, em frase testável, sem "reavaliar"
- **Gestão mecânica**: parcial ou sem parcial, trailing por estrutura, gap contra já decidido, saída por tempo
- **Custo de carregar em R** (swap, funding, aluguel) e **ficha de 6 linhas** pro journal

**A conta aparece sempre**, pra você conferir tamanho, R e custo.

## O que mudou nesta versão

- Especificações de contratos (WIN, WDO, NQ, MNQ, ES, MES, GC, MGC) e grade da B3 **conferidas em 07/11/2026**, com fonte; a skill reconfere na web quando a resposta depende disso
- **Sem busca na web**, ela avisa, pede preço e datas colados e segue com placeholders
- **Print do gráfico**: todo preço sai marcado `(lido)` ou `(aprox.)`
- **Conversa que continua**: posição carregada, resultado ou notícia nova, gap contra, revisão semanal, aumentar posição
- Funciona sozinha: a agenda e a camada de cripto saem enxutas aqui mesmo quando as outras skills não estão instaladas

## Revisão de posição carregada

*"tô comprado desde X, e agora?"*: ela calcula onde você está em R, confere tese e stop e responde
pelo plano: manter com stop em Z, reduzir pra N ou sair, com o motivo em uma linha. **Ela não
ajuda a construir a narrativa que justifica segurar.**

## Como ativar

> *"swing em PETR4 pras próximas semanas"* · *"tese pra NVDA"* · *"onde entro e saio num trade de uns dias?"* · *"estou carregando X, saiu o resultado, revisa"*

## O que ela nunca faz

Não vê o mercado, não inventa preço (placeholder nomeado quando falta) e não dá call.

---
📄 A skill em si: [`SKILL.md`](SKILL.md) · 📚 [`references/ativos.md`](references/ativos.md) · [`references/overnight.md`](references/overnight.md) · ⬅️ [Voltar ao pacote](../README.md)
