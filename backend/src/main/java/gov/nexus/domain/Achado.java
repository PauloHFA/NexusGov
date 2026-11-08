package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "achado")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Achado {

    @Id
    @Column(length = 36)
    private String id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "execucao_id", nullable = false)
    private ExecucaoAnalise execucao;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "contratacao_id")
    private Contratacao contratacao;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "fornecedor_id")
    private Fornecedor fornecedor;

    @Column(length = 30, nullable = false)
    private String eixo; // GRAFO, BENFORD, FRACIONAMENTO, POPUP_VENDOR

    @Column(length = 50, nullable = false)
    private String sinal;

    @Column(precision = 5, scale = 4, nullable = false)
    private BigDecimal escore;

    @Column(precision = 5, scale = 4, nullable = false)
    private BigDecimal confianca;

    @Column(name = "detalhes_json", columnDefinition = "TEXT", nullable = false)
    private String detalhesJson;

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();

    @OneToMany(mappedBy = "achado", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<Evidencia> evidencias = new ArrayList<>();
}
