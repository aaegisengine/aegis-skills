# Vieses que fazem backtest mentir

Backtest não erra a favor do mercado; erra a favor do trader. Cada viés abaixo infla o resultado
e some no ao vivo. Passe pela lista antes de aceitar qualquer número. (Se a skill
`backtest-honesto` estiver instalada, ela faz a auditoria completa do método; esta lista é a
versão que acompanha os números.)

## Look-ahead (olhar o futuro)

Usar no candle N uma informação que só existe no fechamento de N ou depois. Exemplos comuns:
entrar "no rompimento" ao preço de abertura do candle que rompeu (o rompimento só é conhecido no
fechamento); usar a máxima do dia como referência de manhã; indicador calculado com o fechamento
do candle atual e usado pra entrar nele; indicador que **repinta** (muda os valores passados
quando chega dado novo). Em código, é o `shift(1)` esquecido. Em replay manual, é a mão que
"sabe" onde o gráfico vai.

Teste: para cada informação usada na entrada, pergunte "a que horas exatamente eu saberia disso?".

## Sobrevivência

Testar só nos ativos ou dias que ainda existem ou que "deram certo". Ações que faliram saíram da
lista; contratos vencidos ficam fora do dado contínuo; dias que o trader "não teria operado" são
removidos da amostra depois de ver o resultado.

## Overfitting (ajuste ao passado)

Cada parâmetro numérico (período da média, múltiplo do ATR, horário de corte) é um botão. Com
botões suficientes, qualquer série aleatória vira um setup com profit factor 3. Sinais:
expectância que cai pela metade fora da amostra; resultado que muda muito com uma mudança pequena
do parâmetro (período 20 ótimo, 18 e 22 péssimos); mais de 4 ou 5 filtros; regra com exceção
("exceto em dia de FOMC, exceto na primeira segunda do mês").

Antídoto: menos parâmetros; parâmetros redondos e justificáveis pela lógica do mercado, não pela
otimização; testar a vizinhança do parâmetro escolhido; fora da amostra sagrado.

## Data snooping (tentar até dar certo)

Primo do overfitting, mas em outra escala: não é um setup com botões demais, é testar **muitas
ideias no mesmo dado** e guardar a melhor. Testando 20 variações, com 5% de chance de cada uma
parecer boa por acaso, a expectativa é que uma pareça boa sem ter vantagem nenhuma. Antídoto:
anotar TODAS as variações testadas, exigir resultado mais forte quanto mais variações houve, e
validar a vencedora num dado que nenhuma delas viu.

## Discricionariedade escondida

"Compro no pullback quando o contexto é favorável." Contexto favorável não é regra, é a memória
do trader escolhendo os pullbacks que funcionaram. Em replay manual, o viés é enorme: o olho pula
os sinais feios. Antídoto: escrever a regra de modo que duas pessoas diferentes marquem os mesmos
trades no mesmo gráfico; se não conseguem, a regra não existe ainda.

## Execução idealizada (custos e preenchimento)

Fill no preço exato do gatilho, sem slippage; stop executado no nível exato (em gap, sai no preço
do gap); alvo tocado por 1 tick contado como cheio (a ordem limitada precisa ser atravessada pra
preencher com certeza); ignorar corretagem, emolumentos e spread; ignorar que em notícia o livro
some.

Regra conservadora: alvo só conta se o preço passou 1 tick além; stop conta no toque, com 1 tick
de slippage em ativo líquido (mais em ilíquido); no mesmo candle que toca stop e alvo, assume-se
stop; gap através do stop sai na abertura.

## Gráfico não temporal

Backtest automático em cima de renko, Heikin Ashi ou outro gráfico sintético costuma sair irreal:
o preço do tijolo ou da barra suavizada não é preço negociado naquele momento, e o preenchimento
"no preço do tijolo" muitas vezes não existiu. Teste a regra no dado de tempo real (ou de tick),
mesmo que o sinal venha do renko.

## Regime único

Testar 3 meses de tendência de alta e concluir que o setup de compra de pullback funciona. Cada
setup tem um regime em que brilha e um em que sangra; o backtest precisa cobrir os dois pra o
trader saber qual é qual e, idealmente, ter um filtro de regime na regra ou a decisão consciente
de parar quando o regime muda.

## Dado ruim

Futuro contínuo com rolagem mal costurada (gap artificial no vencimento); dado de CFD que difere
do futuro; horário em fuso diferente do da regra (o "candle das 09:30" é 09:30 de onde?);
feriados e pregões reduzidos misturados. Confira o dado antes de testar a regra.

## Contagem seletiva

O trader lembra dos 15 trades bons do setup e esquece os 25 que "não eram bem o setup". Journal
com todos os trades marcados é o único antídoto, e o motivo de a skill pedir a lista completa.

## Checklist rápida (responda sim ou não)

1. Toda informação usada na entrada era conhecida no momento da entrada (e nada repinta)?
2. A amostra inclui todos os sinais da regra, inclusive os feios?
3. Custos e slippage estão descontados, com preenchimento conservador?
4. O período cobre alta, baixa e lateral?
5. Há menos de 5 parâmetros ou filtros?
6. A expectância se sustenta fora da amostra e na vizinhança dos parâmetros?
7. Duas pessoas marcariam os mesmos trades com a regra escrita?
8. Você sabe quantas variações foram testadas antes desta, e foram poucas?
9. O teste rodou em dado de tempo real ou de tick (não em gráfico sintético)?

Qualquer "não" invalida a conclusão até ser corrigido.
