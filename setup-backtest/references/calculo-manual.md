# Entrada dos trades e cálculo passo a passo (sem execução de código)

Use este roteiro quando a ferramenta de execução de código não estiver disponível na conversa.
O princípio não muda: o número precisa ser **reproduzível**, então toda conta aparece escrita,
com a fórmula e os valores, de um jeito que o trader consiga conferir na calculadora.

## 1. Como o trader envia os trades

Aceite qualquer um destes, nesta ordem de preferência:

1. **Arquivo CSV ou planilha** (xlsx, csv). Com execução de código, leia direto. Sem ela, se a
   plataforma mostrar o conteúdo, trabalhe com ele; se não, peça pra colar como texto.
2. **Tabela colada como texto**, uma linha por trade.
3. **Print da planilha**: transcreva (protocolo abaixo) antes de calcular.

Colunas mínimas (qualquer uma das três opções basta):
- `r` (resultado em R), ou
- `entrada`, `stop` (inicial) e `saida`, ou
- resultado em R$ **e** o risco em R$ de cada trade (ou um risco fixo informado).

Recomendado: `data` (ordem real e resultado por mês). O resto (ativo, setup, obs) é opcional.

Pedido modelo ao trader (imperativo padrão):
> Envie os trades com pelo menos estas colunas: data e resultado em R. Se não tiver o R, envie
> entrada, stop inicial e saída de cada trade. Pode colar a tabela aqui, anexar o CSV ou mandar
> o print da planilha.

## 2. Print de planilha: transcrição honesta

- Transcreva linha por linha numa tabela e diga **quantas linhas leu**.
- Célula ilegível ou cortada: marque `?` e **não adivinhe dígito**. Linha com `?` no resultado
  fica fora da conta até o trader confirmar.
- Vários prints: identifique cada um ("Print 1: linhas 1 a 25 · Print 2: linhas 26 a 48") e
  confira se não há linha repetida ou faltando na emenda.
- Foto da tela ou print borrado: avise que a transcrição tem risco e peça confirmação.
- Antes de concluir qualquer coisa, mostre a tabela transcrita (ou pelo menos o total de linhas,
  a soma dos R e as linhas duvidosas) e peça pra ele confirmar.

## 3. Conversões

- Formato brasileiro: "1.250,50" vira 1250,50; "-1R" vira -1; "(150,00)" é -150.
- R a partir de preços: `R = (saída - entrada) ÷ (entrada - stop inicial)`. Vale pros dois
  lados. Ex.: venda em 100, stop 102, saída 96: (96 - 100) ÷ (100 - 102) = +2R.
- R a partir de dinheiro: `R = resultado R$ ÷ risco R$` daquele trade.
- Custo: subtraia o custo em R de cada trade (ex.: 0,05R) antes de tudo.
- Ordem: coloque em ordem cronológica antes de calcular drawdown e sequências.

## 4. Roteiro de cálculo (mostre cada linha)

Com a lista de R em ordem:

1. **n** = número de trades. **G** = trades com R > 0. **P** = trades com R < 0. Zerados à parte.
2. **Soma dos ganhos** (Σg) e **soma das perdas** (Σp, em módulo).
3. **Win rate** = G ÷ n.
4. **Ganho médio** = Σg ÷ G. **Perda média** = Σp ÷ P.
5. **Payoff** = ganho médio ÷ perda média. **Win rate de empate** = 1 ÷ (1 + payoff).
6. **Expectância** = (Σg - Σp) ÷ n.
7. **Profit factor** = Σg ÷ Σp.
8. **Curva acumulada**: some os R um a um. Em cada linha anote o acumulado e o maior acumulado
   até ali (o pico). **Drawdown** da linha = acumulado - pico. **Max drawdown** = o menor desses
   valores (o mais negativo).
9. **Maior sequência de perdas** e de ganhos: conte na ordem.
10. **Desvio padrão amostral**: média m = expectância; some (R - m)² de todos os trades; divida
    por (n - 1); tire a raiz.
11. **Erro padrão** = desvio ÷ √n. **Faixa aproximada de 95%** da expectância = expectância ± 2 ×
    erro padrão. Se a faixa inclui zero, a amostra não prova vantagem.
12. **SQN** = √n × expectância ÷ desvio (com n limitado a 100 para comparar sistemas).
13. **Expectância sem os 3 melhores**: tire os 3 maiores R e refaça o item 6.
14. **Por mês**: some os R de cada mês; conte quantos meses ficaram positivos.
15. **Trades necessários** pra afirmar expectância > 0: n ≈ (2 × desvio ÷ expectância)².
16. **Sequência de perdas do acaso**: L ≈ log(n × (1 - q)) ÷ log(1 ÷ q), com q = P ÷ n.

Listas longas (mais de ~60 trades): faça em blocos de 20, mostrando a soma parcial de cada bloco
(soma dos R, Σg, Σp, menor ponto da curva no bloco), pra ele conferir sem refazer tudo. Diga que
conta manual em lista grande tem risco de erro aritmético e que, com execução de código ligada,
o script refaz tudo em segundos.

## 5. O que NÃO dá pra fazer à mão

- **Monte Carlo** exige milhares de simulações. Sem execução de código, diga que ele não foi
  feito. Não invente "drawdown do Monte Carlo".
- No lugar, ofereça duas referências marcadas como o que são:
  - **Regra de bolso (não é Monte Carlo):** planeje pra um drawdown de pelo menos 1,5 a 2 vezes o
    máximo histórico.
  - **Sequência de perdas do acaso** (item 16), que é conta fechada.
- Quando a execução de código voltar, rode o script e substitua a regra de bolso pelo número.

## 6. Exemplo (ILUSTRATIVO: 10 trades genéricos)

R em ordem: +2, -1, -1, +1,5, -1, +2, -1, +0,5, -1, +1

1. n = 10 · G = 5 · P = 5
2. Σg = 2 + 1,5 + 2 + 0,5 + 1 = 7 · Σp = 5
3. Win rate = 5 ÷ 10 = 50%
4. Ganho médio = 7 ÷ 5 = 1,4R · Perda média = 5 ÷ 5 = 1R
5. Payoff = 1,4 · Empate = 1 ÷ 2,4 = 42%
6. Expectância = (7 - 5) ÷ 10 = 0,2R
7. Profit factor = 7 ÷ 5 = 1,4
8. Curva: 2, 1, 0, 1,5, 0,5, 2,5, 1,5, 2, 1, 2 · picos: 2, 2, 2, 2, 2, 2,5, 2,5, 2,5, 2,5, 2,5
   Max drawdown = 0 - 2 = -2R
9. Maior sequência de perdas = 2
10. Desvio: soma dos (R - 0,2)² = 3,24 + 1,44 + 1,44 + 1,69 + 1,44 + 3,24 + 1,44 + 0,09 + 1,44
    + 0,64 = 16,1 · ÷ 9 = 1,79 · raiz = 1,34R
11. Erro padrão = 1,34 ÷ 3,16 = 0,42R · faixa: 0,2 ± 0,85, ou seja, de -0,65R a +1,05R. Inclui
    zero: 10 trades não provam nada.
15. Trades necessários ≈ (2 × 1,34 ÷ 0,2)² ≈ 180.
