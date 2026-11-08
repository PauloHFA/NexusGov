# ADR-005: Definição do Escopo Piloto — Estado da Paraíba (PB)

## Status
Aprovado pelo Usuário

## Contexto
O universo nacional de compras públicas no PNCP e a base de CNPJs da Receita Federal abrangem mais de 50 milhões de cadastros empresariais e dezenas de gigabytes de dados colunares. Para validar a arquitetura, calibrar os limiares de sensibilidade estatística e verificar o fluxo forense ponta a ponta com agilidade no desenvolvimento, fez-se necessária a escolha de uma Unidade Federativa (UF) para o escopo piloto inicial.

## Decisão
Adotar o **Estado da Paraíba (UF: PB, código IBGE 25)** como o território piloto oficial do NexusGov:
1. **Abrangência:** A Paraíba engloba 223 municípios, incluindo cidades de grande porte regional (João Pessoa - 2507507, Campina Grande - 2504009), polos do semiárido (Patos, Sousa, Cajazeiras) e municípios de pequeno porte, proporcionando uma diversidade rica de cenários de contratação.
2. **Qualidade dos Dados:** O ecossistema de controle público da Paraíba (com histórico do SAGRES no TCE-PB e ampla adesão ao PNCP conforme a Lei 14.133/2021) oferece massa crítica confiável de dispensas, pregões eletrônicos e atas de registro de preços.
3. **Estratégia de Ingestão Focada:** A ingestão dos dumps da Receita Federal filtrará inicialmente os estabelecimentos domiciliados na PB (UF = 'PB') e fornecedores com certames em órgãos estaduais e municipais paraibanos, viabilizando tempos de processamento e teste de poucos minutos na máquina de desenvolvimento.
4. **Generalização:** O pipeline e a arquitetura permanecem totalmente agnósticos a qualquer UF, permitindo a expansão nacional bastando alterar o filtro de particionamento.

## Consequências
- **Positivas:** Ciclos de feedback ultra-rápidos; dados reais de auditoria prontamente acessíveis; validação empírica de mercados concentrados em municípios menores da PB com modelo nulo.
- **Negativas:** Nenhuma, dado que o design colunar particionado por UF suporta a adição de outras UFs sem refatoração de código.
