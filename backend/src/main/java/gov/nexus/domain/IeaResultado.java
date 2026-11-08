package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Entity
@Table(name = "iea_resultado", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"contratacao_id", "parametro_versao_id"})
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class IeaResultado {

    @Id
    @Column(length = 36)
    private String id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "contratacao_id", nullable = false)
    private Contratacao contratacao;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parametro_versao_id", nullable = false)
    private ParametroVersao parametroVersao;

    @Column(name = "valor_iea", precision = 5, scale = 2, nullable = false)
    private BigDecimal valorIea;

    @Column(name = "nivel_risco", length = 20, nullable = false)
    private String nivelRisco; // Baixo, Médio, Elevado

    @Column(name = "qtd_eixos_independentes", nullable = false)
    private Integer qtdEixosIndependentes;

    @Column(name = "decomposicao_sinais", columnDefinition = "TEXT", nullable = false)
    private String decomposicaoSinais;

    @Column(name = "calculado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime calculadoEm = OffsetDateTime.now();
}
