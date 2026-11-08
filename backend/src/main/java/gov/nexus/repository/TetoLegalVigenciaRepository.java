package gov.nexus.repository;

import gov.nexus.domain.TetoLegalVigencia;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface TetoLegalVigenciaRepository extends JpaRepository<TetoLegalVigencia, String> {

    @Query("SELECT t FROM TetoLegalVigencia t WHERE t.modalidadeObjeto = :modalidade " +
           "AND t.dataInicioVigencia <= :dataReferencia " +
           "AND (t.dataFimVigencia IS NULL OR t.dataFimVigencia >= :dataReferencia) " +
           "ORDER BY t.dataInicioVigencia DESC")
    Optional<TetoLegalVigencia> findVigenteEm(@Param("modalidade") String modalidade,
                                             @Param("dataReferencia") LocalDate dataReferencia);

    List<TetoLegalVigencia> findByModalidadeObjetoOrderByDataInicioVigenciaAsc(String modalidadeObjeto);
}
