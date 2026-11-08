import React from 'react';
import { ShieldCheck, Network, FileCheck2, UserCheck2, HelpCircle } from 'lucide-react';

interface NavbarProps {
  currentTab: 'search' | 'graph' | 'verifier' | 'contestation';
  setCurrentTab: (tab: 'search' | 'graph' | 'verifier' | 'contestation') => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentTab, setCurrentTab }) => {
  return (
    <header className="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        {/* Logo and Pilot badge */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setCurrentTab('search')}>
          <div className="w-9 h-9 rounded-lg bg-teal-500 flex items-center justify-center text-slate-950 font-black shadow-md">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg tracking-tight text-white">NexusGov</span>
              <span className="bg-teal-500/20 text-teal-300 border border-teal-500/40 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                Piloto PB (IBGE 25)
              </span>
            </div>
            <p className="text-[11px] text-slate-400">Auditoria Forense de Contratações (Lei 14.133/2021)</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 sm:gap-2">
          <button
            onClick={() => setCurrentTab('search')}
            className={`px-3 py-2 rounded-md text-xs sm:text-sm font-medium transition flex items-center gap-1.5 ${
              currentTab === 'search'
                ? 'bg-teal-600 text-white shadow'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'
            }`}
          >
            <span>Contratações</span>
          </button>

          <button
            onClick={() => setCurrentTab('verifier')}
            className={`px-3 py-2 rounded-md text-xs sm:text-sm font-medium transition flex items-center gap-1.5 ${
              currentTab === 'verifier'
                ? 'bg-teal-600 text-white shadow'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'
            }`}
          >
            <FileCheck2 className="w-4 h-4" />
            <span>Verificador SHA-256</span>
          </button>

          <button
            onClick={() => setCurrentTab('contestation')}
            className={`px-3 py-2 rounded-md text-xs sm:text-sm font-medium transition flex items-center gap-1.5 ${
              currentTab === 'contestation'
                ? 'bg-teal-600 text-white shadow'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'
            }`}
          >
            <UserCheck2 className="w-4 h-4" />
            <span>Retificação Cadastral</span>
          </button>
        </nav>
      </div>
    </header>
  );
};
