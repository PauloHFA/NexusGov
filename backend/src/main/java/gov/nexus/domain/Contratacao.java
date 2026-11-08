package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "contratacao")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Contratacao {

    @Id
    @Column(length = 36)
    private String id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "orgao_id", nullable = false)
    private Orgao orgao;

    @Column(name = "numero_controle_pncp", length = 50, nullable = false, unique = true)
    private String numeroControlePncp;

    @Column(name = "codigo_unidade_compradora", length = 30)
    private String codigoUnidadeCompradora;

    @Column(name = "modalidade_nome", length = 100, nullable = false)
    private String modalidadeNome;

    @Column(name = "numero_edital", length = 50)
    private String numeroEdital;

    @Column(name = "ano_compra", nullable = false)
    private Integer anoCompra;

    @Column(columnDefinition = "TEXT")
    private String objeto;

    @Column(name = "valor_total_estimado", precision = 15, scale = 2)
    private BigDecimal valorTotalEstimado;

    @Column(name = "valor_total_homologado", precision = 15, scale = 2)
    private BigDecimal valorTotalHomologado;

    @Column(name = "data_abertura_proposta")
    private OffsetDateTime dataAberturaProposta;

    @Column(name = "data_homologacao")
    private OffsetDateTime dataHomologacao;

    @Column(length = 50)
    private String situacao;

    @Column(name = "url_pncp", length = 255)
    private String urlPncp;

    @Column(length = 2, nullable = false)
    private String uf;

    @Column(name = "municipio_ibge", length = 7)
    private String municipioIbge;

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();

    @OneToMany(mappedBy = "contratacao", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<ItemContratacao> itens = new ArrayList<>();

    @OneToMany(mappedBy = "contratacao", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<ParticipacaoLicitacao> participacoes = new ArrayList<>();

    @OneToMany(mappedBy = "contratacao", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<Achado> achados = new ArrayList<>();

    @OneToMany(mappedBy = "contratacao", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<IeaResultado> ieaResultados = new ArrayList<>();
}
