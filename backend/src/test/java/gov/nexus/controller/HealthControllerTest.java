package gov.nexus.controller;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("RF-API-06: Endpoints de Saúde e Monitoramento")
class HealthControllerTest {

    @Test
    @DisplayName("Endpoint de saúde deve retornar status UP e componentes ativos")
    void testHealthEndpoint() {
        HealthController controller = new HealthController();
        ResponseEntity<HealthController.HealthStatusDto> response = controller.getHealth();

        assertEquals(200, response.getStatusCode().value());
        assertNotNull(response.getBody());
        assertEquals("UP", response.getBody().getStatus());
        assertEquals("PB (Paraíba)", response.getBody().getUfPiloto());
        assertEquals("UP", response.getBody().getComponentes().get("database"));
    }
}
