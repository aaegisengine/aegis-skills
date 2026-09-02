# Vieses que fazem backtest mentir

Backtest não erra a favor do mercado; erra a favor do trader. Cada viés abaixo infla o resultado e some no ao vivo. Passe pela lista antes de aceitar qualquer número.

## Look-ahead (olhar o futuro)

Usar no candle N uma informação que só existe no fechamento de N ou depois. Exemplos comuns: entrar "no rompimento" ao preço de abertura do candle que rompeu (o rompimento só é conhecido no fechamento); usar a máxima do dia como referência de manhã; indicadores calculados com o fechamento do candle atual e usados para entrar nele. Em código, é o `shift(1)` esquecido. Em replay manual, é a mão que "sabe" onde o gráfico vai.

Teste: para cada informação usada na entrada, pergunte "a que horas exatamente eu saberia disso?".

## Sobrevivência

Testar só nos ativos/dias que ainda existem ou que "deram certo". Ações que faliram saíram da lista; contratos de futuro vencidos ficam fora do dado contínuo; dias que o trader "não teria operado" são removidos da amostra depois de ver o resultado.

## Overfitting (ajuste ao passado)

Cada parâmetro numérico (período da média, múltiplo do ATR, horário de corte) é um botão. Com botões suficientes, qualquer série aleatória vira um setup com profit factor 3. Sinais: expectância que cai pela metade fora da amostra; resultado que muda muito com uma mudança pequena do parâmetro (período 20 ótimo, 18 e 22 péssimos); mais de 4–5 filtros na regra; regra com exceção ("exceto em dia de FOMC, exceto na primeira segunda do mês").

Antídoto: menos parâmetros; parâmetros "redondos" e justificáveis pela lógica do mercado, não pela otimização; testar a vizinhança do parâmetro escolhido; fora da amostra sagrado.

## Discricionariedade escondida

"Compro no pullback quando o contexto é favorável." Contexto favorável não é regra, é a memória do trader escolhendo os pullbacks que funcionaram. Em replay manual, o viés é enorme: o olho pula os sinais feios. Antídoto: escrever a regra de modo que duas pessoas diferentes marquem os mesmos trades no mesmo gráfico; se não conseguem, a regra não existe ainda.

## Execução idealizada

Fill no preço exato do gatilho, sem slippage; stop executado no nível exato (em gap, não executa); alvo tocado por 1 tick contado como cheio (na prática o alvo precisa ser atravessado para a ordem limitada preencher com certeza); ignorar spread em CFD/forex; ignorar que em notícia o livro some.

Regra conservadora: alvo só conta se o preço passou 1 tick além; stop conta no toque; slippage de 1 tick por lado em ativos líquidos, mais em ilíquidos; no mesmo candle que toca stop e alvo, assume-se stop.

## Regime único

Testar 3 meses de tendência de alta e concluir que o setup de compra de pullback funciona. Cada setup tem um regime em que brilha e um em que sangra; o backtest precisa cobrir os dois para o trader saber qual é qual — e, idealmente, ter um filtro de regime na regra ou a decisão consciente de parar de operar quando o regime muda.

## Dado ruim

Candle de futuro contínuo com rolagem mal costurada (gap artificial no vencimento); dado de CFD que difere do futuro; horário do dado em fuso diferente do da regra (o "candle das 09:30" é 09:30 de onde?); feriados e pregões reduzidos misturados. Confira o dado antes de testar a regra.

## Contagem seletiva

O trader lembra dos 15 trades bons do setup e esquece os 25 que "não eram bem o setup". Journal com todos os trades marcados é o único antídoto — e o motivo de a skill pedir a lista completa.

## Checklist rápida (responda sim/não)

1. Toda informação usada na entrada era conhecida no momento da entrada?
2. A amostra inclui todos os sinais da regra, inclusive os feios?
3. Custos e slippage estão descontados?
4. O período cobre alta, baixa e lateral?
5. Há menos de 5 parâmetros/filtros?
6. A expectância se sustenta fora da amostra ou na vizinhança dos parâmetros?
7. Duas pessoas marcariam os mesmos trades com a regra escrita?

Qualquer "não" invalida a conclusão até ser corrigido.
