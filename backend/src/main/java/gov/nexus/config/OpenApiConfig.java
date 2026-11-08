package gov.nexus.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    public static final String METHODOLOGICAL_NOTICE = 
        "AVISO METODOLÓGICO REGULAMENTAR (Resolução TCU nº 367/2024, Art. 19-B): " +
        "Este sistema fornece análises probabilísticas e estatísticas com base em registros públicos abertos " +
        "(PNCP, Receita Federal e IBGE). As classificações e pontuações de risco do Índice de Exposição a Anomalias (IEA) " +
        "constituem ferramentas de triagem e direcionamento de esforço analítico, não representando juízo definitivo de culpa, " +
        "imputação de conduta delituosa ou declaração de irregularidade comprovada. A verificação aprofundada cabe aos " +
        "órgãos de controle competentes com observância do contraditório e da ampla defesa.";

    @Bean
    public OpenAPI customOpenAPI() {
        final String securitySchemeName = "BearerAuth";
        return new OpenAPI()
                .info(new Info()
                        .title("NexusGov - API Forense de Contratações Públicas (Piloto PB)")
                        .version("1.0.0")
                        .description("Plataforma aberta e auditável para detecção de anomalias estatísticas em contratações públicas " +
                                "(Lei 14.133/2021). Escopo Piloto: Estado da Paraíba (PB, prefixo IBGE 25).\n\n" +
                                "**Salvaguarda Metodológica (SG-03):**\n" + METHODOLOGICAL_NOTICE)
                        .contact(new Contact()
                                .name("Equipe NexusGov")
                                .url("https://github.com/nexusgov/nexusgov"))
                        .license(new License()
                                .name("GNU Affero General Public License v3.0 (AGPL-3.0)")
                                .url("https://www.gnu.org/licenses/agpl-3.0.html")))
                .addSecurityItem(new SecurityRequirement().addList(securitySchemeName))
                .components(new Components()
                        .addSecuritySchemes(securitySchemeName,
                                new SecurityScheme()
                                        .name(securitySchemeName)
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                                        .description("Token JWT OIDC para controle de acesso por papéis (ADMIN, AUDITOR, GESTOR, PUBLICO)")));
    }
}
