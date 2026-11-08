package gov.nexus.controller;

import gov.nexus.dto.ContratacaoDetailDto;
import gov.nexus.dto.ContratacaoSummaryDto;
import gov.nexus.dto.PageResponse;
import gov.nexus.service.AuditoriaService;
import gov.nexus.service.ContratacaoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/contratacoes")
@RequiredArgsConstructor
@Tag(name = "Contratações Públicas", description = "Endpoints de consulta e detalhamento forense de contratações do PNCP")
public class ContratacaoController {

    private final ContratacaoService contratacaoService;
    private final AuditoriaService auditoriaService;

    @GetMapping
    @Operation(summary = "Listar contratações públicas com filtros e paginação")
    public ResponseEntity<PageResponse<ContratacaoSummaryDto>> listar(
            @RequestParam(required = false) String uf,
            @RequestParam(required = false) Integer ano,
            @RequestParam(required = false) String orgaoId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "anoCompra") String sort,
            HttpServletRequest request) {

        int clampedSize = Math.min(Math.max(1, size), 100);
        Pageable pageable = PageRequest.of(page, clampedSize, Sort.by(Sort.Direction.DESC, sort));
        PageResponse<ContratacaoSummaryDto> resultado = contratacaoService.listar(uf, ano, orgaoId, pageable);

        auditoriaService.registrarLog("CONSULTA_LISTA_CONTRATACOES", "/api/v1/contratacoes",
                "uf=" + uf + "&ano=" + ano, resultado.toString(), request);

        return ResponseEntity.ok(resultado);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obter ficha de detalhe da contratação com decomposição de sinais e IEA")
    public ResponseEntity<ContratacaoDetailDto> buscarPorId(@PathVariable String id, HttpServletRequest request) {
        return contratacaoService.buscarDetalhePorId(id)
                .map(detalhe -> {
                    auditoriaService.registrarLog("CONSULTA_DETALHE_CONTRATACAO", "/api/v1/contratacoes/" + id,
                            "id=" + id, detalhe.getId(), request);
                    return ResponseEntity.ok(detalhe);
                })
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/pncp/{numeroControlePncp}")
    @Operation(summary = "Buscar contratação pelo número de controle oficial do PNCP")
    public ResponseEntity<ContratacaoDetailDto> buscarPorNumeroPncp(
            @PathVariable String numeroControlePncp, HttpServletRequest request) {
        return contratacaoService.buscarPorNumeroPncp(numeroControlePncp)
                .map(detalhe -> {
                    auditoriaService.registrarLog("CONSULTA_PNCP_CONTRATACAO",
                            "/api/v1/contratacoes/pncp/" + numeroControlePncp,
                            "pncp=" + numeroControlePncp, detalhe.getId(), request);
                    return ResponseEntity.ok(detalhe);
                })
                .orElse(ResponseEntity.notFound().build());
    }
}
