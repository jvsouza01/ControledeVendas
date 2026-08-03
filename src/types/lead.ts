export type LeadStatus =
  | 'nao_contatado'
  | 'contatado_aguardando'
  | 'em_conversa'
  | 'reuniao_agendada'
  | 'reuniao_realizada'
  | 'fechado'
  | 'arquivado';

export type LeadPrioridade = 'alta' | 'media' | 'baixa';

export interface Lead {
  id: string;
  nome: string;
  instagram: string;
  nicho: string;
  comoEncontrei: string;
  status: LeadStatus;
  data1Contato: string; // YYYY-MM-DD
  respondeu: boolean;
  data2Contato: string; // YYYY-MM-DD
  dataFollowUp: string; // YYYY-MM-DD
  tentativasFollowUp: number;
  dataReuniao: string; // YYYY-MM-DD
  reuniaoRealizada: boolean;
  prioridade: LeadPrioridade;
  proximoPasso: string;
  observacoes: string;
  valorProposta?: number;
  createdAt: string;
  updatedAt: string;
}

export type ViewMode = 'kanban' | 'table' | 'dashboard';

export interface FilterOptions {
  search: string;
  nicho: string;
  status: string;
  prioridade: string;
  apenasFollowUpHojeOuAtrasado: boolean;
}
