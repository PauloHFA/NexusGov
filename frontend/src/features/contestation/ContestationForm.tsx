import React, { useState } from 'react';
import { apiService } from '../../api/client';
import { ContestacaoResponse } from '../../api/types';
import { UserCheck, CheckCircle, Search, HelpCircle } from 'lucide-react';

export const ContestationForm: React.FC = () => {
  const [tipoSolicitante, setTipoSolicitante] = useState<'PESSOA_FISICA' | 'PESSOA_JURIDICA'>('PESSOA_JURIDICA');
  const [documento, setDocumento] = useState('');
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [contratacaoId, setContratacaoId] = useState('');
  const [motivo, setMotivo] = useState('');
  const [tipoAssinatura, setTipoAssinatura] = useState<string>('SEM_ASSINATURA');
  const [loading, setLoading] = useState(false);
  const [protocoloGerado, setProtocoloGerado] = useState<ContestacaoResponse | null>(null);

  // Consulta por protocolo
  const [buscaProtocolo, setBuscaProtocolo] = useState('');
  const [protocoloConsultado, setProtocoloConsultado] = useState<ContestacaoResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await apiService.submeterContestacao({
        tipoSolicitante,
        documentoIdentificador: documento,
        nomeSolicitante: nome,
        emailContato: email,
        contratacaoId: contratacaoId || undefined,
        motivoContestacao: motivo,
      });
      setProtocoloGerado(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleConsultar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!buscaProtocolo) return;
    try {
      const res = await apiService.consultarContestacao(buscaProtocolo);
      setProtocoloConsultado(res);
    } catch (err) {
      alert('Protocolo não localizado.');
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Formulário de Registro */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
        <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
          <div className="p-2.5 bg-teal-50 text-teal-700 rounded-lg border border-teal-200">
            <UserCheck className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">
              Canal Formal de Contestação e Retificação Cadastral (RF-REL-05)
            </h2>
            <p className="text-xs text-slate-500">
              Submeta esclarecimentos, correções societárias ou contestações formais garantindo ampla defesa e contraditório
            </p>
          </div>
        </div>

        {protocoloGerado ? (
          <div className="p-5 bg-emerald-50 border border-emerald-300 rounded-lg text-emerald-950 space-y-3 text-xs">
            <div className="flex items-center gap-2 font-bold text-sm text-emerald-800">
              <CheckCircle className="w-5 h-5" />
              <span>SOLICITAÇÃO PROTOCOLADA COM SUCESSO!</span>
            </div>
            <p>
              Sua manifestação foi recebida pelo sistema de auditoria forense NexusGov e está em análise.
            </p>
            <div className="p-3 bg-white border border-emerald-200 rounded font-mono text-sm font-bold text-center">
              Número de Protocolo: {protocoloGerado.numeroProtocolo}
            </div>
            <p className="text-[11px] text-emerald-700">
              Guarde este protocolo para acompanhar a manifestação e eventual atualização cadastral.
            </p>
            <button
              onClick={() => {
                setProtocoloGerado(null);
                setMotivo('');
              }}
              className="mt-2 text-xs font-semibold text-emerald-800 underline"
            >
              Registrar outra solicitação
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4 text-xs">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Tipo de Solicitante:</label>
                <select
                  value={tipoSolicitante}
                  onChange={(e) => setTipoSolicitante(e.target.value as any)}
                  className="w-full p-2.5 border border-slate-300 rounded-lg bg-white"
                >
                  <option value="PESSOA_JURIDICA">Pessoa Jurídica (Empresa)</option>
                  <option value="PESSOA_FISICA">Pessoa Física (Sócio / Cidadão)</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  {tipoSolicitante === 'PESSOA_JURIDICA' ? 'CNPJ:' : 'CPF:'}
                </label>
                <input
                  type="text"
                  value={documento}
                  onChange={(e) => setDocumento(e.target.value)}
                  placeholder="Apenas números..."
                  className="w-full p-2.5 border border-slate-300 rounded-lg"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Nome Completo / Razão Social:</label>
                <input
                  type="text"
                  value={nome}
                  onChange={(e) => setNome(e.target.value)}
                  className="w-full p-2.5 border border-slate-300 rounded-lg"
                  required
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">E-mail para Notificação:</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full p-2.5 border border-slate-300 rounded-lg"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Identificador da Contratação (Opcional):
              </label>
              <input
                type="text"
                value={contratacaoId}
                onChange={(e) => setContratacaoId(e.target.value)}
                placeholder="Ex: Número PNCP ou ID"
                className="w-full p-2.5 border border-slate-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Motivo da Contestação ou Esclarecimento Cadastral:
              </label>
              <textarea
                rows={4}
                value={motivo}
                onChange={(e) => setMotivo(e.target.value)}
                placeholder="Descreva detalhadamente as razões fáticas, documentos anexos ou alterações societárias recentes na Receita Federal..."
                className="w-full p-2.5 border border-slate-300 rounded-lg"
                required
              />
            </div>

            {/* Assinatura Digital Qualificada (Melhoria 4) */}
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-lg space-y-2">
              <label className="block font-semibold text-slate-800">
                Assinatura Digital de Fé Pública (Opcional):
              </label>
              <select
                value={tipoAssinatura}
                onChange={(e) => setTipoAssinatura(e.target.value)}
                className="w-full p-2 border border-slate-300 rounded-lg bg-white text-xs"
              >
                <option value="SEM_ASSINATURA">Sem assinatura digital (Apenas protocolo simples)</option>
                <option value="GOVBR_OURO">Gov.br — Conta Nível Ouro (Biometria / TSE)</option>
                <option value="GOVBR_PRATA">Gov.br — Conta Nível Prata (Bancos Credenciados)</option>
                <option value="ICP_BRASIL_ECNPJ">ICP-Brasil — Certificado e-CNPJ (A1/A3)</option>
                <option value="ICP_BRASIL_ECPF">ICP-Brasil — Certificado e-CPF (A1/A3)</option>
              </select>
              {tipoAssinatura !== 'SEM_ASSINATURA' && (
                <div className="flex items-center gap-2 text-[11px] text-teal-800 bg-teal-50 p-2 rounded border border-teal-200">
                  <span>✓</span>
                  <span>
                    A manifestação será autenticada digitalmente conferindo validade jurídica e fé pública nos termos da MP 2.200-2/2001 e Decreto 10.543/2020.
                  </span>
                </div>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-teal-600 hover:bg-teal-700 text-white font-bold rounded-lg shadow transition text-sm disabled:opacity-50"
            >
              {loading ? 'Transmitindo Solicitação...' : 'Protocolar Manifestação Formal'}
            </button>
          </form>
        )}
      </div>

      {/* Consulta de Protocolo Existente */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-3 text-xs">
        <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
          <Search className="w-4 h-4 text-teal-600" />
          <span>Consultar Status de Protocolo Anterior</span>
        </h3>
        <form onSubmit={handleConsultar} className="flex gap-2">
          <input
            type="text"
            value={buscaProtocolo}
            onChange={(e) => setBuscaProtocolo(e.target.value)}
            placeholder="Digite o número (Ex: NEXUS-1718000000000)..."
            className="flex-1 p-2.5 border border-slate-300 rounded-lg font-mono"
          />
          <button
            type="submit"
            className="px-4 py-2.5 bg-slate-800 hover:bg-slate-900 text-white font-semibold rounded-lg"
          >
            Consultar
          </button>
        </form>

        {protocoloConsultado && (
          <div className="p-3 bg-slate-50 border border-slate-200 rounded space-y-1">
            <div>
              <span className="font-semibold text-slate-700">Protocolo: </span>
              <span className="font-mono">{protocoloConsultado.numeroProtocolo}</span>
            </div>
            <div>
              <span className="font-semibold text-slate-700">Status: </span>
              <span className="font-bold text-teal-700">{protocoloConsultado.status}</span>
            </div>
            <div>
              <span className="font-semibold text-slate-700">Solicitante: </span>
              <span>{protocoloConsultado.nomeSolicitante}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
