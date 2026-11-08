package gov.nexus.repository;

import gov.nexus.domain.Orgao;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface OrgaoRepository extends JpaRepository<Orgao, String> {
    Optional<Orgao> findByCnpj(String cnpj);
    Page<Orgao> findByUf(String uf, Pageable pageable);
}
