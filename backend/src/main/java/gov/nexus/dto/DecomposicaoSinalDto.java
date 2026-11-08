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
public class DecomposicaoSinalDto {
    private String sinal;
    private String eixo;
    private BigDecimal escore;
    private BigDecimal confianca;
    private BigDecimal peso;
    private BigDecimal contribuicaoPonderada;
    private String detalhes;
}
