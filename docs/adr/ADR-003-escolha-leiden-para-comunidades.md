# ADR-003: Adoção do Algoritmo de Leiden para Detecção de Comunidades

## Status
Aprovado

## Contexto
O Eixo 1 da metodologia analítica (RF-ANA-02) exige a identificação de comunidades e grupos coligados de fornecedores em redes de contratação pública. O SRS v1.0 menciona a possibilidade de uso do algoritmo de Louvain ou do algoritmo de Leiden.

O algoritmo clássico de Louvain possui um defeito matemático amplamente demonstrado na literatura (Traag, Waltman, van Eck, 2019): ele tende a produzir comunidades desconexas internamente (subgrafos fragmentados agrupados sob o mesmo rótulo de comunidade) e apresenta forte instabilidade se a ordem de iteração variar.

## Decisão
Adotar o **Algoritmo de Leiden** como padrão analítico do NexusGov, implementado via `python-igraph`:
1. **Conectividade Garantida:** O Leiden garante que todas as comunidades encontradas são subgrafos conectados, eliminando agrupamentos fictícios entre empresas que não possuem caminho real de ligação.
2. **Determinismo Estrito:** Fixação obrigatória de semente pseudoaleatória (*random seed*) em todas as execuções, garantindo que o reprocessamento com os mesmos dados produza exatamente a mesma partição bit a bit (respeitando RNF-08 e CA-ANA-05).
3. **Desempenho:** A implementação em C do `python-igraph` oferece tempo de execução compatível ou superior ao Louvain puro, processando dezenas de milhares de vértices em poucos segundos.

## Consequências
- **Positivas:** Rigor matemático e científico; eliminação de comunidades desconectadas; estabilidade e reprodutibilidade forense.
- **Negativas:** Dependência da biblioteca binária de `igraph` no contêiner analítico.
