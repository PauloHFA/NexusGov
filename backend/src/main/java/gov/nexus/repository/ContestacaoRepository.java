package gov.nexus.repository;

import gov.nexus.domain.Contestacao;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ContestacaoRepository extends JpaRepository<Contestacao, String> {
    Optional<Contestacao> findByNumeroProtocolo(String numeroProtocolo);
    Page<Contestacao> findByStatus(String status, Pageable pageable);
}
