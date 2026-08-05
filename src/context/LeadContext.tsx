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

  // Detectar parâmetros de URL vindos do Bookmarklet 1-Clique do Instagram
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const instaHandle = params.get('instaHandle');
    const instaName = params.get('instaName');

    if (instaHandle) {
      const cleanHandle = instaHandle.replace('@', '').trim();
      const cleanName = instaName || cleanHandle.replace(/[._]/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());

      setEditingLead({
        id: '',
        nome: cleanName,
        instagram: cleanHandle,
        nicho: 'Mentoria de Concursos',
        comoEncontrei: 'Instagram Outbound (Bookmarklet)',
        status: 'nao_contatado',
        data1Contato: new Date().toISOString().split('T')[0],
        respondeu: false,
        data2Contato: '',
        dataFollowUp: new Date().toISOString().split('T')[0],
        tentativasFollowUp: 0,
        dataReuniao: '',
        reuniaoRealizada: false,
        prioridade: 'media',
        proximoPasso: 'Enviar Direct de apresentação da Trajetória',
        observacoes: `Lead capturado via Bookmarklet 1-Clique do Instagram (@${cleanHandle}).`,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      });
      setIsModalOpen(true);

      // Limpar parâmetros da URL suavemente
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  // Salvar no LocalStorage como backup local
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(leads));
  }, [leads]);

  // Carregar e Sincronizar em Tempo Real do Supabase se estiver configurado
  useEffect(() => {
    if (!isSupabaseConfigured || !supabase) return;

    const client = supabase;
    if (!client) return;

    // 1. Carregar do Supabase e mesclar com dados locais sem perder nada
    const fetchLeadsFromSupabase = async () => {
      try {
        const { data, error } = await client
          .from('leads')
          .select('*')
          .order('createdAt', { ascending: false });

        if (error) {
          console.error('Erro ao buscar do Supabase:', error);
          return;
        }

        if (data && data.length > 0) {
          const cloudLeads = data as Lead[];
          setLeads((prevLeads) => {
            const cloudMap = new Map(cloudLeads.map((l) => [l.id, l]));
            const merged = [...cloudLeads];

            // Preserva e envia pro banco qualquer lead criado localmente que ainda não esteja na nuvem
            for (const localLead of prevLeads) {
              if (!cloudMap.has(localLead.id)) {
                merged.unshift(localLead);
                client.from('leads').insert([localLead]).then(({ error: insErr }) => {
                  if (insErr) console.error('Erro ao enviar lead pendente para Supabase:', insErr);
                });
              } else {
                const cloudLead = cloudMap.get(localLead.id)!;
                const localTime = new Date(localLead.updatedAt || localLead.createdAt || 0).getTime();
                const cloudTime = new Date(cloudLead.updatedAt || cloudLead.createdAt || 0).getTime();
                if (localTime > cloudTime) {
                  const idx = merged.findIndex((l) => l.id === localLead.id);
                  if (idx !== -1) merged[idx] = localLead;
                  client.from('leads').update(localLead).eq('id', localLead.id).then(({ error: upErr }) => {
                    if (upErr) console.error('Erro ao atualizar lead pendente no Supabase:', upErr);
                  });
                }
              }
            }
            return merged;
          });
        }
      } catch (err) {
        console.error('Exceção ao sincronizar com Supabase:', err);
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
      try {
        const { error } = await supabase.from('leads').insert([newLead]);
        if (error) console.error('Erro Supabase addLead:', error);
      } catch (err) {
        console.error('Erro na conexão do Supabase ao adicionar lead:', err);
      }
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
      try {
        const { error } = await supabase.from('leads').update(updatedLead).eq('id', id);
        if (error) console.error('Erro Supabase updateLead:', error);
      } catch (err) {
        console.error('Erro na conexão do Supabase ao atualizar lead:', err);
      }
    }
  };

  const deleteLead = async (id: string) => {
    setLeads((prev) => prev.filter((lead) => lead.id !== id));
    if (selectedLead?.id === id) {
      setSelectedLead(null);
    }

    if (isSupabaseConfigured && supabase) {
      try {
        const { error } = await supabase.from('leads').delete().eq('id', id);
        if (error) console.error('Erro Supabase deleteLead:', error);
      } catch (err) {
        console.error('Erro na conexão do Supabase ao deletar lead:', err);
      }
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
        try {
          await supabase.from('leads').delete().neq('id', '0');
          await supabase.from('leads').insert(newLeads);
        } catch (err) {
          console.error('Erro Supabase importLeads replace:', err);
        }
      }
    } else {
      setLeads((prev) => [...newLeads, ...prev]);
      if (isSupabaseConfigured && supabase) {
        try {
          await supabase.from('leads').insert(newLeads);
        } catch (err) {
          console.error('Erro Supabase importLeads append:', err);
        }
      }
    }
  };

  const exportToExcel = () => {
    exportLeadsToExcel(leads);
  };

  const resetToDefaultData = async () => {
    const input = window.prompt(
      'ATENÇÃO: Esta ação apaga todos os seus dados e restaura a lista padrão.\n\nPara confirmar, digite "RESETAR" abaixo:'
    );
    if (input === 'RESETAR' || input === 'resetar') {
      setLeads(INITIAL_LEADS);
      localStorage.removeItem(STORAGE_KEY);
      if (isSupabaseConfigured && supabase) {
        try {
          await supabase.from('leads').delete().neq('id', '0');
          await supabase.from('leads').insert(INITIAL_LEADS);
        } catch (err) {
          console.error('Erro Supabase resetToDefaultData:', err);
        }
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
