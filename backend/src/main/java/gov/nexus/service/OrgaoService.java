package gov.nexus.service;

import gov.nexus.domain.Orgao;
import gov.nexus.dto.OrgaoDto;
import gov.nexus.dto.PageResponse;
import gov.nexus.repository.OrgaoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class OrgaoService {

    private final OrgaoRepository orgaoRepository;

    @Transactional(readOnly = true)
    public PageResponse<OrgaoDto> listarPorUf(String uf, Pageable pageable) {
        Page<Orgao> page = (uf != null && !uf.isBlank())
                ? orgaoRepository.findByUf(uf, pageable)
                : orgaoRepository.findAll(pageable);
        return PageResponse.from(page.map(this::toDto));
    }

    @Transactional(readOnly = true)
    public Optional<OrgaoDto> buscarPorId(String id) {
        return orgaoRepository.findById(id).map(this::toDto);
    }

    @Transactional(readOnly = true)
    public Optional<OrgaoDto> buscarPorCnpj(String cnpj) {
        return orgaoRepository.findByCnpj(cnpj).map(this::toDto);
    }

    public OrgaoDto toDto(Orgao entity) {
        return OrgaoDto.builder()
                .id(entity.getId())
                .cnpj(entity.getCnpj())
                .nomeOrgao(entity.getNomeOrgao())
                .esfera(entity.getEsfera())
                .poder(entity.getPoder())
                .uf(entity.getUf())
                .codigoIbgeMunicipio(entity.getCodigoIbgeMunicipio())
                .criadoEm(entity.getCriadoEm())
                .build();
    }
}
