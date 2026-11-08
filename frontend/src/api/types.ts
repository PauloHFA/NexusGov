export type NivelRisco = 'Baixo' | 'Médio' | 'Elevado';

export interface PageResponse<T> {
  content: T[];
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
  last: boolean;
}

export interface Orgao {
  id: string;
  cnpj: string;
  nomeOrgao: string;
  esfera: string;
  poder: string;
  uf: string;
  codigoIbgeMunicipio: string;
  criadoEm?: string;
}

export interface Socio {
  id: string;
  tipoPessoa: string;
  cpfCnpjMascarado: string;
  nome: string;
  qualificacao?: string;
  confiancaIdentidade: number;
  rotuloIdentidade: string;
}

export interface Fornecedor {
  id: string;
  cnpj: string;
  razaoSocial: string;
  nomeFantasia?: string;
  situacaoCadastral?: string;
  dataAbertura?: string;
  capitalSocial?: number;
  porte?: string;
  cnaeFiscalPrincipal?: string;
  municipioIbge?: string;
  uf?: string;
  socios?: Socio[];
}

export interface ItemContratacao {
  id: string;
  numeroItem: number;
  descricao: string;
  codigoCatmatCatser?: string;
  quantidade?: number;
  unidadeMedida?: string;
  valorUnitarioHomologado?: number;
  valorTotal?: number;
}

export interface Evidencia {
  id: string;
  hashSha256: string;
  urlFonte: string;
  coletadoEm: string;
  competenciaBase: string;
  trechoDado: string;
  caminhoStorageRaw: string;
}

export interface Achado {
  id: string;
  eixo: string;
  sinal: string;
  escore: number;
  confianca: number;
  detalhesJson: string;
  criadoEm: string;
  evidencias: Evidencia[];
}

export interface DecomposicaoSinal {
  sinal: string;
  eixo: string;
  escore: number;
  confianca: number;
  peso: number;
  contribuicaoPonderada: number;
  detalhes: string;
}

export interface IeaResultado {
  id: string;
  contratacaoId: string;
  versaoParametros: string;
  valorIea: number;
  nivelRisco: NivelRisco;
  qtdEixosIndependentes: number;
  multiEixoValido: boolean;
  decomposicaoSinais: DecomposicaoSinal[];
  calculadoEm: string;
  avisoMetodologico: string;
}

export interface ContratacaoSummary {
  id: string;
  numeroControlePncp: string;
  orgaoNome: string;
  orgaoCnpj: string;
  modalidadeNome: string;
  anoCompra: number;
  objeto: string;
  valorTotalHomologado: number;
  uf: string;
  municipioIbge: string;
  ieaScore?: number;
  nivelRisco?: NivelRisco;
  dataPublicacaoPncp: string;
}

export interface ContratacaoDetail {
  id: string;
  numeroControlePncp: string;
  orgao: Orgao;
  modalidadeNome: string;
  numeroEdital?: string;
  anoCompra: number;
  objeto: string;
  valorTotalEstimado?: number;
  valorTotalHomologado?: number;
  dataAberturaProposta?: string;
  dataHomologacao?: string;
  situacao?: string;
  urlPncp?: string;
  uf: string;
  municipioIbge?: string;
  itens: ItemContratacao[];
  achados: Achado[];
  iea?: IeaResultado;
  avisoMetodologico: string;
}

export interface CytoscapeNode {
  data: {
    id: string;
    label: string;
    tipo: 'EMPRESA' | 'SOCIO' | 'LICITACAO' | 'ORGAO';
    centrality?: number;
    communityId?: string;
    metadata?: Record<string, any>;
  };
}

export interface CytoscapeEdge {
  data: {
    id: string;
    source: string;
    target: string;
    label: string;
    linkType: string;
    weight?: number;
    confidence?: number;
    color?: string;
  };
}

export interface CytoscapeGraph {
  nodes: CytoscapeNode[];
  edges: CytoscapeEdge[];
}

export interface ResultadoVerificacao {
  integro: boolean;
  hashCalculado: string;
  hashEsperado: string;
  mensagem: string;
  evidenciaCadastrada?: Evidencia;
}

export interface ContestacaoRequest {
  tipoSolicitante: 'PESSOA_FISICA' | 'PESSOA_JURIDICA';
  documentoIdentificador: string;
  nomeSolicitante: string;
  emailContato: string;
  contratacaoId?: string;
  fornecedorId?: string;
  motivoContestacao: string;
  documentosAnexos?: string;
}

export interface ContestacaoResponse extends ContestacaoRequest {
  id: string;
  numeroProtocolo: string;
  status: string;
  parecerResposta?: string;
  criadoEm: string;
  respondidoEm?: string;
}
