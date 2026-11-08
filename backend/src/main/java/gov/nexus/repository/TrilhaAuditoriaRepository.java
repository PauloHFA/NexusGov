package gov.nexus.repository;

import gov.nexus.domain.TrilhaAuditoria;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TrilhaAuditoriaRepository extends JpaRepository<TrilhaAuditoria, String> {
    Page<TrilhaAuditoria> findByPapelUsuario(String papelUsuario, Pageable pageable);
    Page<TrilhaAuditoria> findByAcao(String acao, Pageable pageable);
}
