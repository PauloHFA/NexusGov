-- ==============================================================================
-- NexusGov - Migração Inicial Flyway (V1__init_schema.sql)
-- Especificação: SRS v1.0 Seção 7.4 (Modelo de Dados) e Requisitos RF-API-04 / RF-CFG-02
-- ==============================================================================

-- 1. Tabela de Órgãos Públicos Compradores
CREATE TABLE orgao (
    id VARCHAR(36) PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    nome_orgao VARCHAR(255) NOT NULL,
    esfera VARCHAR(20) NOT NULL, -- MUNICIPAL, ESTADUAL, FEDERAL
    poder VARCHAR(20) NOT NULL,  -- EXECUTIVO, LEGISLATIVO, JUDICIARIO
    uf CHAR(2) NOT NULL,
    codigo_ibge_municipio VARCHAR(7),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_orgao_uf_ibge ON orgao (uf, codigo_ibge_municipio);

-- 2. Tabela de Fornecedores / Empresas
CREATE TABLE fornecedor (
    id VARCHAR(36) PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    situacao_cadastral VARCHAR(50),
    data_abertura DATE,
    capital_social NUMERIC(15, 2),
    porte VARCHAR(50),
    cnae_fiscal_principal VARCHAR(10),
    logradouro VARCHAR(255),
    numero VARCHAR(50),
    cep VARCHAR(8),
    municipio_ibge VARCHAR(7),
    uf CHAR(2),
    telefone VARCHAR(50),
    email VARCHAR(150),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_fornecedor_uf ON fornecedor (uf);
CREATE INDEX idx_fornecedor_cnae ON fornecedor (cnae_fiscal_principal);

-- 3. Tabela de Sócios e Administradores (QSA) com Confiança de Identidade
CREATE TABLE socio (
    id VARCHAR(36) PRIMARY KEY,
    tipo_pessoa VARCHAR(2) NOT NULL, -- PF ou PJ
    cpf_cnpj_mascarado VARCHAR(14) NOT NULL,
    nome_normalizado VARCHAR(255) NOT NULL,
    confianca_identidade NUMERIC(4, 3) DEFAULT 1.000 NOT NULL, -- [0.000 a 1.000]
    rotulo_identidade VARCHAR(50) DEFAULT 'confirmada' NOT NULL, -- confirmada, presumida
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_socio_nome_cpf ON socio (nome_normalizado, cpf_mascarado);

-- 4. Vínculos Societários entre Fornecedores e Sócios
CREATE TABLE vinculo_societario (
    id VARCHAR(36) PRIMARY KEY,
    fornecedor_id VARCHAR(36) NOT NULL REFERENCES fornecedor(id) ON DELETE CASCADE,
    socio_id VARCHAR(36) NOT NULL REFERENCES socio(id) ON DELETE CASCADE,
    qualificacao VARCHAR(100),
    data_entrada DATE,
    percentual_capital NUMERIC(5, 2),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(fornecedor_id, socio_id)
);

-- 5. Versão Imutável de Parâmetros e Pesos Analíticos (RF-CFG-01)
CREATE TABLE parametro_versao (
    id VARCHAR(36) PRIMARY KEY,
    versao VARCHAR(20) NOT NULL UNIQUE, -- ex.: 'v1.0.0'
    descricao TEXT,
    payload_json JSONB NOT NULL,
    hash_sha256 CHAR(64) NOT NULL,
    ativo BOOLEAN DEFAULT FALSE NOT NULL,
    criado_por VARCHAR(100) NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 6. Tabela de Tetos Legais com Vigência Temporal (RF-CFG-02 / CA-ANA-04)
CREATE TABLE teto_legal_vigencia (
    id VARCHAR(36) PRIMARY KEY,
    modalidade_objeto VARCHAR(60) NOT NULL, -- 'DISPENSA_COMPRAS_SERVICOS', 'DISPENSA_OBRAS_ENGENHARIA'
    valor_limite NUMERIC(15, 2) NOT NULL,
    data_inicio_vigencia DATE NOT NULL,
    data_fim_vigencia DATE, -- NULL indica vigência aberta
    base_legal TEXT NOT NULL, -- ex: 'Lei 14.133/2021 art. 75, II', 'Decreto 11.871/2023'
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_teto_vigencia ON teto_legal_vigencia (modalidade_objeto, data_inicio_vigencia, data_fim_vigencia);

-- Carga inicial dos tetos legais da Lei 14.133/2021 e Decretos Federais
INSERT INTO teto_legal_vigencia (id, modalidade_objeto, valor_limite, data_inicio_vigencia, data_fim_vigencia, base_legal) VALUES
('teto-14133-orig-disp-compras', 'DISPENSA_COMPRAS_SERVICOS', 50000.00, '2021-04-01', '2021-12-31', 'Lei 14.133/2021 Art. 75, II (valor original)'),
('teto-14133-orig-disp-obras', 'DISPENSA_OBRAS_ENGENHARIA', 100000.00, '2021-04-01', '2021-12-31', 'Lei 14.133/2021 Art. 75, I (valor original)'),
('teto-dec-10922-disp-compras', 'DISPENSA_COMPRAS_SERVICOS', 54020.41, '2022-01-01', '2022-12-31', 'Decreto Federal nº 10.922/2021'),
('teto-dec-10922-disp-obras', 'DISPENSA_OBRAS_ENGENHARIA', 108040.82, '2022-01-01', '2022-12-31', 'Decreto Federal nº 10.922/2021'),
('teto-dec-11317-disp-compras', 'DISPENSA_COMPRAS_SERVICOS', 57209.60, '2023-01-01', '2023-12-31', 'Decreto Federal nº 11.317/2022'),
('teto-dec-11317-disp-obras', 'DISPENSA_OBRAS_ENGENHARIA', 114416.65, '2023-01-01', '2023-12-31', 'Decreto Federal nº 11.317/2022'),
('teto-dec-11871-disp-compras', 'DISPENSA_COMPRAS_SERVICOS', 59906.02, '2024-01-01', NULL, 'Decreto Federal nº 11.871/2023');

-- 7. Tabela de Contratações e Editais (PNCP)
CREATE TABLE contratacao (
    id VARCHAR(36) PRIMARY KEY,
    orgao_id VARCHAR(36) NOT NULL REFERENCES orgao(id),
    numero_controle_pncp VARCHAR(50) NOT NULL UNIQUE,
    codigo_unidade_compradora VARCHAR(30),
    modalidade_nome VARCHAR(100) NOT NULL,
    numero_edital VARCHAR(50),
    ano_compra INT NOT NULL,
    objeto TEXT,
    valor_total_estimado NUMERIC(15, 2),
    valor_total_homologado NUMERIC(15, 2),
    data_abertura_proposta TIMESTAMP WITH TIME ZONE,
    data_homologacao TIMESTAMP WITH TIME ZONE,
    situacao VARCHAR(50),
    url_pncp VARCHAR(255),
    uf CHAR(2) NOT NULL,
    municipio_ibge VARCHAR(7),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_contratacao_uf_ano ON contratacao (uf, ano_compra);
CREATE INDEX idx_contratacao_orgao ON contratacao (orgao_id);

-- 8. Itens da Contratação
CREATE TABLE item_contratacao (
    id VARCHAR(36) PRIMARY KEY,
    contratacao_id VARCHAR(36) NOT NULL REFERENCES contratacao(id) ON DELETE CASCADE,
    numero_item INT NOT NULL,
    descricao TEXT,
    codigo_catmat_catser VARCHAR(20),
    quantidade NUMERIC(12, 3),
    unidade_medida VARCHAR(30),
    valor_unitario_estimado NUMERIC(15, 4),
    valor_unitario_homologado NUMERIC(15, 4),
    valor_total NUMERIC(15, 2),
    situacao VARCHAR(50)
);
CREATE INDEX idx_item_catmat ON item_contratacao (codigo_catmat_catser);

-- 9. Participações e Propostas de Fornecedores na Licitação
CREATE TABLE participacao_licitacao (
    id VARCHAR(36) PRIMARY KEY,
    contratacao_id VARCHAR(36) NOT NULL REFERENCES contratacao(id) ON DELETE CASCADE,
    fornecedor_id VARCHAR(36) NOT NULL REFERENCES fornecedor(id),
    vencedor BOOLEAN DEFAULT FALSE NOT NULL,
    valor_proposta NUMERIC(15, 2),
    classificacao INT,
    desclassificado BOOLEAN DEFAULT FALSE,
    motivo_desclassificacao TEXT
);
CREATE INDEX idx_part_contratacao ON participacao_licitacao (contratacao_id);
CREATE INDEX idx_part_fornecedor ON participacao_licitacao (fornecedor_id);

-- 10. Execuções de Rotinas Analíticas
CREATE TABLE execucao_analise (
    id VARCHAR(36) PRIMARY KEY,
    tipo_escopo VARCHAR(20) NOT NULL, -- CONTRATACAO, ORGAO, MUNICIPIO, UF
    alvo_identificador VARCHAR(50) NOT NULL, -- ex: 'PB', '2507507' (João Pessoa), etc.
    parametro_versao_id VARCHAR(36) NOT NULL REFERENCES parametro_versao(id),
    status VARCHAR(30) NOT NULL, -- INICIADO, PROCESSANDO, CONCLUIDO, ERRO
    progresso_percentual INT DEFAULT 0 NOT NULL,
    iniciado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    finalizado_em TIMESTAMP WITH TIME ZONE,
    mensagem_erro TEXT
);

-- 11. Tabela de Achados Analíticos (Detecções dos 4 Eixos)
CREATE TABLE achado (
    id VARCHAR(36) PRIMARY KEY,
    execucao_id VARCHAR(36) NOT NULL REFERENCES execucao_analise(id) ON DELETE CASCADE,
    contratacao_id VARCHAR(36) REFERENCES contratacao(id),
    fornecedor_id VARCHAR(36) REFERENCES fornecedor(id),
    eixo VARCHAR(30) NOT NULL, -- GRAFO, BENFORD, FRACIONAMENTO, POPUP_VENDOR
    sinal VARCHAR(50) NOT NULL, -- ex: 'COMMUNITY_COVER_BIDDING', 'BENFORD_MAD_HIGH', 'SLIDING_WINDOW_EXCEEDED'
    escore NUMERIC(5, 4) NOT NULL, -- s_i ∈ [0, 1]
    confianca NUMERIC(5, 4) NOT NULL, -- c_i ∈ [0, 1]
    detalhes_json JSONB NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_achado_contratacao ON achado (contratacao_id);
CREATE INDEX idx_achado_eixo ON achado (eixo);

-- 12. Cadeia de Custódia e Evidências Forenses (RF-ING-02 / RF-REL-03)
CREATE TABLE evidencia (
    id VARCHAR(36) PRIMARY KEY,
    achado_id VARCHAR(36) NOT NULL REFERENCES achado(id) ON DELETE CASCADE,
    hash_sha256 CHAR(64) NOT NULL,
    url_fonte VARCHAR(255) NOT NULL,
    coletado_em TIMESTAMP WITH TIME ZONE NOT NULL,
    competencia_base VARCHAR(10) NOT NULL, -- YYYY-MM da Receita Federal
    trecho_dado TEXT NOT NULL,
    caminho_storage_raw VARCHAR(255) NOT NULL
);
CREATE INDEX idx_evidencia_hash ON evidencia (hash_sha256);

-- 13. Índice de Exposição a Anomalias (IEA) Consolidado
CREATE TABLE iea_resultado (
    id VARCHAR(36) PRIMARY KEY,
    contratacao_id VARCHAR(36) NOT NULL REFERENCES contratacao(id) ON DELETE CASCADE,
    parametro_versao_id VARCHAR(36) NOT NULL REFERENCES parametro_versao(id),
    valor_iea NUMERIC(5, 2) NOT NULL, -- [0.00 a 100.00]
    nivel_risco VARCHAR(20) NOT NULL, -- 'Baixo', 'Médio', 'Elevado'
    qtd_eixos_independentes INT NOT NULL,
    decomposicao_sinais JSONB NOT NULL,
    calculado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(contratacao_id, parametro_versao_id)
);
CREATE INDEX idx_iea_nivel ON iea_resultado (nivel_risco);

-- 14. Trilha de Auditoria Imutável (RF-API-05 / RNF-09)
CREATE TABLE trilha_auditoria (
    id VARCHAR(36) PRIMARY KEY,
    usuario_id VARCHAR(50),
    papel_usuario VARCHAR(20) NOT NULL, -- ADMIN, AUDITOR, GESTOR, PUBLICO
    endereco_ip VARCHAR(45) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    acao VARCHAR(50) NOT NULL, -- CONSULTA, EXPORTACAO_PDF, EXPORTACAO_CSV, ALTERACAO_PARAMETRO
    parametros_requisicao JSONB,
    hash_resultado CHAR(64),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_trilha_criado_em ON trilha_auditoria (criado_em);

-- 15. Canal de Contestação e Retificação Cadastral (RF-REL-05)
CREATE TABLE contestacao (
    id VARCHAR(36) PRIMARY KEY,
    numero_protocolo VARCHAR(30) NOT NULL UNIQUE,
    tipo_solicitante VARCHAR(20) NOT NULL, -- PESSOA_FISICA, PESSOA_JURIDICA
    documento_identificador VARCHAR(14) NOT NULL,
    nome_solicitante VARCHAR(255) NOT NULL,
    email_contato VARCHAR(150) NOT NULL,
    contratacao_id VARCHAR(36) REFERENCES contratacao(id),
    fornecedor_id VARCHAR(36) REFERENCES fornecedor(id),
    motivo_contestacao TEXT NOT NULL,
    documentos_anexos JSONB,
    status VARCHAR(30) DEFAULT 'EM_ANALISE' NOT NULL, -- EM_ANALISE, DEFERIDO, INDEFERIDO
    parecer_resposta TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    respondido_em TIMESTAMP WITH TIME ZONE
);
CREATE INDEX idx_contestacao_protocolo ON contestacao (numero_protocolo);
