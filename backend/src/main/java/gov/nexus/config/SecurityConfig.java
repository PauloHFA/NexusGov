package gov.nexus.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.web.SecurityFilterChain;

import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(AbstractHttpConfigurer::disable)
            .cors(AbstractHttpConfigurer::disable)
            .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                // Documentação e Actuator
                .requestMatchers("/v3/api-docs/**", "/swagger-ui/**", "/swagger-ui.html").permitAll()
                .requestMatchers("/actuator/health/**", "/actuator/info").permitAll()

                // Verificação de autenticidade de relatórios e canal de contestação
                .requestMatchers(HttpMethod.POST, "/api/v1/relatorios/verificar").permitAll()
                .requestMatchers(HttpMethod.POST, "/api/v1/contestacoes").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/v1/contestacoes/{protocolo}").permitAll()

                // Consultas públicas (mascaramento de PII via serviço)
                .requestMatchers(HttpMethod.GET, "/api/v1/contratacoes/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/v1/orgaos/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/v1/fornecedores/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/v1/grafos/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/v1/tetos-legais/**").permitAll()

                // Dossiê em PDF (permitido para auditor, gestor e público com marca d'água)
                .requestMatchers(HttpMethod.GET, "/api/v1/relatorios/dossie/**").permitAll()

                // Gestão de parâmetros e configurações analíticas (exclusivo ADMIN)
                .requestMatchers(HttpMethod.POST, "/api/v1/parametros/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.PUT, "/api/v1/parametros/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.GET, "/api/v1/parametros/**").permitAll()

                // Execução de rotinas analíticas (ADMIN ou AUDITOR)
                .requestMatchers(HttpMethod.POST, "/api/v1/analises/**").hasAnyRole("ADMIN", "AUDITOR")

                // Trilha de auditoria (ADMIN ou AUDITOR)
                .requestMatchers("/api/v1/auditoria/**").hasAnyRole("ADMIN", "AUDITOR")

                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthenticationConverter()))
            );

        return http.build();
    }

    @Bean
    public JwtAuthenticationConverter jwtAuthenticationConverter() {
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(new Converter<Jwt, Collection<GrantedAuthority>>() {
            @Override
            public Collection<GrantedAuthority> convert(Jwt jwt) {
                // Suporte a roles nos claims comuns de OIDC (realm_access.roles, roles ou authorithies)
                List<String> roles = jwt.getClaimAsStringList("roles");
                if (roles == null) {
                    roles = jwt.getClaimAsStringList("authorities");
                }
                if (roles == null) {
                    return Collections.singletonList(new SimpleGrantedAuthority("ROLE_PUBLICO"));
                }
                return roles.stream()
                        .map(r -> r.startsWith("ROLE_") ? r : "ROLE_" + r)
                        .map(SimpleGrantedAuthority::new)
                        .collect(Collectors.toList());
            }
        });
        return converter;
    }
}
