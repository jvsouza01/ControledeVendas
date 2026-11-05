import React from 'react';
import { LeadProvider, useLeads } from './context/LeadContext';
import { Header } from './components/Header';
import { FollowUpAlertBanner } from './components/FollowUpAlertBanner';
import { KanbanBoard } from './components/KanbanBoard';
import { TableView } from './components/TableView';
import { MetricsDashboard } from './components/MetricsDashboard';
import { LeadModal } from './components/LeadModal';
import { LeadDetailDrawer } from './components/LeadDetailDrawer';
import { ExcelImportModal } from './components/ExcelImportModal';
import { Sparkles, User, Users, Filter } from 'lucide-react';

const MainContent: React.FC = () => {
  const { viewMode, leads, filteredLeads, filters, setFilters } = useLeads();

  const totalCount = leads.length;
  const minedCount = leads.filter((l) => l.id.startsWith('fb_')).length;
  const userCount = leads.filter((l) => !l.id.startsWith('fb_')).length;

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Banner de Follow-ups Urgentes */}
        <FollowUpAlertBanner />

        {/* Barra de Filtro Rápido de Origem: Todos | Novos Minerados | Meus Cadastrados */}
        <div className="flex flex-wrap items-center justify-between gap-3 mb-4 bg-white/90 p-2.5 rounded-xl border border-slate-200/90 shadow-xs">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-semibold text-slate-500 mr-1 flex items-center gap-1.5">
              <Filter className="w-3.5 h-3.5 text-slate-400" />
              Origem dos Leads:
            </span>

            <button
              onClick={() => setFilters((prev) => ({ ...prev, origemTipo: 'todos' }))}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                (filters.origemTipo || 'todos') === 'todos'
                  ? 'bg-slate-900 text-white shadow-xs font-bold'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200'
              }`}
            >
              <Users className="w-3.5 h-3.5" />
              <span>Todos ({totalCount})</span>
            </button>

            <button
              onClick={() => setFilters((prev) => ({ ...prev, origemTipo: 'minerados' }))}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                filters.origemTipo === 'minerados'
                  ? 'bg-emerald-600 text-white shadow-xs font-bold'
                  : 'bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-emerald-500 animate-pulse" />
              <span>✨ Novos Minerados ({minedCount})</span>
            </button>

            <button
              onClick={() => setFilters((prev) => ({ ...prev, origemTipo: 'cadastrados' }))}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                filters.origemTipo === 'cadastrados'
                  ? 'bg-indigo-600 text-white shadow-xs font-bold'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200'
              }`}
            >
              <User className="w-3.5 h-3.5 text-slate-500" />
              <span>👤 Meus Cadastrados ({userCount})</span>
            </button>
          </div>

          <div className="text-[11px] text-slate-500 font-medium">
            Exibindo <strong>{filteredLeads.length}</strong> de <strong>{totalCount}</strong> leads
          </div>
        </div>

        {/* Alternância de Visões */}
        {viewMode === 'kanban' && <KanbanBoard />}
        {viewMode === 'table' && <TableView />}
        {viewMode === 'dashboard' && <MetricsDashboard />}
      </main>

      {/* Modais e Drawers */}
      <LeadModal />
      <LeadDetailDrawer />
      <ExcelImportModal />
    </div>
  );
};

export function App() {
  return (
    <LeadProvider>
      <MainContent />
    </LeadProvider>
  );
}

export default App;
