package gov.nexus.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SocioDto {
    private String id;
    private String tipoPessoa;
    private String cpfCnpjMascarado;
    private String nome;
    private String qualificacao;
    private BigDecimal confiancaIdentidade;
    private String rotuloIdentidade;

    public SocioDto toPublicMasked() {
        if ("PF".equalsIgnoreCase(this.tipoPessoa)) {
            return SocioDto.builder()
                    .id(this.id)
                    .tipoPessoa("PF")
                    .cpfCnpjMascarado("***.***.***-**")
                    .nome("[Pessoa Física Protegida - Acesso Público]")
                    .qualificacao(this.qualificacao)
                    .confiancaIdentidade(this.confiancaIdentidade)
                    .rotuloIdentidade(this.rotuloIdentidade)
                    .build();
        }
        return this;
    }
}
