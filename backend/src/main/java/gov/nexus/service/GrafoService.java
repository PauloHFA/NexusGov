package gov.nexus.service;

import gov.nexus.config.SecurityUtils;
import gov.nexus.domain.*;
import gov.nexus.dto.CytoscapeGraphDto;
import gov.nexus.dto.CytoscapeGraphDto.EdgeData;
import gov.nexus.dto.CytoscapeGraphDto.EdgeElement;
import gov.nexus.dto.CytoscapeGraphDto.NodeData;
import gov.nexus.dto.CytoscapeGraphDto.NodeElement;
import gov.nexus.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

@Service
@RequiredArgsConstructor
public class GrafoService {

    private final ContratacaoRepository contratacaoRepository;
    private final ParticipacaoLicitacaoRepository participacaoLicitacaoRepository;
    private final VinculoSocietarioRepository vinculoSocietarioRepository;
    private final SecurityUtils securityUtils;

    @Transactional(readOnly = true)
    public CytoscapeGraphDto construirSubgrafoContratacao(String contratacaoId) {
        Optional<Contratacao> contratacaoOpt = contratacaoRepository.findById(contratacaoId);
        if (contratacaoOpt.isEmpty()) {
            return CytoscapeGraphDto.builder().build();
        }

        Contratacao c = contratacaoOpt.get();
        boolean isPublic = securityUtils.isPublicUser();

        List<NodeElement> nodes = new ArrayList<>();
        List<EdgeElement> edges = new ArrayList<>();
        Set<String> addedNodes = new HashSet<>();

        // 1. Nó da Contratação
        String licNodeId = "lic_" + c.getId();
        nodes.add(NodeElement.builder()
                .data(NodeData.builder()
                        .id(licNodeId)
                        .label("Edital: " + (c.getNumeroEdital() != null ? c.getNumeroEdital() : c.getNumeroControlePncp()))
                        .tipo("LICITACAO")
                        .centrality(1.0)
                        .communityId("0")
                        .metadata(Map.of(
                                "valor", c.getValorTotalHomologado() != null ? c.getValorTotalHomologado() : 0,
                                "modalidade", c.getModalidadeNome(),
                                "ano", c.getAnoCompra()
                        ))
                        .build())
                .build());
        addedNodes.add(licNodeId);

        // 2. Nó do Órgão
        if (c.getOrgao() != null) {
            String orgNodeId = "org_" + c.getOrgao().getId();
            if (!addedNodes.contains(orgNodeId)) {
                nodes.add(NodeElement.builder()
                        .data(NodeData.builder()
                                .id(orgNodeId)
                                .label(c.getOrgao().getNomeOrgao())
                                .tipo("ORGAO")
                                .centrality(0.8)
                                .communityId("0")
                                .metadata(Map.of("cnpj", c.getOrgao().getCnpj(), "uf", c.getOrgao().getUf()))
                                .build())
                        .build());
                addedNodes.add(orgNodeId);
            }
            // Aresta Órgão -> Licitação
            edges.add(EdgeElement.builder()
                    .data(EdgeData.builder()
                            .id("e_org_" + c.getId())
                            .source(orgNodeId)
                            .target(licNodeId)
                            .label("COMPRADOR")
                            .linkType("ORGAO_CONTRATANTE")
                            .weight(1.0)
                            .color("#64748b")
                            .build())
                    .build());
        }

        // 3. Fornecedores Participantes
        List<ParticipacaoLicitacao> participacoes = participacaoLicitacaoRepository.findByContratacaoId(c.getId());
        Map<String, List<Fornecedor>> socioParaFornecedores = new HashMap<>();

        for (ParticipacaoLicitacao part : participacoes) {
            Fornecedor f = part.getFornecedor();
            String empNodeId = "emp_" + f.getId();

            if (!addedNodes.contains(empNodeId)) {
                nodes.add(NodeElement.builder()
                        .data(NodeData.builder()
                                .id(empNodeId)
                                .label(f.getRazaoSocial())
                                .tipo("EMPRESA")
                                .centrality(0.5)
                                .communityId("1")
                                .metadata(Map.of("cnpj", f.getCnpj(), "vencedor", part.getVencedor()))
                                .build())
                        .build());
                addedNodes.add(empNodeId);
            }

            // Aresta Fornecedor -> Licitação
            edges.add(EdgeElement.builder()
                    .data(EdgeData.builder()
                            .id("e_part_" + part.getId())
                            .source(empNodeId)
                            .target(licNodeId)
                            .label(Boolean.TRUE.equals(part.getVencedor()) ? "ADJUDICADO" : "PARTICIPANTE")
                            .linkType(Boolean.TRUE.equals(part.getVencedor()) ? "VENCEU" : "PARTICIPOU")
                            .weight(Boolean.TRUE.equals(part.getVencedor()) ? 2.0 : 1.0)
                            .color(Boolean.TRUE.equals(part.getVencedor()) ? "#059669" : "#3b82f6")
                            .build())
                    .build());

            // 4. Vínculos Societários
            List<VinculoSocietario> vinculos = vinculoSocietarioRepository.findByFornecedorId(f.getId());
            for (VinculoSocietario vs : vinculos) {
                Socio s = vs.getSocio();
                String socioKey = s.getId();
                socioParaFornecedores.computeIfAbsent(socioKey, k -> new ArrayList<>()).add(f);

                String socioNodeId = "soc_" + s.getId();
                if (!addedNodes.contains(socioNodeId)) {
                    String nomeExibicao = (isPublic && "PF".equalsIgnoreCase(s.getTipoPessoa()))
                            ? "[Pessoa Física Protegida]"
                            : s.getNomeNormalizado();

                    nodes.add(NodeElement.builder()
                            .data(NodeData.builder()
                                    .id(socioNodeId)
                                    .label(nomeExibicao)
                                    .tipo("SOCIO")
                                    .centrality(0.3)
                                    .communityId("1")
                                    .metadata(Map.of(
                                            "confianca", s.getConfiancaIdentidade(),
                                            "rotulo", s.getRotuloIdentidade()
                                    ))
                                    .build())
                            .build());
                    addedNodes.add(socioNodeId);
                }

                edges.add(EdgeElement.builder()
                        .data(EdgeData.builder()
                                .id("e_vs_" + vs.getId())
                                .source(empNodeId)
                                .target(socioNodeId)
                                .label("QUADRO_SOCIETARIO")
                                .linkType("SOCIEDADE")
                                .weight(s.getConfiancaIdentidade().doubleValue())
                                .confidence(s.getConfiancaIdentidade().doubleValue())
                                .color("#8b5cf6")
                                .build())
                        .build());
            }
        }

        // 5. Arestas Diretas de Vínculo Societário Compartilhado entre Fornecedores (Destacado em Vermelho)
        int linkSeq = 1;
        for (Map.Entry<String, List<Fornecedor>> entry : socioParaFornecedores.entrySet()) {
            List<Fornecedor> fornecedoresComSocio = entry.getValue();
            if (fornecedoresComSocio.size() > 1) {
                for (int i = 0; i < fornecedoresComSocio.size(); i++) {
                    for (int j = i + 1; j < fornecedoresComSocio.size(); j++) {
                        String id1 = "emp_" + fornecedoresComSocio.get(i).getId();
                        String id2 = "emp_" + fornecedoresComSocio.get(j).getId();
                        edges.add(EdgeElement.builder()
                                .data(EdgeData.builder()
                                        .id("e_shared_soc_" + (linkSeq++))
                                        .source(id1)
                                        .target(id2)
                                        .label("SÓCIO COMPARTILHADO")
                                        .linkType("SOCIO_COMPARTILHADO")
                                        .weight(3.0)
                                        .color("#dc2626") // Vermelho destacado
                                        .build())
                                .build());
                    }
                }
            }
        }

        return CytoscapeGraphDto.builder()
                .nodes(nodes)
                .edges(edges)
                .build();
    }
}
