# Requisitos de Resolução de Entidades e Normalização (ENT)

## RF-ENT-01: Normalização de CNPJ e Nomes
- **Prioridade:** Must
- **Descrição:** Normalizar CNPJ (14 dígitos numéricos, com cálculo e validação obrigatória dos dígitos verificadores) e sanitização de nomes empresariais e de pessoas físicas (remoção de acentuação, caixa alta, limpeza de partículas societárias como ME, EPP, LTDA, S/A).
- **Critério de Aceite (CA-ENT-01-A):**
  - **Dado** uma entrada de CNPJ formatada ou desformatada,
  - **Quando** o validador processa o número,
  - **Então** valida os dois dígitos verificadores via módulo 11 e armazena os 14 dígitos numéricos limpos.

## RF-ENT-02: Normalização de Endereços e Telefones
- **Prioridade:** Must
- **Descrição:** Normalizar logradouro, número, complemento, bairro, CEP (8 dígitos) e números de telefone (DDD + número) para permitir detecção de compartilhamento de atributos de contato.
- **Critério de Aceite (CA-ENT-02):**
  - **Dado** dois estabelecimentos que informam o mesmo endereço físico com pequenas variações ortográficas (ex.: "Av. Epitácio Pessoa, 100" e "Avenida Presidente Epitacio Pessoa 100"),
  - **Quando** a normalização é executada,
  - **Então** gera chaves canônicas idênticas e sinaliza aresta de compartilhamento de endereço.

## RF-ENT-03: Resolução de Sócios Pessoa Física com Nível de Confiança
- **Prioridade:** Must
- **Descrição:** Resolver sócios pessoa física cruzando nome normalizado + CPF mascarado (fornecido publicamente pela Receita Federal com dígitos centrais `***123456**`), atribuindo nível de confiança `c_i < 1.0` para mitigar o risco de homonímia.
- **Critério de Aceite (CA-ENT-01):**
  - **Dado** dois registros societários com mesmo nome e CPF mascarado idêntico,
  - **Quando** a resolução de entidades é executada,
  - **Então** o vínculo é criado com nível de confiança estritamente menor que 1,0 e rotulado como "identidade presumida" na API e na interface gráfica (respeitando a salvaguarda SG-05).

## RF-ENT-04: Vinculação de Fornecedores PNCP à Receita Federal
- **Prioridade:** Must
- **Descrição:** Vincular cada fornecedor participante ou adjudicado no PNCP ao respectivo cadastro analítico de estabelecimentos e empresas da Receita Federal por meio da raiz e filial do CNPJ.
- **Critério de Aceite (CA-ENT-04):**
  - **Dado** um fornecedor registrado em certame no PNCP,
  - **Quando** ocorre a ingestão do certame,
  - **Então** o registro do fornecedor é enriquecido com situação cadastral, data de abertura, capital social, CNAE principal e secundários.

## RF-ENT-05: Encadeamento de Cadeias Societárias (PJ)
- **Prioridade:** Should
- **Descrição:** Resolver cadeias de participação onde sócios são outras pessoas jurídicas (PJs), com nível de profundidade configurável (padrão de até 2 saltos).
- **Critério de Aceite (CA-ENT-05):**
  - **Dado** que a Empresa A tem como sócia a Empresa B, cujos sócios são Pessoas Físicas,
  - **Quando** o grafo corporativo é expandido até profundidade 2,
  - **Então** as pessoas físicas da Empresa B são associadas indiretamente à Empresa A com ponderação de confiança decrescente.
