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

const MainContent: React.FC = () => {
  const { viewMode } = useLeads();

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Banner de Follow-ups Urgentes */}
        <FollowUpAlertBanner />

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
