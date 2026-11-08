package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Table(name = "item_contratacao")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ItemContratacao {

    @Id
    @Column(length = 36)
    private String id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "contratacao_id", nullable = false)
    private Contratacao contratacao;

    @Column(name = "numero_item", nullable = false)
    private Integer numeroItem;

    @Column(columnDefinition = "TEXT")
    private String descricao;

    @Column(name = "codigo_catmat_catser", length = 20)
    private String codigoCatmatCatser;

    @Column(precision = 12, scale = 3)
    private BigDecimal quantidade;

    @Column(name = "unidade_medida", length = 30)
    private String unidadeMedida;

    @Column(name = "valor_unitario_estimado", precision = 15, scale = 4)
    private BigDecimal valorUnitarioEstimado;

    @Column(name = "valor_unitario_homologado", precision = 15, scale = 4)
    private BigDecimal valorUnitarioHomologado;

    @Column(name = "valor_total", precision = 15, scale = 2)
    private BigDecimal valorTotal;

    @Column(length = 50)
    private String situacao;
}
