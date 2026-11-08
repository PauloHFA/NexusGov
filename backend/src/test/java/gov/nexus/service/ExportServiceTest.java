package gov.nexus.service;

import gov.nexus.domain.Achado;
import gov.nexus.domain.Contratacao;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("RF-REL-02: Exportação em Formatos Abertos (CSV)")
class ExportServiceTest {

    private final ExportService exportService = new ExportService();

    @Test
    @DisplayName("Exportação CSV de contratações deve gerar cabeçalho e dados consistentes")
    void testExportarContratacoesCsv() {
        Contratacao c = new Contratacao();
        c.setId("c_001");
        c.setNumeroControlePncp("08778268000160-1-000001/2024");
        c.setObjeto("Aquisição de Medicamentos");
        c.setValorTotalEstimado(new BigDecimal("150000.00"));
        c.setSituacao("DIVULGADA");

        byte[] csvBytes = exportService.exportarContratacoesCsv(List.of(c));
        String csv = new String(csvBytes, StandardCharsets.UTF_8);

        assertTrue(csv.contains("numero_controle_pncp"));
        assertTrue(csv.contains("08778268000160-1-000001/2024"));
        assertTrue(csv.contains("Aquisição de Medicamentos"));
    }

    @Test
    @DisplayName("Exportação CSV de achados deve incluir metadados e metodologia")
    void testExportarAchadosCsv() {
        Achado a = new Achado();
        a.setId("ach_01");
        a.setEixo("FRACIONAMENTO");
        a.setSinal("SLIDING_WINDOW_EXCEEDED");
        a.setEscore(new BigDecimal("0.8500"));
        a.setConfianca(new BigDecimal("1.0000"));
        a.setDetalhesJson("{\"motivo\": \"Teto excedido\"}");

        byte[] csvBytes = exportService.exportarAchadosCsv(List.of(a));
        String csv = new String(csvBytes, StandardCharsets.UTF_8);

        assertTrue(csv.contains("id,eixo,sinal,escore,confianca,detalhes_json"));
        assertTrue(csv.contains("FRACIONAMENTO"));
        assertTrue(csv.contains("SLIDING_WINDOW_EXCEEDED"));
        assertTrue(csv.contains("0.8500"));
    }
}
