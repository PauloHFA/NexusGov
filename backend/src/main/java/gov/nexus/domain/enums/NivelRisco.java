package gov.nexus.domain.enums;

import com.fasterxml.jackson.annotation.JsonValue;

public enum NivelRisco {
    BAIXO("Baixo"),
    MEDIO("Médio"),
    ELEVADO("Elevado");

    private final String descricao;

    NivelRisco(String descricao) {
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao() {
        return descricao;
    }

    public static NivelRisco fromScore(double score) {
        if (score >= 60.0) {
            return ELEVADO;
        } else if (score >= 30.0) {
            return MEDIO;
        }
        return BAIXO;
    }

    public static NivelRisco fromString(String valor) {
        if (valor == null) return BAIXO;
        for (NivelRisco n : values()) {
            if (n.name().equalsIgnoreCase(valor) || n.descricao.equalsIgnoreCase(valor)) {
                return n;
            }
        }
        return BAIXO;
    }
}
