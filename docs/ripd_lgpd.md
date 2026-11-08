# Relatório de Impacto à Proteção de Dados Pessoais (RIPD Preliminar)

## 1. Identificação do Projeto
- **Nome:** NexusGov — Plataforma de Auditoria Forense por Grafos e Triagem Estatística de Contratações Públicas
- **Finalidade:** Auditoria de conformidade, transparência e controle social de gastos públicos.
- **Bases Legais (LGPD - Lei 13.709/2018):**
  - Art. 7º, § 3º: O tratamento de dados pessoais cujo acesso é público deve considerar a finalidade, a boa-fé e o interesse público que justificaram sua disponibilização.
  - Art. 23: O tratamento de dados pessoais pelas pessoas jurídicas de direito público deverá ser realizado para o atendimento de sua finalidade pública, na persecução do interesse público.
  - Lei de Acesso à Informação (Lei 12.527/2011) e Nova Lei de Licitações (Lei 14.133/2021).

---

## 2. Dados Tratados e Medidas de Minimização
| Dado Pessoal | Fonte Oficial | Tratamento | Medida de Salvaguarda |
|---|---|---|---|
| Nome do Sócio / Administrador | QSA - Receita Federal | Normalização e resolução em grafos | Exibição de grau de confiança em homonímias; perfil público anonimizado |
| CPF do Sócio | QSA - Receita Federal | Cruzamento para resolução de entidade | Preservação estrita da máscara pública oficial (`***123456**`). Proibição expressa de desmascaramento |
| Endereço do Estabelecimento | RFB (Cadastro de Estabelecimentos) | Georreferenciamento e detecção de endereço comum | Informação cadastral de pessoa jurídica aberta |

---

## 3. Avaliação de Riscos aos Titulares e Mitigações
1. **Risco de Falsos Positivos por Homonímia:**
   - *Risco:* Um cidadão homônimo a outro ser associado indevidamente a empresas concorrentes.
   - *Mitigação:* Confiança fracionada ($c_i < 1.0$), rótulo visual obrigatório de "identidade presumida", limitação ao nível "Médio" (SG-05) e canal de retificação imediata (RF-REL-05).
2. **Risco de Dano Reputacional por Linguagem:**
   - *Risco:* Usuários interpretarem indicadores estatísticos como condenação ou acusação criminal.
   - *Mitigação:* Salvaguarda de linguagem SG-01 (banimento de termos como "fraude" ou "crime", uso restrito de "indício" e "exposição"), banner metodológico compulsório em todas as telas (SG-03).
3. **Acesso Público vs. Restrito:**
   - *Risco:* Exposição indiscriminada de dados de pessoas físicas na internet aberta.
   - *Mitigação:* Perfil `PUBLICO` acessa visões consolidadas e métricas agregadas por município sem identificação nominal de pessoas físicas. Apenas auditores autenticados (`AUDITOR`, `ADMIN`) visualizam a rede nominal com máscara.
