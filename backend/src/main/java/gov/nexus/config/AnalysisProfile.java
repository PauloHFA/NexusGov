package gov.nexus.config;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.util.Map;

/**
 * NexusGov - Perfis de Análise Parametrizáveis (RF-CFG-03 / CA-CFG-03)
 * Conservador: ignora parentesco presumido e exige limiares mais estritos para mitigar falsos positivos.
 * Padrão: calibração de referência do TCU / Lei 14.133.
 * Exploratório: alta sensibilidade para triagem prévia e varredura ampla.
 */
@Getter
@RequiredArgsConstructor
public enum AnalysisProfile {

    CONSERVADOR(
            "Perfil Conservador",
            false, // Ignora parentesco presumido / homonímia sem documento adicional
            70.0,  // Limiar IEA Elevado mais exigente
            35.0,  // Limiar IEA Médio
            Map.of("GRAFO", 1.2, "BENFORD", 0.8, "FRACIONAMENTO", 1.0, "POPUP", 1.0)
    ),

    PADRAO(
            "Perfil Padrão Regulamentar",
            true,
            60.0,
            30.0,
            Map.of("GRAFO", 1.0, "BENFORD", 1.0, "FRACIONAMENTO", 1.0, "POPUP", 1.0)
    ),

    EXPLORATORIO(
            "Perfil Exploratório e Amplo",
            true,
            50.0,
            25.0,
            Map.of("GRAFO", 1.0, "BENFORD", 1.2, "FRACIONAMENTO", 1.2, "POPUP", 1.2)
    );

    private final String descricao;
    private final boolean considerarHomonimiaPresumida;
    private final double limiarIeaElevado;
    private final double limiarIeaMedio;
    private final Map<String, Double> pesosEixos;

    public boolean permiteClassificacaoElevada(int eixosAtivos, double ieaAritmetico) {
        // Salvaguarda SG-04: mínimo de 2 eixos independentes para Elevado
        if (eixosAtivos < 2) {
            return false;
        }
        return ieaAritmetico >= this.limiarIeaElevado;
    }
}
