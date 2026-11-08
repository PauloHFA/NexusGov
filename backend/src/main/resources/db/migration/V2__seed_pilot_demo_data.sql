-- ==============================================================================
-- NexusGov - Carga Inicial de Dados de Demonstração do Piloto da Paraíba (PB)
-- Migração: V2__seed_pilot_demo_data.sql
-- Escopo: Municípios com prefixo IBGE 25 (João Pessoa, Campina Grande, Patos, Santa Rita)
-- Casos: Cartel/Sócio Compartilhado, Fracionamento de Dispensa, Pop-up Vendor e Caso Conforme
-- ==============================================================================

-- 1. Versão Inicial de Parâmetros
INSERT INTO parametro_versao (id, versao, descricao, payload_json, hash_sha256, ativo, criado_por) VALUES
('param-v100', 'v1.0.0', 'Parâmetros Oficiais de Referência do Piloto Paraíba per Resolução TCU 367/2024',
 '{"pesos": {"GRAFO": 1.0, "BENFORD": 1.0, "FRACIONAMENTO": 1.0, "POPUP_VENDOR": 1.0}, "limiares": {"elevado": 60.0, "medio": 30.0}}'::jsonb,
 '4a5e1e53b93f10d184f88194c6140f35da909b5329c21d8b688d6c7022067710', TRUE, 'Sistema NexusGov')
ON CONFLICT (id) DO NOTHING;

-- 2. Órgãos Públicos da Paraíba (PB)
INSERT INTO orgao (id, cnpj, nome_orgao, esfera, poder, uf, codigo_ibge_municipio) VALUES
('org-jp', '08778268000160', 'Prefeitura Municipal de João Pessoa', 'MUNICIPAL', 'EXECUTIVO', 'PB', '2507507'),
('org-cg', '08993714000185', 'Prefeitura Municipal de Campina Grande', 'MUNICIPAL', 'EXECUTIVO', 'PB', '2504009'),
('org-patos', '08889988000112', 'Prefeitura Municipal de Patos', 'MUNICIPAL', 'EXECUTIVO', 'PB', '2510808'),
('org-srita', '08776655000199', 'Prefeitura Municipal de Santa Rita', 'MUNICIPAL', 'EXECUTIVO', 'PB', '2513703')
ON CONFLICT (id) DO NOTHING;

-- 3. Fornecedores
INSERT INTO fornecedor (id, cnpj, razao_social, nome_fantasia, situacao_cadastral, data_abertura, capital_social, porte, cnae_fiscal_principal, municipio_ibge, uf) VALUES
('forn-alfa', '12345678000190', 'Alfa Construções e Pavimentação Ltda', 'Alfa Pav', 'ATIVA', '2018-03-15', 500000.00, 'DEMAIS', '4211101', '2507507', 'PB'),
('forn-beta', '23456789000101', 'Beta Serviços de Engenharia Eireli', 'Beta Engenharia', 'ATIVA', '2019-07-20', 350000.00, 'DEMAIS', '4211101', '2504009', 'PB'),
('forn-delta', '34567890000112', 'Delta Tech Soluções em Informática Ltda', 'Delta Tech', 'ATIVA', '2017-01-10', 200000.00, 'EPP', '6201501', '2510808', 'PB'),
('forn-popup', '45678901000123', 'Nova Aurora Distribuidora e Serviços Ltda', 'Nova Aurora', 'ATIVA', '2024-01-15', 2000.00, 'ME', '4771701', '2513703', 'PB')
ON CONFLICT (id) DO NOTHING;

-- 4. Sócios e Administradores (QSA)
INSERT INTO socio (id, tipo_pessoa, cpf_cnpj_mascarado, nome_normalizado, confianca_identidade, rotulo_identidade) VALUES
('soc-jose', 'PF', '***.123.456-**', 'JOSE CARLOS DA SILVA', 0.900, 'identidade presumida'),
('soc-maria', 'PF', '***.987.654-**', 'MARIA HELENA SANTOS', 1.000, 'identidade confirmada'),
('soc-antonio', 'PF', '***.555.444-**', 'ANTONIO PEREIRA LIMA', 1.000, 'identidade confirmada')
ON CONFLICT (id) DO NOTHING;

-- Vínculos Societários (José Carlos é sócio da Alfa e da Beta ao mesmo tempo)
INSERT INTO vinculo_societario (id, fornecedor_id, socio_id, qualificacao, data_entrada, percentual_capital) VALUES
('vinc-alfa-jose', 'forn-alfa', 'soc-jose', 'Sócio-Administrador', '2018-03-15', 60.00),
('vinc-beta-jose', 'forn-beta', 'soc-jose', 'Sócio Majoritário', '2019-07-20', 80.00),
('vinc-delta-maria', 'forn-delta', 'soc-maria', 'Sócia-Administradora', '2017-01-10', 100.00),
('vinc-popup-antonio', 'forn-popup', 'soc-antonio', 'Sócio Titular', '2024-01-15', 100.00)
ON CONFLICT (id) DO NOTHING;

