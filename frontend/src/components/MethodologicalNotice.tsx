import React from 'react';
import { AlertCircle, Scale } from 'lucide-react';

export const METHODOLOGICAL_TEXT =
  'AVISO METODOLÓGICO REGULAMENTAR (Resolução TCU nº 367/2024, Art. 19-B): ' +
  'As análises apresentadas nesta plataforma constituem triagem estatística probabilística baseada em dados públicos ' +
  'abertos (PNCP, Receita Federal e IBGE). As classificações de risco e os Índices de Exposição a Anomalias (IEA) ' +
  'representam indicadores analíticos e NÃO configuram juízo de culpa, acusação formal, declaração de conluio ou ilicitude. ' +
  'A investigação conclusiva compete exclusivamente aos órgãos de controle e persecução competentes, respeitando-se o contraditório e a ampla defesa.';

export const MethodologicalNotice: React.FC<{ compact?: boolean }> = ({ compact = false }) => {
  if (compact) {
    return (
      <div
        role="complementary"
        aria-label="Aviso Metodológico Regulamentar"
        className="bg-indigo-50 border-l-4 border-indigo-600 p-3 text-xs text-indigo-900 flex items-center justify-between gap-3 shadow-sm"
      >
        <div className="flex items-center gap-2">
          <Scale className="w-4 h-4 text-indigo-700 shrink-0" />
          <span className="font-semibold text-indigo-950">Aviso Regulamentar (TCU 367/2024):</span>
          <span className="line-clamp-1">{METHODOLOGICAL_TEXT}</span>
        </div>
        <span className="text-[10px] uppercase font-bold tracking-wider text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">
          SG-03 / Salvaguarda
        </span>
      </div>
    );
  }

  return (
    <aside
      role="complementary"
      aria-label="Aviso Metodológico Regulamentar"
      className="bg-gradient-to-r from-indigo-50 to-slate-50 border border-indigo-200 rounded-lg p-4 shadow-sm my-4"
    >
      <div className="flex items-start gap-3">
        <div className="p-2 bg-indigo-600 text-white rounded-md mt-0.5">
          <Scale className="w-5 h-5" />
        </div>
        <div className="flex-1 text-xs text-indigo-950 leading-relaxed">
          <div className="flex items-center gap-2 font-bold text-sm text-indigo-900 mb-1">
            <span>Aviso Metodológico Regulamentar</span>
            <span className="text-[10px] font-semibold bg-indigo-200 text-indigo-900 px-2 py-0.5 rounded-full">
              Resolução TCU nº 367/2024 (Art. 19-B)
            </span>
          </div>
          <p>{METHODOLOGICAL_TEXT}</p>
        </div>
      </div>
    </aside>
  );
};
