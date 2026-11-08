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
public class EvidenciaDto {
    private String id;
    private String hashSha256;
    private String urlFonte;
    private OffsetDateTime coletadoEm;
    private String competenciaBase;
    private String trechoDado;
    private String caminhoStorageRaw;
}
