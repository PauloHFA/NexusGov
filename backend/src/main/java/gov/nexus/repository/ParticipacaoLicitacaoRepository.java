package gov.nexus.repository;

import gov.nexus.domain.ParticipacaoLicitacao;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ParticipacaoLicitacaoRepository extends JpaRepository<ParticipacaoLicitacao, String> {
    List<ParticipacaoLicitacao> findByContratacaoId(String contratacaoId);
    List<ParticipacaoLicitacao> findByFornecedorId(String fornecedorId);
}
