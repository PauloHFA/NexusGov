# Requisitos de Análise Estatística e Grafos (ANA)

## RF-ANA-01: Construção do Grafo Heterogêneo
- **Prioridade:** Must
- **Descrição:** Construir o grafo heterogêneo $V = \{E, S, L, A\}$ (Empresas, Sócios, Licitações, Atributos) filtrado por órgão, município (ex.: municípios da Paraíba), UF ou período.
- **Critério de Aceite (CA-ANA-01-A):**
  - **Dado** o conjunto de licitações e cadastros de um município da PB,
  - **Quando** o construtor de grafo executa,
  - **Então** gera nós para cada entidade e arestas ponderadas (E-S peso 1.0 x confiança; E-A peso 0.6 a 0.8; E-L peso 1.0).

## RF-ANA-02: Detecção de Comunidades (Leiden) e Centralidade
- **Prioridade:** Must
- **Descrição:** Projetar o grafo bipartido em coocorrência de empresas, detectar comunidades com o algoritmo de Leiden (semente fixa) e calcular *betweenness centrality* (com amostragem para grafos grandes).
- **Critério de Aceite (CA-ANA-02-A):**
  - **Dado** um grafo de coocorrência de fornecedores,
  - **Quando** o algoritmo Leiden é executado repetidas vezes com a mesma semente,
  - **Então** a partição de comunidades é estritamente determinística (mesmos nós nas mesmas comunidades) e todas as comunidades são conectadas.

## RF-ANA-03: Cálculo de Risco por Licitação (RC) com Grafo Nulo
- **Prioridade:** Must
- **Descrição:** Calcular a métrica de risco $RC$ por certame (proporção de pares de licitantes pertencentes à mesma comunidade ou com vínculo direto) e comparar com o modelo nulo de permutação/configuração para controlar mercados naturalmente concentrados.
- **Critério de Aceite (CA-ANA-01):**
  - **Dado** um conjunto sintético ou real com 5 empresas compartilhando 2 sócios e disputando 20 licitações,
  - **Quando** o grafo é analisado,
  - **Então** as 5 empresas pertencem à mesma comunidade e o $RC$ das 20 licitações supera o limiar "Médio" (revocação $\ge 90\%$).

## RF-ANA-04: Teste de Conformidade à Lei de Benford
- **Prioridade:** Must
- **Descrição:** Executar teste de Benford sobre valores de itens/contratações com verificação de aplicabilidade ($n \ge 300$, $\ge 2$ ordens de grandeza), MAD de Nigrini, Kolmogorov-Smirnov sobre a mantissa contínua e correção de Benjamini-Hochberg.
- **Critério de Aceite (CA-ANA-02):**
  - **Dado** um conjunto com menos de 300 valores ($n < 300$),
  - **Quando** o teste é solicitado,
  - **Então** o resultado é marcado categoricamente como "não aplicável" (e não como "conforme") e nenhum achado espúrio é emitido.
  - **Dado** um conjunto com 5.000 valores conformes a Benford,
  - **Quando** o teste é solicitado,
  - **Então** MAD $\le 0,006$ e nenhum achado é gerado.

## RF-ANA-05: Detecção de Fracionamento de Despesa em Janela Deslizante
- **Prioridade:** Must
- **Descrição:** Agrupar contratações diretas por (órgão, fornecedor, CATMAT/classe), aplicar janelas deslizantes de 30, 60 e 90 dias, e sinalizar quando a soma dos valores superar o teto da modalidade vigente na data ou houver $\ge k$ contratações (padrão $k=3$) entre 80% e 100% do teto.
- **Critério de Aceite (CA-ANA-03):**
  - **Dado** um fornecedor com 4 dispensas do mesmo CATMAT em 45 dias no município X da PB, cada uma a 95% do teto vigente,
  - **Quando** a análise de janelas deslizantes é executada,
  - **Então** um achado de fracionamento é gerado agrupando as 4 contratações e referenciando os tetos vigentes em suas respectivas datas.

## RF-ANA-06: Detecção de Empresas Recém-Criadas (Pop-up Vendors)
- **Prioridade:** Must
- **Descrição:** Calcular razão entre valor homologado e capital social, idade do CNPJ na data de abertura da licitação (em dias), distância geográfica sede-órgão (via coordenadas IBGE) e porte declarado.
- **Critério de Aceite (CA-ANA-06):**
  - **Dado** uma empresa criada há menos de 30 dias com capital de R$ 1.000 que vence certame de R$ 500.000,
  - **Quando** o detector de recém-criadas é processado,
  - **Então** emite sinal proporcional de alta exposição no eixo de perfil societário.

## RF-ANA-07: Cálculo do IEA com Salvaguardas Invioláveis
- **Prioridade:** Must
- **Descrição:** Consolidar os sinais normalizados pela fórmula $IEA = 100 \times \frac{\sum w_i \cdot s_i \cdot c_i}{\sum w_i}$, aplicando os limiares Baixo (<30), Médio (30-60) e Elevado (>60), subordinado às salvaguardas SG-04 e SG-05.
- **Critério de Aceite (CA-ANA-05 & CA-SG-02):**
  - **Dado** um edital com sinal elevado em apenas 1 eixo (ex.: apenas Benford),
  - **Quando** o IEA é consolidado,
  - **Então** a regra SG-04 impede classificação "Elevada", rebaixando o nível máximo para "Médio".
  - **Dado** os mesmos insumos e versão de parâmetros,
  - **Quando** a análise é recomputada,
  - **Então** o resultado numérico do IEA é 100% idêntico bit a bit (determinismo estrito).

## RF-ANA-08: Disparo Assíncrono de Análises
- **Prioridade:** Must
- **Descrição:** Permitir o disparo de tarefas analíticas em lote ou por demanda via mensageria (RabbitMQ), reportando progresso e status.
- **Critério de Aceite (CA-ANA-08):**
  - **Dado** uma solicitação de análise forense para uma prefeitura inteira,
  - **Quando** a requisição é enfileirada no RabbitMQ,
  - **Então** o backend recebe confirmação imediata com ID de execução e acompanha o progresso das etapas.

## RF-ANA-09: Recálculo Histórico Versionado
- **Prioridade:** Should
- **Descrição:** Permitir recalcular análises com novos conjuntos de pesos/parâmetros mantendo o histórico de execuções passadas intacto.
- **Critério de Aceite (CA-ANA-09):**
  - **Dado** uma mudança de pesos de parâmetros (versão v1.1),
  - **Quando** um recálculo é solicitado,
  - **Então** os resultados anteriores da v1.0 são mantidos com seus respectivos hashes e uma nova linha de execução é vinculada à v1.1.

## RF-ANA-10: Cruzamento com Preços de Referência
- **Prioridade:** Could
- **Descrição:** Comparar valor adjudicado do item com preços medianos de bancos de preços públicos de referência quando disponíveis.
- **Critério de Aceite (CA-ANA-10):**
  - **Dado** um catálogo de itens com referencial de preço homologado,
  - **Quando** o valor unitário for superior em mais de 50% à mediana regional,
  - **Então** gera sinal de sobrepreço relativo.
