package gov.nexus.controller;

import gov.nexus.copilot.AuditCopilotService;
import gov.nexus.service.AuditoriaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/copilot")
@RequiredArgsConstructor
@Tag(name = "Assistente de Auditoria (Copilot)", description = "Geração de minutas estruturadas de instrução técnica de auditoria com aplicação da SG-01")
public class CopilotController {

    private final AuditCopilotService copilotService;
    private final AuditoriaService auditoriaService;

    @GetMapping("/minuta/{contratacaoId}")
    @Operation(summary = "Gerar minuta preliminar de instrução técnica de fiscalização para a contratação")
    public ResponseEntity<AuditCopilotService.MinutaAuditoriaDto> gerarMinuta(
            @PathVariable String contratacaoId, HttpServletRequest request) {

        AuditCopilotService.MinutaAuditoriaDto minuta = copilotService.gerarMinutaInstrucaoTecnica(contratacaoId);

        auditoriaService.registrarLog("GERACAO_MINUTA_COPILOT", "/api/v1/copilot/minuta/" + contratacaoId,
                "contratacaoId=" + contratacaoId, AuditoriaService.calcularSha256(minuta.getTextoMinutaMarkdown()), request);

        return ResponseEntity.ok(minuta);
    }
}
