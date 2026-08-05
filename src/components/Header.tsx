import React from 'react';
import { useLeads } from '../context/LeadContext';
import {
  LayoutGrid,
  Table as TableIcon,
  BarChart3,
  Plus,
  FileSpreadsheet,
  Download,
  RotateCcw,
  Search,
  Filter,
  Cloud,
  HardDrive,
  Zap,
} from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';
import { InstagramCaptureModal } from './InstagramCaptureModal';

export const Header: React.FC = () => {
  const [isCaptureOpen, setIsCaptureOpen] = React.useState(false);
  const {
    viewMode,
    setViewMode,
    filters,
    setFilters,
    setIsModalOpen,
    setEditingLead,
    setIsImportModalOpen,
    exportToExcel,
    resetToDefaultData,
    nichosDisponiveis,
    leads,
    isCloudSynced,
  } = useLeads();

  const handleOpenAddModal = () => {
    setEditingLead(null);
    setIsModalOpen(true);
  };

  return (
    <header className="bg-white/80 border-b border-slate-200/80 sticky top-0 z-30 backdrop-blur-md shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-slate-900 text-white flex items-center justify-center shadow-xs">
                <InstagramIcon className="w-4 h-4" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="font-semibold text-sm text-slate-900 tracking-tight">
                    Prospecção & Vendas
                  </h1>
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] font-medium border flex items-center gap-1 ${
                      isCloudSynced
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                        : 'bg-slate-100 text-slate-600 border-slate-200'
                    }`}
                    title={isCloudSynced ? 'Sincronizado na Nuvem Supabase' : 'Modo Backup Local (LocalStorage)'}
                  >
                    {isCloudSynced ? <Cloud className="w-3 h-3 text-emerald-600" /> : <HardDrive className="w-3 h-3 text-slate-400" />}
                    {isCloudSynced ? 'Nuvem Realtime' : 'Modo Local'}
                  </span>
                </div>
                <p className="text-[11px] text-slate-500">
                  {leads.length} prospects cadastrados
                </p>
              </div>
            </div>

            <div className="flex lg:hidden bg-slate-100 p-1 rounded-lg border border-slate-200">
              <button
                onClick={() => setViewMode('kanban')}
                className={`p-1.5 rounded-md text-xs ${viewMode === 'kanban' ? 'bg-white text-slate-900 shadow-xs font-semibold' : 'text-slate-500'}`}
                title="Kanban"
              >
                <LayoutGrid className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`p-1.5 rounded-md text-xs ${viewMode === 'table' ? 'bg-white text-slate-900 shadow-xs font-semibold' : 'text-slate-500'}`}
                title="Tabela"
              >
                <TableIcon className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('dashboard')}
                className={`p-1.5 rounded-md text-xs ${viewMode === 'dashboard' ? 'bg-white text-slate-900 shadow-xs font-semibold' : 'text-slate-500'}`}
                title="Dashboard"
              >
                <BarChart3 className="w-4 h-4" />
              </button>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 flex-1 max-w-2xl">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Buscar por nome, @instagram, notas..."
                value={filters.search}
                onChange={(e) => setFilters((prev) => ({ ...prev, search: e.target.value }))}
                className="w-full bg-slate-100/70 border border-slate-200/80 focus:border-slate-400 focus:bg-white rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-800 placeholder-slate-400 outline-none transition-all"
              />
            </div>

            <div className="relative">
              <select
                value={filters.nicho}
                onChange={(e) => setFilters((prev) => ({ ...prev, nicho: e.target.value }))}
                className="bg-slate-100/70 border border-slate-200/80 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-xs text-slate-700 outline-none transition-all appearance-none pr-8 cursor-pointer"
              >
                <option value="todos">Todos os Nichos</option>
                {nichosDisponiveis.map((nicho) => (
                  <option key={nicho} value={nicho}>
                    {nicho}
                  </option>
                ))}
              </select>
              <Filter className="w-3 h-3 absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
            </div>

            <select
              value={filters.prioridade}
              onChange={(e) => setFilters((prev) => ({ ...prev, prioridade: e.target.value }))}
              className="bg-slate-100/70 border border-slate-200/80 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-xs text-slate-700 outline-none transition-all cursor-pointer"
            >
              <option value="todas">Prioridade: Todas</option>
              <option value="alta">Alta</option>
              <option value="media">Média</option>
              <option value="baixa">Baixa</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <div className="hidden lg:flex bg-slate-100/80 p-1 rounded-lg border border-slate-200/80">
              <button
                onClick={() => setViewMode('kanban')}
                className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all ${
                  viewMode === 'kanban'
                    ? 'bg-white text-slate-900 shadow-xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <LayoutGrid className="w-3.5 h-3.5" />
                Kanban
              </button>

              <button
                onClick={() => setViewMode('table')}
                className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all ${
                  viewMode === 'table'
                    ? 'bg-white text-slate-900 shadow-xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <TableIcon className="w-3.5 h-3.5" />
                Tabela
              </button>

              <button
                onClick={() => setViewMode('dashboard')}
                className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all ${
                  viewMode === 'dashboard'
                    ? 'bg-white text-slate-900 shadow-xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <BarChart3 className="w-3.5 h-3.5" />
                Métricas
              </button>
            </div>

            <div className="flex items-center gap-1 border-l border-slate-200 pl-2">
              <button
                onClick={() => setIsImportModalOpen(true)}
                className="p-1.5 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-md transition-colors"
                title="Importar Excel / CSV"
              >
                <FileSpreadsheet className="w-4 h-4" />
              </button>
              <button
                onClick={exportToExcel}
                className="p-1.5 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-md transition-colors"
                title="Baixar Excel"
              >
                <Download className="w-4 h-4" />
              </button>
              <button
                onClick={resetToDefaultData}
                className="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                title="Restaurar Dados Padrão (ATENÇÃO: Requer confirmação)"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            </div>

            <button
              onClick={() => setIsCaptureOpen(true)}
              className="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 transition-all shadow-xs active:scale-95 border border-amber-400"
              title="Captura Rápida de Mentorias no Instagram (Cole link ou use Bookmarklet)"
            >
              <Zap className="w-3.5 h-3.5 fill-current text-slate-950" />
              <span className="hidden sm:inline">Capturar Insta</span>
            </button>

            <button
              onClick={handleOpenAddModal}
              className="bg-slate-900 hover:bg-slate-800 text-white font-medium px-3.5 py-1.5 rounded-lg text-xs flex items-center gap-1.5 transition-all shadow-xs active:scale-95"
            >
              <Plus className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Novo Lead</span>
            </button>
          </div>

        </div>
      </div>

      <InstagramCaptureModal isOpen={isCaptureOpen} onClose={() => setIsCaptureOpen(false)} />
    </header>
  );
};
