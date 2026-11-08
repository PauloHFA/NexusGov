package gov.nexus.service;

import gov.nexus.config.SecurityUtils;
import gov.nexus.domain.TrilhaAuditoria;
import gov.nexus.repository.TrilhaAuditoriaRepository;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.OffsetDateTime;
import java.util.HexFormat;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuditoriaService {

    private final TrilhaAuditoriaRepository trilhaAuditoriaRepository;
    private final SecurityUtils securityUtils;

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void registrarLog(String acao, String endpoint, String parametros, String resultadoParaHash, HttpServletRequest request) {
        try {
            String ip = "127.0.0.1";
            if (request != null) {
                String fwd = request.getHeader("X-Forwarded-For");
                ip = (fwd != null && !fwd.isBlank()) ? fwd.split(",")[0].trim() : request.getRemoteAddr();
            }

            String hash = null;
            if (resultadoParaHash != null) {
                hash = calcularSha256(resultadoParaHash);
            }

            TrilhaAuditoria registro = TrilhaAuditoria.builder()
                    .id(UUID.randomUUID().toString())
                    .usuarioId(securityUtils.getCurrentUserId())
                    .papelUsuario(securityUtils.getCurrentUserRole())
                    .enderecoIp(ip != null ? ip : "desconhecido")
                    .endpoint(endpoint)
                    .acao(acao)
                    .parametrosRequisicao(parametros)
                    .hashResultado(hash)
                    .criadoEm(OffsetDateTime.now())
                    .build();

            trilhaAuditoriaRepository.save(registro);
        } catch (Exception e) {
            log.error("Erro ao gravar trilha de auditoria para ação {}: {}", acao, e.getMessage());
        }
    }

    public static String calcularSha256(String texto) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(texto.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 não disponível", e);
        }
    }
}
