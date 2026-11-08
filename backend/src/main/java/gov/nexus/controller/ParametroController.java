package gov.nexus.controller;

import gov.nexus.config.SecurityUtils;
import gov.nexus.dto.ParametroVersaoDto;
import gov.nexus.dto.TetoLegalDto;
import gov.nexus.service.AuditoriaService;
import gov.nexus.service.ParametroService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
@Tag(name = "Parâmetros e Tetos Legais", description = "Endpoints de consulta e configuração versionada de parâmetros analíticos e tetos da Lei 14.133/2021")
public class ParametroController {

    private final ParametroService parametroService;
    private final AuditoriaService auditoriaService;
    private final SecurityUtils securityUtils;

    @Data
    public static class CriarParametroRequest {
        private String versao;
        private String descricao;
        private String payloadJson;
    }

    @GetMapping("/parametros/ativo")
    @Operation(summary = "Obter versão ativa dos parâmetros analíticos e pesos do IEA")
    public ResponseEntity<ParametroVersaoDto> getVersaoAtiva() {
        return parametroService.getVersaoAtiva()
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/parametros/{versao}")
    @Operation(summary = "Obter parâmetros analíticos por versão específica")
    public ResponseEntity<ParametroVersaoDto> getPorVersao(@PathVariable String versao) {
        return parametroService.getPorVersao(versao)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/parametros")
    @PreAuthorize("hasRole('ADMIN')")
    @Operation(summary = "Cadastrar nova versão imutável de parâmetros e pesos analíticos (Exclusivo ADMIN)")
    public ResponseEntity<ParametroVersaoDto> cadastrarVersao(
            @RequestBody CriarParametroRequest body, HttpServletRequest request) {

        ParametroVersaoDto criado = parametroService.salvarNovaVersao(
                body.getVersao(),
                body.getDescricao(),
                body.getPayloadJson(),
                securityUtils.getCurrentUserId()
        );

        auditoriaService.registrarLog("ALTERACAO_PARAMETROS", "/api/v1/parametros",
                "versao=" + body.getVersao(), criado.getHashSha256(), request);

        return ResponseEntity.ok(criado);
    }

    @GetMapping("/tetos-legais/vigente")
    @Operation(summary = "Consultar teto legal em vigor para uma modalidade e data de referência")
    public ResponseEntity<TetoLegalDto> consultarTetoVigente(
            @RequestParam String modalidade,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate data) {

        LocalDate dataRef = (data != null) ? data : LocalDate.now();
        return parametroService.consultarTetoVigente(modalidade, dataRef)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/tetos-legais")
    @Operation(summary = "Listar histórico de tetos legais e decretos para uma modalidade")
    public ResponseEntity<List<TetoLegalDto>> listarTetos(@RequestParam String modalidade) {
        return ResponseEntity.ok(parametroService.listarTetos(modalidade));
    }
}
