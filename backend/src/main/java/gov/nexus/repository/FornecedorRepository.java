package gov.nexus.repository;

import gov.nexus.domain.Fornecedor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface FornecedorRepository extends JpaRepository<Fornecedor, String> {
    Optional<Fornecedor> findByCnpj(String cnpj);
    Page<Fornecedor> findByUf(String uf, Pageable pageable);
}
