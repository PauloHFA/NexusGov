package gov.nexus.repository;

import gov.nexus.domain.VinculoSocietario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface VinculoSocietarioRepository extends JpaRepository<VinculoSocietario, String> {
    List<VinculoSocietario> findByFornecedorId(String fornecedorId);
    List<VinculoSocietario> findBySocioId(String socioId);
}
