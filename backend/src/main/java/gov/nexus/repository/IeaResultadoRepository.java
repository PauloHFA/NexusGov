package gov.nexus.repository;

import gov.nexus.domain.IeaResultado;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface IeaResultadoRepository extends JpaRepository<IeaResultado, String> {
    Optional<IeaResultado> findByContratacaoId(String contratacaoId);
    Page<IeaResultado> findByNivelRisco(String nivelRisco, Pageable pageable);
}
