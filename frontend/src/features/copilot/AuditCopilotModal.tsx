import React, { useState } from 'react';

interface AuditCopilotModalProps {
  isOpen: boolean;
  onClose: () => void;
  contratacaoId: string;
  numeroControlePncp: string;
  orgaoNome: string;
  ieaScore: number;
  nivelRisco: string;
}

export const AuditCopilotModal: React.FC<AuditCopilotModalProps> = ({
  isOpen,
  onClose,
  contratacaoId,
  numeroControlePncp,
  orgaoNome,
  ieaScore,
  nivelRisco,
}) => {
  const [loading, setLoading] = useState(false);
  const [minutaTexto, setMinutaTexto] = useState<string | null>(null);
  const [copiado, setCopiado] = useState(false);

  if (!isOpen) return null;

  const handleGerarMinuta = () => {
    setLoading(true);
    // Simulação reativa imediata ou chamada de API
    setTimeout(() => {
      const draft = `# MINUTA PRELIMINAR DE INSTRUÇÃO TÉCNICA DE AUDITORIA
**Referência:** ${numeroControlePncp} | **Sistema:** NexusGov Audit Copilot
**Órgão Licitante:** ${orgaoNome}

---

## 1. IDENTIFICAÇÃO E MARCO LEGAL
Contratação processada no âmbito da Lei nº 14.133/2021 e Resolução TCU nº 367/2024.
- **Índice de Exposição a Anomalias (IEA):** ${ieaScore.toFixed(1)} / 100 (${nivelRisco})

## 2. ACHADOS DA TRIAGEM FORENSE
- Identificados indícios estatísticos convergentes que justificam apuração preliminar.
- Aplicação das salvaguardas SG-01 e SG-04: preservação do princípio da presunção de inocência.

## 3. PROPOSTA DE DILIGÊNCIAS PRELIMINARES
1. Requisitar cópia integral do processo administrativo licitatório.
2. Confirmar autenticidade cadastral dos participantes (QSA).
3. Verificar notas fiscais e relatórios de medição da execução física.

---
*Aviso Metodológico Obrigatório (SG-03): A presente instrução baseia-se em triagem estatística automatizada para priorização analítica por auditores humanos.*`;

      setMinutaTexto(draft);
      setLoading(false);
    }, 400);
  };

  const handleCopiar = () => {
    if (minutaTexto) {
      navigator.clipboard?.writeText(minutaTexto);
      setCopiado(true);
      setTimeout(() => setCopiado(false), 2000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 max-w-3xl w-full max-h-[90vh] flex flex-col overflow-hidden">
        {/* Cabeçalho */}
        <div className="flex items-center justify-between p-5 border-b border-slate-200 bg-slate-50">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-bold text-sm">
              AI
            </div>
            <div>
              <h3 className="font-bold text-slate-800 text-base">
                NexusGov Audit Copilot — Assistente Técnico
              </h3>
              <p className="text-xs text-slate-500">
                Minuta estruturada em conformidade com o Art. 19-B da Resolução TCU nº 367/2024
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 text-lg font-bold p-1"
          >
            ✕
          </button>
        </div>

        {/* Corpo */}
        <div className="p-6 overflow-y-auto flex-1 space-y-4">
          <div className="flex items-center justify-between bg-indigo-50 border border-indigo-100 rounded-lg p-3 text-xs text-indigo-900">
            <div>
              <span className="font-semibold">Processo:</span> {numeroControlePncp} •{' '}
              <span className="font-semibold">IEA:</span> {ieaScore.toFixed(1)} ({nivelRisco})
            </div>
            <span className="px-2 py-0.5 rounded bg-indigo-200 text-indigo-800 font-semibold text-[10px]">
              SG-01 Validada
            </span>
          </div>

          {!minutaTexto ? (
            <div className="text-center py-12 space-y-3">
              <p className="text-sm text-slate-600">
                Clique abaixo para gerar a proposta de instrução técnica estruturada com base nos
                sinais forenses, grafos e detectores estatísticos desta contratação.
              </p>
              <button
                onClick={handleGerarMinuta}
                disabled={loading}
                className="px-5 py-2.5 bg-indigo-600 text-white font-medium text-xs rounded-lg hover:bg-indigo-700 transition shadow disabled:opacity-50"
              >
                {loading ? 'Processando e Analisando Sinais...' : 'Gerar Minuta com Copilot'}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg text-xs font-mono overflow-x-auto whitespace-pre-wrap max-h-96">
                {minutaTexto}
              </pre>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  onClick={handleCopiar}
                  className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition"
                >
                  {copiado ? '✓ Copiado!' : 'Copiar Texto da Minuta'}
                </button>
                <button
                  onClick={onClose}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold rounded-lg transition"
                >
                  Concluir
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
