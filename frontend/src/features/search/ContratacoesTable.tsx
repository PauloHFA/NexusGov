import React from 'react';
import { ContratacaoSummary, NivelRisco } from '../../api/types';
import { Eye, Network, ChevronLeft, ChevronRight, FileText } from 'lucide-react';

interface ContratacoesTableProps {
  contratacoes: ContratacaoSummary[];
  onSelect: (id: string) => void;
  onOpenGraph: (id: string) => void;
  page: number;
  totalPages: number;
  onPageChange: (newPage: number) => void;
  loading: boolean;
}

export const ContratacoesTable: React.FC<ContratacoesTableProps> = ({
  contratacoes,
  onSelect,
  onOpenGraph,
  page,
  totalPages,
  onPageChange,
  loading,
}) => {
  const getBadgeClass = (risco?: NivelRisco) => {
    switch (risco) {
      case 'Elevado':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'Médio':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      default:
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
    }
  };

  const formatCurrency = (val?: number) => {
    if (!val) return 'R$ 0,00';
    return val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  };

  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-100 text-slate-700 uppercase font-semibold border-b border-slate-200 tracking-wider">
            <tr>
              <th className="py-3 px-4">Contratação / PNCP</th>
              <th className="py-3 px-4">Órgão Comprador</th>
              <th className="py-3 px-4">Objeto</th>
              <th className="py-3 px-4">Valor Homologado</th>
              <th className="py-3 px-4 text-center">Índice IEA</th>
              <th className="py-3 px-4 text-center">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {loading ? (
              <tr>
                <td colSpan={6} className="py-8 text-center text-slate-500">
                  Carregando contratações do estado da Paraíba...
                </td>
              </tr>
            ) : contratacoes.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-8 text-center text-slate-500">
                  Nenhuma contratação encontrada com os filtros selecionados.
                </td>
              </tr>
            ) : (
              contratacoes.map((c) => (
                <tr key={c.id} className="hover:bg-slate-50 transition">
                  <td className="py-3 px-4">
                    <div className="font-semibold text-slate-900 line-clamp-1">{c.numeroControlePncp}</div>
                    <div className="text-[11px] text-slate-500">
                      {c.modalidadeNome} • Ano {c.anoCompra}
                    </div>
                  </td>

                  <td className="py-3 px-4">
                    <div className="font-medium text-slate-800 line-clamp-1">{c.orgaoNome || 'Não informado'}</div>
                    <div className="text-[11px] text-slate-500">
                      CNPJ: {c.orgaoCnpj || 'N/D'} • UF: {c.uf}
                    </div>
                  </td>

                  <td className="py-3 px-4 max-w-xs">
                    <p className="line-clamp-2 text-slate-700">{c.objeto || 'Sem descrição'}</p>
                  </td>

                  <td className="py-3 px-4 font-semibold text-slate-900 whitespace-nowrap">
                    {formatCurrency(c.valorTotalHomologado)}
                  </td>

                  <td className="py-3 px-4 text-center whitespace-nowrap">
                    <span
                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold border ${getBadgeClass(
                        c.nivelRisco
                      )}`}
                    >
                      <span>IEA {c.ieaScore !== undefined ? c.ieaScore.toFixed(1) : '0.0'}</span>
                      <span className="text-[10px] font-normal uppercase">({c.nivelRisco || 'Baixo'})</span>
                    </span>
                  </td>

                  <td className="py-3 px-4 text-center whitespace-nowrap">
                    <div className="flex items-center justify-center gap-2">
                      <button
                        onClick={() => onSelect(c.id)}
                        className="p-1.5 text-teal-700 hover:bg-teal-50 rounded border border-teal-200 transition"
                        title="Ver Ficha Técnica Detalhada"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => onOpenGraph(c.id)}
                        className="p-1.5 text-indigo-700 hover:bg-indigo-50 rounded border border-indigo-200 transition"
                        title="Explorar Grafo de Relações"
                      >
                        <Network className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="p-3 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600">
        <div>
          Página <span className="font-semibold text-slate-900">{page + 1}</span> de{' '}
          <span className="font-semibold text-slate-900">{Math.max(1, totalPages)}</span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 0}
            className="p-1.5 rounded border border-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-white transition"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= totalPages - 1}
            className="p-1.5 rounded border border-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-white transition"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
