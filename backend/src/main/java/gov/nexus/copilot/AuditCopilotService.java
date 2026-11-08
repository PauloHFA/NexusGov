package gov.nexus.copilot;

import gov.nexus.dto.ContratacaoDetailDto;
import gov.nexus.dto.DecomposicaoSinalDto;
import gov.nexus.service.ContratacaoService;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Collections;
import java.util.List;

/**
 * NexusGov - Assistente de Auditoria e Copilot de Instrução Técnica (Melhoria 3)
 * Gera minutas padronizadas de instrução técnica de fiscalização preliminar.
 * Aplica estritamente a salvaguarda SG-01 (linguagem neutra e indiciária) e
 * referencia o marco legal: Lei 14.133/2021 e Resolução TCU nº 367/2024 Art. 19-B.
 */
@Service
@RequiredArgsConstructor
public class AuditCopilotService {

    private final ContratacaoService contratacaoService;

    @Data
    @Builder
    public static class MinutaAuditoriaDto {
        private String contratacaoId;
        private String numeroControlePncp;
        private String tituloDocumento;
        private String textoMinutaMarkdown;
        private String nivelExposicao;
        private Double valorIea;
        private int quantidadeSinaisAvaliados;
        private String avisoMetodologico;
        private String dataEmissao;
    }

