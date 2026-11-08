package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Table(name = "participacao_licitacao")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ParticipacaoLicitacao {

    @Id
    @Column(length = 36)
    private String id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "contratacao_id", nullable = false)
    private Contratacao contratacao;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "fornecedor_id", nullable = false)
    private Fornecedor fornecedor;

    @Column(nullable = false)
    @Builder.Default
    private Boolean vencedor = false;

    @Column(name = "valor_proposta", precision = 15, scale = 2)
    private BigDecimal valorProposta;

    @Column
    private Integer classificacao;

    @Column
    @Builder.Default
    private Boolean desclassificado = false;

    @Column(name = "motivo_desclassificacao", columnDefinition = "TEXT")
    private String motivoDesclassificacao;
}
