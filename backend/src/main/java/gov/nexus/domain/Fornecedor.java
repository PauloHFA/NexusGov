package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.OffsetDateTime;

@Entity
@Table(name = "fornecedor")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Fornecedor {

    @Id
    @Column(length = 36)
    private String id;

    @Column(length = 14, nullable = false, unique = true)
    private String cnpj;

    @Column(name = "razao_social", nullable = false)
    private String razaoSocial;

    @Column(name = "nome_fantasia")
    private String nomeFantasia;

    @Column(name = "situacao_cadastral", length = 50)
    private String situacaoCadastral;

    @Column(name = "data_abertura")
    private LocalDate dataAbertura;

    @Column(name = "capital_social", precision = 15, scale = 2)
    private BigDecimal capitalSocial;

    @Column(length = 50)
    private String porte;

    @Column(name = "cnae_fiscal_principal", length = 10)
    private String cnaeFiscalPrincipal;

    @Column
    private String logradouro;

    @Column(length = 50)
    private String numero;

    @Column(length = 8)
    private String cep;

    @Column(name = "municipio_ibge", length = 7)
    private String municipioIbge;

    @Column(length = 2)
    private String uf;

    @Column(length = 50)
    private String telefone;

    @Column(length = 150)
    private String email;

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();

    @Column(name = "atualizado_em", nullable = false)
    @Builder.Default
    private OffsetDateTime atualizadoEm = OffsetDateTime.now();
}
