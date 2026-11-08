package gov.nexus.controller;

import gov.nexus.dto.FornecedorDto;
import gov.nexus.dto.PageResponse;
import gov.nexus.service.AuditoriaService;
import gov.nexus.service.FornecedorService;
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
@RequestMapping("/api/v1/fornecedores")
@RequiredArgsConstructor
@Tag(name = "Fornecedores e Empresas", description = "Endpoints de consulta a empresas participantes de licitações")
public class FornecedorController {

    private final FornecedorService fornecedorService;
    private final AuditoriaService auditoriaService;

    @GetMapping
    @Operation(summary = "Listar fornecedores com filtros e paginação (com mascaramento LGPD para acesso público)")
    public ResponseEntity<PageResponse<FornecedorDto>> listar(
            @RequestParam(required = false) String uf,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            HttpServletRequest request) {

        int clampedSize = Math.min(Math.max(1, size), 100);
        Pageable pageable = PageRequest.of(page, clampedSize, Sort.by("razaoSocial").ascending());
        PageResponse<FornecedorDto> resultado = fornecedorService.listarPorUf(uf, pageable);

        auditoriaService.registrarLog("CONSULTA_FORNECEDORES", "/api/v1/fornecedores", "uf=" + uf, resultado.toString(), request);

        return ResponseEntity.ok(resultado);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obter ficha de fornecedor com sócios e confiança")
    public ResponseEntity<FornecedorDto> buscarPorId(@PathVariable String id) {
        return fornecedorService.buscarPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/cnpj/{cnpj}")
    @Operation(summary = "Obter dados do fornecedor pelo CNPJ")
    public ResponseEntity<FornecedorDto> buscarPorCnpj(@PathVariable String cnpj) {
        return fornecedorService.buscarPorCnpj(cnpj)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
