-- Inicialização do Banco NexusGov
-- Habilitação da extensão de similaridade textual (trigramas)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Comentário explicativo
COMMENT ON EXTENSION pg_trgm IS 'Extensão para comparação difusa de nomes empresariais e endereços no NexusGov';
