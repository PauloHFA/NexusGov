package gov.nexus.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ItemContratacaoDto {
    private String id;
    private Integer numeroItem;
    private String descricao;
    private String codigoCatmatCatser;
    private BigDecimal quantidade;
    private String unidadeMedida;
    private BigDecimal valorUnitarioHomologado;
    private BigDecimal valorTotal;
}
