package gov.nexus.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class IeaResultadoDto {
    private String id;
    private String contratacaoId;
    private String versaoParametros;
    private BigDecimal valorIea;
    private String nivelRisco; // Baixo, Médio, Elevado
    private int qtdEixosIndependentes;
    private boolean multiEixoValido;
    private List<DecomposicaoSinalDto> decomposicaoSinais;
    private OffsetDateTime calculadoEm;
    private String avisoMetodologico;
}