-- 5. Contratações Públicas
INSERT INTO contratacao (id, orgao_id, numero_controle_pncp, modalidade_nome, numero_edital, ano_compra, objeto, valor_total_estimado, valor_total_homologado, data_abertura_proposta, data_homologacao, situacao, url_pncp, uf, municipio_ibge) VALUES
-- Caso 1: Cover Bidding / Sócio Comum
('c-pb-001', 'org-jp', '08778268000160-1-000001/2024', 'Pregão Eletrônico', 'PE 001/2024', 2024,
 'Obras de pavimentação asfáltica e drenagem de vias urbanas no Bairro de Mangabeira',
 1500000.00, 1450000.00, '2024-02-15 09:00:00-03', '2024-03-01 14:30:00-03', 'HOMOLOGADA',
 'https://pncp.gov.br/app/editais/08778268000160/2024/000001', 'PB', '2507507'),

-- Caso 2: Fracionamento de Dispensa de Medicamentos
('c-pb-002', 'org-cg', '08993714000185-1-000045/2024', 'Dispensa de Licitação', 'DISP 045/2024', 2024,
 'Aquisição direta e emergencial de insumos farmacêuticos e seringas descartáveis para a UPA Alto Branco',
 58000.00, 57500.00, '2024-04-10 08:00:00-03', '2024-04-12 11:00:00-03', 'HOMOLOGADA',
 'https://pncp.gov.br/app/editais/08993714000185/2024/000045', 'PB', '2504009'),

-- Caso 3: Pop-up Vendor (Empresa recém-criada)
('c-pb-003', 'org-patos', '08889988000112-1-000012/2024', 'Pregão Eletrônico', 'PE 012/2024', 2024,
 'Fornecimento continuado de material penso e correlatos para a rede municipal de saúde',
 820000.00, 790000.00, '2024-02-20 10:00:00-03', '2024-03-05 16:00:00-03', 'HOMOLOGADA',
 'https://pncp.gov.br/app/editais/08889988000112/2024/000012', 'PB', '2510808'),

-- Caso 4: Contratação Conforme (Baixo Risco)
('c-pb-004', 'org-srita', '08776655000199-1-000008/2024', 'Pregão Eletrônico', 'PE 008/2024', 2024,
 'Aquisição de licenças de software e suporte técnico para gestão tributária',
 190000.00, 182000.00, '2024-05-10 09:00:00-03', '2024-05-25 15:00:00-03', 'HOMOLOGADA',
 'https://pncp.gov.br/app/editais/08776655000199/2024/000008', 'PB', '2513703')
ON CONFLICT (id) DO NOTHING;

-- 6. Participação em Licitação
INSERT INTO participacao_licitacao (id, contratacao_id, fornecedor_id, vencedor, valor_proposta, classificacao) VALUES
('part-001', 'c-pb-001', 'forn-alfa', TRUE, 1450000.00, 1),
('part-002', 'c-pb-001', 'forn-beta', FALSE, 1480000.00, 2),
('part-003', 'c-pb-002', 'forn-popup', TRUE, 57500.00, 1),
('part-004', 'c-pb-003', 'forn-popup', TRUE, 790000.00, 1),
('part-005', 'c-pb-004', 'forn-delta', TRUE, 182000.00, 1)
ON CONFLICT (id) DO NOTHING;

-- 7. Execução de Análise
INSERT INTO execucao_analise (id, tipo_escopo, alvo_identificador, parametro_versao_id, status, progresso_percentual) VALUES
('exec-demo-pb', 'UF', 'PB', 'param-v100', 'CONCLUIDO', 100)
ON CONFLICT (id) DO NOTHING;

-- 8. Achados Forenses dos Casos
INSERT INTO achado (id, execucao_id, contratacao_id, fornecedor_id, eixo, sinal, escore, confianca, detalhes_json) VALUES
('ach-c01-grafo', 'exec-demo-pb', 'c-pb-001', 'forn-alfa', 'GRAFO', 'COMMUNITY_COVER_BIDDING', 0.8500, 0.9000,
 '{"motivo": "Empresas Alfa e Beta compartilham sócio administrador JOSE CARLOS DA SILVA com confiança 0.90 per QSA da Receita Federal."}'::jsonb),

('ach-c01-popup', 'exec-demo-pb', 'c-pb-001', 'forn-beta', 'POPUP_VENDOR', 'SHARED_NETWORK_PROXIMITY', 0.6500, 0.8500,
 '{"motivo": "Vínculo societário cruzado identificado na mesma microrregião metropolitana da Paraíba."}'::jsonb),

