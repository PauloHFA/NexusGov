package gov.nexus.domain.enums;

public enum EixoAnalitico {
    GRAFO("Análise de Redes e Coocorrência"),
    BENFORD("Conformidade Estatística de Benford"),
    FRACIONAMENTO("Fracionamento de Despesa"),
    POPUP_VENDOR("Fornecedor Pop-up / Recém-aberto");

    private final String descricao;

    EixoAnalitico(String descricao) {
        this.descricao = descricao;
    }

    public String getDescricao() {
        return descricao;
    }
}
