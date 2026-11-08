import React, { useState } from 'react';
import { apiService } from '../../api/client';
import { ResultadoVerificacao } from '../../api/types';
import { ShieldCheck, ShieldAlert, FileText, CheckCircle2, AlertOctagon } from 'lucide-react';

export const DossierVerifier: React.FC = () => {
  const [payloadBruto, setPayloadBruto] = useState('');
  const [hashEsperado, setHashEsperado] = useState('');
  const [resultado, setResultado] = useState<ResultadoVerificacao | null>(null);
  const [loading, setLoading] = useState(false);

  const handleVerificar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!payloadBruto || !hashEsperado) return;

    setLoading(true);
    try {
      const res = await apiService.verificarIntegridade(payloadBruto, hashEsperado);
      setResultado(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExemplo = () => {
    const exemplo = '{"edital": "001/2024", "orgao": "Prefeitura Municipal de João Pessoa", "valor": 45000.00}';
    setPayloadBruto(exemplo);
    // SHA-256 de exemplo
    setHashEsperado('8ac2ff1d68019a7ee1d8bb699a77eeac93d9b4b0e5015b367123aa17666d628f');
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-teal-50 text-teal-700 rounded-lg border border-teal-200">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">
                Verificador Independente de Integridade Forense (RF-REL-04)
              </h2>
              <p className="text-xs text-slate-500">
                Valide a cadeia de custódia confrontando o payload bruto com o hash criptográfico SHA-256
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={handleExemplo}
            className="text-xs text-teal-700 hover:text-teal-900 font-semibold underline"
          >
            Carregar Exemplo
          </button>
        </div>

        <form onSubmit={handleVerificar} className="space-y-4 text-xs">
          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              Payload Bruto ou Trecho de Evidência:
            </label>
            <textarea
              rows={5}
              value={payloadBruto}
              onChange={(e) => setPayloadBruto(e.target.value)}
              placeholder="Cole aqui o JSON ou texto original da evidência..."
              className="w-full p-3 font-mono border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:outline-none bg-slate-50"
              required
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              Hash Criptográfico SHA-256 Esperado:
            </label>
            <input
              type="text"
              value={hashEsperado}
              onChange={(e) => setHashEsperado(e.target.value)}
              placeholder="64 caracteres hexadecimais..."
              className="w-full p-2.5 font-mono border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:outline-none"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-teal-600 hover:bg-teal-700 text-white font-bold rounded-lg shadow transition disabled:opacity-50 text-sm flex items-center justify-center gap-2"
          >
            {loading ? 'Calculando Hash e Confrontando Evidência...' : 'Conferir Integridade Pericial'}
          </button>
        </form>

        {resultado && (
          <div
            className={`p-4 rounded-lg border text-xs space-y-2 mt-4 ${
              resultado.integro
                ? 'bg-emerald-50 border-emerald-300 text-emerald-950'
                : 'bg-red-50 border-red-300 text-red-950'
            }`}
          >
            <div className="flex items-center gap-2 font-bold text-sm">
              {resultado.integro ? (
                <>
                  <CheckCircle2 className="w-5 h-5 text-emerald-700" />
                  <span>INTEGRIDADE CRIPTOGRÁFICA CONFIRMADA</span>
                </>
              ) : (
                <>
                  <AlertOctagon className="w-5 h-5 text-red-700" />
                  <span>DIVERGÊNCIA DE INTEGRIDADE DETECTADA</span>
                </>
              )}
            </div>

            <p>{resultado.mensagem}</p>

            <div className="pt-2 border-t border-current/20 space-y-1 font-mono text-[11px]">
              <div>
                <span className="font-semibold">Hash Calculado: </span>
                <span>{resultado.hashCalculado}</span>
              </div>
              <div>
                <span className="font-semibold">Hash Esperado: </span>
                <span>{resultado.hashEsperado}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
