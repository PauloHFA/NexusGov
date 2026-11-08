package gov.nexus.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TetoLegalDto {
    private String id;
    private String modalidadeObjeto;
    private BigDecimal valorLimite;
    private LocalDate dataInicioVigencia;
    private LocalDate dataFimVigencia;
    private String baseLegal;
}
