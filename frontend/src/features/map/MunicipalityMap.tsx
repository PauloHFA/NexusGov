import React, { useState } from 'react';

export interface MunicipalityRiskSummary {
  codigoIbge: string;
  nome: string;
  uf: string;
  ieaMedio: number;
  totalContratacoes: number;
  volumeFinanceiroTotal: number;
  nivelRiscoPredominante: 'Baixo' | 'Médio' | 'Elevado';
}

interface MunicipalityMapProps {
  municipios?: MunicipalityRiskSummary[];
  onSelectMunicipality?: (codigoIbge: string) => void;
}

const DEFAULT_PARAIBA_MUNICIPIOS: MunicipalityRiskSummary[] = [
  {
    codigoIbge: '2507507',
    nome: 'João Pessoa',
    uf: 'PB',
    ieaMedio: 38.4,
    totalContratacoes: 412,
    volumeFinanceiroTotal: 48500000.0,
    nivelRiscoPredominante: 'Médio',
  },
  {
    codigoIbge: '2504009',
    nome: 'Campina Grande',
    uf: 'PB',
    ieaMedio: 44.2,
    totalContratacoes: 285,
    volumeFinanceiroTotal: 31200000.0,
    nivelRiscoPredominante: 'Médio',
  },
  {
    codigoIbge: '2510808',
    nome: 'Patos',
    uf: 'PB',
    ieaMedio: 62.1,
    totalContratacoes: 94,
    volumeFinanceiroTotal: 9800000.0,
    nivelRiscoPredominante: 'Elevado',
  },
  {
    codigoIbge: '2513703',
    nome: 'Santa Rita',
    uf: 'PB',
    ieaMedio: 26.5,
    totalContratacoes: 78,
    volumeFinanceiroTotal: 7400000.0,
    nivelRiscoPredominante: 'Baixo',
  },
  {
    codigoIbge: '2503704',
    nome: 'Cajazeiras',
    uf: 'PB',
    ieaMedio: 31.0,
    totalContratacoes: 63,
    volumeFinanceiroTotal: 5900000.0,
    nivelRiscoPredominante: 'Médio',
  },
  {
    codigoIbge: '2516201',
    nome: 'Sousa',
    uf: 'PB',
    ieaMedio: 22.8,
    totalContratacoes: 52,
    volumeFinanceiroTotal: 4300000.0,
    nivelRiscoPredominante: 'Baixo',
  },
];

export const MunicipalityMap: React.FC<MunicipalityMapProps> = ({
  municipios = DEFAULT_PARAIBA_MUNICIPIOS,
  onSelectMunicipality,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCity, setSelectedCity] = useState<MunicipalityRiskSummary | null>(null);

  const filtered = municipios.filter(
    (m) =>
      m.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
      m.codigoIbge.includes(searchTerm)
  );

  const handleSelect = (m: MunicipalityRiskSummary) => {
    setSelectedCity(m);
    if (onSelectMunicipality) {
      onSelectMunicipality(m.codigoIbge);
    }
  };

  const getBadgeClass = (nivel: string) => {
    switch (nivel) {
      case 'Elevado':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'Médio':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      default:
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
    }
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-4 border-b border-slate-200 gap-3">
        <div>
          <h3 className="text-lg font-bold text-slate-800">
            Distribuição Territorial de Exposição — Piloto Paraíba (PB)
          </h3>
          <p className="text-xs text-slate-500">
            Métricas agregadas por município (sem dados pessoais de PII per LGPD Art. 12)
          </p>
        </div>
        <div className="w-full sm:w-64">
          <input
            type="text"
            placeholder="Filtrar município ou código IBGE..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full text-xs px-3 py-1.5 border border-slate-300 rounded focus:ring-1 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-5">
        <div className="lg:col-span-2 space-y-2 max-h-96 overflow-y-auto pr-1">
          {filtered.map((m) => (
            <div
              key={m.codigoIbge}
              onClick={() => handleSelect(m)}
              className={`p-3.5 rounded-lg border cursor-pointer transition flex items-center justify-between ${
                selectedCity?.codigoIbge === m.codigoIbge
                  ? 'border-blue-500 bg-blue-50/50'
                  : 'border-slate-200 hover:border-slate-300 bg-white'
              }`}
            >
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-sm text-slate-800">{m.nome}</span>
                  <span className="text-xs text-slate-400">IBGE {m.codigoIbge}</span>
                </div>
                <div className="text-xs text-slate-500 mt-1">
                  {m.totalContratacoes} contratações analisadas • Volume: R${' '}
                  {m.volumeFinanceiroTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <div className="text-xs text-slate-500">IEA Médio</div>
                  <div className="font-bold text-sm text-slate-800">{m.ieaMedio.toFixed(1)}</div>
                </div>
                <span
                  className={`text-xs px-2.5 py-1 font-semibold rounded border ${getBadgeClass(
                    m.nivelRiscoPredominante
                  )}`}
                >
                  {m.nivelRiscoPredominante}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-600 mb-3">
            Detalhamento do Território
          </h4>
          {selectedCity ? (
            <div className="space-y-3">
              <div>
                <span className="text-xs text-slate-500">Município Selecionado</span>
                <p className="font-bold text-base text-slate-800">
                  {selectedCity.nome} - {selectedCity.uf}
                </p>
                <p className="text-xs text-slate-400">Código IBGE: {selectedCity.codigoIbge}</p>
              </div>

              <div className="pt-2 border-t border-slate-200">
                <span className="text-xs text-slate-500">Índice Médio IEA</span>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-2xl font-black text-slate-900">
                    {selectedCity.ieaMedio.toFixed(1)}
                  </span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-bold border ${getBadgeClass(
                      selectedCity.nivelRiscoPredominante
                    )}`}
                  >
                    {selectedCity.nivelRiscoPredominante}
                  </span>
                </div>
              </div>

              <div className="pt-2 border-t border-slate-200">
                <span className="text-xs text-slate-500">Volume Homologado</span>
                <p className="font-semibold text-sm text-slate-800 mt-0.5">
                  R$ {selectedCity.volumeFinanceiroTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-200">
                <span className="text-xs text-slate-500">Contratações Registradas</span>
                <p className="font-semibold text-sm text-slate-800 mt-0.5">
                  {selectedCity.totalContratacoes} processos
                </p>
              </div>
            </div>
          ) : (
            <div className="text-center py-10 text-xs text-slate-400">
              Selecione um município ao lado para inspecionar os indicadores territoriais agregados.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
