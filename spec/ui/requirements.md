# Requisitos de Interface de Usuário e Visualização (UI)

## RF-UI-01: Mecanismo de Busca Global
- **Prioridade:** Must
- **Descrição:** Barra de pesquisa global responsiva com busca parametrizada por nome ou CNPJ do fornecedor, código do edital, órgão contratante ou município.
- **Critério de Aceite (CA-UI-01-A):**
  - **Dado** o usuário na tela inicial do sistema,
  - **Quando** digita o nome de um município da Paraíba (ex.: "Campina Grande") ou um CNPJ,
  - **Então** apresenta sugestões em tempo real em menos de 500 ms com opções de navegação direta.

## RF-UI-02: Visualizador Interativo de Redes (Cytoscape.js)
- **Prioridade:** Must
- **Descrição:** Renderizar rede gráfica com Cytoscape.js ao selecionar uma licitação: nós diferenciados por tipo (empresa, sócio, edital, contato), arestas coloridas por tipo de relação (vermelho para sócio ou endereço compartilhado) e diâmetro do nó proporcional à centralidade.
- **Critério de Aceite (CA-UI-01):**
  - **Dado** um edital com 8 licitantes concorrentes, onde dois compartilham o mesmo sócio,
  - **Quando** o usuário abre a visualização da rede,
  - **Então** o grafo exibe os nós com aresta vermelha destacando a ligação societária e painel lateral com a evidência em até 3 segundos.

## RF-UI-03: Painel de Detalhes da Contratação com IEA
- **Prioridade:** Must
- **Descrição:** Painel analítico exibindo o velocímetro do IEA (0-100), sinalizador de nível (Baixo, Médio, Elevado), lista discriminada de sinais ativados, pontuações de confiança e links diretos para o edital no PNCP.
- **Critério de Aceite (CA-UI-03):**
  - **Dado** uma contratação selecionada,
  - **Quando** o painel carrega,
  - **Então** exibe os botões de ação para baixar o Dossiê PDF, ver dados brutos da evidência e navegar para a fonte oficial.

## RF-UI-04: Filtros e Tabela de Resultados
- **Prioridade:** Must
- **Descrição:** Tabela paginada com ordenação e filtros múltiplos: intervalo de datas, UF (PB padrão no piloto), faixa de valor estimado/homologado, modalidade de contratação e faixa de IEA.
- **Critério de Aceite (CA-UI-04):**
  - **Dado** uma listagem de contratações,
  - **Quando** o usuário aplica o filtro "Apenas IEA Elevado na Paraíba no ano corrente",
  - **Então** atualiza a listagem de forma reativa exibindo apenas os processos correspondentes.

## RF-UI-05: Linha do Tempo de Fracionamento
- **Prioridade:** Should
- **Descrição:** Visualização em gráfico de linha do tempo (*timeline*) demonstrando a sucessão de compras diretas por fornecedor ao longo dos meses e os limites dos tetos legais vigentes.
- **Critério de Aceite (CA-UI-05):**
  - **Dado** um fornecedor sob suspeita de fracionamento de compras diretas,
  - **Quando** o usuário abre a visão temporal,
  - **Então** as janelas de 30/60/90 dias que ultrapassam o teto legal são visualmente destacadas com blocos sombreados de alerta.

## RF-UI-06: Visão Agregada em Mapa Geográfico
- **Prioridade:** Could
- **Descrição:** Mapa com distribuição de risco agregado por município (sem expor nomes de pessoas físicas para perfil público).
- **Critério de Aceite (CA-UI-06):**
  - **Dado** o perfil `PUBLICO` navegando pelo mapa do Estado da Paraíba,
  - **Quando** aproxima o zoom sobre um município,
  - **Então** exibe taxa média de exposição e volume financeiro analisado sem dados pessoais.

## RF-UI-07: Aviso Metodológico Permanente
- **Prioridade:** Must
- **Descrição:** Aviso metodológico e legal obrigatório visível e fixo em todas as páginas, relatórios e modais que apresentem classificações de risco ou escores de IEA.
- **Critério de Aceite (CA-SG-01):**
  - **Dado** qualquer página do sistema que renderize indicadores estatísticos,
  - **Quando** visualizada na tela,
  - **Então** contém o banner permanente informando a natureza estritamente probabilística de triagem e o respeito à presunção de inocência.
