import axios from 'axios';
import {
  ContratacaoSummary,
  ContratacaoDetail,
  CytoscapeGraph,
  PageResponse,
  ResultadoVerificacao,
  ContestacaoRequest,
  ContestacaoResponse,
} from './types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  async listarContratacoes(params: {
    uf?: string;
    ano?: number;
    orgaoId?: string;
    page?: number;
    size?: number;
  }): Promise<PageResponse<ContratacaoSummary>> {
    const res = await api.get<PageResponse<ContratacaoSummary>>('/contratacoes', { params });
    return res.data;
  },

  async buscarContratacao(id: string): Promise<ContratacaoDetail> {
    const res = await api.get<ContratacaoDetail>(`/contratacoes/${id}`);
    return res.data;
  },

  async obterSubgrafo(contratacaoId: string): Promise<CytoscapeGraph> {
    const res = await api.get<CytoscapeGraph>(`/grafos/${contratacaoId}`);
    return res.data;
  },

  async verificarIntegridade(payloadBruto: string, hashEsperado: string): Promise<ResultadoVerificacao> {
    const res = await api.post<ResultadoVerificacao>('/relatorios/verificar', {
      payloadBruto,
      hashEsperado,
    });
    return res.data;
  },

  async submeterContestacao(dados: ContestacaoRequest): Promise<ContestacaoResponse> {
    const res = await api.post<ContestacaoResponse>('/contestacoes', dados);
    return res.data;
  },

  async consultarContestacao(protocolo: string): Promise<ContestacaoResponse> {
    const res = await api.get<ContestacaoResponse>(`/contestacoes/${protocolo}`);
    return res.data;
  },

  getDossiePdfUrl(contratacaoId: string): string {
    return `/api/v1/relatorios/dossie/${contratacaoId}`;
  },
};
