package gov.nexus.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import gov.nexus.config.OpenApiConfig;
import gov.nexus.domain.*;
import gov.nexus.dto.*;
import gov.nexus.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class ContratacaoService {

    private final ContratacaoRepository contratacaoRepository;
    private final ItemContratacaoRepository itemContratacaoRepository;
    private final AchadoRepository achadoRepository;
    private final EvidenciaRepository evidenciaRepository;
    private final IeaResultadoRepository ieaResultadoRepository;
    private final OrgaoService orgaoService;
    private final ObjectMapper objectMapper;

    @Transactional(readOnly = true)
    public PageResponse<ContratacaoSummaryDto> listar(String uf, Integer ano, String orgaoId, Pageable pageable) {
        Page<Contratacao> page = contratacaoRepository.findByFiltros(uf, ano, orgaoId, pageable);
        return PageResponse.from(page.map(this::toSummaryDto));
    }

    @Transactional(readOnly = true)
    public Optional<ContratacaoDetailDto> buscarDetalhePorId(String id) {
        return contratacaoRepository.findById(id).map(this::toDetailDto);
    }

    @Transactional(readOnly = true)
    public Optional<ContratacaoDetailDto> buscarPorNumeroPncp(String pncp) {
        return contratacaoRepository.findByNumeroControlePncp(pncp).map(this::toDetailDto);
    }

    private ContratacaoSummaryDto toSummaryDto(Contratacao c) {
        Optional<IeaResultado> ieaOpt = ieaResultadoRepository.findByContratacaoId(c.getId());

        return ContratacaoSummaryDto.builder()
                .id(c.getId())
                .numeroControlePncp(c.getNumeroControlePncp())
                .orgaoNome(c.getOrgao() != null ? c.getOrgao().getNomeOrgao() : null)
                .orgaoCnpj(c.getOrgao() != null ? c.getOrgao().getCnpj() : null)
                .modalidadeNome(c.getModalidadeNome())
                .anoCompra(c.getAnoCompra())
                .objeto(c.getObjeto())
                .valorTotalHomologado(c.getValorTotalHomologado())
                .uf(c.getUf())
                .municipioIbge(c.getMunicipioIbge())
                .ieaScore(ieaOpt.map(IeaResultado::getValorIea).orElse(null))
                .nivelRisco(ieaOpt.map(IeaResultado::getNivelRisco).orElse(null))
                .dataPublicacaoPncp(c.getCriadoEm())
                .build();
    }

    private ContratacaoDetailDto toDetailDto(Contratacao c) {
        List<ItemContratacaoDto> itensDto = itemContratacaoRepository.findByContratacaoId(c.getId()).stream()
                .map(i -> ItemContratacaoDto.builder()
                        .id(i.getId())
                        .numeroItem(i.getNumeroItem())
                        .descricao(i.getDescricao())
                        .codigoCatmatCatser(i.getCodigoCatmatCatser())
                        .quantidade(i.getQuantidade())
                        .unidadeMedida(i.getUnidadeMedida())
                        .valorUnitarioHomologado(i.getValorUnitarioHomologado())
                        .valorTotal(i.getValorTotal())
                        .build())
                .collect(Collectors.toList());

        List<AchadoDto> achadosDto = achadoRepository.findByContratacaoId(c.getId()).stream()
                .map(a -> {
                    List<EvidenciaDto> evidDto = evidenciaRepository.findByAchadoId(a.getId()).stream()
                            .map(e -> EvidenciaDto.builder()
                                    .id(e.getId())
                                    .hashSha256(e.getHashSha256())
                                    .urlFonte(e.getUrlFonte())
                                    .coletadoEm(e.getColetadoEm())
                                    .competenciaBase(e.getCompetenciaBase())
                                    .trechoDado(e.getTrechoDado())
                                    .caminhoStorageRaw(e.getCaminhoStorageRaw())
                                    .build())
                            .collect(Collectors.toList());

                    return AchadoDto.builder()
                            .id(a.getId())
                            .eixo(a.getEixo())
                            .sinal(a.getSinal())
                            .escore(a.getEscore())
                            .confianca(a.getConfianca())
                            .detalhesJson(a.getDetalhesJson())
                            .criadoEm(a.getCriadoEm())
                            .evidencias(evidDto)
                            .build();
                })
                .collect(Collectors.toList());

        IeaResultadoDto ieaDto = ieaResultadoRepository.findByContratacaoId(c.getId())
                .map(this::toIeaDto)
                .orElse(null);

        return ContratacaoDetailDto.builder()
                .id(c.getId())
                .numeroControlePncp(c.getNumeroControlePncp())
                .orgao(orgaoService.toDto(c.getOrgao()))
                .modalidadeNome(c.getModalidadeNome())
                .numeroEdital(c.getNumeroEdital())
                .anoCompra(c.getAnoCompra())
                .objeto(c.getObjeto())
                .valorTotalEstimado(c.getValorTotalEstimado())
                .valorTotalHomologado(c.getValorTotalHomologado())
                .dataAberturaProposta(c.getDataAberturaProposta())
                .dataHomologacao(c.getDataHomologacao())
                .situacao(c.getSituacao())
                .urlPncp(c.getUrlPncp())
                .uf(c.getUf())
                .municipioIbge(c.getMunicipioIbge())
                .itens(itensDto)
                .achados(achadosDto)
                .iea(ieaDto)
                .avisoMetodologico(OpenApiConfig.METHODOLOGICAL_NOTICE)
                .build();
    }

    public IeaResultadoDto toIeaDto(IeaResultado iea) {
        List<DecomposicaoSinalDto> decomposicao = new ArrayList<>();
        if (iea.getDecomposicaoSinais() != null && !iea.getDecomposicaoSinais().isBlank()) {
            try {
                decomposicao = objectMapper.readValue(iea.getDecomposicaoSinais(), new TypeReference<>() {});
            } catch (Exception e) {
                log.warn("Erro ao desserializar decomposição de sinais IEA: {}", e.getMessage());
            }
        }

        return IeaResultadoDto.builder()
                .id(iea.getId())
                .contratacaoId(iea.getContratacao().getId())
                .versaoParametros(iea.getParametroVersao() != null ? iea.getParametroVersao().getVersao() : "v1.0.0")
                .valorIea(iea.getValorIea())
                .nivelRisco(iea.getNivelRisco())
                .qtdEixosIndependentes(iea.getQtdEixosIndependentes())
                .multiEixoValido(iea.getQtdEixosIndependentes() >= 2)
                .decomposicaoSinais(decomposicao)
                .calculadoEm(iea.getCalculadoEm())
                .avisoMetodologico(OpenApiConfig.METHODOLOGICAL_NOTICE)
                .build();
    }
}
