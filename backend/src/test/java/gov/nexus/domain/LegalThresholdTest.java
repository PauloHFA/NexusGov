package gov.nexus.domain;

import gov.nexus.dto.TetoLegalDto;
import gov.nexus.repository.TetoLegalVigenciaRepository;
import gov.nexus.service.ParametroService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("RF-CFG-02 / CA-ANA-04: Testes de Tetos Legais com Vigência Temporal")
class LegalThresholdTest {

    @Mock
    private TetoLegalVigenciaRepository tetoRepository;

    @InjectMocks
    private ParametroService parametroService;

    @Test
    @DisplayName("Deve retornar teto de R$ 50.000,00 para dispensa de compras em 2021 (Lei 14.133 art. 75, II)")
    void testTetoOriginal2021() {
        LocalDate dataRef = LocalDate.of(2021, 6, 15);
        TetoLegalVigencia teto2021 = TetoLegalVigencia.builder()
                .id("teto-14133-orig-disp-compras")
                .modalidadeObjeto("DISPENSA_COMPRAS_SERVICOS")
                .valorLimite(new BigDecimal("50000.00"))
                .dataInicioVigencia(LocalDate.of(2021, 4, 1))
                .dataFimVigencia(LocalDate.of(2021, 12, 31))
                .baseLegal("Lei 14.133/2021 Art. 75, II (valor original)")
                .build();

        when(tetoRepository.findVigenteEm("DISPENSA_COMPRAS_SERVICOS", dataRef))
                .thenReturn(Optional.of(teto2021));

        Optional<TetoLegalDto> resultado = parametroService.consultarTetoVigente("DISPENSA_COMPRAS_SERVICOS", dataRef);

        assertThat(resultado).isPresent();
        assertThat(resultado.get().getValorLimite()).isEqualByComparingTo(new BigDecimal("50000.00"));
        assertThat(resultado.get().getBaseLegal()).contains("Lei 14.133/2021");
    }

    @Test
    @DisplayName("Deve retornar teto de R$ 59.906,02 para dispensa de compras em 2024 (Decreto 11.871/2023)")
    void testTetoAtualizado2024() {
        LocalDate dataRef = LocalDate.of(2024, 5, 10);
        TetoLegalVigencia teto2024 = TetoLegalVigencia.builder()
                .id("teto-dec-11871-disp-compras")
                .modalidadeObjeto("DISPENSA_COMPRAS_SERVICOS")
                .valorLimite(new BigDecimal("59906.02"))
                .dataInicioVigencia(LocalDate.of(2024, 1, 1))
                .dataFimVigencia(null) // Vigência aberta
                .baseLegal("Decreto Federal nº 11.871/2023")
                .build();

        when(tetoRepository.findVigenteEm("DISPENSA_COMPRAS_SERVICOS", dataRef))
                .thenReturn(Optional.of(teto2024));

        Optional<TetoLegalDto> resultado = parametroService.consultarTetoVigente("DISPENSA_COMPRAS_SERVICOS", dataRef);

        assertThat(resultado).isPresent();
        assertThat(resultado.get().getValorLimite()).isEqualByComparingTo(new BigDecimal("59906.02"));
        assertThat(resultado.get().getDataFimVigencia()).isNull();
    }
}
