package gov.nexus.report;

import gov.nexus.domain.Evidencia;
import gov.nexus.repository.EvidenciaRepository;
import gov.nexus.service.AuditoriaService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("RF-REL-04: Testes de Verificação Independente de Autenticidade Forense")
class IntegrityVerificationTest {

    @Mock
    private EvidenciaRepository evidenciaRepository;

    @InjectMocks
    private DossierIntegrityVerifier verifier;

    @Test
    @DisplayName("Deve atestar integridade com sucesso quando o hash SHA-256 coincide com a evidência custodiada")
    void testVerificacaoIntegra() {
        String payload = "{\"edital\": \"001/2024\", \"orgao\": \"Prefeitura Municipal de João Pessoa\", \"valor\": 45000.00}";
        String hashEsperado = AuditoriaService.calcularSha256(payload);

        Evidencia evidencia = Evidencia.builder()
                .id("ev-1")
                .hashSha256(hashEsperado)
                .urlFonte("https://pncp.gov.br/api/v1/contratacoes/123456")
                .competenciaBase("2024-11")
                .build();

        when(evidenciaRepository.findByHashSha256(hashEsperado)).thenReturn(Optional.of(evidencia));

        DossierIntegrityVerifier.ResultadoVerificacao resultado =
                verifier.verificarIntegridadePayload(payload, hashEsperado);

        assertThat(resultado.isIntegro()).isTrue();
        assertThat(resultado.getHashCalculado()).isEqualTo(hashEsperado);
        assertThat(resultado.getEvidenciaCadastrada()).isNotNull();
        assertThat(resultado.getMensagem()).contains("Integridade criptográfica confirmada");
    }

    @Test
    @DisplayName("Deve acusar violação de integridade caso o payload tenha sido alterado em um único caractere")
    void testDeteccaoDeAdulteracao() {
        String payloadOriginal = "{\"edital\": \"001/2024\", \"valor\": 45000.00}";
        String payloadAdulterado = "{\"edital\": \"001/2024\", \"valor\": 45000.01}"; // Modificação de 1 centavo
        String hashEsperado = AuditoriaService.calcularSha256(payloadOriginal);

        DossierIntegrityVerifier.ResultadoVerificacao resultado =
                verifier.verificarIntegridadePayload(payloadAdulterado, hashEsperado);

        assertThat(resultado.isIntegro()).isFalse();
        assertThat(resultado.getHashCalculado()).isNotEqualTo(hashEsperado);
        assertThat(resultado.getMensagem()).contains("Alerta de divergência de integridade");
    }
}
