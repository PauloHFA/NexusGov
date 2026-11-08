package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "trilha_auditoria")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TrilhaAuditoria {

    @Id
    @Column(length = 36)
    private String id;

    @Column(name = "usuario_id", length = 50)
    private String usuarioId;

    @Column(name = "papel_usuario", length = 20, nullable = false)
    private String papelUsuario;

    @Column(name = "endereco_ip", length = 45, nullable = false)
    private String enderecoIp;

    @Column(nullable = false)
    private String endpoint;

    @Column(length = 50, nullable = false)
    private String acao; // CONSULTA, EXPORTACAO_PDF, EXPORTACAO_CSV, ALTERACAO_PARAMETRO

    @Column(name = "parametros_requisicao", columnDefinition = "TEXT")
    private String parametrosRequisicao;

    @Column(name = "hash_resultado", length = 64)
    private String hashResultado;

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();
}
