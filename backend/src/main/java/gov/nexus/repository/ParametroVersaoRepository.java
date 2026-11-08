package gov.nexus.repository;

import gov.nexus.domain.ParametroVersao;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ParametroVersaoRepository extends JpaRepository<ParametroVersao, String> {
    Optional<ParametroVersao> findByVersao(String versao);
    Optional<ParametroVersao> findByAtivoTrue();
}
