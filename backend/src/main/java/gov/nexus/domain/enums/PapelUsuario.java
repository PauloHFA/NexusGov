package gov.nexus.domain.enums;

public enum PapelUsuario {
    ADMIN("Administrador do Sistema"),
    AUDITOR("Auditor de Controle Externo/Interno"),
    GESTOR("Gestor Público e Pesquisador"),
    PUBLICO("Cidadão / Consulta Aberta");

    private final String descricao;

    PapelUsuario(String descricao) {
        this.descricao = descricao;
    }

    public String getDescricao() {
        return descricao;
    }
}
