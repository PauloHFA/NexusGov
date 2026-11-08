package gov.nexus.report;

import gov.nexus.domain.Evidencia;
import gov.nexus.repository.EvidenciaRepository;
import gov.nexus.service.AuditoriaService;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class DossierIntegrityVerifier {

    private final EvidenciaRepository evidenciaRepository;

    @Data
    @Builder
    public static class ResultadoVerificacao {
        private boolean integro;
        private String hashCalculado;
        private String hashEsperado;
        private String mensagem;
        private Evidencia evidenciaCadastrada;
    }

    @Transactional(readOnly = true)
    public ResultadoVerificacao verificarIntegridadePayload(String payloadBruto, String hashEsperado) {
        String hashCalculado = AuditoriaService.calcularSha256(payloadBruto);
        boolean integro = hashCalculado.equalsIgnoreCase(hashEsperado);

        Optional<Evidencia> evidenciaOpt = evidenciaRepository.findByHashSha256(hashCalculado);

        String msg = integro
                ? "Integridade criptográfica confirmada com sucesso. Payload coincide com a evidência custodiada."
                : "Alerta de divergência de integridade: O hash do conteúdo difere do esperado.";

        return ResultadoVerificacao.builder()
                .integro(integro)
                .hashCalculado(hashCalculado)
                .hashEsperado(hashEsperado)
                .mensagem(msg)
                .evidenciaCadastrada(evidenciaOpt.orElse(null))
                .build();
    }
}
