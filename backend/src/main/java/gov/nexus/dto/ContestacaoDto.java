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
public class ContestacaoDto {
    private String id;
    private String numeroProtocolo;
    private String tipoSolicitante;
    private String documentoIdentificador;
    private String nomeSolicitante;
    private String emailContato;
    private String contratacaoId;
    private String fornecedorId;
    private String motivoContestacao;
    private String documentosAnexos;
    private String status;
    private String parecerResposta;
    private OffsetDateTime criadoEm;
    private OffsetDateTime respondidoEm;
}
