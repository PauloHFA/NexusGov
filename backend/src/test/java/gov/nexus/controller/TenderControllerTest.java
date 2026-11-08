package gov.nexus.controller;

import gov.nexus.config.OpenApiConfig;
import gov.nexus.dto.ContratacaoDetailDto;
import gov.nexus.dto.ContratacaoSummaryDto;
import gov.nexus.dto.IeaResultadoDto;
import gov.nexus.dto.PageResponse;
import gov.nexus.service.AuditoriaService;
import gov.nexus.service.ContratacaoService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("RF-API-01 / RF-API-03: Testes de API REST, Paginação e Limitação de Taxa")
class TenderControllerTest {

    @Mock
    private ContratacaoService contratacaoService;

    @Mock
    private AuditoriaService auditoriaService;

    @InjectMocks
    private ContratacaoController contratacaoController;

    @Test
    @DisplayName("RF-API-03: Paginação deve limitar tamanho máximo de página a 100 itens mesmo se solicitado valor maior")
    void testLimitacaoTamanhoPaginaMaximo100() {
        ArgumentCaptor<Pageable> pageableCaptor = ArgumentCaptor.forClass(Pageable.class);
        PageResponse<ContratacaoSummaryDto> pageVazia = PageResponse.<ContratacaoSummaryDto>builder()
                .content(List.of())
                .page(0)
                .size(100)
                .totalElements(0)
                .totalPages(0)
                .build();

        when(contratacaoService.listar(eq("PB"), eq(2024), eq("org-1"), pageableCaptor.capture()))
                .thenReturn(pageVazia);

        // Solicita size=500 abusivo
        ResponseEntity<PageResponse<ContratacaoSummaryDto>> resposta =
                contratacaoController.listar("PB", 2024, "org-1", 0, 500, "anoCompra", null);

        assertThat(resposta.getStatusCode()).isEqualTo(HttpStatus.OK);
        // Garante que o Pageable repassado foi limitado a 100
        assertThat(pageableCaptor.getValue().getPageSize()).isEqualTo(100);
    }

    @Test
    @DisplayName("RF-API-01: Deve retornar 200 OK com Ficha de Detalhe e aviso metodológico regulamentar")
    void testBuscarDetalhePorIdSucesso() {
        String contratacaoId = "c-123";
        ContratacaoDetailDto detalhe = ContratacaoDetailDto.builder()
                .id(contratacaoId)
                .numeroControlePncp("08778268000160-1-000001/2024")
                .modalidadeNome("Dispensa de Licitação")
                .anoCompra(2024)
                .valorTotalHomologado(new BigDecimal("45000.00"))
                .uf("PB")
                .iea(IeaResultadoDto.builder()
                        .valorIea(new BigDecimal("35.00"))
                        .nivelRisco("Médio")
                        .qtdEixosIndependentes(1)
                        .build())
                .avisoMetodologico(OpenApiConfig.METHODOLOGICAL_NOTICE)
                .build();

        when(contratacaoService.buscarDetalhePorId(contratacaoId)).thenReturn(Optional.of(detalhe));

        ResponseEntity<ContratacaoDetailDto> resposta = contratacaoController.buscarPorId(contratacaoId, null);

        assertThat(resposta.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(resposta.getBody()).isNotNull();
        assertThat(resposta.getBody().getNumeroControlePncp()).isEqualTo("08778268000160-1-000001/2024");
        assertThat(resposta.getBody().getAvisoMetodologico()).contains("Resolução TCU nº 367/2024");
    }

    @Test
    @DisplayName("Deve retornar 404 NOT FOUND para ID inexistente")
    void testBuscarDetalhePorIdInexistente() {
        when(contratacaoService.buscarDetalhePorId("nao-existe")).thenReturn(Optional.empty());

        ResponseEntity<ContratacaoDetailDto> resposta = contratacaoController.buscarPorId("nao-existe", null);

        assertThat(resposta.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }
}
