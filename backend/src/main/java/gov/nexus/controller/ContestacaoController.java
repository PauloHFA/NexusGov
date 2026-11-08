package gov.nexus.controller;

import gov.nexus.dto.ContestacaoDto;
import gov.nexus.dto.PageResponse;
import gov.nexus.service.AuditoriaService;
import gov.nexus.service.ContestacaoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/contestacoes")
@RequiredArgsConstructor
@Tag(name = "Contestação e Retificação Cadastral", description = "Endpoints de solicitação e consulta de contestações cadastrais (RF-REL-05)")
public class ContestacaoController {

    private final ContestacaoService contestacaoService;
    private final AuditoriaService auditoriaService;

    @PostMapping
    @Operation(summary = "Registrar pedido formal de contestação ou retificação cadastral")
    public ResponseEntity<ContestacaoDto> registrar(@RequestBody ContestacaoDto dto, HttpServletRequest request) {
        ContestacaoDto criado = contestacaoService.criarContestacao(dto);

        auditoriaService.registrarLog("REGISTRO_CONTESTACAO", "/api/v1/contestacoes",
                "protocolo=" + criado.getNumeroProtocolo(), criado.getId(), request);

        return ResponseEntity.ok(criado);
    }

    @GetMapping("/{protocolo}")
    @Operation(summary = "Consultar status de um protocolo de contestação cadastral")
    public ResponseEntity<ContestacaoDto> consultarPorProtocolo(@PathVariable String protocolo) {
        return contestacaoService.consultarPorProtocolo(protocolo)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'AUDITOR')")
    @Operation(summary = "Listar contestações cadastradas por status (Exclusivo ADMIN e AUDITOR)")
    public ResponseEntity<PageResponse<ContestacaoDto>> listarPorStatus(
            @RequestParam(defaultValue = "EM_ANALISE") String status,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {

        Pageable pageable = PageRequest.of(page, size, Sort.by("criadoEm").descending());
        return ResponseEntity.ok(contestacaoService.listarPorStatus(status, pageable));
    }
}
