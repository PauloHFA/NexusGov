# Requisitos de API REST e Backend (API)

## RF-API-01: Endpoints REST Documentados em OpenAPI 3.1
- **Prioridade:** Must
- **Descrição:** Expor rotas REST padronizadas para consultas de órgãos, fornecedores, contratações, achados, subgrafos e pontuação IEA, com documentação interativa gerada automaticamente em conformidade com OpenAPI 3.1.
- **Critério de Aceite (CA-API-01-A):**
  - **Dado** o backend Spring Boot em execução,
  - **Quando** o endpoint `/v3/api-docs` ou `/swagger-ui.html` for acessado,
  - **Então** todos os schemas, parâmetros de query, cabeçalhos de autenticação e códigos de status HTTP estão especificados.

## RF-API-02: Autenticação OIDC/JWT e Controle de Acesso por Papéis (RBAC)
- **Prioridade:** Must
- **Descrição:** Proteger as rotas via tokens JWT/OIDC com 4 papéis de acesso: `ADMIN`, `AUDITOR`, `GESTOR`, `PUBLICO`.
- **Critério de Aceite (CA-API-01):**
  - **Dado** um usuário não autenticado ou com perfil `PUBLICO`,
  - **Quando** requisita dados de pessoa física identificada ou dados brutos não mascarados,
  - **Então** a API retorna dados agregados/mascarados e registra a tentativa de acesso na trilha de auditoria.

## RF-API-03: Paginação, Filtros e Limitação de Taxa (Rate Limiting)
- **Prioridade:** Must
- **Descrição:** Padronizar respostas de paginação (page, size, sort) e aplicar limite de requisições por IP e perfil de usuário para mitigar sobrecargas ou raspagens abusivas.
- **Critério de Aceite (CA-API-03):**
  - **Dado** uma consulta com centenas de milhares de contratações,
  - **Quando** requisitada sem paginação excessiva,
  - **Então** limita a página ao tamanho máximo de 100 itens e bloqueia requisições em excesso com HTTP 429.

## RF-API-04: Persistência Relacional com Migrações Flyway
- **Prioridade:** Must
- **Descrição:** Persistir entidades principais, achados, evidências, parâmetros e auditoria em banco PostgreSQL 16 com controle estrito de migração de esquema via Flyway.
- **Critério de Aceite (CA-API-04):**
  - **Dado** uma nova instância de banco de dados,
  - **Quando** a aplicação backend inicia,
  - **Então** as migrações SQL são executadas de forma determinística na ordem dos scripts `V1__...`, `V2__...` sem intervenção manual.

## RF-API-05: Trilha de Auditoria Imutável
- **Prioridade:** Must
- **Descrição:** Registrar log estruturado imutável de todas as consultas forenses, downloads de relatórios, exportações de dados e alterações em parâmetros de sistema.
- **Critério de Aceite (CA-API-05):**
  - **Dado** qualquer requisição autenticada de exportação de dossiê ou alteração de pesos,
  - **Quando** a operação for concluída com sucesso ou erro,
  - **Então** um registro com ID do usuário, IP, timestamp UTC, ação executada e hash dos dados solicitados é inserido na tabela `trilha_auditoria`.

## RF-API-06: Endpoints de Saúde e Observabilidade (Liveness/Readiness)
- **Prioridade:** Should
- **Descrição:** Fornecer rotas de monitoramento de saúde `/actuator/health/liveness` e `/actuator/health/readiness` e exposição de métricas no padrão Prometheus.
- **Critério de Aceite (CA-API-06):**
  - **Dado** o contêiner de backend em execução,
  - **Quando** o orquestrador consulta `/actuator/health/readiness`,
  - **Então** confirma conexão com PostgreSQL e RabbitMQ antes de rotear tráfego.
