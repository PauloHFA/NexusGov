# Relatório de Impacto à Proteção de Dados Pessoais (RIPD)

**Plataforma:** NexusGov — Análise Forense de Contratações Públicas (Piloto PB)  
**Marco Legal:** Lei Geral de Proteção de Dados Pessoais (Lei Federal nº 13.709/2018, Art. 38)  
**Conformidade Adicional:** Resolução TCU nº 367/2024 (Art. 19-B) e Lei de Acesso à Informação (Lei nº 12.527/2011)  
**Versão:** 1.0.0 — Piloto Estado da Paraíba (PB, prefixo IBGE 25)

---

## 1. Descrição do Tratamento de Dados

### 1.1 Natureza e Origem dos Dados
O NexusGov realiza o tratamento de dados de registros públicos governamentais estritamente abertos:
1. **PNCP (Portal Nacional de Contratações Públicas - Lei 14.133/2021):** Contratações, valores homologados, órgãos compradores e empresas participantes.
2. **Receita Federal do Brasil (RFB):** Cadastro Nacional de Pessoa Jurídica (CNPJ) e Quadro de Sócios e Administradores (QSA), disponibilizados em formato de dados abertos sob a Lei 12.527/2011.
3. **IBGE:** Malha territorial e coordenadas geográficas de municípios da Paraíba.

### 1.2 Categorias de Titulares e Dados Pessoais Tratados
- **Titulares:** Pessoas físicas constantes no Quadro de Sócios e Administradores (QSA) de empresas contratadas pelo poder público.
- **Dados:** Nome completo de sócios/administradores e número parcial de CPF mascarado (`***.XXX.XXX-**`), conforme fornecido pela Receita Federal.
- **Vedação:** A plataforma NÃO trata dados pessoais sensíveis (Art. 5º, II da LGPD) como saúde, religião, biometria ou orientação política.

---

## 2. Bases Legais e Finalidade Pública

O tratamento encontra respaldo direto nos incisos do Artigo 7º da LGPD:
1. **Art. 7º, II (Cumprimento de Obrigação Legal/Regulatória):** Aferição de conformidade aos limites e impedimentos de participação societária previstos nos artigos 14 e 75 da Lei nº 14.133/2021.
2. **Art. 7º, IX (Legítimo Interesse Público / Transparência Ativa):** Princípio constitucional da publicidade (CF/88 Art. 37) e Lei de Acesso à Informação, assegurando o controle social dos gastos públicos.

---

## 3. Salvaguardas Metodológicas e Medidas de Mitigação de Riscos

O NexusGov implementa salvaguardas invioláveis integradas à arquitetura do software:

### 3.1 SG-01: Linguagem Não Acusatória e Presunção de Inocência
O código, as APIs e as interfaces gráficas são rigidamente blindados por linters automáticos contra o uso de termos terminativos ou acusatórios (ex.: "fraude", "crime", "culpado", "conluio comprovado"). Todos os resultados são classificados tecnicamente como "exposição", "indício" ou "anomalia estatística de triagem", respeitando o Art. 19-B da Resolução TCU nº 367/2024.

### 3.2 SG-02: Transparência e Explicabilidade dos Sinais
A classificação de risco é acompanhada da decomposição matemática transparente de cada sinal individual ativado ($s_i$, $c_i$, $w_i$), impedindo decisões automatizadas opacas ("caixa preta").

### 3.3 SG-03: Aviso Metodológico Permanente
Todo relatório gerado (PDF) e tela do sistema exibe advertência obrigatória sobre a natureza probabilística dos indicadores e a necessidade de apuração contraditória por auditores humanos competentes.

### 3.4 SG-05 / RF-API-02: Mascaramento Compulsorio de PII em Consulta Pública
Para perfis não autenticados ou de cidadãos (`PUBLICO`), nomes de pessoas físicas são mascarados como `[Pessoa Física Protegida - Acesso Público]` e CPFs como `***.***.***-**`. Apenas auditores e gestores autenticados sob termo de responsabilidade funcional acessam dados de identificação completos.

### 3.5 RF-REL-05: Canal Formal de Contestação e Retificação Cadastral
A plataforma disponibiliza funcionalidade nativa para que qualquer titular ou empresa protocole pedido formal de retificação ou esclarecimento de vínculos societários com geração imediata de número de protocolo auditável.

---

## 4. Medidas de Segurança Técnica da Informação

1. **Criptografia em Trânsito:** Protocolo HTTPS / TLS 1.3 obrigatório para todas as comunicações.
2. **Cadeia de Custódia Forense:** Cálculo imediato de hash SHA-256 no momento da ingestão do payload bruto, com imutabilidade assegurada em banco relacional e buckets MinIO.
3. **Trilha de Auditoria Imutável (RF-API-05):** Registro de data/hora UTC, IP de origem, identificador de usuário e hash de dados requisitados para cada consulta ou exportação.
4. **Controle de Acesso Baseado em Papéis (RBAC):** Segregação estrita entre perfis `ADMIN`, `AUDITOR`, `GESTOR` e `PUBLICO`.

---

## 5. Conclusão e Parecer do Encarregado (DPO)

Diante do interesse público primordial no controle dos gastos públicos, da minimização dos dados coletados, do mascaramento preventivo para visualização pública e da garantia expressa do contraditório e da ampla defesa, conclui-se que o risco aos direitos e liberdades individuais dos titulares é **baixo** e devidamente mitigado pelas salvaguardas técnicas e metodológicas implementadas.
