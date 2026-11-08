package gov.nexus.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.OffsetDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrgaoDto {
    private String id;
    private String cnpj;
    private String nomeOrgao;
    private String esfera;
    private String poder;
    private String uf;
    private String codigoIbgeMunicipio;
    private OffsetDateTime criadoEm;
}
