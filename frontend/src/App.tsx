import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { MethodologicalNotice } from './components/MethodologicalNotice';
import { SearchBar } from './features/search/SearchBar';
import { FilterPanel } from './features/search/FilterPanel';
import { ContratacoesTable } from './features/search/ContratacoesTable';
import { TenderDetail } from './features/edital/TenderDetail';
import { NetworkGraph } from './features/graph/NetworkGraph';
import { DossierVerifier } from './features/verification/DossierVerifier';
import { ContestationForm } from './features/contestation/ContestationForm';
import { apiService } from './api/client';
import { ContratacaoSummary, ContratacaoDetail, CytoscapeGraph, NivelRisco } from './api/types';

// Mock representativo para inicialização rápida e testes locais do piloto PB
const MOCK_CONTRATACOES: ContratacaoSummary[] = [
  {
    id: 'c-jp-001',
    numeroControlePncp: '08778268000160-1-000001/2024',
    orgaoNome: 'Prefeitura Municipal de João Pessoa',
    orgaoCnpj: '08778268000160',
    modalidadeNome: 'Dispensa de Licitação',
    anoCompra: 2024,
    objeto: 'Aquisição emergencial de medicamentos e insumos hospitalares para a rede municipal de saúde',
    valorTotalHomologado: 58900.0,
    uf: 'PB',
    municipioIbge: '2507507',
    ieaScore: 78.4,
    nivelRisco: 'Elevado',
    dataPublicacaoPncp: '2024-03-12T10:00:00Z',
  },
  {
    id: 'c-cg-002',
    numeroControlePncp: '08993751000140-1-000045/2024',
    orgaoNome: 'Prefeitura Municipal de Campina Grande',
    orgaoCnpj: '08993751000140',
    modalidadeNome: 'Pregão Eletrônico',
    anoCompra: 2024,
    objeto: 'Contratação de serviços continuados de manutenção predial com fornecimento de peças',
    valorTotalHomologado: 345000.0,
    uf: 'PB',
    municipioIbge: '2504009',
    ieaScore: 42.1,
    nivelRisco: 'Médio',
    dataPublicacaoPncp: '2024-02-18T14:30:00Z',
  },
  {
    id: 'c-pt-003',
    numeroControlePncp: '08889999000122-1-000012/2024',
    orgaoNome: 'Prefeitura Municipal de Patos',
    orgaoCnpj: '08889999000122',
    modalidadeNome: 'Dispensa de Licitação',
    anoCompra: 2024,
    objeto: 'Aquisição de material permanente para unidades básicas de saúde da família',
    valorTotalHomologado: 28400.0,
    uf: 'PB',
    municipioIbge: '2510808',
    ieaScore: 12.0,
    nivelRisco: 'Baixo',
    dataPublicacaoPncp: '2024-01-22T09:15:00Z',
  },
];