('ach-c02-split', 'exec-demo-pb', 'c-pb-002', 'forn-popup', 'FRACIONAMENTO', 'SLIDING_WINDOW_EXCEEDED', 0.9200, 1.0000,
 '{"motivo": "Soma de contratações do mesmo CATMAT no período de 45 dias atinge R$ 85.000,00 superando o teto legal de dispensa da Lei 14.133/2021 de R$ 59.906,02."}'::jsonb),

('ach-c03-popup', 'exec-demo-pb', 'c-pb-003', 'forn-popup', 'POPUP_VENDOR', 'HIGH_RATIO_LOW_AGE', 0.8800, 0.9500,
 '{"motivo": "Fornecedor criado há apenas 36 dias com capital social de R$ 2.000,00 adjudicado em certame de R$ 790.000,00 (razão de 395x)."}'::jsonb),

('ach-c03-grafo', 'exec-demo-pb', 'c-pb-003', 'forn-popup', 'GRAFO', 'RAPID_BIDDER_INTERLOCKING', 0.7000, 0.8000,
 '{"motivo": "Conexão periférica em cluster de fornecimento hospitalar sem histórico operacional anterior."}'::jsonb)
ON CONFLICT (id) DO NOTHING;

-- 9. Cadeia de Custódia Digital com SHA-256
INSERT INTO evidencia (id, achado_id, hash_sha256, url_fonte, coletado_em, competencia_base, trecho_dado, caminho_storage_raw) VALUES
('ev-001', 'ach-c01-grafo', '4a5e1e53b93f10d184f88194c6140f35da909b5329c21d8b688d6c7022067710',
 'https://pncp.gov.br/app/editais/08778268000160/2024/000001', '2024-03-02 10:15:00-03', '2024-02',
 '{"licitantes": ["12345678000190", "23456789000101"], "socio_comum": "JOSE CARLOS DA SILVA"}',
 's3://nexusgov-raw/pb/2024/02/08778268000160-1-000001-2024.json'),

('ev-002', 'ach-c02-split', '7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c',
 'https://pncp.gov.br/app/editais/08993714000185/2024/000045', '2024-04-13 14:20:00-03', '2024-04',
 '{"dispensas_agrupadas": ["DISP 045/2024", "DISP 040/2024"], "soma": 85000.0, "teto": 59906.02}',
 's3://nexusgov-raw/pb/2024/04/cg-dispensas-janela.parquet')
ON CONFLICT (id) DO NOTHING;

-- 10. Resultados IEA Consolidados com Salvaguardas Metodológicas
INSERT INTO iea_resultado (id, contratacao_id, parametro_versao_id, valor_iea, nivel_risco, qtd_eixos_independentes, decomposicao_sinais) VALUES
-- Caso 1: Elevado com 2 eixos (GRAFO e POPUP)
('iea-c01', 'c-pb-001', 'param-v100', 76.50, 'Elevado', 2,
 '[{"eixo": "GRAFO", "sinal": "COMMUNITY_COVER_BIDDING", "escore": 0.85, "confianca": 0.90, "peso": 1.0, "contribuicaoPonderada": 45.2},
   {"eixo": "POPUP_VENDOR", "sinal": "SHARED_NETWORK_PROXIMITY", "escore": 0.65, "confianca": 0.85, "peso": 1.0, "contribuicaoPonderada": 31.3}]'::jsonb),

-- Caso 2: Elevado com Fracionamento (FRACIONAMENTO)
('iea-c02', 'c-pb-002', 'param-v100', 64.00, 'Elevado', 2,
 '[{"eixo": "FRACIONAMENTO", "sinal": "SLIDING_WINDOW_EXCEEDED", "escore": 0.92, "confianca": 1.00, "peso": 1.0, "contribuicaoPonderada": 50.0},
   {"eixo": "GRAFO", "sinal": "REPEATED_DIRECT_SUPPLIER", "escore": 0.35, "confianca": 0.80, "peso": 1.0, "contribuicaoPonderada": 14.0}]'::jsonb),

-- Caso 3: Elevado com Pop-up Vendor
('iea-c03', 'c-pb-003', 'param-v100', 79.00, 'Elevado', 2,
 '[{"eixo": "POPUP_VENDOR", "sinal": "HIGH_RATIO_LOW_AGE", "escore": 0.88, "confianca": 0.95, "peso": 1.0, "contribuicaoPonderada": 48.0},
   {"eixo": "GRAFO", "sinal": "RAPID_BIDDER_INTERLOCKING", "escore": 0.70, "confianca": 0.80, "peso": 1.0, "contribuicaoPonderada": 31.0}]'::jsonb),

-- Caso 4: Baixo Risco Conforme
('iea-c04', 'c-pb-004', 'param-v100', 18.20, 'Baixo', 0,
 '[]'::jsonb)
ON CONFLICT (id) DO NOTHING;
