import React, { useEffect, useRef, useState } from 'react';
import cytoscape, { Core, EventObject } from 'cytoscape';
import cola from 'cytoscape-cola';
import { CytoscapeGraph, CytoscapeNode } from '../../api/types';
import { ZoomIn, ZoomOut, Maximize2, RotateCcw, AlertTriangle, Users, Building, Shield } from 'lucide-react';

cytoscape.use(cola);

interface NetworkGraphProps {
  graphData: CytoscapeGraph;
  onClose?: () => void;
  contratacaoNumero?: string;
}

export const NetworkGraph: React.FC<NetworkGraphProps> = ({ graphData, onClose, contratacaoNumero }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);
  const [selectedNode, setSelectedNode] = useState<CytoscapeNode['data'] | null>(null);
  const [anoCorte, setAnoCorte] = useState<number>(2026);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  useEffect(() => {
    if (!isPlaying) return;
    const interval = setInterval(() => {
      setAnoCorte((prev) => {
        if (prev >= 2026) {
          setIsPlaying(false);
          return 2026;
        }
        return prev + 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [isPlaying]);

  useEffect(() => {
    if (!cyRef.current) return;
    cyRef.current.batch(() => {
      cyRef.current?.nodes().forEach((node) => {
        const nodeYear = node.data('ano') || node.data('anoAbertura') || 2021;
        if (nodeYear > anoCorte) {
          node.style('display', 'none');
        } else {
          node.style('display', 'element');
        }
      });
    });
  }, [anoCorte]);

  useEffect(() => {
    if (!containerRef.current) return;

    const elements = [
      ...graphData.nodes.map((n) => ({
        group: 'nodes' as const,
        data: n.data,
      })),
      ...graphData.edges.map((e) => ({
        group: 'edges' as const,
        data: e.data,
      })),
    ];

    const cy = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'font-size': '10px',
            'text-valign': 'bottom',
            'text-margin-y': 4,
            'color': '#1e293b',
            'font-family': 'sans-serif',
          },
        },
        // Nós de Empresa
        {
          selector: 'node[tipo = "EMPRESA"]',
          style: {
            'background-color': '#0d9488',
            'shape': 'ellipse',
            'width': 'mapData(centrality, 0, 1, 30, 60)',
            'height': 'mapData(centrality, 0, 1, 30, 60)',
            'border-width': 2,
            'border-color': '#042f2e',
          },
        },
        // Nós de Sócio
        {
          selector: 'node[tipo = "SOCIO"]',
          style: {
            'background-color': '#7c3aed',
            'shape': 'diamond',
            'width': 26,
            'height': 26,
            'border-width': 2,
            'border-color': '#4c1d95',
          },
        },
        // Nós de Licitação
        {
          selector: 'node[tipo = "LICITACAO"]',
          style: {
            'background-color': '#2563eb',
            'shape': 'round-rectangle',
            'width': 44,
            'height': 34,
            'border-width': 2,
            'border-color': '#1e3a8a',
          },
        },
        // Nós de Órgão
        {
          selector: 'node[tipo = "ORGAO"]',
          style: {
            'background-color': '#475569',
            'shape': 'hexagon',
            'width': 40,
            'height': 40,
            'border-width': 2,
            'border-color': '#0f172a',
          },
        },
        // Arestas Gerais
        {
          selector: 'edge',
          style: {
            'width': 'data(weight)',
            'line-color': 'data(color)',
            'curve-style': 'bezier',
            'opacity': 0.85,
          },
        },
        // Arestas de Sócio Compartilhado (Destaque em Vermelho Vivo)
        {
          selector: 'edge[linkType = "SOCIO_COMPARTILHADO"]',
          style: {
            'line-color': '#dc2626',
            'width': 4,
            'line-style': 'solid',
            'opacity': 1.0,
            'label': 'SÓCIO COMUM',
            'font-size': '8px',
            'color': '#991b1b',
            'text-background-opacity': 0.8,
            'text-background-color': '#fee2e2',
            'text-background-padding': '2px',
          },
        },
      ],
      layout: {
        name: 'cola',
        animate: true,
        randomize: false,
        maxSimulationTime: 2000,
      } as any,
    });

    cy.on('tap', 'node', (evt: EventObject) => {
      const nodeData = evt.target.data();
      setSelectedNode(nodeData);
    });

    cy.on('tap', (evt: EventObject) => {
      if (evt.target === cy) {
        setSelectedNode(null);
      }
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
    };
  }, [graphData]);

  const handleZoomIn = () => cyRef.current?.zoom(cyRef.current.zoom() * 1.25);
  const handleZoomOut = () => cyRef.current?.zoom(cyRef.current.zoom() * 0.8);
  const handleFit = () => cyRef.current?.fit();
  const handleReset = () => {
    cyRef.current?.layout({ name: 'cola', animate: true } as any).run();
    cyRef.current?.fit();
  };

  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden flex flex-col h-[650px] relative">
      {/* Top toolbar */}
      <div className="p-3 bg-slate-900 text-white flex items-center justify-between z-10">
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5 text-teal-400" />
          <span className="font-bold text-sm">Visualizador de Redes de Contratação</span>
          {contratacaoNumero && (
            <span className="text-xs text-slate-400 border-l border-slate-700 pl-2">
              PNCP: {contratacaoNumero}
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {/* Legenda rápida */}
          <div className="hidden sm:flex items-center gap-3 text-[11px] text-slate-300 mr-4">
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 rounded-full bg-teal-500 inline-block" /> Empresa
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 rotate-45 bg-purple-500 inline-block" /> Sócio
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 rounded bg-blue-500 inline-block" /> Licitação
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-0.5 bg-red-600 inline-block" /> Sócio Compartilhado
            </span>
          </div>

          <div className="flex items-center bg-slate-800 rounded p-0.5">
            <button onClick={handleZoomIn} className="p-1.5 hover:bg-slate-700 rounded text-slate-300" title="Zoom In">
              <ZoomIn className="w-4 h-4" />
            </button>
            <button onClick={handleZoomOut} className="p-1.5 hover:bg-slate-700 rounded text-slate-300" title="Zoom Out">
              <ZoomOut className="w-4 h-4" />
            </button>
            <button onClick={handleFit} className="p-1.5 hover:bg-slate-700 rounded text-slate-300" title="Ajustar à tela">
              <Maximize2 className="w-4 h-4" />
            </button>
            <button onClick={handleReset} className="p-1.5 hover:bg-slate-700 rounded text-slate-300" title="Redefinir Layout">
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>

          {onClose && (
            <button
              onClick={onClose}
              className="text-xs bg-slate-800 hover:bg-slate-700 px-2.5 py-1.5 rounded text-slate-200 transition"
            >
              Fechar
            </button>
          )}
        </div>
      </div>

      {/* Barra de Linha do Tempo Dinâmica (Melhoria 5) */}
      <div className="bg-slate-800 border-b border-slate-700 px-4 py-2 flex items-center justify-between text-xs text-slate-200 z-10 flex-wrap gap-2">
        <div className="flex items-center gap-3">
          <button
            onClick={() => {
              if (anoCorte >= 2026) setAnoCorte(2021);
              setIsPlaying(!isPlaying);
            }}
            className="px-2.5 py-1 bg-teal-600 hover:bg-teal-500 text-white rounded font-bold text-[11px] flex items-center gap-1 transition"
          >
            {isPlaying ? '⏸ Pausar' : '▶ Reproduzir Evolução Temporal'}
          </button>
          <span className="font-semibold text-slate-300">
            Linha do Tempo da Rede: <strong className="text-teal-400 font-mono text-sm">{anoCorte}</strong>
          </span>
        </div>

        <div className="flex items-center gap-3 w-64">
          <span className="text-[10px] text-slate-400">2021</span>
          <input
            type="range"
            min={2021}
            max={2026}
            step={1}
            value={anoCorte}
            onChange={(e) => setAnoCorte(Number(e.target.value))}
            className="w-full accent-teal-500 cursor-pointer h-1.5 bg-slate-700 rounded-lg"
          />
          <span className="text-[10px] text-slate-400">2026</span>
        </div>
      </div>

      {/* Main Canvas */}
      <div ref={containerRef} className="flex-1 w-full bg-slate-50 cursor-grab active:cursor-grabbing" />

      {/* Selected Node Inspector Drawer */}
      {selectedNode && (
        <div className="absolute bottom-4 right-4 max-w-sm w-full bg-white/95 backdrop-blur border border-slate-300 rounded-lg p-4 shadow-xl z-20 text-xs">
          <div className="flex items-center justify-between border-b border-slate-200 pb-2 mb-2">
            <span className="font-bold text-slate-900 uppercase tracking-wide flex items-center gap-1.5">
              {selectedNode.tipo === 'EMPRESA' && <Building className="w-4 h-4 text-teal-600" />}
              {selectedNode.tipo === 'SOCIO' && <Users className="w-4 h-4 text-purple-600" />}
              {selectedNode.tipo}
            </span>
            <button onClick={() => setSelectedNode(null)} className="text-slate-400 hover:text-slate-600 font-bold">
              ✕
            </button>
          </div>

          <div className="space-y-1.5">
            <div>
              <span className="text-slate-500">Identificação: </span>
              <span className="font-semibold text-slate-800">{selectedNode.label}</span>
            </div>

            {selectedNode.centrality !== undefined && (
              <div>
                <span className="text-slate-500">Centralidade de Intermediação: </span>
                <span className="font-mono font-medium text-slate-900">{selectedNode.centrality.toFixed(4)}</span>
              </div>
            )}

            {selectedNode.metadata && Object.keys(selectedNode.metadata).length > 0 && (
              <div className="mt-2 pt-2 border-t border-slate-100 space-y-1">
                {Object.entries(selectedNode.metadata).map(([key, val]) => (
                  <div key={key} className="flex justify-between">
                    <span className="text-slate-500 capitalize">{key}:</span>
                    <span className="font-medium text-slate-800">{String(val)}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
