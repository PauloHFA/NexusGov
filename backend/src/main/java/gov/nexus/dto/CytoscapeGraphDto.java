package gov.nexus.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CytoscapeGraphDto {
    @Builder.Default
    private List<NodeElement> nodes = new ArrayList<>();
    @Builder.Default
    private List<EdgeElement> edges = new ArrayList<>();

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class NodeElement {
        private NodeData data;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class NodeData {
        private String id;
        private String label;
        private String tipo; // EMPRESA, SOCIO, LICITACAO, ORGAO
        private Double centrality;
        private String communityId;
        private Map<String, Object> metadata;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class EdgeElement {
        private EdgeData data;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class EdgeData {
        private String id;
        private String source;
        private String target;
        private String label;
        private String linkType; // SOCIO_COMPARTILHADO, ENDERECO_COMPARTILHADO, COOCORRENCIA_LICITACAO
        private Double weight;
        private Double confidence;
        private String color;
    }
}
