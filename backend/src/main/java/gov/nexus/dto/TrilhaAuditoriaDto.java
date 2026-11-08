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
public class TrilhaAuditoriaDto {
    private String id;
    private String usuarioId;
    private String papelUsuario;
    private String enderecoIp;
    private String endpoint;
    private String acao;
    private String parametrosRequisicao;
    private String hashResultado;
    private OffsetDateTime criadoEm;
}