    public MinutaAuditoriaDto gerarMinutaInstrucaoTecnica(String contratacaoId) {
        ContratacaoDetailDto c = contratacaoService.buscarDetalhePorId(contratacaoId)
                .orElseThrow(() -> new IllegalArgumentException("Contratação não encontrada: " + contratacaoId));

        StringBuilder sb = new StringBuilder();
        String dataHoje = LocalDate.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy"));

        sb.append("# MINUTA PRELIMINAR DE INSTRUÇÃO TÉCNICA DE AUDITORIA\n\n");
        sb.append("**Referência:** ").append(c.getNumeroControlePncp()).append(" | **Data de Emissão:** ").append(dataHoje).append("\n");
        sb.append("**Sistema Emissor:** NexusGov — Triagem Estatística e Governança Forense\n\n");
        sb.append("---\n\n");

        sb.append("## 1. IDENTIFICAÇÃO DO PROCESSO E MARCO REGULATÓRIO\n\n");
        String nomeOrgao = c.getOrgao() != null ? c.getOrgao().getNomeOrgao() : "Órgão Não Informado";
        String cnpjOrgao = c.getOrgao() != null ? c.getOrgao().getCnpj() : "N/D";
        String uf = c.getOrgao() != null ? c.getOrgao().getUf() : c.getUf();
        String ibge = c.getOrgao() != null ? c.getOrgao().getCodigoIbgeMunicipio() : c.getMunicipioIbge();

        sb.append("- **Órgão Licitante:** ").append(nomeOrgao).append(" (CNPJ: ").append(cnpjOrgao).append(")\n");
        sb.append("- **Unidade Federativa:** ").append(uf).append(" | Município IBGE: ").append(ibge).append("\n");
        sb.append("- **Modalidade:** ").append(c.getModalidadeNome()).append(" | Ano: ").append(c.getAnoCompra()).append("\n");
        sb.append("- **Objeto Declarado:** ").append(c.getObjeto()).append("\n");
        sb.append("- **Valor Total Estimado / Homologado:** R$ ").append(c.getValorTotalEstimado() != null ? String.format("%,.2f", c.getValorTotalEstimado()) : "0,00").append("\n");
        sb.append("- **Fundamentação Legal:** Lei nº 14.133/2021 e Resolução TCU nº 367/2024.\n\n");

        sb.append("## 2. SÍNTESE DA TRIAGEM E ÍNDICE DE EXPOSIÇÃO A ANOMALIAS (IEA)\n\n");
        sb.append("A presente contratação foi processada pelos motores analíticos e de teoria dos grafos do NexusGov, registrando:\n\n");

        double valorIea = (c.getIea() != null && c.getIea().getValorIea() != null) ? c.getIea().getValorIea().doubleValue() : 0.0;
        String nivelRisco = c.getIea() != null ? c.getIea().getNivelRisco() : "Baixo";
        int eixosAtivos = c.getIea() != null ? c.getIea().getQtdEixosIndependentes() : 0;
        boolean multiValido = c.getIea() != null && c.getIea().isMultiEixoValido();
        String aviso = (c.getIea() != null && c.getIea().getAvisoMetodologico() != null)
                ? c.getIea().getAvisoMetodologico()
                : "Aviso Metodológico Obrigatório (SG-03): Triagem estatística para priorização analítica.";

        sb.append("- **Pontuação IEA:** **").append(String.format("%.1f", valorIea)).append(" / 100**\n");
        sb.append("- **Classificação de Exposição:** **").append(nivelRisco).append("**\n");
        sb.append("- **Eixos Analíticos com Sinais Ativos:** ").append(eixosAtivos).append(" eixo(s) independente(s)\n");
        sb.append("- **Regra Multieixo (SG-04):** ").append(multiValido ? "Atendida (presença de múltiplos eixos independentes)" : "Classificação limitada a Médio por sinal isolado").append("\n\n");

        sb.append("## 3. DECOMPOSIÇÃO ANALÍTICA DAS EVIDÊNCIAS E SINAIS REGISTRADOS\n\n");
        List<DecomposicaoSinalDto> sinais = (c.getIea() != null && c.getIea().getDecomposicaoSinais() != null)
                ? c.getIea().getDecomposicaoSinais()
                : Collections.emptyList();

        if (sinais.isEmpty()) {
            sb.append("Nenhum sinal anômalo estatisticamente relevante foi registrado para este certame.\n\n");
        } else {
            for (int i = 0; i < sinais.size(); i++) {
                DecomposicaoSinalDto s = sinais.get(i);
                sb.append("### 3.").append(i + 1).append(". Eixo: ").append(s.getEixo()).append(" — Sinal: `").append(s.getSinal()).append("`\n");
                sb.append("- **Intensidade do Sinal:** ").append(s.getEscore() != null ? String.format("%.2f", s.getEscore()) : "0.00").append(" (de 0 a 1.0)\n");
                sb.append("- **Nível de Confiança Estatística:** ").append(s.getConfianca() != null ? String.format("%.2f", s.getConfianca()) : "0.00").append("\n");
                sb.append("- **Contribuição Ponderada no IEA:** ").append(s.getContribuicaoPonderada() != null ? String.format("%.2f%%", s.getContribuicaoPonderada()) : "0.00%").append("\n");
                sb.append("- **Contexto Técnico:** Identificada convergência de métricas indiciárias que recomenda verificação detalhada da documentação fiscal e de propostas.\n\n");
            }
        }

        sb.append("## 4. PROPOSTA DE DILIGÊNCIAS PRELIMINARES E ENCAMINHAMENTO\n\n");
        sb.append("Com base nos indícios estatísticos e de redes identificados, sugere-se à equipe de fiscalização:\n\n");
        sb.append("1. **Inspeção Documental:** Requisitar do órgão contratante cópia integral dos autos do processo de contratação, com destaque para atas de lances e mapa de cotação de preços.\n");
        sb.append("2. **Verificação Cadastral:** Confirmar a autenticidade das certidões e quadros societários (QSA) dos fornecedores participantes junto à base da Receita Federal.\n");
        sb.append("3. **Exame de Execução Física:** Caso a fase contratual já se encontre em execução ou liquidada, verificar as notas fiscais e relatórios de medição / entrega dos bens.\n");
        sb.append("4. **Oitiva Facultativa:** Oportunizar prévio esclarecimento aos envolvidos caso a unidade técnica decida pela autuação de procedimento formal de fiscalização.\n\n");

        sb.append("## 5. AVISO METODOLÓGICO OBRIGATÓRIO (SG-03)\n\n");
        sb.append("> ").append(aviso).append("\n\n");
        sb.append("---\n");
        sb.append("*Minuta gerada automaticamente pelo NexusGov Audit Copilot para apoio exclusivo a auditores humanos.*");

        return MinutaAuditoriaDto.builder()
                .contratacaoId(c.getId())
                .numeroControlePncp(c.getNumeroControlePncp())
                .tituloDocumento("Minuta de Instrução Técnica de Auditoria - " + c.getNumeroControlePncp())
                .textoMinutaMarkdown(sb.toString())
                .nivelExposicao(nivelRisco)
                .valorIea(valorIea)
                .quantidadeSinaisAvaliados(sinais.size())
                .avisoMetodologico(aviso)
                .dataEmissao(dataHoje)
                .build();
    }
}
