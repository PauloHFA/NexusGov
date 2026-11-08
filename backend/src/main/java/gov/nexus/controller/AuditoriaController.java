package gov.nexus.controller;

import gov.nexus.domain.TrilhaAuditoria;
import gov.nexus.dto.PageResponse;
import gov.nexus.dto.TrilhaAuditoriaDto;
import gov.nexus.repository.TrilhaAuditoriaRepository;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/auditoria")
@RequiredArgsConstructor
@Tag(name = "Trilha de Auditoria Forense", description = "Endpoints de consulta à trilha imutável de logs de acesso e operações (RF-API-05)")
public class AuditoriaController {

    private final TrilhaAuditoriaRepository trilhaAuditoriaRepository;

    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'AUDITOR')")
    @Operation(summary = "Consultar trilha imutável de auditoria (Exclusivo ADMIN e AUDITOR)")
    public ResponseEntity<PageResponse<TrilhaAuditoriaDto>> listarLogs(
            @RequestParam(required = false) String papel,
            @RequestParam(required = false) String acao,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {

        int clampedSize = Math.min(Math.max(1, size), 100);
        Pageable pageable = PageRequest.of(page, clampedSize, Sort.by("criadoEm").descending());

        Page<TrilhaAuditoria> logs;
        if (papel != null && !papel.isBlank()) {
            logs = trilhaAuditoriaRepository.findByPapelUsuario(papel, pageable);
        } else if (acao != null && !acao.isBlank()) {
            logs = trilhaAuditoriaRepository.findByAcao(acao, pageable);
        } else {
            logs = trilhaAuditoriaRepository.findAll(pageable);
        }

        Page<TrilhaAuditoriaDto> dtos = logs.map(l -> TrilhaAuditoriaDto.builder()
                .id(l.getId())
                .usuarioId(l.getUsuarioId())
                .papelUsuario(l.getPapelUsuario())
                .enderecoIp(l.getEnderecoIp())
                .endpoint(l.getEndpoint())
                .acao(l.getAcao())
                .parametrosRequisicao(l.getParametrosRequisicao())
                .hashResultado(l.getHashResultado())
                .criadoEm(l.getCriadoEm())
                .build());

        return ResponseEntity.ok(PageResponse.from(dtos));
    }
}
