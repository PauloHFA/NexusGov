package gov.nexus.config;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("RF-CFG-03: Perfis de Análise Parametrizáveis")
class AnalysisProfileTest {

    @Test
    @DisplayName("Perfil Conservador deve ignorar homonímia presumida e elevar limiar")
    void testPerfilConservador() {
        AnalysisProfile conservador = AnalysisProfile.CONSERVADOR;
        assertFalse(conservador.isConsiderarHomonimiaPresumida(), "Perfil conservador não considera homonímia presumida (CA-CFG-03)");
        assertEquals(70.0, conservador.getLimiarIeaElevado());
        assertEquals(35.0, conservador.getLimiarIeaMedio());

        // Com apenas 1 eixo ativo, não permite classificação Elevada (SG-04)
        assertFalse(conservador.permiteClassificacaoElevada(1, 75.0));

        // Com 2 eixos ativos e score 72, permite Elevado
        assertTrue(conservador.permiteClassificacaoElevada(2, 72.0));
    }

    @Test
    @DisplayName("Perfil Padrão segue calibração de 60 pontos para Elevado")
    void testPerfilPadrao() {
        AnalysisProfile padrao = AnalysisProfile.PADRAO;
        assertEquals(60.0, padrao.getLimiarIeaElevado());
        assertTrue(padrao.permiteClassificacaoElevada(2, 60.0));
        assertFalse(padrao.permiteClassificacaoElevada(2, 59.9));
    }
}
