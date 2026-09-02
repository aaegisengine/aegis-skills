# Ler o mercado de derivativos de cripto

Em cripto, o preço à vista é só metade da história. A outra metade está nos perpétuos: quem está alavancado, para que lado, e quanto custa ficar ali. Estas quatro métricas são públicas (Coinglass, Velo, exchanges) e o trader ou você consegue buscá-las. Use-as para qualificar o cenário, não para gerar sinal sozinho — nenhuma delas prevê direção; elas dizem **quem está vulnerável** se a direção vier.

## Funding rate

Taxa que comprados pagam a vendidos (positiva) ou vendidos pagam a comprados (negativa) a cada 8 horas na maioria das exchanges (algumas cobram a cada 1h ou 4h).

| Funding por 8h | Anualizado aproximado | Leitura |
|---|---|---|
| ~0,01% | ~11% | neutro (é o padrão da maioria das exchanges) |
| 0,03–0,05% | 33–55% | comprados pagando caro; mercado inclinado para o long |
| > 0,1% | > 100% | euforia; posições longas alavancadas demais, combustível para squeeze de baixa |
| negativo persistente | — | vendidos pagando; mercado pessimista, combustível para squeeze de alta |

Custo de carregar: `custo = notional × funding × número_de_períodos`. Uma posição de US$ 10.000 comprada com funding 0,05%/8h por 5 dias paga 10.000 × 0,0005 × 15 = US$ 75. Isso vira R no plano.

Funding extremo por si só não reverte o mercado — pode ficar extremo por semanas em tendência. O que ele diz é: "se vier um choque contra o lado lotado, a cascata será grande."

## Open interest (OI)

Total de contratos abertos. Interprete junto com o preço:

| Preço | OI | Leitura |
|---|---|---|
| sobe | sobe | dinheiro novo entrando comprado — tendência com sustento |
| sobe | cai | short squeeze / cobertura — movimento pode ser curto |
| cai | sobe | dinheiro novo entrando vendido — pressão |
| cai | cai | long liquidation / desalavancagem — pode limpar e formar fundo |

OI em máxima histórica + funding alto = mercado alavancado nos dois lados, amplitude vai subir. Após grande liquidação (OI cai 10–20% em horas), o mercado costuma ficar mais "limpo" e menos propenso a cascata por um tempo.

## Liquidações

Onde estão os clusters de liquidação (mapas de calor no Coinglass/Hyblock) é onde o preço tende a ser puxado em movimento de baixa liquidez — porque liquidação é ordem a mercado forçada, e market makers sabem onde ela está. Cluster grande logo acima do preço = imã para cima; logo abaixo = imã para baixo. Não é garantia, é probabilidade de "pavio".

Para o plano: nunca coloque stop dentro de um cluster óbvio. Coloque além dele, ou aceite que o stop será "pescado".

## Basis (perp vs spot) e contango de futuros datados

Perp negociando acima do spot (basis positivo) confirma demanda alavancada. Futuros trimestrais em contango forte (>10% anualizado) indicam otimismo e atraem carry trade (compra spot, vende futuro), que estabiliza. Basis negativo persistente é sinal de estresse.

## Outros dados que valem uma busca

- **Fluxo de ETFs spot** (BTC e ETH nos EUA): divulgado após o fechamento de NY; três dias seguidos de saída pesada costuma pesar no preço no dia seguinte.
- **Reservas em exchanges**: saída de moedas para carteira própria é lido como retenção; entrada grande em exchange precede venda.
- **Dominância do BTC**: subindo = dinheiro se protegendo em BTC (altcoins sofrem mais); caindo em alta = "alt season", risco maior.
- **Stablecoins (supply de USDT/USDC)**: crescendo = pólvora seca; encolhendo = saída do ecossistema.
- **Desbloqueios de tokens** (para altcoins): data pública; oferta nova = pressão vendedora.

## Alavancagem e liquidação

Preço de liquidação aproximado (perpétuo linear, modo isolado):

```
long:  liq ≈ entrada × (1 − 1/alavancagem + margem_de_manutenção)
short: liq ≈ entrada × (1 + 1/alavancagem − margem_de_manutenção)
```

Margem de manutenção típica: 0,4–0,5% para BTC em posição pequena; sobe por faixa de notional (exchanges publicam a tabela). Modo cross usa a conta inteira como margem — liquidação mais longe, mas quando vem leva tudo.

O script `scripts/crypto_calc.py` faz essa conta e a de tamanho por risco. Use-o em vez de calcular de cabeça.

A regra que sustenta tudo: **o stop tem que ser acionado antes da liquidação, com folga**. Alavancagem é só uma forma de usar menos margem para o mesmo tamanho; ela não deveria mudar o tamanho da posição, que é definido pelo risco. Se 10x "permite" uma posição maior, a conta está sendo feita de trás para frente.
