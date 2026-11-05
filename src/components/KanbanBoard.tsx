import React from 'react';
import { useLeads } from '../context/LeadContext';
import type { Lead, LeadStatus } from '../types/lead';
import {
  formatDaysAgoText,
  getFollowUpStatus,
  formatDateBR,
  getTodayString,
  addDaysToDate,
} from '../utils/dateUtils';
import {
  Clock,
  Edit2,
  ExternalLink,
  PlusCircle,
  CheckCircle2,
  RefreshCw,
  MessageCircle,
  Sparkles,
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
        // Garantir que leads minerados (fb_) fiquem no topo da coluna
        const columnLeads = filteredLeads
          .filter((l) => l.status === col.id)
          .sort((a, b) => {
            const aIsFb = a.id.startsWith('fb_') ? 1 : 0;
            const bIsFb = b.id.startsWith('fb_') ? 1 : 0;
            return bIsFb - aIsFb;
          });

        return (
          <div
            key={col.id}
            className="flex-shrink-0 w-80 rounded-xl border border-slate-200/80 bg-slate-100/50 p-3 flex flex-col justify-between max-h-[82vh] shadow-xs"
          >
            <div>
              {/* Cabeçalho de Coluna */}
              <div className="flex items-center justify-between pb-2.5 border-b border-slate-200 mb-3">
                <h3 className="font-semibold text-xs text-slate-800 tracking-tight">{col.title}</h3>
                <span className="px-1.5 py-0.5 rounded text-[11px] font-mono font-semibold bg-white text-slate-600 border border-slate-200">
                  {columnLeads.length}
                </span>
              </div>

              {/* Cards dos Leads */}
              <div className="space-y-2.5 overflow-y-auto max-h-[70vh] pr-1 scrollbar-thin">
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
                    nicho: 'Mentoria de Concursos',
                    comoEncontrei: 'Instagram Outbound',
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
  const { setSelectedLead, setEditingLead, setIsModalOpen, updateLeadStatus, updateLead } = useLeads();

  const daysInfo = formatDaysAgoText(lead.data1Contato);
  const followUpStatus = getFollowUpStatus(lead.dataFollowUp, lead.status, lead.data1Contato);
  const cleanHandle = (lead.instagram || '').replace('@', '').trim();

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

  // Ações de 1 Clique
  const handleMarkContatado = (e: React.MouseEvent) => {
    e.stopPropagation();
    const today = getTodayString();
    const nextFollow = addDaysToDate(3);
    updateLead(lead.id, {
      status: 'contatado_aguardando',
      data1Contato: today,
      dataFollowUp: nextFollow,
      proximoPasso: 'Fazer 1º Follow-up no Direct/WhatsApp',
    });
  };

  const handleFollowUpFeito = (e: React.MouseEvent) => {
    e.stopPropagation();
    const today = getTodayString();
    const nextFollow = addDaysToDate(4);
    updateLead(lead.id, {
      tentativasFollowUp: (lead.tentativasFollowUp || 0) + 1,
      data2Contato: today,
      dataFollowUp: nextFollow,
      proximoPasso: 'Aguardando resposta do Follow-up',
    });
  };

  const handleRespondeu = (e: React.MouseEvent) => {
    e.stopPropagation();
    updateLead(lead.id, {
      status: 'em_conversa',
      respondeu: true,
      proximoPasso: 'Desenvolver conversa / sondar dores da plataforma',
    });
  };

  return (
    <div
      onClick={() => setSelectedLead(lead)}
      className="bg-white border border-slate-200/90 hover:border-slate-300 rounded-lg p-3 shadow-xs hover:shadow-sm transition-all group relative cursor-pointer"
    >
      {/* Badge de Destaque: Novo Lead Minerado */}
      {lead.id.startsWith('fb_') && (
        <div className="mb-2 inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200/90 shadow-2xs">
          <Sparkles className="w-3 h-3 text-emerald-600 animate-pulse" />
          <span>✨ NOVO LEAD MINERADO</span>
        </div>
      )}

      {/* Topo do Card: Nome e Ações */}
      <div className="flex items-start justify-between gap-2">
        <div className="overflow-hidden flex-1">
          <h4
            className="font-semibold text-xs text-slate-900 group-hover:text-indigo-600 truncate transition-colors"
            title={lead.nome}
          >
            {lead.nome || cleanHandle || 'Lead sem nome'}
          </h4>

          {cleanHandle && (
            <div className="flex items-center gap-1.5 mt-0.5">
              <a
                href={`https://instagram.com/${cleanHandle}`}
                target="_blank"
                rel="noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="inline-flex items-center gap-1 text-[11px] font-medium text-slate-500 hover:text-slate-800 transition-colors"
                title="Abrir Perfil no Instagram"
              >
                <InstagramIcon className="w-3 h-3 text-slate-400" />
                @{cleanHandle}
                <ExternalLink className="w-2.5 h-2.5 text-slate-400" />
              </a>

              <a
                href={`https://ig.me/m/${cleanHandle}`}
                target="_blank"
                rel="noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="text-[10px] text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-1 py-0.2 rounded font-medium transition-colors"
                title="Abrir conversa de Direct diretamente"
              >
                Direct ✉️
              </a>
            </div>
          )}
        </div>

        <button
          onClick={(e) => {
            e.stopPropagation();
            setEditingLead(lead);
            setIsModalOpen(true);
          }}
          className="p-1 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded transition-colors flex-shrink-0"
          title="Editar Dados"
        >
          <Edit2 className="w-3 h-3" />
        </button>
      </div>

      {/* Badges de Nicho e Prioridade */}
      <div className="flex items-center gap-1.5 my-2 flex-wrap">
        {lead.nicho && (
          <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-700 border border-slate-200 truncate max-w-[170px]">
            {lead.nicho}
          </span>
        )}
        {getPriorityBadge(lead.prioridade)}
        {lead.comoEncontrei && (
          <span className="px-1.5 py-0.5 rounded text-[9px] font-medium bg-slate-50 text-slate-500 border border-slate-200/60 truncate max-w-[120px]" title={lead.comoEncontrei}>
            {lead.comoEncontrei.split(' - ')[0].split(' + ')[0]}
          </span>
        )}
      </div>

      {/* Indicador de Follow-up ou Tempo */}
      {lead.status !== 'nao_contatado' && (
        <div className="bg-slate-50 p-2 rounded-md border border-slate-200/60 text-[11px] space-y-1 my-2">
          <div className="flex justify-between items-center text-slate-500">
            <span>Tempo:</span>
            <span className="font-semibold text-slate-800">{daysInfo.text}</span>
          </div>

          {lead.dataFollowUp && (
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Follow-up:</span>
              <span
                className={`px-1.5 py-0.2 rounded text-[10px] font-semibold flex items-center gap-1 ${
                  followUpStatus === 'hoje'
                    ? 'bg-amber-100 text-amber-900 border border-amber-300 animate-pulse'
                    : followUpStatus === 'atrasado'
                    ? 'bg-rose-100 text-rose-900 border border-rose-300 font-bold'
                    : 'text-slate-700'
                }`}
              >
                <Clock className="w-2.5 h-2.5" />
                {formatDateBR(lead.dataFollowUp)}
              </span>
            </div>
          )}

          {lead.tentativasFollowUp > 0 && (
            <div className="flex justify-between items-center text-slate-500">
              <span>Tentativas:</span>
              <span className="font-bold text-amber-700">{lead.tentativasFollowUp}x</span>
            </div>
          )}
        </div>
      )}

      {/* Próximo Passo */}
      {lead.proximoPasso && (
        <div className="my-1.5 text-[10px] text-slate-600 bg-slate-50 border border-slate-200/70 p-1.5 rounded truncate" title={lead.proximoPasso}>
          <strong className="text-slate-500">Próximo:</strong> {lead.proximoPasso}
        </div>
      )}

      {/* BOTÕES DE AÇÃO RÁPIDA DE 1 CLIQUE */}
      <div className="mt-2.5 pt-2 border-t border-slate-100 space-y-1.5" onClick={(e) => e.stopPropagation()}>
        {lead.status === 'nao_contatado' && (
          <button
            onClick={handleMarkContatado}
            className="w-full py-1.5 px-2 bg-emerald-600 hover:bg-emerald-700 active:scale-98 text-white rounded-md text-xs font-bold flex items-center justify-center gap-1.5 transition-all shadow-xs"
            title="Muda para Aguardando Resposta + Define 1º Contato Hoje + Agenda Follow-up para daqui a 3 dias"
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Já Contatei (+3d)</span>
          </button>
        )}

        {lead.status === 'contatado_aguardando' && (
          <div className="grid grid-cols-2 gap-1.5">
            <button
              onClick={handleFollowUpFeito}
              className="py-1 px-1.5 bg-amber-50 hover:bg-amber-100 border border-amber-300 text-amber-900 rounded-md text-[11px] font-semibold flex items-center justify-center gap-1 transition-all"
              title="+1 Tentativa de Follow-up + Reagenda para daqui a 4 dias"
            >
              <RefreshCw className="w-3 h-3 text-amber-700" />
              <span>Follow (+4d)</span>
            </button>
            <button
              onClick={handleRespondeu}
              className="py-1 px-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-[11px] font-bold flex items-center justify-center gap-1 transition-all shadow-2xs"
              title="Marca que o mentor respondeu e move para Em Conversa"
            >
              <MessageCircle className="w-3 h-3" />
              <span>Respondeu!</span>
            </button>
          </div>
        )}

        {/* Dropdown de Status Compacto */}
        <select
          value={lead.status}
          onChange={(e) => updateLeadStatus(lead.id, e.target.value as LeadStatus)}
          className="w-full bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-[11px] rounded px-2 py-1 outline-none cursor-pointer"
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
