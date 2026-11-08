# ADR-004: Versionamento de Parâmetros e Tetos Legais com Vigência Temporal

## Status
Aprovado

## Contexto
Na auditoria de compras públicas, os tetos para dispensa de licitação (art. 75, I e II da Lei 14.133/2021) não são estáticos: eles são atualizados anualmente por decreto do Poder Executivo federal. Além disso, os pesos estatísticos atribuídos a cada indicador no cálculo do IEA podem ser refinados com o tempo através de calibrações empíricas.
Fixar valores ou datas diretamente no código-fonte tornaria o sistema incapaz de auditar retrospectivamente contratações de anos passados e violaria o princípio da reprodutibilidade forense.

## Decisão
1. **Tabela de Tetos Legais com Intervalo de Vigência:**
   - Criação da tabela `teto_legal_vigencia` no PostgreSQL:
     - `modalidade_tipo` (ex.: OBRAS_SERVICOS_ENGENHARIA, COMPRAS_SERVICOS_GERAIS)
     - `valor_limite` (DECIMAL)
     - `data_inicio_vigencia` (DATE)
     - `data_fim_vigencia` (DATE, anulável para teto atual)
     - `base_normativa` (TEXT - ex.: "Lei 14.133/2021 art. 75, II", "Decreto Federal nº 11.871/2023")
   - Na análise de fracionamento (Eixo 3), o valor de cada contratação é avaliado contra o teto em vigor **na data exata de sua homologação**.
2. **Versionamento Imutável de Parâmetros Analíticos:**
   - Criação da tabela `parametro_versao`:
     - `versao` (VARCHAR - ex.: "v1.0.0")
     - `payload_json` (JSONB com os pesos $w_i$, limiares de Benford e janelas deslizantes)
     - `hash_sha256` (SHA-256 do JSON canônico)
     - `criado_em` (TIMESTAMP UTC)
     - `autor` (VARCHAR)
     - `ativo` (BOOLEAN)
   - Todo achado e IEA registrado faz chave estrangeira obrigatória para a versão de parâmetros utilizada no momento do cálculo.

## Consequências
- **Positivas:** Rastreabilidade temporal impecável; auditoria retrospectiva precisa; capacidade de simular novos pesos sem destruir o histórico já auditado.
- **Negativas:** Requer consultas temporais com intervalos `BETWEEN data_inicio AND COALESCE(data_fim, '9999-12-31')`.