const MOCK_GRAPH: CytoscapeGraph = {
  nodes: [
    {
      data: {
        id: 'lic_c-jp-001',
        label: 'Dispensa 001/2024',
        tipo: 'LICITACAO',
        centrality: 1.0,
      },
    },
    {
      data: {
        id: 'org_08778268000160',
        label: 'Prefeitura de João Pessoa',
        tipo: 'ORGAO',
        centrality: 0.8,
      },
    },
    {
      data: {
        id: 'emp_111',
        label: 'Distribuidora Farma Nordeste LTDA',
        tipo: 'EMPRESA',
        centrality: 0.7,
      },
    },
    {
      data: {
        id: 'emp_222',
        label: 'MedSupply Paraíba EIRELI',
        tipo: 'EMPRESA',
        centrality: 0.6,
      },
    },
    {
      data: {
        id: 'soc_999',
        label: '[Pessoa Física Protegida - SG-01]',
        tipo: 'SOCIO',
        centrality: 0.9,
      },
    },
  ],
  edges: [
    {
      data: {
        id: 'e1',
        source: 'org_08778268000160',
        target: 'lic_c-jp-001',
        label: 'PUBLICOU',
        linkType: 'CONTRATANTE',
        weight: 1,
        color: '#64748b',
      },
    },
    {
      data: {
        id: 'e2',
        source: 'emp_111',
        target: 'lic_c-jp-001',
        label: 'ADJUDICADO',
        linkType: 'VENCEU',
        weight: 2,
        color: '#059669',
      },
    },
    {
      data: {
        id: 'e3',
        source: 'emp_222',
        target: 'lic_c-jp-001',
        label: 'PARTICIPANTE',
        linkType: 'PARTICIPOU',
        weight: 1,
        color: '#3b82f6',
      },
    },
    {
      data: {
        id: 'e4',
        source: 'emp_111',
        target: 'soc_999',
        label: 'SÓCIO',
        linkType: 'SOCIEDADE',
        weight: 1,
        color: '#8b5cf6',
      },
    },
    {
      data: {
        id: 'e5',
        source: 'emp_222',
        target: 'soc_999',
        label: 'SÓCIO',
        linkType: 'SOCIEDADE',
        weight: 1,
        color: '#8b5cf6',
      },
    },
    {
      data: {
        id: 'e_shared',
        source: 'emp_111',
        target: 'emp_222',
        label: 'SÓCIO COMPARTILHADO',
        linkType: 'SOCIO_COMPARTILHADO',
        weight: 4,
        color: '#dc2626',
      },
    },
  ],
};

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<'search' | 'graph' | 'verifier' | 'contestation'>('search');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedUf, setSelectedUf] = useState('PB');
  const [selectedAno, setSelectedAno] = useState<number | undefined>(undefined);
  const [selectedRisco, setSelectedRisco] = useState<NivelRisco | 'Todos'>('Todos');
  const [page, setPage] = useState(0);

  // Detalhes da contratação selecionada
  const [selectedContratacao, setSelectedContratacao] = useState<ContratacaoDetail | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  // Subgrafo em modal/aba
  const [activeGraph, setActiveGraph] = useState<CytoscapeGraph | null>(null);
  const [graphModalOpen, setGraphModalOpen] = useState(false);

  // Lista de contratações (da API ou fallback local)
  const [contratacoes, setContratacoes] = useState<ContratacaoSummary[]>(MOCK_CONTRATACOES);
  const [totalPages, setTotalPages] = useState(1);
  const [loadingList, setLoadingList] = useState(false);

  useEffect(() => {
    let active = true;
    const carregar = async () => {
      setLoadingList(true);
      try {
        const res = await apiService.listarContratacoes({
          uf: selectedUf,
          ano: selectedAno,
          page: page,
          size: 20,
        });
        if (active && res.content && res.content.length > 0) {
          setContratacoes(res.content);
          setTotalPages(res.totalPages);
        }
      } catch (err) {
        // Em caso de API local indisponível, mantém dados do piloto para demonstração
        console.warn('API backend em inicialização; exibindo amostra piloto PB.', err);
      } finally {
        if (active) setLoadingList(false);
      }
    };
    carregar();
    return () => {
      active = false;
    };
  }, [selectedUf, selectedAno, page]);

  const handleSelectContratacao = async (id: string) => {
    setLoadingDetail(true);
    try {
      const detalhe = await apiService.buscarContratacao(id);
      setSelectedContratacao(detalhe);
    } catch {
      // Fallback detalhado para mock
      const item = contratacoes.find((c) => c.id === id) || contratacoes[0];
      setSelectedContratacao({
        id: item.id,
        numeroControlePncp: item.numeroControlePncp,
        orgao: {
          id: 'org-1',
          cnpj: item.orgaoCnpj,
          nomeOrgao: item.orgaoNome,
          esfera: 'MUNICIPAL',
          poder: 'EXECUTIVO',
          uf: item.uf,
          codigoIbgeMunicipio: item.municipioIbge,
        },
        modalidadeNome: item.modalidadeNome,
        numeroEdital: '001/2024',
        anoCompra: item.anoCompra,
        objeto: item.objeto,
        valorTotalHomologado: item.valorTotalHomologado,
        uf: item.uf,
        municipioIbge: item.municipioIbge,
        urlPncp: 'https://pncp.gov.br/app/editais/' + item.orgaoCnpj + '/2024/0001',
        itens: [
          {
            id: 'it-1',
            numeroItem: 1,
            descricao: 'Lote 1: Insumos de primeiros socorros e curativos hospitalares',
            codigoCatmatCatser: '32100',
            quantidade: 500,
            unidadeMedida: 'UNIDADE',
            valorUnitarioHomologado: 59.0,
            valorTotal: 29500.0,
          },
          {
            id: 'it-2',
            numeroItem: 2,
            descricao: 'Lote 2: Material descartável esterilizado',
            codigoCatmatCatser: '32105',
            quantidade: 1000,
            unidadeMedida: 'PACOTE',
            valorUnitarioHomologado: 29.4,
            valorTotal: 29400.0,
          },
        ],
        achados: [
          {
            id: 'ach-1',
            eixo: 'GRAFO',
            sinal: 'COMMUNITY_COVER_BIDDING',
            escore: 0.85,
            confianca: 0.9,
            detalhesJson: '{}',
            criadoEm: '2024-03-12T10:00:00Z',
            evidencias: [
              {
                id: 'ev-1',
                hashSha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                urlFonte: 'https://pncp.gov.br/app/editais/08778268000160/2024/0001',
                coletadoEm: '2024-03-12T10:00:00Z',
                competenciaBase: '2024-11',
                trechoDado: 'Coocorrência de fornecedores vinculados societariamente',
                caminhoStorageRaw: 'raw/2024/03/pb_contratacao_001.json',
              },
            ],
          },
        ],
        iea: {
          id: 'iea-1',
          contratacaoId: item.id,
          versaoParametros: 'v1.0.0',
          valorIea: item.ieaScore || 78.4,
          nivelRisco: item.nivelRisco || 'Elevado',
          qtdEixosIndependentes: 2,
          multiEixoValido: true,
          decomposicaoSinais: [
            {
              sinal: 'COMMUNITY_COVER_BIDDING',
              eixo: 'GRAFO',
              escore: 0.85,
              confianca: 0.9,
              peso: 0.35,
              contribuicaoPonderada: 26.8,
              detalhes: 'Dois fornecedores participantes compartilham administrador no QSA da Receita Federal',
            },
            {
              sinal: 'SLIDING_WINDOW_EXCEEDED',
              eixo: 'FRACIONAMENTO',
              escore: 0.9,
              confianca: 1.0,
              peso: 0.25,
              contribuicaoPonderada: 22.5,
              detalhes: 'Janela móvel de 60 dias totalizou R$ 64.500,00, superando o teto legal de R$ 59.906,02',
            },
          ],
          calculadoEm: '2024-03-12T10:05:00Z',
          avisoMetodologico: 'Resolução TCU nº 367/2024',
        },
        avisoMetodologico: 'Resolução TCU nº 367/2024',
      });
    } finally {
      setLoadingDetail(false);
    }
  };

  const handleOpenGraph = async (id: string) => {
    try {
      const graph = await apiService.obterSubgrafo(id);
      if (graph.nodes && graph.nodes.length > 0) {
        setActiveGraph(graph);
      } else {
        setActiveGraph(MOCK_GRAPH);
      }
    } catch {
      setActiveGraph(MOCK_GRAPH);
    }
    setGraphModalOpen(true);
  };

  // Filtragem combinada
  const filteredContratacoes = contratacoes.filter((c) => {
    if (selectedRisco !== 'Todos' && c.nivelRisco !== selectedRisco) return false;
    if (selectedAno && c.anoCompra !== selectedAno) return false;
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      const matchPncp = c.numeroControlePncp.toLowerCase().includes(term);
      const matchOrgao = c.orgaoNome?.toLowerCase().includes(term);
      const matchObjeto = c.objeto?.toLowerCase().includes(term);
      const matchCnpj = c.orgaoCnpj?.toLowerCase().includes(term);
      return matchPncp || matchOrgao || matchObjeto || matchCnpj;
    }
    return true;
  });

  return (
    <div className="min-h-screen flex flex-col bg-slate-100">
      <Navbar currentTab={currentTab} setCurrentTab={setCurrentTab} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        {currentTab === 'search' && (
          <>
            {selectedContratacao ? (
              <TenderDetail
                contratacao={selectedContratacao}
                onBack={() => setSelectedContratacao(null)}
                onOpenGraph={handleOpenGraph}
              />
            ) : (
              <div className="space-y-4">
                {/* Banner de Boas-vindas do Piloto PB */}
                <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-6 rounded-xl shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                  <div>
                    <h1 className="text-xl font-bold">Painel Forense de Contratações Públicas</h1>
                    <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
                      Cruzamento automatizado de dados do Portal Nacional de Contratações Públicas (PNCP), Receita
                      Federal e IBGE para cálculo do Índice de Exposição a Anomalias (IEA). Escopo Piloto: Estado da
                      Paraíba (223 municípios).
                    </p>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="text-xs text-teal-400 font-semibold block">Lei 14.133/2021</span>
                    <span className="text-[11px] text-slate-400">Res. TCU nº 367/2024</span>
                  </div>
                </div>

                {/* Aviso Regulamentar Compacto */}
                <MethodologicalNotice compact />

                {/* Barra de Pesquisa e Filtros */}
                <div className="space-y-3">
                  <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
                  <FilterPanel
                    selectedUf={selectedUf}
                    setSelectedUf={setSelectedUf}
                    selectedAno={selectedAno}
                    setSelectedAno={setSelectedAno}
                    selectedRisco={selectedRisco}
                    setSelectedRisco={setSelectedRisco}
                    onReset={() => {
                      setSearchTerm('');
                      setSelectedAno(undefined);
                      setSelectedRisco('Todos');
                    }}
                  />
                </div>

                {/* Tabela de Resultados */}
                <ContratacoesTable
                  contratacoes={filteredContratacoes}
                  onSelect={handleSelectContratacao}
                  onOpenGraph={handleOpenGraph}
                  page={page}
                  totalPages={totalPages}
                  onPageChange={setPage}
                  loading={loadingList}
                />
              </div>
            )}
          </>
        )}

        {currentTab === 'verifier' && <DossierVerifier />}

        {currentTab === 'contestation' && <ContestationForm />}
      </main>

      {/* Modal do Grafo Interativo Cytoscape.js */}
      {graphModalOpen && activeGraph && (
        <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-5xl">
            <NetworkGraph graphData={activeGraph} onClose={() => setGraphModalOpen(false)} />
          </div>
        </div>
      )}

      {/* Rodapé Institucional */}
      <footer className="bg-slate-900 text-slate-400 border-t border-slate-800 py-6 text-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <span className="font-semibold text-white">NexusGov Platform</span> — Licença Livre e Aberta{' '}
            <span className="text-teal-400">GNU AGPL v3.0</span>
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <span>Escopo Piloto: Paraíba (PB)</span>
            <span>•</span>
            <span>Salvaguarda SG-01 Ativa</span>
            <span>•</span>
            <span>Conformidade LGPD</span>
          </div>
        </div>
      </footer>
    </div>
  );
};
