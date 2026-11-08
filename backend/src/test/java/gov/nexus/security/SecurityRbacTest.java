package gov.nexus.security;

import gov.nexus.config.SecurityUtils;
import gov.nexus.domain.Fornecedor;
import gov.nexus.domain.Socio;
import gov.nexus.domain.VinculoSocietario;
import gov.nexus.dto.FornecedorDto;
import gov.nexus.dto.SocioDto;
import gov.nexus.repository.FornecedorRepository;
import gov.nexus.repository.VinculoSocietarioRepository;
import gov.nexus.service.FornecedorService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("RF-API-02 / CA-API-01: Testes de Controle de Acesso por Papéis (RBAC) e Mascaramento de PII")
class SecurityRbacTest {

    @Mock
    private FornecedorRepository fornecedorRepository;

    @Mock
    private VinculoSocietarioRepository vinculoSocietarioRepository;

    @Mock
    private SecurityUtils securityUtils;

    @InjectMocks
    private FornecedorService fornecedorService;

    @Test
    @DisplayName("Perfil PUBLICO deve receber sócios Pessoa Física devidamente mascarados (LGPD)")
    void testAcessoPublicoComMascaramento() {
        String fornecedorId = "forn-pb-1";
        Fornecedor fornecedor = Fornecedor.builder()
                .id(fornecedorId)
                .cnpj("12345678000199")
                .razaoSocial("Empresa Alfa LTDA")
                .uf("PB")
                .build();

        Socio socioPf = Socio.builder()
                .id("soc-1")
                .tipoPessoa("PF")
                .cpfCnpjMascarado("***.123.456-**")
                .nomeNormalizado("JOSE CARLOS DA SILVA")
                .confiancaIdentidade(new BigDecimal("0.950"))
                .rotuloIdentidade("confirmada")
                .build();

        VinculoSocietario vinculo = VinculoSocietario.builder()
                .id("vin-1")
                .fornecedor(fornecedor)
                .socio(socioPf)
                .qualificacao("Sócio-Administrador")
                .build();

        when(fornecedorRepository.findById(fornecedorId)).thenReturn(Optional.of(fornecedor));
        when(vinculoSocietarioRepository.findByFornecedorId(fornecedorId)).thenReturn(List.of(vinculo));
        when(securityUtils.isPublicUser()).thenReturn(true); // Usuário público

        Optional<FornecedorDto> resultado = fornecedorService.buscarPorId(fornecedorId);

        assertThat(resultado).isPresent();
        assertThat(resultado.get().getSocios()).hasSize(1);

        SocioDto socioRetornado = resultado.get().getSocios().get(0);
        assertThat(socioRetornado.getNome()).isEqualTo("[Pessoa Física Protegida - Acesso Público]");
        assertThat(socioRetornado.getCpfCnpjMascarado()).isEqualTo("***.***.***-**");
    }

    @Test
    @DisplayName("Perfil AUDITOR/ADMIN deve receber nomes de sócios e dados cadastrais sem restrição")
    void testAcessoAuditorSemMascaramento() {
        String fornecedorId = "forn-pb-1";
        Fornecedor fornecedor = Fornecedor.builder()
                .id(fornecedorId)
                .cnpj("12345678000199")
                .razaoSocial("Empresa Alfa LTDA")
                .uf("PB")
                .build();

        Socio socioPf = Socio.builder()
                .id("soc-1")
                .tipoPessoa("PF")
                .cpfCnpjMascarado("***.123.456-**")
                .nomeNormalizado("JOSE CARLOS DA SILVA")
                .confiancaIdentidade(new BigDecimal("0.950"))
                .rotuloIdentidade("confirmada")
                .build();

        VinculoSocietario vinculo = VinculoSocietario.builder()
                .id("vin-1")
                .fornecedor(fornecedor)
                .socio(socioPf)
                .qualificacao("Sócio-Administrador")
                .build();

        when(fornecedorRepository.findById(fornecedorId)).thenReturn(Optional.of(fornecedor));
        when(vinculoSocietarioRepository.findByFornecedorId(fornecedorId)).thenReturn(List.of(vinculo));
        when(securityUtils.isPublicUser()).thenReturn(false); // Auditor / Admin autenticado

        Optional<FornecedorDto> resultado = fornecedorService.buscarPorId(fornecedorId);

        assertThat(resultado).isPresent();
        SocioDto socioRetornado = resultado.get().getSocios().get(0);
        assertThat(socioRetornado.getNome()).isEqualTo("JOSE CARLOS DA SILVA");
        assertThat(socioRetornado.getCpfCnpjMascarado()).isEqualTo("***.123.456-**");
    }
}
