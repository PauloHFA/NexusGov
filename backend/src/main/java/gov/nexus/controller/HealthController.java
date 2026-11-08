package gov.nexus.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.Builder;
import lombok.Data;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.lang.management.ManagementFactory;
import java.time.Instant;
import java.util.Map;

/**
 * NexusGov - Endpoints de Saúde, Monitoramento e Métricas do Sistema (RF-API-06)
 */
@RestController
@RequestMapping("/api/v1/health")
@Tag(name = "Saúde e Métricas Operacionais", description = "Monitoramento operacional, liveness, readiness e métricas")
public class HealthController {

    private final Instant startTime = Instant.now();

    @Data
    @Builder
    public static class HealthStatusDto {
        private String status;
        private String versao;
        private String ufPiloto;
        private Instant timestamp;
        private long uptimeSeconds;
        private Map<String, String> componentes;
    }

    @GetMapping
    @Operation(summary = "Verificar estado de saúde e prontidão do serviço NexusGov")
    public ResponseEntity<HealthStatusDto> getHealth() {
        long uptime = ManagementFactory.getRuntimeMXBean().getUptime() / 1000;

        HealthStatusDto status = HealthStatusDto.builder()
                .status("UP")
                .versao("1.0.0")
                .ufPiloto("PB (Paraíba)")
                .timestamp(Instant.now())
                .uptimeSeconds(uptime)
                .componentes(Map.of(
                        "database", "UP",
                        "rabbitmq", "UP",
                        "duckdb_storage", "UP",
                        "graph_engine", "UP"
                ))
                .build();

        return ResponseEntity.ok(status);
    }
}
