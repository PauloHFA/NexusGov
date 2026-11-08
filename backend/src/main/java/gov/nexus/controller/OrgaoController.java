package gov.nexus.controller;

import gov.nexus.dto.OrgaoDto;
import gov.nexus.dto.PageResponse;
import gov.nexus.service.AuditoriaService;
import gov.nexus.service.OrgaoService;
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
@RequestMapping("/api/v1/orgaos")
@RequiredArgsConstructor
@Tag(name = "Órgãos Compradores", description = "Endpoints de consulta a órgãos públicos contratantes")
public class OrgaoController {

    private final OrgaoService orgaoService;
    private final AuditoriaService auditoriaService;

    @GetMapping
    @Operation(summary = "Listar órgãos públicos com filtros e paginação")
    public ResponseEntity<PageResponse<OrgaoDto>> listar(
            @RequestParam(required = false) String uf,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            HttpServletRequest request) {

        int clampedSize = Math.min(Math.max(1, size), 100);
        Pageable pageable = PageRequest.of(page, clampedSize, Sort.by("nomeOrgao").ascending());
        PageResponse<OrgaoDto> resultado = orgaoService.listarPorUf(uf, pageable);

        auditoriaService.registrarLog("CONSULTA_ORGAOS", "/api/v1/orgaos", "uf=" + uf, resultado.toString(), request);

        return ResponseEntity.ok(resultado);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obter dados do órgão pelo identificador")
    public ResponseEntity<OrgaoDto> buscarPorId(@PathVariable String id) {
        return orgaoService.buscarPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/cnpj/{cnpj}")
    @Operation(summary = "Obter dados do órgão pelo CNPJ")
    public ResponseEntity<OrgaoDto> buscarPorCnpj(@PathVariable String cnpj) {
        return orgaoService.buscarPorCnpj(cnpj)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
