package gov.nexus.controller;

import gov.nexus.dto.CytoscapeGraphDto;
import gov.nexus.service.AuditoriaService;
import gov.nexus.service.GrafoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/grafos")
@RequiredArgsConstructor
@Tag(name = "Grafo Forense Interativo", description = "Endpoints de geração de subgrafos para visualização com Cytoscape.js")
public class GrafoController {

    private final GrafoService grafoService;
    private final AuditoriaService auditoriaService;

    @GetMapping("/{contratacaoId}")
    @Operation(summary = "Obter subgrafo no formato Cytoscape.js para visualização de relacionamentos da contratação")
    public ResponseEntity<CytoscapeGraphDto> obterSubgrafo(@PathVariable String contratacaoId, HttpServletRequest request) {
        CytoscapeGraphDto grafo = grafoService.construirSubgrafoContratacao(contratacaoId);

        auditoriaService.registrarLog("CONSULTA_SUBGRAFO", "/api/v1/grafos/" + contratacaoId,
                "contratacaoId=" + contratacaoId, contratacaoId, request);

        return ResponseEntity.ok(grafo);
    }
}
