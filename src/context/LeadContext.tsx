import React, { createContext, useContext, useState, useEffect } from 'react';
import type { Lead, FilterOptions, ViewMode } from '../types/lead';
import { INITIAL_LEADS } from '../data/initialLeads';
import { exportLeadsToExcel } from '../utils/excelUtils';
import { getFollowUpStatus } from '../utils/dateUtils';
import confetti from 'canvas-confetti';

interface LeadContextType {
  leads: Lead[];
  filteredLeads: Lead[];
  viewMode: ViewMode;
  setViewMode: (mode: ViewMode) => void;
  filters: FilterOptions;
  setFilters: React.Dispatch<React.SetStateAction<FilterOptions>>;
  selectedLead: Lead | null;
  setSelectedLead: (lead: Lead | null) => void;
  isModalOpen: boolean;
  setIsModalOpen: (open: boolean) => void;
  isImportModalOpen: boolean;
  setIsImportModalOpen: (open: boolean) => void;
  editingLead: Lead | null;
  setEditingLead: (lead: Lead | null) => void;
  addLead: (lead: Omit<Lead, 'id' | 'createdAt' | 'updatedAt'>) => void;
  updateLead: (id: string, leadData: Partial<Lead>) => void;
  deleteLead: (id: string) => void;
  updateLeadStatus: (id: string, newStatus: Lead['status']) => void;
  incrementFollowUpAttempt: (id: string) => void;
  importLeads: (newLeads: Lead[], replaceExisting: boolean) => void;
  exportToExcel: () => void;
  resetToDefaultData: () => void;
  nichosDisponiveis: string[];
}

const STORAGE_KEY = 'crm_prospeccao_vendas_leads_v1';

const LeadContext = createContext<LeadContextType | undefined>(undefined);

export const LeadProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [leads, setLeads] = useState<Lead[]>(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      } catch (e) {
        console.error('Erro ao ler localStorage', e);
      }
    }
    return INITIAL_LEADS;
  });

  const [viewMode, setViewMode] = useState<ViewMode>('kanban');
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isImportModalOpen, setIsImportModalOpen] = useState(false);
  const [editingLead, setEditingLead] = useState<Lead | null>(null);

  const [filters, setFilters] = useState<FilterOptions>({
    search: '',
    nicho: 'todos',
    status: 'todos',
    prioridade: 'todas',
    apenasFollowUpHojeOuAtrasado: false,
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(leads));
  }, [leads]);

  const nichosDisponiveis = Array.from(
    new Set(leads.map((l) => l.nicho).filter(Boolean))
  ).sort();

  const filteredLeads = leads.filter((lead) => {
    if (filters.search) {
      const q = filters.search.toLowerCase();
      const matchNome = lead.nome.toLowerCase().includes(q);
      const matchInsta = lead.instagram.toLowerCase().includes(q);
      const matchObs = lead.observacoes.toLowerCase().includes(q);
      if (!matchNome && !matchInsta && !matchObs) return false;
    }

    if (filters.nicho !== 'todos' && lead.nicho !== filters.nicho) {
      return false;
    }

    if (filters.status !== 'todos' && lead.status !== filters.status) {
      return false;
    }

    if (filters.prioridade !== 'todas' && lead.prioridade !== filters.prioridade) {
      return false;
    }

    if (filters.apenasFollowUpHojeOuAtrasado) {
      const fStatus = getFollowUpStatus(lead.dataFollowUp, lead.status);
      if (fStatus !== 'hoje' && fStatus !== 'atrasado') {
        return false;
      }
    }

    return true;
  });

  const addLead = (leadData: Omit<Lead, 'id' | 'createdAt' | 'updatedAt'>) => {
    const now = new Date().toISOString();
    const newLead: Lead = {
      ...leadData,
      id: `lead_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
      createdAt: now,
      updatedAt: now,
    };
    setLeads((prev) => [newLead, ...prev]);

    if (newLead.status === 'fechado') {
      confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
    }
  };

  const updateLead = (id: string, leadData: Partial<Lead>) => {
    const now = new Date().toISOString();
    setLeads((prev) =>
      prev.map((lead) => {
        if (lead.id === id) {
          const updated = { ...lead, ...leadData, updatedAt: now };
          if (lead.status !== 'fechado' && updated.status === 'fechado') {
            confetti({ particleCount: 120, spread: 80, origin: { y: 0.6 } });
          }
          return updated;
        }
        return lead;
      })
    );
  };

  const deleteLead = (id: string) => {
    setLeads((prev) => prev.filter((lead) => lead.id !== id));
    if (selectedLead?.id === id) {
      setSelectedLead(null);
    }
  };

  const updateLeadStatus = (id: string, newStatus: Lead['status']) => {
    updateLead(id, { status: newStatus });
  };

  const incrementFollowUpAttempt = (id: string) => {
    setLeads((prev) =>
      prev.map((lead) => {
        if (lead.id === id) {
          return {
            ...lead,
            tentativasFollowUp: (lead.tentativasFollowUp || 0) + 1,
            updatedAt: new Date().toISOString(),
          };
        }
        return lead;
      })
    );
  };

  const importLeads = (newLeads: Lead[], replaceExisting: boolean) => {
    if (replaceExisting) {
      setLeads(newLeads);
    } else {
      setLeads((prev) => [...newLeads, ...prev]);
    }
  };

  const exportToExcel = () => {
    exportLeadsToExcel(leads);
  };

  const resetToDefaultData = () => {
    if (window.confirm('Tem certeza que deseja restaurar os dados iniciais da planilha?')) {
      setLeads(INITIAL_LEADS);
      localStorage.removeItem(STORAGE_KEY);
    }
  };

  return (
    <LeadContext.Provider
      value={{
        leads,
        filteredLeads,
        viewMode,
        setViewMode,
        filters,
        setFilters,
        selectedLead,
        setSelectedLead,
        isModalOpen,
        setIsModalOpen,
        isImportModalOpen,
        setIsImportModalOpen,
        editingLead,
        setEditingLead,
        addLead,
        updateLead,
        deleteLead,
        updateLeadStatus,
        incrementFollowUpAttempt,
        importLeads,
        exportToExcel,
        resetToDefaultData,
        nichosDisponiveis,
      }}
    >
      {children}
    </LeadContext.Provider>
  );
};

export const useLeads = () => {
  const context = useContext(LeadContext);
  if (!context) {
    throw new Error('useLeads deve ser usado dentro de LeadProvider');
  }
  return context;
};
