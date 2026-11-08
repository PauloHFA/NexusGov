# NexusGov

> **Plataforma de Auditoria Forense por Grafos e Triagem Estatística de Contratações Públicas**

NexusGov é uma infraestrutura aberta e auditável desenvolvida sob a metodologia **Spec-Driven Development (SDD)**. O sistema cruza dados abertos do **Portal Nacional de Contratações Públicas (PNCP)**, da base cadastral pública de **CNPJs da Receita Federal** e do **IBGE** para triar indícios de:
- **Concorrência Fictícia / Cartéis (*Cover Bidding*)**: Grafos heterogêneos de empresas, sócios e certames com projeção de coocorrência, detecção de comunidades (Leiden/Louvain) e modelo de controle nulo.
- **Anomalias de Preço e Dígitos**: Aplicação da Lei de Benford (MAD de Nigrini, Kolmogorov-Smirnov sobre a mantissa contínua e Benjamini-Hochberg).
- **Fracionamento de Despesa**: Detecção em janelas deslizantes (30, 60 e 90 dias) para compras sucessivas do mesmo objeto/fornecedor próximas ao teto da Lei 14.133/2021.
- **Empresas Recém-Criadas (*Pop-up Vendors*)**: Triagem de novas empresas vencedoras de certames vultosos com capital social incompatível.

---

## ⚖️ Salvaguardas Metodológicas e Éticas (Invioláveis)

O NexusGov produz **indícios estatísticos de triagem e priorização para auditores humanos**, nunca acusação ou juízo de mérito:
1. **Linguagem Controlada (SG-01)**: Nenhuma interface, relatório ou endpoint utiliza termos como "fraude", "crime", "culpado" ou "conluio comprovado". Utilizam-se estritamente **"indício"**, **"exposição"** e **"sinal"**.
2. **Exposição de Evidências (SG-02)**: Todo índice de risco exibe a decomposição dos sinais e os links oficiais rastreáveis.
3. **Aviso Metodológico Obrigatório (SG-03)**: Relatórios e interfaces possuem aviso metodológico explícito e identificação da versão dos parâmetros.
4. **Exigência Multieixo (SG-04)**: O nível de risco "Elevado" (> 60) exige no mínimo dois sinais independentes de eixos analíticos distintos.
5. **Mitigação de Homonímia (SG-05)**: Vínculos por nomes comuns ou parentesco presumido possuem confiança rebaixada e nunca elevam o índice acima de "Médio".
6. **Conformidade LGPD**: Preservação da máscara oficial de CPFs da Receita Federal. O perfil `PUBLICO` visualiza dados agregados sem identificação de pessoas físicas.

---

## 🏗️ Arquitetura do Sistema

```
NexusGov/
├── backend/     # Java 21, Spring Boot 3.4, Spring Security (OIDC/JWT), Flyway, OpenPDF
├── ingestion/   # Python 3.12, DuckDB, httpx, tenacity, PyArrow (PNCP, Receita, IBGE)
├── analytics/   # Python 3.12, Polars, NetworkX, python-igraph (Leiden), SciPy, scikit-learn
├── frontend/    # React 18, TypeScript, Vite, Tailwind CSS, Cytoscape.js
├── spec/        # Matriz de rastreabilidade e especificações de requisitos SDD
├── infra/       # Docker Compose, Helm, CI/CD
└── docs/        # Metodologia matemática, RIPD (LGPD) e ADRs
```

---

## 🚀 Ambiente de Desenvolvimento e Execução

### Status do Projeto
- **Especificações SDD:** 50 / 50 Requisitos Concluídos (100%)
- **Testes Automatizados:** 69 testes aprovados (44 Python + 16 Java + 9 React)
- **Piloto Regional Homologado:** Estado da Paraíba (UF: PB - IBGE 25)
- **Validação Científica:** Precision $\ge 86\%$, Recall $\ge 87\%$, Inversão por sensibilidade de pesos de apenas 2.0%

### Execução Completa via Docker Compose
Para iniciar toda a infraestrutura (PostgreSQL 16, RabbitMQ, MinIO, Backend Spring Boot 3.4 e Frontend Nginx):
```bash
docker compose -f infra/compose/docker-compose.yml up --build -d
```
Acessos:
- **Frontend SPA & Cytoscape:** [http://localhost](http://localhost)
- **Swagger / OpenAPI 3.1:** [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html)
- **Health Check & Métricas:** [http://localhost:8080/api/v1/health](http://localhost:8080/api/v1/health)
- **RabbitMQ Dashboard:** [http://localhost:15672](http://localhost:15672) (usuário: `nexus`, senha: `nexus_rabbit_password`)
- **MinIO Console:** [http://localhost:9001](http://localhost:9001)

### Execução dos Testes Locais
```bash
# 1. Testes de Estatística, Grafos e Ingestão (Python 3.12)
pytest

# 2. Pipeline E2E do Piloto da Paraíba
python scripts/run_pb_pilot_e2e.py

# 3. Testes do Backend REST e Dossiês Forenses (Java 21)
cd backend && mvn test

# 4. Testes do Frontend (React / Vitest)
cd frontend && npm test
```

---

## 📜 Licença

Distribuído sob a licença **GNU Affero General Public License v3.0 (AGPL-3.0)**. Consulte [LICENSE](LICENSE) para mais informações.
