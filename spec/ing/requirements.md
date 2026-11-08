# Requisitos de Ingestão e Dados (ING)

## RF-ING-01: Coleta da API REST do PNCP
- **Prioridade:** Must
- **Descrição:** Coletar contratações, itens, atas, contratos e resultados da API REST do PNCP com paginação, retentativas com backoff exponencial e respeito aos limites de taxa.
- **Critério de Aceite (CA-ING-01-A):**
  - **Dado** uma chamada à API do PNCP sujeita a limite de taxa (*rate limiting* ou HTTP 429),
  - **Quando** o coletor executa a requisição,
  - **Então** aplica espera com *exponential backoff* com jitter e retoma a paginação sem perda de registros.

## RF-ING-02: Armazenamento de Payload Bruto Imutável
- **Prioridade:** Must
- **Descrição:** Armazenar o payload bruto imutável com hash SHA-256 e carimbo de coleta UTC.
- **Critério de Aceite (CA-ING-02):**
  - **Dado** um payload coletado do PNCP,
  - **Quando** o registro é salvo,
  - **Então** existe hash SHA-256 correspondente ao conteúdo bruto, e qualquer alteração posterior do payload invalida a verificação forense (RF-REL-04).

## RF-ING-03: Importação de Dumps da Receita Federal
- **Prioridade:** Must
- **Descrição:** Importar os dumps mensais da Receita Federal (Empresas, Estabelecimentos, Sócios, CNAEs, Municípios, Naturezas) por processamento colunar em blocos (chunks).
- **Critério de Aceite (CA-ING-03):**
  - **Dado** um arquivo de dump de dezenas de gigabytes (ex.: Estabelecimentos),
  - **Quando** o processamento é iniciado,
  - **Então** o processamento ocorre via streaming colunar sem esgotamento de memória e registra métricas de progresso.

## RF-ING-04: Conversão para Parquet Particionado
- **Prioridade:** Must
- **Descrição:** Converter arquivos CSV para formato Parquet particionado por competência e UF, com esquema validado.
- **Critério de Aceite (CA-ING-04):**
  - **Dado** um conjunto de dados brutos processados,
  - **Quando** persistidos na camada analítica,
  - **Então** são gravados em arquivos Parquet com compressão snappy/zstd organizados por diretórios `/competencia=YYYY-MM/uf=XX/`.

## RF-ING-05: Filtro do Universo de Fornecedores PNCP
- **Prioridade:** Should
- **Descrição:** Filtrar o universo de CNPJs para focar nos fornecedores presentes no PNCP, preservando a base completa em armazenamento frio.
- **Critério de Aceite (CA-ING-05):**
  - **Dado** a base cadastral de mais de 50 milhões de CNPJs,
  - **Quando** a tabela analítica quente for construída,
  - **Então** apenas fornecedores participantes de contratações do PNCP (e seus sócios) são mantidos em memória de consulta rápida.

## RF-ING-06: Carga Incremental e Idempotência
- **Prioridade:** Must
- **Descrição:** Carga incremental e idempotente: reprocessar a mesma competência não duplica registros.
- **Critério de Aceite (CA-ING-01):**
  - **Dado** que a competência 2026-09 da Receita já foi importada,
  - **Quando** a importação é executada novamente,
  - **Então** a contagem de registros permanece idêntica e o relatório de qualidade indica 0 inserções novas duplicadas.

## RF-ING-07: Importação de Municípios do IBGE
- **Prioridade:** Must
- **Descrição:** Importar tabela de municípios do IBGE contendo código, UF e coordenadas geográficas do centróide.
- **Critério de Aceite (CA-ING-07):**
  - **Dado** o dataset de municípios do IBGE,
  - **Quando** importado no sistema,
  - **Então** todos os 5.570 municípios possuem latitude e longitude do centróide para cálculo de distância geodésica.

## RF-ING-08: Relatório de Qualidade de Carga
- **Prioridade:** Should
- **Descrição:** Registrar relatório de qualidade por carga com contagem de linhas, nulos, rejeições e tempo de execução.
- **Critério de Aceite (CA-ING-08):**
  - **Dado** uma rotina de ingestão finalizada,
  - **Quando** consultado o relatório da carga,
  - **Então** exibe total de linhas lidas, aceitas, rejeitadas por validação e checksum da execução.

## RF-ING-09: Detecção de Mudanças de Esquema
- **Prioridade:** Should
- **Descrição:** Detectar alterações estruturais de esquema nos dados de origem e falhar de forma explícita com alerta.
- **Critério de Aceite (CA-ING-09):**
  - **Dado** um novo arquivo com colunas renomeadas ou tipos incompatíveis,
  - **Quando** a validação de esquema executa,
  - **Então** a carga é interrompida antes da escrita no banco e uma notificação de inconformidade é gerada.
