package gov.nexus.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ContratacaoSummaryDto {
    private String id;
    private String numeroControlePncp;
    private String orgaoNome;
    private String orgaoCnpj;
    private String modalidadeNome;
    private Integer anoCompra;
    private String objeto;
    private BigDecimal valorTotalHomologado;
    private String uf;
    private String municipioIbge;
    private BigDecimal ieaScore;
    private String nivelRisco; // Baixo, Médio, Elevado
    private OffsetDateTime dataPublicacaoPncp;
}
