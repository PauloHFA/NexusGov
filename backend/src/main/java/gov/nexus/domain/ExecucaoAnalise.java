package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "execucao_analise")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ExecucaoAnalise {

    @Id
    @Column(length = 36)
    private String id;

    @Column(name = "tipo_escopo", length = 20, nullable = false)
    private String tipoEscopo; // CONTRATACAO, ORGAO, MUNICIPIO, UF

    @Column(name = "alvo_identificador", length = 50, nullable = false)
    private String alvoIdentificador;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parametro_versao_id", nullable = false)
    private ParametroVersao parametroVersao;

    @Column(length = 30, nullable = false)
    private String status; // INICIADO, PROCESSANDO, CONCLUIDO, ERRO

    @Column(name = "progresso_percentual", nullable = false)
    @Builder.Default
    private Integer progressoPercentual = 0;

    @Column(name = "iniciado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime iniciadoEm = OffsetDateTime.now();

    @Column(name = "finalizado_em")
    private OffsetDateTime finalizadoEm;

    @Column(name = "mensagem_erro", columnDefinition = "TEXT")
    private String mensagemErro;
}
