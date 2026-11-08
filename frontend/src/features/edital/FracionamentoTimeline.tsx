import React from 'react';
import { Calendar, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface CompraEvento {
  id: string;
  data: string;
  valor: number;
  orgao: string;
  catmat: string;
}

interface FracionamentoTimelineProps {
  compras?: CompraEvento[];
  tetoLegal?: number;
  limiarExcedido?: boolean;
}

export const FracionamentoTimeline: React.FC<FracionamentoTimelineProps> = ({
  compras = [
    { id: '1', data: '2024-02-10', valor: 18500.0, orgao: 'PM João Pessoa', catmat: '32100' },
    { id: '2', data: '2024-02-28', valor: 24000.0, orgao: 'PM João Pessoa', catmat: '32100' },
    { id: '3', data: '2024-03-15', valor: 22000.0, orgao: 'PM João Pessoa', catmat: '32100' },
  ],
  tetoLegal = 59906.02,
  limiarExcedido = true,
}) => {
  const valorTotal = compras.reduce((acc, c) => acc + c.valor, 0);

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <Calendar className="w-5 h-5 text-teal-600" />
          <h3 className="font-bold text-sm text-slate-900">
            Linha do Tempo de Compras Sucessivas e Janelas Deslizantes (RF-UI-05)
          </h3>
        </div>

        <div className="flex items-center gap-2">
          {limiarExcedido ? (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-700" />
              <span>Sinal de Fracionamento Potencial</span>
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-900 border border-emerald-300">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
              <span>Conforme ao Teto Legal</span>
            </span>
          )}
        </div>
      </div>

      {/* Indicadores Numéricos */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div className="bg-slate-50 p-3 rounded border border-slate-200">
          <span className="text-slate-500">Total Acumulado na Janela (60 dias):</span>
          <div className="font-bold text-sm text-slate-900 mt-0.5">
            {valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </div>
        </div>

        <div className="bg-slate-50 p-3 rounded border border-slate-200">
          <span className="text-slate-500">Teto Legal Vigente (Dec. 11.871/2023):</span>
          <div className="font-bold text-sm text-slate-900 mt-0.5">
            {tetoLegal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </div>
        </div>

        <div className="bg-slate-50 p-3 rounded border border-slate-200">
          <span className="text-slate-500">Diferença / Excedente:</span>
          <div
            className={`font-bold text-sm mt-0.5 ${
              valorTotal > tetoLegal ? 'text-amber-700' : 'text-emerald-700'
            }`}
          >
            {(valorTotal - tetoLegal).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </div>
        </div>
      </div>

      {/* Linha do tempo visual */}
      <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
        {compras.map((compra, idx) => (
          <div key={compra.id} className="relative flex items-start gap-4 text-xs">
            {/* Ponto na timeline */}
            <div className="absolute -left-6 top-1 w-3.5 h-3.5 rounded-full bg-teal-500 border-2 border-white shadow-sm" />

            <div className="flex-1 bg-slate-50 p-3 rounded border border-slate-200 hover:border-teal-300 transition">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-slate-800">
                  Compra #{idx + 1} — Dispensa de Licitação
                </span>
                <span className="text-slate-500 font-mono">{compra.data}</span>
              </div>
              <div className="text-slate-600 flex justify-between">
                <span>{compra.orgao} • CATMAT {compra.catmat}</span>
                <span className="font-semibold text-slate-900">
                  {compra.valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
