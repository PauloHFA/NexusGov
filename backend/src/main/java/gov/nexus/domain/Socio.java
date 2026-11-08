package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Entity
@Table(name = "socio")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Socio {

    @Id
    @Column(length = 36)
    private String id;

    @Column(name = "tipo_pessoa", length = 2, nullable = false)
    private String tipoPessoa; // PF ou PJ

    @Column(name = "cpf_cnpj_mascarado", length = 14, nullable = false)
    private String cpfCnpjMascarado;

    @Column(name = "nome_normalizado", nullable = false)
    private String nomeNormalizado;

    @Column(name = "confianca_identidade", precision = 4, scale = 3, nullable = false)
    @Builder.Default
    private BigDecimal confiancaIdentidade = BigDecimal.ONE;

    @Column(name = "rotulo_identidade", length = 50, nullable = false)
    @Builder.Default
    private String rotuloIdentidade = "confirmada";

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();
}
