package gov.nexus.repository;

import gov.nexus.domain.Contratacao;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ContratacaoRepository extends JpaRepository<Contratacao, String> {
    Optional<Contratacao> findByNumeroControlePncp(String numeroControlePncp);

    Page<Contratacao> findByUf(String uf, Pageable pageable);

    @Query("SELECT c FROM Contratacao c WHERE (:uf IS NULL OR c.uf = :uf) " +
           "AND (:ano IS NULL OR c.anoCompra = :ano) " +
           "AND (:orgaoId IS NULL OR c.orgao.id = :orgaoId)")
    Page<Contratacao> findByFiltros(@Param("uf") String uf,
                                   @Param("ano") Integer ano,
                                   @Param("orgaoId") String orgaoId,
                                   Pageable pageable);
}
