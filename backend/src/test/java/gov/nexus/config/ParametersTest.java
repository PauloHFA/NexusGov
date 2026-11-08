package gov.nexus.config;

import gov.nexus.domain.ParametroVersao;
import gov.nexus.dto.ParametroVersaoDto;
import gov.nexus.repository.ParametroVersaoRepository;
import gov.nexus.repository.TetoLegalVigenciaRepository;
import gov.nexus.service.AuditoriaService;
import gov.nexus.service.ParametroService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("RF-CFG-01: Testes de Versionamento Imutável de Parâmetros e Pesos Analíticos")
class ParametersTest {

    @Mock
    private ParametroVersaoRepository parametroVersaoRepository;

    @Mock
    private TetoLegalVigenciaRepository tetoLegalVigenciaRepository;

    @InjectMocks
    private ParametroService parametroService;

    @Test
    @DisplayName("Deve salvar nova versão calculando hash SHA-256 e desativando versão anterior")
    void testSalvarNovaVersaoComHashSha256() {
        String payloadJson = "{\"weights\": {\"GRAFO\": 0.35, \"BENFORD\": 0.25, \"FRACIONAMENTO\": 0.25, \"POPUP_VENDOR\": 0.15}}";
        String expectedHash = AuditoriaService.calcularSha256(payloadJson);

        ParametroVersao versaoAnterior = ParametroVersao.builder()
                .id("pv-v100")
                .versao("v1.0.0")
                .ativo(true)
                .build();

        when(parametroVersaoRepository.findByAtivoTrue()).thenReturn(Optional.of(versaoAnterior));
        when(parametroVersaoRepository.save(any(ParametroVersao.class))).thenAnswer(i -> i.getArgument(0));

        ParametroVersaoDto novoDto = parametroService.salvarNovaVersao("v1.1.0", "Ajuste de pesos para PB", payloadJson, "admin@nexus.gov");

        assertThat(novoDto).isNotNull();
        assertThat(novoDto.getVersao()).isEqualTo("v1.1.0");
        assertThat(novoDto.getHashSha256()).isEqualTo(expectedHash);
        assertThat(novoDto.getAtivo()).isTrue();

        // Verifica que a versão anterior foi desativada
        assertThat(versaoAnterior.getAtivo()).isFalse();
        verify(parametroVersaoRepository, atLeastOnce()).save(versaoAnterior);
    }
}
