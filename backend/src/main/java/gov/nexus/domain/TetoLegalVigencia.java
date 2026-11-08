package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.OffsetDateTime;

@Entity
@Table(name = "teto_legal_vigencia")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TetoLegalVigencia {

    @Id
    @Column(length = 36)
    private String id;

    @Column(name = "modalidade_objeto", length = 60, nullable = false)
    private String modalidadeObjeto;

    @Column(name = "valor_limite", precision = 15, scale = 2, nullable = false)
    private BigDecimal valorLimite;

    @Column(name = "data_inicio_vigencia", nullable = false)
    private LocalDate dataInicioVigencia;

    @Column(name = "data_fim_vigencia")
    private LocalDate dataFimVigencia;

    @Column(name = "base_legal", columnDefinition = "TEXT", nullable = false)
    private String baseLegal;

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();
}
