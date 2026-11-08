package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.OffsetDateTime;

@Entity
@Table(name = "vinculo_societario", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"fornecedor_id", "socio_id"})
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class VinculoSocietario {

    @Id
    @Column(length = 36)
    private String id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "fornecedor_id", nullable = false)
    private Fornecedor fornecedor;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "socio_id", nullable = false)
    private Socio socio;

    @Column(length = 100)
    private String qualificacao;

    @Column(name = "data_entrada")
    private LocalDate dataEntrada;

    @Column(name = "percentual_capital", precision = 5, scale = 2)
    private BigDecimal percentualCapital;

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();
}
