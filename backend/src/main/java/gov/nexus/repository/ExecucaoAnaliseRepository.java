package gov.nexus.repository;

import gov.nexus.domain.ExecucaoAnalise;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ExecucaoAnaliseRepository extends JpaRepository<ExecucaoAnalise, String> {
    List<ExecucaoAnalise> findByStatus(String status);
}
