package gov.nexus.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class FornecedorDto {
    private String id;
    private String cnpj;
    private String razaoSocial;
    private String nomeFantasia;
    private String situacaoCadastral;
    private LocalDate dataAbertura;
    private BigDecimal capitalSocial;
    private String porte;
    private String cnaeFiscalPrincipal;
    private String municipioIbge;
    private String uf;
    private List<SocioDto> socios;
}
