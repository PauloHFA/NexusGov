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
public class ContratacaoDetailDto {
    private String id;
    private String numeroControlePncp;
    private OrgaoDto orgao;
    private String modalidadeNome;
    private String numeroEdital;
    private Integer anoCompra;
    private String objeto;
    private BigDecimal valorTotalEstimado;
    private BigDecimal valorTotalHomologado;
    private OffsetDateTime dataAberturaProposta;
    private OffsetDateTime dataHomologacao;
    private String situacao;
    private String urlPncp;
    private String uf;
    private String municipioIbge;
    private IeaResultadoDto iea;
    private List<ItemContratacaoDto> itens;
    private List<AchadoDto> achados;
    private String avisoMetodologico;
}
