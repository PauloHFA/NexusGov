# ADR-001: Fronteira de Comunicação entre Backend Java e Analytics Python

## Status
Aprovado

## Contexto
O NexusGov utiliza Java 21 com Spring Boot 3.4 para o backend corporativo (persistência relacional, autenticação RBAC, geração de PDFs, controle de sessão e API REST) e Python 3.12 para o ecossistema de dados e analytics (DuckDB, Polars, NetworkX, python-igraph, SciPy e scikit-learn).
É imperativo definir como esses dois subsistemas se comunicam de forma desacoplada, resiliente e escalável, sem gargalos síncronos de chamadas HTTP bloqueantes ou acoplamento direto via JNI/execução de subprocessos lentos.

## Decisão
Adotamos uma arquitetura assíncrona orientada a eventos e mensagens apoiada em **RabbitMQ** e persistência compartilhada em **PostgreSQL** e **Parquet**:
1. **Disparo de Análises:** O Backend Java envia comandos de análise via mensageria para o RabbitMQ (ex.: exchange `nexus.analytics.exchange`, routing key `analysis.request`).
2. **Processamento Assíncrono:** Os workers em Python consomem a fila de forma distribuída, processam os dados analíticos (Parquet/DuckDB) e gravam os achados, evidências e escores IEA diretamente nas tabelas transacionais do PostgreSQL (`achado`, `evidencia`, `iea_resultado`).
3. **Notificação de Término:** O worker publica um evento de conclusão (`analysis.completed`) que o backend Java consome para atualizar o status do lote e notificar a interface de usuário (SSE ou polling).
4. **Resiliência:** Filas duráveis com confirmação de entrega (*manual ack*), retentativa exponencial e *Dead-Letter Queue* (DLQ) para mensagens corrompidas ou falhas irrecuperáveis.

## Consequências
- **Positivas:** Desacoplamento total; escalabilidade horizontal independente dos workers Python; isolamento de falhas pesadas de memória no cálculo de grafos; contratos baseados em esquemas JSON bem definidos.
- **Negativas:** Necessidade de gerenciar a infraestrutura do RabbitMQ; eventual consistência exigindo controle explícito de status na API.
