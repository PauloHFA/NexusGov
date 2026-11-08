package gov.nexus.repository;

import gov.nexus.domain.Socio;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SocioRepository extends JpaRepository<Socio, String> {
    List<Socio> findByNomeNormalizadoContainingIgnoreCase(String nome);
}
