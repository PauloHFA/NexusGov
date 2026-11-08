import React, { useState } from 'react';
import { ContratacaoDetail, NivelRisco } from '../../api/types';
import { apiService } from '../../api/client';
import { MethodologicalNotice } from '../../components/MethodologicalNotice';
import { FracionamentoTimeline } from './FracionamentoTimeline';
import {
  FileDown,
  ExternalLink,
  Network,
  ArrowLeft,
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Building2,
  FileCheck,
} from 'lucide-react';

interface TenderDetailProps {
  contratacao: ContratacaoDetail;
  onBack: () => void;
  onOpenGraph: (id: string) => void;
}

export const TenderDetail: React.FC<TenderDetailProps> = ({ contratacao, onBack, onOpenGraph }) => {
  const [activeTab, setActiveTab] = useState<'sinais' | 'itens' | 'fracionamento' | 'custodia'>('sinais');

  const iea = contratacao.iea;
  const score = iea?.valorIea || 0;
  const nivel: NivelRisco = iea?.nivelRisco || 'Baixo';

  const getScoreColor = (n: NivelRisco) => {
    switch (n) {
      case 'Elevado':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'Médio':
        return 'text-amber-600 bg-amber-50 border-amber-200';
      default:
        return 'text-emerald-600 bg-emerald-50 border-emerald-200';
    }
  };

  const formatCurrency = (val?: number) => {
    if (!val) return 'R$ 0,00';
    return val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  };

  return (
    <div className="space-y-6">
      {/* Botão Voltar e Ações */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 bg-white border border-slate-200 px-3 py-2 rounded-lg shadow-sm transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Voltar para Listagem</span>
        </button>

        <div className="flex items-center gap-2">
          {contratacao.urlPncp && (
            <a
              href={contratacao.urlPncp}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-700 hover:text-slate-900 bg-white border border-slate-300 px-3 py-2 rounded-lg shadow-sm transition"
            >
              <span>Ver no PNCP Oficial</span>
              <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
            </a>
          )}

          <button
            onClick={() => onOpenGraph(contratacao.id)}
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 px-3.5 py-2 rounded-lg shadow-sm transition"
          >
            <Network className="w-4 h-4 text-indigo-600" />
            <span>Explorar Grafo</span>
          </button>

          <a
            href={apiService.getDossiePdfUrl(contratacao.id)}
            download
            className="inline-flex items-center gap-1.5 text-xs font-bold text-white bg-teal-600 hover:bg-teal-700 px-4 py-2 rounded-lg shadow transition"
          >
            <FileDown className="w-4 h-4" />
            <span>Baixar Dossiê PDF Forense</span>
          </a>
        </div>
      </div>

      {/* Card Principal: Resumo & Velocímetro IEA */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
        {/* Dados da Contratação */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center gap-2">
            <span className="bg-slate-100 text-slate-700 text-xs font-bold px-2.5 py-1 rounded border border-slate-300">
              {contratacao.modalidadeNome}
            </span>
            <span className="text-xs text-slate-500">Ano: {contratacao.anoCompra}</span>
            <span className="text-xs text-slate-500">• UF: {contratacao.uf} (Paraíba)</span>
          </div>

          <h1 className="text-lg font-bold text-slate-900 leading-snug">
            {contratacao.numeroControlePncp}
          </h1>

          <p className="text-xs text-slate-600 leading-relaxed">
            {contratacao.objeto || 'Sem descrição cadastrada'}
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2 text-xs">
            <div>
              <span className="text-slate-400 block">Órgão Comprador:</span>
              <span className="font-semibold text-slate-800">
                {contratacao.orgao?.nomeOrgao || 'N/D'}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block">CNPJ Órgão:</span>
              <span className="font-mono text-slate-700">{contratacao.orgao?.cnpj || 'N/D'}</span>
            </div>
            <div>
              <span className="text-slate-400 block">Valor Homologado:</span>
              <span className="font-bold text-slate-900">
                {formatCurrency(contratacao.valorTotalHomologado)}
              </span>
            </div>
          </div>
        </div>

        {/* Medidor IEA */}
        <div className={`p-5 rounded-xl border flex flex-col items-center justify-center text-center ${getScoreColor(nivel)}`}>
          <span className="text-xs font-bold uppercase tracking-wider">Índice IEA</span>
          <div className="text-4xl font-black my-1">{score.toFixed(1)}</div>
          <span className="text-xs font-bold uppercase tracking-wider px-3 py-0.5 rounded-full bg-white/80 border border-current shadow-sm">
            Nível {nivel}
          </span>

          <div className="mt-3 pt-3 border-t border-current/20 text-[11px] space-y-1 w-full text-left">
            <div className="flex justify-between">
              <span>Eixos Independentes:</span>
              <span className="font-bold">{iea?.qtdEixosIndependentes || 0} de 4</span>
            </div>
            <div className="flex justify-between">
              <span>Regra Multieixo (SG-04):</span>
              <span className="font-bold">{iea?.multiEixoValido ? 'Conforme' : 'Sem Elevação'}</span>
            </div>
            <div className="flex justify-between">
              <span>Versão Parâmetros:</span>
              <span className="font-mono">{iea?.versaoParametros || 'v1.0.0'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Aviso Metodológico Obrigatório (SG-03) */}
      <MethodologicalNotice />

      {/* Tabs Analíticas */}
      <div className="border-b border-slate-200 flex gap-4 text-xs font-semibold">
        <button
          onClick={() => setActiveTab('sinais')}
          className={`pb-2.5 transition border-b-2 ${
            activeTab === 'sinais'
              ? 'border-teal-600 text-teal-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Decomposição dos Sinais (SG-02)
        </button>

        <button
          onClick={() => setActiveTab('fracionamento')}
          className={`pb-2.5 transition border-b-2 ${
            activeTab === 'fracionamento'
              ? 'border-teal-600 text-teal-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Linha do Tempo de Fracionamento (RF-UI-05)
        </button>

        <button
          onClick={() => setActiveTab('itens')}
          className={`pb-2.5 transition border-b-2 ${
            activeTab === 'itens'
              ? 'border-teal-600 text-teal-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Itens Homologados ({contratacao.itens?.length || 0})
        </button>

        <button
          onClick={() => setActiveTab('custodia')}
          className={`pb-2.5 transition border-b-2 ${
            activeTab === 'custodia'
              ? 'border-teal-600 text-teal-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Cadeia de Custódia Forense (SHA-256)
        </button>
      </div>

      {/* Conteúdo da Tab Ativa */}
      {activeTab === 'sinais' && (
        <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm space-y-4">
          <h3 className="font-bold text-sm text-slate-900">
            Detalhamento Transparente dos Sinais Analíticos (SG-02 / Art. 19-B)
          </h3>

          {iea?.decomposicaoSinais && iea.decomposicaoSinais.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                  <tr>
                    <th className="py-2.5 px-3">Sinal</th>
                    <th className="py-2.5 px-3">Eixo</th>
                    <th className="py-2.5 px-3 text-right">Escore ($s_i$)</th>
                    <th className="py-2.5 px-3 text-right">Confiança ($c_i$)</th>
                    <th className="py-2.5 px-3 text-right">Peso ($w_i$)</th>
                    <th className="py-2.5 px-3 text-right">Contribuição</th>
                    <th className="py-2.5 px-3">Detalhamento Metodológico</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {iea.decomposicaoSinais.map((s, idx) => (
                    <tr key={idx} className="hover:bg-slate-50">
                      <td className="py-2.5 px-3 font-semibold text-slate-800">{s.sinal}</td>
                      <td className="py-2.5 px-3 text-slate-600">{s.eixo}</td>
                      <td className="py-2.5 px-3 text-right font-mono">{s.escore.toFixed(2)}</td>
                      <td className="py-2.5 px-3 text-right font-mono">{s.confianca.toFixed(2)}</td>
                      <td className="py-2.5 px-3 text-right font-mono">{s.peso.toFixed(2)}</td>
                      <td className="py-2.5 px-3 text-right font-bold text-teal-700 font-mono">
                        +{s.contribuicaoPonderada.toFixed(1)}
                      </td>
                      <td className="py-2.5 px-3 text-slate-600">{s.detalhes}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs text-slate-500 py-4">
              Nenhum sinal anômalo relevante acima dos limiares de tolerância foi detectado para esta contratação.
            </p>
          )}
        </div>
      )}

      {activeTab === 'fracionamento' && (
        <FracionamentoTimeline />
      )}

      {activeTab === 'itens' && (
        <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm space-y-4">
          <h3 className="font-bold text-sm text-slate-900">Itens e Serviços da Contratação</h3>
          {contratacao.itens && contratacao.itens.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                  <tr>
                    <th className="py-2.5 px-3">#</th>
                    <th className="py-2.5 px-3">Descrição do Item</th>
                    <th className="py-2.5 px-3">CATMAT</th>
                    <th className="py-2.5 px-3 text-right">Qtd</th>
                    <th className="py-2.5 px-3 text-right">Valor Unitário</th>
                    <th className="py-2.5 px-3 text-right">Valor Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {contratacao.itens.map((i) => (
                    <tr key={i.id} className="hover:bg-slate-50">
                      <td className="py-2.5 px-3 font-semibold text-slate-500">{i.numeroItem}</td>
                      <td className="py-2.5 px-3 text-slate-800">{i.descricao}</td>
                      <td className="py-2.5 px-3 font-mono text-slate-500">{i.codigoCatmatCatser || 'N/D'}</td>
                      <td className="py-2.5 px-3 text-right">{i.quantidade || 1} {i.unidadeMedida}</td>
                      <td className="py-2.5 px-3 text-right font-mono">{formatCurrency(i.valorUnitarioHomologado)}</td>
                      <td className="py-2.5 px-3 text-right font-bold text-slate-900 font-mono">{formatCurrency(i.valorTotal)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs text-slate-500">Sem itens discriminados no payload bruto.</p>
          )}
        </div>
      )}

      {activeTab === 'custodia' && (
        <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm space-y-4">
          <h3 className="font-bold text-sm text-slate-900">
            Cadeia de Custódia Digital Forense (RF-REL-03)
          </h3>
          <p className="text-xs text-slate-500">
            Identificadores criptográficos imutáveis SHA-256 gerados no momento da ingestão primária para garantir
            reprodutibilidade e integridade pericial.
          </p>

          <div className="space-y-3">
            {contratacao.achados?.map((a) =>
              a.evidencias?.map((e) => (
                <div key={e.id} className="p-3 bg-slate-50 border border-slate-200 rounded text-xs space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-slate-800">
                      Evidência Eixo: {a.eixo} ({a.sinal})
                    </span>
                    <span className="text-[11px] text-slate-400">Competência: {e.competenciaBase}</span>
                  </div>
                  <div className="font-mono text-[11px] text-slate-700 break-all bg-white p-2 rounded border border-slate-200">
                    SHA-256: {e.hashSha256}
                  </div>
                  <div className="text-[11px] text-slate-500 truncate">Fonte: {e.urlFonte}</div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};
