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

## 🚀 Ambiente de Desenvolvimento

### Pré-requisitos
- Docker & Docker Compose
- Java 21 (JDK)
- Python 3.12+
- Node.js 20+

### Subindo os Serviços Base
```bash
docker compose -f infra/compose/docker-compose.yml up -d
```
Serviços iniciados:
- **PostgreSQL 16** (com `pg_trgm` habilitado) na porta `5432`
- **RabbitMQ 3** (com interface de gerenciamento) na porta `5672` / `15672`
- **MinIO** (S3 compatível para dados analíticos) na porta `9000` / `9001`

---

## 📜 Licença

Distribuído sob a licença **GNU Affero General Public License v3.0 (AGPL-3.0)**. Consulte [LICENSE](LICENSE) para mais informações.
