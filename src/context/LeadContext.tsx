import React, { createContext, useContext, useState, useEffect } from 'react';
import type { Lead, FilterOptions, ViewMode } from '../types/lead';
import { INITIAL_LEADS } from '../data/initialLeads';
import { exportLeadsToExcel } from '../utils/excelUtils';
import { getFollowUpStatus } from '../utils/dateUtils';
import { supabase, isSupabaseConfigured } from '../lib/supabase';
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
  isCloudSynced: boolean;
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

  // Salvar no LocalStorage como backup local
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(leads));
  }, [leads]);

  // Carregar e Sincronizar em Tempo Real do Supabase se estiver configurado
  useEffect(() => {
    if (!isSupabaseConfigured || !supabase) return;

    const client = supabase;
    if (!client) return;

    // 1. Carregar do Supabase
    const fetchLeadsFromSupabase = async () => {
      const { data, error } = await client
        .from('leads')
        .select('*')
        .order('createdAt', { ascending: false });

      if (error) {
        console.error('Erro ao buscar do Supabase:', error);
      } else if (data && data.length > 0) {
        setLeads(data as Lead[]);
      }
    };

    fetchLeadsFromSupabase();

    // 2. Inscrição para Realtime
    const subscription = client
      .channel('leads_changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'leads' },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            const newLead = payload.new as Lead;
            setLeads((prev) => [newLead, ...prev.filter((l) => l.id !== newLead.id)]);
          } else if (payload.eventType === 'UPDATE') {
            const updated = payload.new as Lead;
            setLeads((prev) => prev.map((l) => (l.id === updated.id ? updated : l)));
          } else if (payload.eventType === 'DELETE') {
            const deletedId = payload.old.id;
            setLeads((prev) => prev.filter((l) => l.id !== deletedId));
          }
        }
      )
      .subscribe();

    return () => {
      client.removeChannel(subscription);
    };
  }, []);

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

  const addLead = async (leadData: Omit<Lead, 'id' | 'createdAt' | 'updatedAt'>) => {
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

    if (isSupabaseConfigured && supabase) {
      await supabase.from('leads').insert([newLead]);
    }
  };

  const updateLead = async (id: string, leadData: Partial<Lead>) => {
    const now = new Date().toISOString();
    const targetLead = leads.find((l) => l.id === id);
    if (!targetLead) return;

    const updatedLead = { ...targetLead, ...leadData, updatedAt: now };

    setLeads((prev) => prev.map((l) => (l.id === id ? updatedLead : l)));

    if (targetLead.status !== 'fechado' && updatedLead.status === 'fechado') {
      confetti({ particleCount: 120, spread: 80, origin: { y: 0.6 } });
    }

    if (isSupabaseConfigured && supabase) {
      await supabase.from('leads').update(leadData).eq('id', id);
    }
  };

  const deleteLead = async (id: string) => {
    setLeads((prev) => prev.filter((lead) => lead.id !== id));
    if (selectedLead?.id === id) {
      setSelectedLead(null);
    }

    if (isSupabaseConfigured && supabase) {
      await supabase.from('leads').delete().eq('id', id);
    }
  };

  const updateLeadStatus = (id: string, newStatus: Lead['status']) => {
    updateLead(id, { status: newStatus });
  };

  const incrementFollowUpAttempt = (id: string) => {
    const target = leads.find((l) => l.id === id);
    if (target) {
      updateLead(id, { tentativasFollowUp: (target.tentativasFollowUp || 0) + 1 });
    }
  };

  const importLeads = async (newLeads: Lead[], replaceExisting: boolean) => {
    if (replaceExisting) {
      setLeads(newLeads);
      if (isSupabaseConfigured && supabase) {
        await supabase.from('leads').delete().neq('id', '0');
        await supabase.from('leads').insert(newLeads);
      }
    } else {
      setLeads((prev) => [...newLeads, ...prev]);
      if (isSupabaseConfigured && supabase) {
        await supabase.from('leads').insert(newLeads);
      }
    }
  };

  const exportToExcel = () => {
    exportLeadsToExcel(leads);
  };

  const resetToDefaultData = async () => {
    if (window.confirm('Tem certeza que deseja restaurar os dados iniciais da planilha?')) {
      setLeads(INITIAL_LEADS);
      localStorage.removeItem(STORAGE_KEY);
      if (isSupabaseConfigured && supabase) {
        await supabase.from('leads').delete().neq('id', '0');
        await supabase.from('leads').insert(INITIAL_LEADS);
      }
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
        isCloudSynced: isSupabaseConfigured,
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
