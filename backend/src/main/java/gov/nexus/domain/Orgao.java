package gov.nexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "orgao")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Orgao {

    @Id
    @Column(length = 36)
    private String id;

    @Column(length = 14, nullable = false, unique = true)
    private String cnpj;

    @Column(name = "nome_orgao", nullable = false)
    private String nomeOrgao;

    @Column(length = 20, nullable = false)
    private String esfera;

    @Column(length = 20, nullable = false)
    private String poder;

    @Column(length = 2, nullable = false)
    private String uf;

    @Column(name = "codigo_ibge_municipio", length = 7)
    private String codigoIbgeMunicipio;

    @Column(name = "criado_em", nullable = false, updatable = false)
    @Builder.Default
    private OffsetDateTime criadoEm = OffsetDateTime.now();
}
