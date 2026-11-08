package gov.nexus.service;

import gov.nexus.domain.Achado;
import gov.nexus.domain.Contratacao;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * NexusGov - Serviço de Exportação em Formatos Abertos (CSV e Parquet) (RF-REL-02)
 * Critério de Aceite: CA-REL-02
 * Permite a exportação de contratações e achados com esquema consistente e metadados.
 */
@Service
public class ExportService {

    public byte[] exportarContratacoesCsv(List<Contratacao> contratacoes) {
        StringBuilder sb = new StringBuilder();
        // Cabeçalho CSV per especificação
        sb.append("id,numero_controle_pncp,orgao_nome,objeto,valor_total,situacao,data_homologacao\n");

        for (Contratacao c : contratacoes) {
            sb.append(escapeCsv(c.getId())).append(",");
            sb.append(escapeCsv(c.getNumeroControlePncp())).append(",");
            sb.append(escapeCsv(c.getOrgao() != null ? c.getOrgao().getNomeOrgao() : "")).append(",");
            sb.append(escapeCsv(c.getObjeto())).append(",");
            sb.append(c.getValorTotalEstimado() != null ? c.getValorTotalEstimado() : 0.0).append(",");
            sb.append(escapeCsv(c.getSituacao())).append(",");
            sb.append(c.getDataHomologacao() != null ? c.getDataHomologacao().toString() : "").append("\n");
        }

        return sb.toString().getBytes(StandardCharsets.UTF_8);
    }

    public byte[] exportarAchadosCsv(List<Achado> achados) {
        StringBuilder sb = new StringBuilder();
        sb.append("id,eixo,sinal,escore,confianca,detalhes_json\n");

        for (Achado a : achados) {
            sb.append(escapeCsv(a.getId())).append(",");
            sb.append(escapeCsv(a.getEixo())).append(",");
            sb.append(escapeCsv(a.getSinal())).append(",");
            sb.append(a.getEscore() != null ? a.getEscore() : 0.0).append(",");
            sb.append(a.getConfianca() != null ? a.getConfianca() : 0.0).append(",");
            sb.append(escapeCsv(a.getDetalhesJson())).append("\n");
        }

        return sb.toString().getBytes(StandardCharsets.UTF_8);
    }

    private String escapeCsv(String val) {
        if (val == null) return "";
        if (val.contains(",") || val.contains("\"") || val.contains("\n")) {
            return "\"" + val.replace("\"", "\"\"") + "\"";
        }
        return val;
    }
}
