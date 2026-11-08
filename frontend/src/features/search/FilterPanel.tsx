import React from 'react';
import { Filter, RotateCcw } from 'lucide-react';
import { NivelRisco } from '../../api/types';

interface FilterPanelProps {
  selectedUf: string;
  setSelectedUf: (uf: string) => void;
  selectedAno: number | undefined;
  setSelectedAno: (ano: number | undefined) => void;
  selectedRisco: NivelRisco | 'Todos';
  setSelectedRisco: (risco: NivelRisco | 'Todos') => void;
  onReset: () => void;
}

export const FilterPanel: React.FC<FilterPanelProps> = ({
  selectedUf,
  setSelectedUf,
  selectedAno,
  setSelectedAno,
  selectedRisco,
  setSelectedRisco,
  onReset,
}) => {
  return (
    <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
      <div className="flex items-center gap-2 text-slate-700 font-semibold text-sm">
        <Filter className="w-4 h-4 text-teal-600" />
        <span>Filtros Analíticos</span>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        {/* UF (Travado em PB no piloto) */}
        <div className="flex items-center gap-1.5 text-xs">
          <label className="text-slate-500 font-medium">UF:</label>
          <select
            value={selectedUf}
            onChange={(e) => setSelectedUf(e.target.value)}
            className="border border-slate-300 rounded px-2.5 py-1.5 bg-slate-50 text-slate-800 font-medium focus:ring-1 focus:ring-teal-500"
          >
            <option value="PB">Paraíba (PB - Piloto)</option>
          </select>
        </div>

        {/* Ano */}
        <div className="flex items-center gap-1.5 text-xs">
          <label className="text-slate-500 font-medium">Ano:</label>
          <select
            value={selectedAno || ''}
            onChange={(e) => setSelectedAno(e.target.value ? Number(e.target.value) : undefined)}
            className="border border-slate-300 rounded px-2.5 py-1.5 bg-white text-slate-800 focus:ring-1 focus:ring-teal-500"
          >
            <option value="">Todos os Anos</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
            <option value="2022">2022</option>
            <option value="2021">2021</option>
          </select>
        </div>

        {/* Nível de Risco IEA */}
        <div className="flex items-center gap-1.5 text-xs">
          <label className="text-slate-500 font-medium">Exposição IEA:</label>
          <select
            value={selectedRisco}
            onChange={(e) => setSelectedRisco(e.target.value as NivelRisco | 'Todos')}
            className="border border-slate-300 rounded px-2.5 py-1.5 bg-white text-slate-800 focus:ring-1 focus:ring-teal-500 font-medium"
          >
            <option value="Todos">Todas as Faixas</option>
            <option value="Elevado">Apenas Elevado (≥ 60)</option>
            <option value="Médio">Apenas Médio (30 a 59)</option>
            <option value="Baixo">Apenas Baixo (&lt; 30)</option>
          </select>
        </div>

        {/* Botão Reset */}
        <button
          onClick={onReset}
          className="text-xs text-slate-500 hover:text-slate-800 flex items-center gap-1 px-2.5 py-1.5 rounded border border-slate-200 hover:bg-slate-50 transition"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Limpar</span>
        </button>
      </div>
    </div>
  );
};
