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
public class AchadoDto {
    private String id;
    private String eixo;
    private String sinal;
    private BigDecimal escore;
    private BigDecimal confianca;
    private String detalhesJson;
    private OffsetDateTime criadoEm;
    private List<EvidenciaDto> evidencias;
}
