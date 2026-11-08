# Requisitos Não-Funcionais (RNF)

## RNF-01: Desempenho de Importação de Dumps
- **Categoria:** Desempenho
- **Requisito:** Importação completa do dump da Receita Federal (~80 GB descompactados) em $\le 6\text{ h}$ em servidor de referência (16 vCPU, 64 GB RAM, NVMe). Para o escopo piloto (Paraíba), o tempo de carga dos estabelecimentos da PB deve ser inferior a 15 minutos.

## RNF-02: Tempo de Resposta em Consultas
- **Categoria:** Desempenho
- **Requisito:** Consulta analítica de um órgão médio ($\le 5.000$ contratações/ano) com cálculo do IEA em $\le 60\text{ s}$ na primeira execução e $\le 2\text{ s}$ com dados cacheados.

## RNF-03: Desempenho de Renderização de Grafos
- **Categoria:** Desempenho
- **Requisito:** Renderização interativa de rede com até 2.000 nós e 5.000 arestas em $\le 3\text{ s}$ no navegador cliente (Cytoscape.js).

## RNF-04: Escalabilidade Horizontal e Filas
- **Categoria:** Escalabilidade
- **Requisito:** Workers de analytics e ingestão horizontalmente escaláveis, com fila durável RabbitMQ, confirmação de entrega (*ack*) e *Dead-Letter Queue* (DLQ) para mensagens com falha.

## RNF-05: Disponibilidade do Serviço
- **Categoria:** Disponibilidade
- **Requisito:** Meta de disponibilidade de 99,5% para API e interface Web (excluídas janelas programadas de manutenção).

## RNF-06: Segurança e Boas Práticas
- **Categoria:** Segurança
- **Requisito:** Alinhamento com OWASP ASVS nível 2, comunicação TLS 1.2+, segredos e credenciais via variáveis de ambiente/cofre (fora do repositório) e varredura de vulnerabilidades de dependências (SCA) no pipeline de CI.

## RNF-07: Privacidade e Conformidade LGPD
- **Categoria:** Privacidade
- **Requisito:** Princípio de minimização de dados, máscara nativa de CPFs, perfil `PUBLICO` sem identificação nominal de pessoas físicas, registro explícito de bases legais (Lei 12.527/2011 e 14.133/2021) e elaboração de RIPD.

## RNF-08: Reprodutibilidade Científica
- **Categoria:** Reprodutibilidade
- **Requisito:** Mesma entrada + mesma versão de parâmetros e código $\Rightarrow$ mesma saída exata bit a bit nas métricas estatísticas e no IEA (determinismo absoluto com sementes fixadas).

## RNF-09: Trilha de Auditoria e Retenção
- **Categoria:** Auditabilidade
- **Requisito:** Logs estruturados em formato JSON com correlation ID em cada requisição; trilha de auditoria de consultas analíticas e exportações com política de retenção $\ge 5$ anos.

## RNF-10: Cobertura de Testes e Manutenibilidade
- **Categoria:** Manutenibilidade
- **Requisito:** Cobertura de testes unitários e de integração $\ge 80\%$ no backend Spring Boot e no motor analítico Python; análise estática contínua sem falhas críticas.

## RNF-11: Observabilidade
- **Categoria:** Observabilidade
- **Requisito:** Exposição de métricas para Prometheus, tracing distribuído com OpenTelemetry e dashboards de monitoramento no Grafana para ingestão, filas e APIs.

## RNF-12: Usabilidade e Acessibilidade
- **Categoria:** Usabilidade
- **Requisito:** Interface responsiva em português do Brasil em conformidade com as diretrizes de acessibilidade WCAG 2.1 nível AA.

## RNF-13: Portabilidade e Implantação
- **Categoria:** Portabilidade
- **Requisito:** Execução conteinerizada via Docker Compose para desenvolvimento local e Helm/Kubernetes para ambientes de produção.

## RNF-14: Licenciamento Aberto
- **Categoria:** Licenciamento
- **Requisito:** Código sob licença AGPL-3.0; verificação de compatibilidade de todas as bibliotecas de terceiros; dados públicos preservando atribuições de origem.

## RNF-15: Respeito aos Limites da Fonte de Dados
- **Categoria:** Respeito à Fonte
- **Requisito:** Coleta na API pública do PNCP respeitando estritamente os limites de taxa de requisições, com cache local e escalonamento em horários de menor carga pública.
