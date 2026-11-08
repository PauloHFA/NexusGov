package gov.nexus.repository;

import gov.nexus.domain.Evidencia;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface EvidenciaRepository extends JpaRepository<Evidencia, String> {
    List<Evidencia> findByAchadoId(String achadoId);
    Optional<Evidencia> findByHashSha256(String hashSha256);
}
