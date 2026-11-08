package gov.nexus.security;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Melhoria 4: Validação de Assinaturas Digitais Gov.br e ICP-Brasil")
class DigitalSignatureTest {

    private final DigitalSignatureValidator validator = new DigitalSignatureValidator();

    @Test
    @DisplayName("Deve validar assinatura Gov.br Nível Ouro e emitir recibo criptográfico")
    void testValidarAssinaturaGovBrOuro() {
        DigitalSignatureValidator.SignatureValidationResult res = validator.validarAssinatura(
                DigitalSignatureValidator.SignatureType.GOVBR_OURO,
                "token_oauth2_govbr_mock_sign_valid",
                "Requerimento de retificação de quadro societário",
                "CARLOS ALBERTO SILVA"
        );

        assertTrue(res.isValida());
        assertEquals(DigitalSignatureValidator.SignatureType.GOVBR_OURO, res.getTipoAssinatura());
        assertNotNull(res.getHashAssinaturaSha256());
        assertEquals("CARLOS ALBERTO SILVA", res.getSignatarioNome());
        assertTrue(res.getAutoridadeCertificadora().contains("Gov.br"));
    }

    @Test
    @DisplayName("Deve validar assinatura ICP-Brasil com e-CNPJ")
    void testValidarAssinaturaIcpBrasilEcnpj() {
        DigitalSignatureValidator.SignatureValidationResult res = validator.validarAssinatura(
                DigitalSignatureValidator.SignatureType.ICP_BRASIL_ECNPJ,
                "x509_pkcs7_detached_signature_base64",
                "Esclarecimento técnico sobre preços praticados",
                "EMPRESA CONSTRUTORA EXEMPLO LTDA"
        );

        assertTrue(res.isValida());
        assertEquals(DigitalSignatureValidator.SignatureType.ICP_BRASIL_ECNPJ, res.getTipoAssinatura());
        assertTrue(res.getAutoridadeCertificadora().contains("ICP-Brasil"));
    }

    @Test
    @DisplayName("Deve rejeitar ou marcar inválida submissão sem token de assinatura")
    void testSubmissaoSemAssinatura() {
        DigitalSignatureValidator.SignatureValidationResult res = validator.validarAssinatura(
                DigitalSignatureValidator.SignatureType.SEM_ASSINATURA_DIGITAL,
                null,
                "Texto sem assinatura",
                "ANONIMO"
        );

        assertFalse(res.isValida());
    }
}
