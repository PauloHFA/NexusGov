package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "evidencia")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Evidencia {

    @Id
    @Column(length = 36)
    private String id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "achado_id", nullable = false)
    private Achado achado;

    @Column(name = "hash_sha256", length = 64, nullable = false)
    private String hashSha256;

    @Column(name = "url_fonte", length = 255, nullable = false)
    private String urlFonte;

    @Column(name = "coletado_em", nullable = false)
    private OffsetDateTime coletadoEm;

    @Column(name = "competencia_base", length = 10, nullable = false)
    private String competenciaBase;

    @Column(name = "trecho_dado", columnDefinition = "TEXT", nullable = false)
    private String trechoDado;

    @Column(name = "caminho_storage_raw", length = 255, nullable = false)
    private String caminhoStorageRaw;
}
