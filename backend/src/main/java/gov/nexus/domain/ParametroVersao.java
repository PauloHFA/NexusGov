package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "parametro_versao")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ParametroVersao {

    @Id
    @Column(length = 36)
    private String id;

    @Column(length = 20, nullable = false, unique = true)
    private String versao;

    @Column(columnDefinition = "TEXT")
    private String descricao;

    @Column(name = "payload_json", columnDefinition = "TEXT", nullable = false)
    private String payloadJson;

    @Column(name = "hash_sha256", length = 64, nullable = false)
    private String hashSha256;

    @Column(nullable = false)
    @Builder.Default
    private Boolean ativo = false;

    @Column(name = "criado_por", length = 100, nullable = false)
    private String criadoPor;

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();
}
