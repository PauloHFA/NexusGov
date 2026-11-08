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
public class ParametroVersaoDto {
    private String id;
    private String versao;
    private String descricao;
    private String payloadJson;
    private String hashSha256;
    private Boolean ativo;
    private String criadoPor;
    private OffsetDateTime criadoEm;
}
