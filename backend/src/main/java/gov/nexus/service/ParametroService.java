package gov.nexus.service;

import gov.nexus.domain.ParametroVersao;
import gov.nexus.domain.TetoLegalVigencia;
import gov.nexus.dto.ParametroVersaoDto;
import gov.nexus.dto.TetoLegalDto;
import gov.nexus.repository.ParametroVersaoRepository;
import gov.nexus.repository.TetoLegalVigenciaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ParametroService {

    private final ParametroVersaoRepository parametroVersaoRepository;
    private final TetoLegalVigenciaRepository tetoLegalVigenciaRepository;

    @Transactional(readOnly = true)
    public Optional<ParametroVersaoDto> getVersaoAtiva() {
        return parametroVersaoRepository.findByAtivoTrue()
                .map(this::toDto);
    }

    @Transactional(readOnly = true)
    public Optional<ParametroVersaoDto> getPorVersao(String versao) {
        return parametroVersaoRepository.findByVersao(versao)
                .map(this::toDto);
    }

    @Transactional
    public ParametroVersaoDto salvarNovaVersao(String versao, String descricao, String payloadJson, String usuario) {
        String hash = AuditoriaService.calcularSha256(payloadJson);

        ParametroVersao novo = ParametroVersao.builder()
                .id(UUID.randomUUID().toString())
                .versao(versao)
                .descricao(descricao)
                .payloadJson(payloadJson)
                .hashSha256(hash)
                .ativo(true)
                .criadoPor(usuario)
                .build();

        // Desativa a versão anterior se houver
        parametroVersaoRepository.findByAtivoTrue().ifPresent(anterior -> {
            anterior.setAtivo(false);
            parametroVersaoRepository.save(anterior);
        });

        ParametroVersao salvo = parametroVersaoRepository.save(novo);
        return toDto(salvo);
    }

    @Transactional(readOnly = true)
    public Optional<TetoLegalDto> consultarTetoVigente(String modalidade, LocalDate dataReferencia) {
        return tetoLegalVigenciaRepository.findVigenteEm(modalidade, dataReferencia)
                .map(this::toDto);
    }

    @Transactional(readOnly = true)
    public List<TetoLegalDto> listarTetos(String modalidade) {
        return tetoLegalVigenciaRepository.findByModalidadeObjetoOrderByDataInicioVigenciaAsc(modalidade)
                .stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    private ParametroVersaoDto toDto(ParametroVersao entity) {
        return ParametroVersaoDto.builder()
                .id(entity.getId())
                .versao(entity.getVersao())
                .descricao(entity.getDescricao())
                .payloadJson(entity.getPayloadJson())
                .hashSha256(entity.getHashSha256())
                .ativo(entity.getAtivo())
                .criadoPor(entity.getCriadoPor())
                .criadoEm(entity.getCriadoEm())
                .build();
    }

    private TetoLegalDto toDto(TetoLegalVigencia entity) {
        return TetoLegalDto.builder()
                .id(entity.getId())
                .modalidadeObjeto(entity.getModalidadeObjeto())
                .valorLimite(entity.getValorLimite())
                .dataInicioVigencia(entity.getDataInicioVigencia())
                .dataFimVigencia(entity.getDataFimVigencia())
                .baseLegal(entity.getBaseLegal())
                .build();
    }
}
