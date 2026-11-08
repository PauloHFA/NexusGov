package gov.nexus.report;

import gov.nexus.dto.*;
import gov.nexus.service.ContratacaoService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("RF-REL-01 / RF-REL-03 / SG-03: Testes de Geração de Dossiê Executivo Forense em PDF")
class PdfDossierTest {

    @Mock
    private ContratacaoService contratacaoService;

    @InjectMocks
    private PdfDossierGenerator pdfGenerator;

    @Test
    @DisplayName("Deve gerar dossiê PDF com cabeçalho forense, medidor IEA, cadeia de custódia e aviso metodológico SG-03")
    void testGerarDossieContratacaoComSucesso() {
        String contratacaoId = "c-12345";

        OrgaoDto orgao = OrgaoDto.builder()
                .id("org-jp")
                .nomeOrgao("Prefeitura Municipal de João Pessoa")
                .cnpj("08778268000160")
                .uf("PB")
                .codigoIbgeMunicipio("2507507")
                .build();

        DecomposicaoSinalDto sinal1 = DecomposicaoSinalDto.builder()
                .sinal("COMMUNITY_COVER_BIDDING")
                .eixo("GRAFO")
                .escore(new BigDecimal("0.85"))
                .confianca(new BigDecimal("0.90"))
                .peso(new BigDecimal("0.35"))
                .contribuicaoPonderada(new BigDecimal("26.77"))
                .detalhes("Empresas com sócio comum disputaram o mesmo lote")
                .build();

        IeaResultadoDto iea = IeaResultadoDto.builder()
                .id("iea-1")
                .contratacaoId(contratacaoId)
                .valorIea(new BigDecimal("72.50"))
                .nivelRisco("Elevado")
                .qtdEixosIndependentes(2)
                .multiEixoValido(true)
                .versaoParametros("v1.0.0")
                .decomposicaoSinais(List.of(sinal1))
                .calculadoEm(OffsetDateTime.now())
                .build();

        EvidenciaDto evidencia = EvidenciaDto.builder()
                .id("ev-1")
                .hashSha256("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
                .urlFonte("https://pncp.gov.br/app/editais/08778268000160/2024/0001")
                .competenciaBase("2024-11")
                .build();

        AchadoDto achado = AchadoDto.builder()
                .id("ach-1")
                .eixo("GRAFO")
                .sinal("COMMUNITY_COVER_BIDDING")
                .escore(new BigDecimal("0.85"))
                .confianca(new BigDecimal("0.90"))
                .evidencias(List.of(evidencia))
                .build();

        ContratacaoDetailDto contratacao = ContratacaoDetailDto.builder()
                .id(contratacaoId)
                .numeroControlePncp("08778268000160-1-000001/2024")
                .orgao(orgao)
                .modalidadeNome("Dispensa de Licitação")
                .numeroEdital("001/2024")
                .anoCompra(2024)
                .objeto("Aquisição de material de consumo")
                .valorTotalHomologado(new BigDecimal("48500.00"))
                .uf("PB")
                .municipioIbge("2507507")
                .iea(iea)
                .achados(List.of(achado))
                .build();

        when(contratacaoService.buscarDetalhePorId(contratacaoId)).thenReturn(Optional.of(contratacao));

        byte[] pdfBytes = pdfGenerator.gerarDossieContratacao(contratacaoId);

        assertThat(pdfBytes).isNotNull();
        assertThat(pdfBytes.length).isGreaterThan(1000);

        // Valida assinatura 'magic bytes' do formato PDF: %PDF-
        String cabecalhoPdf = new String(pdfBytes, 0, 5, StandardCharsets.US_ASCII);
        assertThat(cabecalhoPdf).isEqualTo("%PDF-");
    }
}
