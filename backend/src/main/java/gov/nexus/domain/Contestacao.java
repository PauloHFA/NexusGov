package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "contestacao")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Contestacao {

    @Id
    @Column(length = 36)
    private String id;

    @Column(name = "numero_protocolo", length = 30, nullable = false, unique = true)
    private String numeroProtocolo;

    @Column(name = "tipo_solicitante", length = 20, nullable = false)
    private String tipoSolicitante; // PESSOA_FISICA, PESSOA_JURIDICA

    @Column(name = "documento_identificador", length = 14, nullable = false)
    private String documentoIdentificador;

    @Column(name = "nome_solicitante", nullable = false)
    private String nomeSolicitante;

    @Column(name = "email_contato", length = 150, nullable = false)
    private String emailContato;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "contratacao_id")
    private Contratacao contratacao;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "fornecedor_id")
    private Fornecedor fornecedor;

    @Column(name = "motivo_contestacao", columnDefinition = "TEXT", nullable = false)
    private String motivoContestacao;

    @Column(name = "documentos_anexos", columnDefinition = "TEXT")
    private String documentosAnexos;

    @Column(length = 30, nullable = false)
    @Builder.Default
    private String status = "EM_ANALISE";

    @Column(name = "parecer_resposta", columnDefinition = "TEXT")
    private String parecerResposta;

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();

    @Column(name = "respondido_em")
    private OffsetDateTime respondidoEm;
}
