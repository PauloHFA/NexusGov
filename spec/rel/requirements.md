# Requisitos de Relatórios e Exportação Forense (REL)

## RF-REL-01: Geração de Dossiê Executivo em PDF
- **Prioridade:** Must
- **Descrição:** Gerar relatório executivo e técnico em formato PDF por contratação, órgão público ou fornecedor, contendo sumário do IEA, decomposição dos sinais, evidências rastreáveis e aviso metodológico regulamentar obrigatório.
- **Critério de Aceite (CA-REL-01):**
  - **Dada** uma contratação com IEA "Elevado",
  - **Quando** o dossiê PDF for gerado,
  - **Então** o documento contém: sinais detalhados, evidências com URLs oficiais do PNCP, hashes SHA-256 das fontes, competência do dataset da Receita, versão dos pesos utilizados e o aviso metodológico legal destacado.

## RF-REL-02: Exportação em Formatos Abertos (CSV e Parquet)
- **Prioridade:** Must
- **Descrição:** Permitir a exportação dos achados, índices e dados tabulares de apoio em formatos abertos e estruturados (CSV e Apache Parquet) para análise externa de dados.
- **Critério de Aceite (CA-REL-02):**
  - **Dado** o resultado de uma auditoria em uma prefeitura,
  - **Quando** o usuário solicita o download em Parquet ou CSV,
  - **Então** o arquivo gerado contém metadados de coluna consistentes e esquema correspondente à especificação.

## RF-REL-03: Rastreabilidade Forense no Dossiê
- **Prioridade:** Must
- **Descrição:** Incluir no dossiê forense a versão exata do modelo analítico, hash dos parâmetros em vigor, competência da base de dados da Receita Federal e hash SHA-256 de cada evidência bruta.
- **Critério de Aceite (CA-REL-03):**
  - **Dado** o PDF emitido pelo sistema,
  - **Quando** o documento for inspecionado,
  - **Então** possui uma seção de "Cadeia de Custódia Digital" com identificadores criptográficos permitindo a qualquer perito reproduzir o cálculo.

## RF-REL-04: Verificação Independente de Autenticidade
- **Prioridade:** Should
- **Descrição:** Disponibilizar comando CLI ou rota de API pública que recebe o dossiê/metadados e confere a integridade dos hashes SHA-256 contra os dados históricos armazenados.
- **Critério de Aceite (CA-REL-04):**
  - **Dado** um dossiê gerado e um payload original armazenado,
  - **Quando** a ferramenta de verificação calcula o hash,
  - **Então** confirma a integridade e atesta se houve ou não adulteração no conteúdo emitido.

## RF-REL-05: Canal de Contestação e Retificação de Dados
- **Prioridade:** Should
- **Descrição:** Oferecer canal de registro formal para que pessoas físicas ou jurídicas citadas em relatórios ou pesquisas possam submeter esclarecimentos, correções ou contestações de dados cadastrais.
- **Critério de Aceite (CA-REL-05):**
  - **Dado** um pedido de retificação cadastral recebido,
  - **Quando** o registro for protocolado no sistema,
  - **Então** é gerado protocolo de atendimento e o status do registro passa a indicar "em revisão cadastral".
