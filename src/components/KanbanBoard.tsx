import React from 'react';
import { useLeads } from '../context/LeadContext';
import type { Lead, LeadStatus } from '../types/lead';
import {
  formatDaysAgoText,
  getFollowUpStatus,
  formatDateBR,
} from '../utils/dateUtils';
import {
  Clock,
  Edit2,
  ExternalLink,
  PlusCircle,
} from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';

const COLUMNS: { id: LeadStatus; title: string }[] = [
  { id: 'nao_contatado', title: 'Não Contatados' },
  { id: 'contatado_aguardando', title: 'Aguardando Resposta' },
  { id: 'em_conversa', title: 'Em Conversa' },
  { id: 'reuniao_agendada', title: 'Reunião Agendada' },
  { id: 'reuniao_realizada', title: 'Reunião Realizada' },
  { id: 'fechado', title: 'Cliente Fechado' },
  { id: 'arquivado', title: 'Arquivado' },
];

export const KanbanBoard: React.FC = () => {
  const { filteredLeads, setEditingLead, setIsModalOpen } = useLeads();

  return (
    <div className="flex gap-3 overflow-x-auto pb-6 pt-2 snap-x min-h-[calc(100vh-220px)]">
      {COLUMNS.map((col) => {
        const columnLeads = filteredLeads.filter((l) => l.status === col.id);

        return (
          <div
            key={col.id}
            className="flex-shrink-0 w-80 rounded-xl border border-slate-200/80 bg-slate-100/50 p-3 flex flex-col justify-between max-h-[80vh] shadow-xs"
          >
            <div>
              {/* Cabeçalho de Coluna Notion Style */}
              <div className="flex items-center justify-between pb-2.5 border-b border-slate-200 mb-3">
                <h3 className="font-semibold text-xs text-slate-800 tracking-tight">{col.title}</h3>
                <span className="px-1.5 py-0.5 rounded text-[11px] font-mono font-semibold bg-white text-slate-600 border border-slate-200">
                  {columnLeads.length}
                </span>
              </div>

              {/* Cards dos Leads */}
              <div className="space-y-2.5 overflow-y-auto max-h-[68vh] pr-1 scrollbar-thin">
                {columnLeads.length === 0 ? (
                  <div className="py-8 text-center border border-dashed border-slate-200 rounded-lg text-slate-400 text-xs">
                    Vazio
                  </div>
                ) : (
                  columnLeads.map((lead) => (
                    <KanbanCard key={lead.id} lead={lead} />
                  ))
                )}
              </div>
            </div>

            {/* Botão Adicionar Lead */}
            <div className="pt-2.5 border-t border-slate-200 mt-2">
              <button
                onClick={() => {
                  setEditingLead({
                    id: '',
                    nome: '',
                    instagram: '',
                    nicho: '',
                    comoEncontrei: 'Instagram - prospecção',
                    status: col.id,
                    data1Contato: '',
                    respondeu: false,
                    data2Contato: '',
                    dataFollowUp: '',
                    tentativasFollowUp: 0,
                    dataReuniao: '',
                    reuniaoRealizada: false,
                    prioridade: 'media',
                    proximoPasso: '',
                    observacoes: '',
                    createdAt: '',
                    updatedAt: '',
                  });
                  setIsModalOpen(true);
                }}
                className="w-full py-1.5 rounded-lg border border-dashed border-slate-300 hover:border-slate-400 bg-white/50 hover:bg-white text-slate-600 hover:text-slate-900 text-xs font-medium flex items-center justify-center gap-1 transition-colors shadow-xs"
              >
                <PlusCircle className="w-3.5 h-3.5" />
                Adicionar Lead
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

const KanbanCard: React.FC<{ lead: Lead }> = ({ lead }) => {
  const { setSelectedLead, setEditingLead, setIsModalOpen, updateLeadStatus, incrementFollowUpAttempt } = useLeads();

  const daysInfo = formatDaysAgoText(lead.data1Contato);
  const followUpStatus = getFollowUpStatus(lead.dataFollowUp, lead.status, lead.data1Contato);

  const getPriorityBadge = (p: Lead['prioridade']) => {
    switch (p) {
      case 'alta':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-rose-50 text-rose-700 border border-rose-200">Alta</span>;
      case 'media':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Média</span>;
      case 'baixa':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-600 border border-slate-200">Baixa</span>;
    }
  };

  return (
    <div className="bg-white border border-slate-200/90 hover:border-slate-300 rounded-lg p-3 shadow-xs hover:shadow-sm transition-all group relative">
      <div className="flex items-start justify-between gap-2">
        <div className="overflow-hidden">
          <h4
            onClick={() => setSelectedLead(lead)}
            className="font-semibold text-xs text-slate-900 hover:text-slate-700 truncate cursor-pointer transition-colors"
            title={lead.nome}
          >
            {lead.nome || lead.instagram || 'Lead sem nome'}
          </h4>

          {lead.instagram && (
            <a
              href={`https://instagram.com/${lead.instagram.replace('@', '')}`}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 text-[11px] font-medium text-slate-500 hover:text-slate-800 mt-0.5"
            >
              <InstagramIcon className="w-3 h-3 text-slate-400" />
              @{lead.instagram.replace('@', '')}
              <ExternalLink className="w-2.5 h-2.5 text-slate-400" />
            </a>
          )}
        </div>

        <button
          onClick={() => {
            setEditingLead(lead);
            setIsModalOpen(true);
          }}
          className="p-1 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded transition-colors"
          title="Editar"
        >
          <Edit2 className="w-3 h-3" />
        </button>
      </div>

      <div className="flex items-center gap-1.5 my-2 flex-wrap">
        {lead.nicho && (
          <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
            {lead.nicho}
          </span>
        )}
        {getPriorityBadge(lead.prioridade)}
      </div>

      <div className="bg-slate-50 p-2 rounded-md border border-slate-200/60 text-[11px] space-y-1 my-2">
        <div className="flex justify-between items-center text-slate-500">
          <span>1º Contato:</span>
          <span className="font-mono text-slate-700">
            {lead.data1Contato ? formatDateBR(lead.data1Contato) : '-'}
          </span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-slate-500">Tempo em contato:</span>
          <span className="font-semibold text-slate-900">
            {daysInfo.text}
          </span>
        </div>

        {lead.tentativasFollowUp > 0 && (
          <div className="flex justify-between items-center text-slate-500">
            <span>Tentativas:</span>
            <span className="font-medium text-amber-700">{lead.tentativasFollowUp}x</span>
          </div>
        )}
      </div>

      {lead.dataFollowUp && (
        <div className="flex items-center justify-between gap-1 mt-2">
          <span
            className={`px-1.5 py-0.5 rounded text-[10px] font-medium flex items-center gap-1 ${
              followUpStatus === 'hoje'
                ? 'bg-amber-50 text-amber-700 border border-amber-200'
                : followUpStatus === 'atrasado'
                ? 'bg-rose-50 text-rose-700 border border-rose-200'
                : 'bg-slate-100 text-slate-600 border border-slate-200'
            }`}
          >
            <Clock className="w-3 h-3" />
            Follow: {formatDateBR(lead.dataFollowUp)}
          </span>

          <button
            onClick={() => incrementFollowUpAttempt(lead.id)}
            className="text-[10px] text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 px-1.5 py-0.5 rounded border border-slate-200 transition-colors"
            title="+1 Tentativa"
          >
            +1
          </button>
        </div>
      )}

      {lead.proximoPasso && (
        <div className="mt-2 text-[10px] text-slate-700 bg-slate-50 border border-slate-200/80 p-1.5 rounded truncate">
          <strong className="text-slate-500">Próximo:</strong> {lead.proximoPasso}
        </div>
      )}

      <div className="mt-2.5 pt-2 border-t border-slate-100">
        <select
          value={lead.status}
          onChange={(e) => updateLeadStatus(lead.id, e.target.value as LeadStatus)}
          className="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 text-slate-700 text-[11px] rounded-md px-2 py-1 outline-none cursor-pointer"
        >
          <option value="nao_contatado">Não Contatado</option>
          <option value="contatado_aguardando">Aguardando Resposta</option>
          <option value="em_conversa">Em Conversa</option>
          <option value="reuniao_agendada">Reunião Agendada</option>
          <option value="reuniao_realizada">Reunião Realizada</option>
          <option value="fechado">Cliente Fechado</option>
          <option value="arquivado">Arquivado</option>
        </select>
      </div>
    </div>
  );
};
