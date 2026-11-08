package gov.nexus.repository;

import gov.nexus.domain.Achado;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AchadoRepository extends JpaRepository<Achado, String> {
    List<Achado> findByContratacaoId(String contratacaoId);
    List<Achado> findByFornecedorId(String fornecedorId);
}
