package gov.nexus.repository;

import gov.nexus.domain.ItemContratacao;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ItemContratacaoRepository extends JpaRepository<ItemContratacao, String> {
    List<ItemContratacao> findByContratacaoId(String contratacaoId);
}
