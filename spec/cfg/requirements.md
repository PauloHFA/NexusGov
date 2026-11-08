# Requisitos de Configuração e Parâmetros (CFG)

## RF-CFG-01: Configuração Versionada de Pesos e Limiares
- **Prioridade:** Must
- **Descrição:** Manter pesos $w_i$, limiares dos níveis (Baixo, Médio, Elevado) e janelas temporais em configuração persistida e versionada, com registro do autor da mudança e justificativa técnica.
- **Critério de Aceite (CA-CFG-01):**
  - **Dado** uma alteração autorizada nos pesos de cálculo do IEA,
  - **Quando** o novo conjunto é salvo no sistema,
  - **Então** um novo registro de versão imutável é criado (ex.: v1.2), preservando todas as versões anteriores para garantir a reprodutibilidade forense.

## RF-CFG-02: Tabela de Tetos Legais com Vigência Temporal
- **Prioridade:** Must
- **Descrição:** Manter tabela de limites legais de dispensa de licitação e modalidades por tipo de objeto (obras/serviços de engenharia vs. outros serviços/compras) com período explícito de vigência inicial e final, refletindo a Lei 14.133/2021 e decretos anuais de atualização monetária.
- **Critério de Aceite (CA-ANA-04):**
  - **Dado** que o teto legal de dispensa para compras gerais foi atualizado por decreto em uma data $X$,
  - **Quando** contratações realizadas antes e depois de $X$ são analisadas,
  - **Então** cada contratação é comparada estritamente contra o teto vigente no dia de sua homologação, sem modificações manuais no código-fonte.

## RF-CFG-03: Perfis de Análise Parametrizáveis
- **Prioridade:** Should
- **Descrição:** Permitir perfis predefinidos de execução: conservador (pesos estritos para menor taxa de falsos positivos), padrão e exploratório.
- **Critério de Aceite (CA-CFG-03):**
  - **Dado** um usuário com permissão de auditor,
  - **Quando** seleciona o perfil "conservador",
  - **Então** parâmetros como parentesco presumido são completamente ignorados e o limiar para o sinal "Médio" exige convergência mais densa.
