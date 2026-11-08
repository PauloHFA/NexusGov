package gov.nexus.service;

import gov.nexus.config.SecurityUtils;
import gov.nexus.domain.Fornecedor;
import gov.nexus.domain.VinculoSocietario;
import gov.nexus.dto.FornecedorDto;
import gov.nexus.dto.PageResponse;
import gov.nexus.dto.SocioDto;
import gov.nexus.repository.FornecedorRepository;
import gov.nexus.repository.VinculoSocietarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class FornecedorService {

    private final FornecedorRepository fornecedorRepository;
    private final VinculoSocietarioRepository vinculoSocietarioRepository;
    private final SecurityUtils securityUtils;

    @Transactional(readOnly = true)
    public PageResponse<FornecedorDto> listarPorUf(String uf, Pageable pageable) {
        Page<Fornecedor> page = (uf != null && !uf.isBlank())
                ? fornecedorRepository.findByUf(uf, pageable)
                : fornecedorRepository.findAll(pageable);
        boolean isPublic = securityUtils.isPublicUser();
        return PageResponse.from(page.map(f -> toDto(f, isPublic)));
    }

    @Transactional(readOnly = true)
    public Optional<FornecedorDto> buscarPorId(String id) {
        boolean isPublic = securityUtils.isPublicUser();
        return fornecedorRepository.findById(id).map(f -> toDto(f, isPublic));
    }

    @Transactional(readOnly = true)
    public Optional<FornecedorDto> buscarPorCnpj(String cnpj) {
        boolean isPublic = securityUtils.isPublicUser();
        return fornecedorRepository.findByCnpj(cnpj).map(f -> toDto(f, isPublic));
    }

    public FornecedorDto toDto(Fornecedor entity, boolean isPublic) {
        List<VinculoSocietario> vinculos = vinculoSocietarioRepository.findByFornecedorId(entity.getId());
        List<SocioDto> socios = vinculos.stream().map(v -> {
            SocioDto dto = SocioDto.builder()
                    .id(v.getSocio().getId())
                    .tipoPessoa(v.getSocio().getTipoPessoa())
                    .cpfCnpjMascarado(v.getSocio().getCpfCnpjMascarado())
                    .nome(v.getSocio().getNomeNormalizado())
                    .qualificacao(v.getQualificacao())
                    .confiancaIdentidade(v.getSocio().getConfiancaIdentidade())
                    .rotuloIdentidade(v.getSocio().getRotuloIdentidade())
                    .build();
            return isPublic ? dto.toPublicMasked() : dto;
        }).collect(Collectors.toList());

        return FornecedorDto.builder()
                .id(entity.getId())
                .cnpj(entity.getCnpj())
                .razaoSocial(entity.getRazaoSocial())
                .nomeFantasia(entity.getNomeFantasia())
                .situacaoCadastral(entity.getSituacaoCadastral())
                .dataAbertura(entity.getDataAbertura())
                .capitalSocial(entity.getCapitalSocial())
                .porte(entity.getPorte())
                .cnaeFiscalPrincipal(entity.getCnaeFiscalPrincipal())
                .municipioIbge(entity.getMunicipioIbge())
                .uf(entity.getUf())
                .socios(socios)
                .build();
    }
}
