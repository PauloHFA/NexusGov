package gov.nexus.service;

import gov.nexus.domain.Contestacao;
import gov.nexus.domain.Contratacao;
import gov.nexus.domain.Fornecedor;
import gov.nexus.dto.ContestacaoDto;
import gov.nexus.dto.PageResponse;
import gov.nexus.repository.ContestacaoRepository;
import gov.nexus.repository.ContratacaoRepository;
import gov.nexus.repository.FornecedorRepository;
import gov.nexus.security.DigitalSignatureValidator;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ContestacaoService {

    private final ContestacaoRepository contestacaoRepository;
    private final ContratacaoRepository contratacaoRepository;
    private final FornecedorRepository fornecedorRepository;
    private final DigitalSignatureValidator signatureValidator;

    @Transactional
    public ContestacaoDto criarContestacao(ContestacaoDto dto) {
        String protocolo = "NEXUS-" + System.currentTimeMillis();

        // Validação da assinatura digital Gov.br / ICP-Brasil se informada
        DigitalSignatureValidator.SignatureType tipoSig = DigitalSignatureValidator.SignatureType.SEM_ASSINATURA_DIGITAL;
        if (dto.getTipoAssinaturaDigital() != null) {
            try {
                tipoSig = DigitalSignatureValidator.SignatureType.valueOf(dto.getTipoAssinaturaDigital());
            } catch (Exception ignored) {}
        }

        DigitalSignatureValidator.SignatureValidationResult sigResult = signatureValidator.validarAssinatura(
                tipoSig,
                dto.getTokenAssinatura(),
                dto.getMotivoContestacao(),
                dto.getNomeSolicitante()
        );

        Contratacao c = (dto.getContratacaoId() != null)
                ? contratacaoRepository.findById(dto.getContratacaoId()).orElse(null)
                : null;
        Fornecedor f = (dto.getFornecedorId() != null)
                ? fornecedorRepository.findById(dto.getFornecedorId()).orElse(null)
                : null;

        Contestacao entity = Contestacao.builder()
                .id(UUID.randomUUID().toString())
                .numeroProtocolo(protocolo)
                .tipoSolicitante(dto.getTipoSolicitante())
                .documentoIdentificador(dto.getDocumentoIdentificador())
                .nomeSolicitante(dto.getNomeSolicitante())
                .emailContato(dto.getEmailContato())
                .contratacao(c)
                .fornecedor(f)
                .motivoContestacao(dto.getMotivoContestacao())
                .documentosAnexos(dto.getDocumentosAnexos())
                .status(sigResult.isValida() ? "EM_ANALISE_QUALIFICADA" : "EM_ANALISE")
                .criadoEm(OffsetDateTime.now())
                .build();

        Contestacao salvo = contestacaoRepository.save(entity);
        ContestacaoDto ret = toDto(salvo);
        ret.setTipoAssinaturaDigital(sigResult.getTipoAssinatura().name());
        ret.setAssinaturaValida(sigResult.isValida());
        ret.setHashCertificado(sigResult.getHashAssinaturaSha256());
        return ret;
    }

    @Transactional(readOnly = true)
    public Optional<ContestacaoDto> consultarPorProtocolo(String protocolo) {
        return contestacaoRepository.findByNumeroProtocolo(protocolo).map(this::toDto);
    }

    @Transactional(readOnly = true)
    public PageResponse<ContestacaoDto> listarPorStatus(String status, Pageable pageable) {
        Page<Contestacao> page = contestacaoRepository.findByStatus(status, pageable);
        return PageResponse.from(page.map(this::toDto));
    }

    private ContestacaoDto toDto(Contestacao entity) {
        return ContestacaoDto.builder()
                .id(entity.getId())
                .numeroProtocolo(entity.getNumeroProtocolo())
                .tipoSolicitante(entity.getTipoSolicitante())
                .documentoIdentificador(entity.getDocumentoIdentificador())
                .nomeSolicitante(entity.getNomeSolicitante())
                .emailContato(entity.getEmailContato())
                .contratacaoId(entity.getContratacao() != null ? entity.getContratacao().getId() : null)
                .fornecedorId(entity.getFornecedor() != null ? entity.getFornecedor().getId() : null)
                .motivoContestacao(entity.getMotivoContestacao())
                .documentosAnexos(entity.getDocumentosAnexos())
                .status(entity.getStatus())
                .parecerResposta(entity.getParecerResposta())
                .criadoEm(entity.getCriadoEm())
                .respondidoEm(entity.getRespondidoEm())
                .build();
    }
}
