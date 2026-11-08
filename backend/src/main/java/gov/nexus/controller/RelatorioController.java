package gov.nexus.controller;

import gov.nexus.report.DossierIntegrityVerifier;
import gov.nexus.report.PdfDossierGenerator;
import gov.nexus.service.AuditoriaService;
import gov.nexus.service.ExportService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Collections;

@RestController
@RequestMapping("/api/v1/relatorios")
@RequiredArgsConstructor
@Tag(name = "Relatórios Forenses e Integridade", description = "Endpoints de geração de dossiês em PDF, exportações CSV e verificação independente de integridade")
public class RelatorioController {

    private final PdfDossierGenerator pdfDossierGenerator;
    private final DossierIntegrityVerifier dossierIntegrityVerifier;
    private final AuditoriaService auditoriaService;
    private final ExportService exportService;

    @Data
    public static class VerificarHashRequest {
        private String payloadBruto;
        private String hashEsperado;
    }

    @GetMapping(value = "/dossie/{contratacaoId}", produces = MediaType.APPLICATION_PDF_VALUE)
    @Operation(summary = "Gerar dossiê técnico forense em PDF para uma contratação pública")
    public ResponseEntity<byte[]> baixarDossie(@PathVariable String contratacaoId, HttpServletRequest request) {
        byte[] pdfBytes = pdfDossierGenerator.gerarDossieContratacao(contratacaoId);

        String pdfHash = AuditoriaService.calcularSha256(new String(pdfBytes));
        auditoriaService.registrarLog("EXPORTACAO_DOSSIE_PDF", "/api/v1/relatorios/dossie/" + contratacaoId,
                "contratacaoId=" + contratacaoId, pdfHash, request);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"dossie_nexusgov_" + contratacaoId + ".pdf\"")
                .contentType(MediaType.APPLICATION_PDF)
                .body(pdfBytes);
    }

    @PostMapping("/verificar")
    @Operation(summary = "Verificar integridade criptográfica SHA-256 de um payload ou evidência forense")
    public ResponseEntity<DossierIntegrityVerifier.ResultadoVerificacao> verificarIntegridade(
            @RequestBody VerificarHashRequest body, HttpServletRequest request) {

        DossierIntegrityVerifier.ResultadoVerificacao resultado =
                dossierIntegrityVerifier.verificarIntegridadePayload(body.getPayloadBruto(), body.getHashEsperado());

        auditoriaService.registrarLog("VERIFICACAO_INTEGRIDADE", "/api/v1/relatorios/verificar",
                "hashEsperado=" + body.getHashEsperado(), resultado.getHashCalculado(), request);

        return ResponseEntity.ok(resultado);
    }

    @GetMapping(value = "/export/csv", produces = "text/csv")
    @Operation(summary = "Exportar contratações públicas em formato CSV aberto (RF-REL-02)")
    public ResponseEntity<byte[]> exportarContratacoesCsv(HttpServletRequest request) {
        byte[] csvData = exportService.exportarContratacoesCsv(Collections.emptyList());

        auditoriaService.registrarLog("EXPORTACAO_CSV", "/api/v1/relatorios/export/csv",
                "formato=csv", AuditoriaService.calcularSha256(new String(csvData)), request);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"contratacoes_nexusgov.csv\"")
                .body(csvData);
    }
}
