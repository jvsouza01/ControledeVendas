import React, { useState } from 'react';
import { useLeads } from '../context/LeadContext';
import type { Lead, LeadStatus } from '../types/lead';
import {
  formatDateBR,
  formatDaysAgoText,
  getFollowUpStatus,
  getTodayString,
  addDaysToDate,
} from '../utils/dateUtils';
import {
  Edit2,
  Trash2,
  ExternalLink,
  ArrowUpDown,
  CheckCircle,
  XCircle,
  CheckCircle2,
  RefreshCw,
  MessageCircle,
  Sparkles,
} from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';
import { getMicroMentorBadge } from '../utils/leadUtils';

export const TableView: React.FC = () => {
  const { filteredLeads, updateLeadStatus, updateLead, deleteLead, setEditingLead, setIsModalOpen, setSelectedLead } = useLeads();

  const [sortField, setSortField] = useState<keyof Lead>('updatedAt');
  const [sortAsc, setSortAsc] = useState<boolean>(false);

  const handleSort = (field: keyof Lead) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(true);
    }
  };

  const sortedLeads = [...filteredLeads].sort((a, b) => {
    let valA = a[sortField] || '';
    let valB = b[sortField] || '';

    if (typeof valA === 'string') valA = valA.toLowerCase();
    if (typeof valB === 'string') valB = valB.toLowerCase();

    if (valA < valB) return sortAsc ? -1 : 1;
    if (valA > valB) return sortAsc ? 1 : -1;
    return 0;
  });

  const handleMarkContatado = (leadId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const today = getTodayString();
    const nextFollow = addDaysToDate(3);
    updateLead(leadId, {
      status: 'contatado_aguardando',
      data1Contato: today,
      dataFollowUp: nextFollow,
      proximoPasso: 'Fazer 1º Follow-up no Direct/WhatsApp',
    });
  };

  const handleFollowUpFeito = (lead: Lead, e: React.MouseEvent) => {
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

  const handleRespondeu = (leadId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    updateLead(leadId, {
      status: 'em_conversa',
      respondeu: true,
      proximoPasso: 'Desenvolver conversa / sondar dores da plataforma',
    });
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-700 border-collapse min-w-[1250px]">
          <thead className="bg-slate-50 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200">
            <tr>
              <th className="py-3.5 px-4 cursor-pointer hover:text-slate-900" onClick={() => handleSort('nome')}>
                <div className="flex items-center gap-1">
                  <span>Nome / Professor</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>

              <th className="py-3.5 px-4 cursor-pointer hover:text-slate-900" onClick={() => handleSort('instagram')}>
                <div className="flex items-center gap-1">
                  <span>@ Instagram</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>

              <th className="py-3.5 px-4 cursor-pointer hover:text-slate-900" onClick={() => handleSort('nicho')}>
                <div className="flex items-center gap-1">
                  <span>Nicho</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>

              <th className="py-3.5 px-4 cursor-pointer hover:text-slate-900" onClick={() => handleSort('status')}>
                <div className="flex items-center gap-1">
                  <span>Status</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>

              <th className="py-3.5 px-4 text-center">
                <span>Ação Rápida 1-Clique</span>
              </th>

              <th className="py-3.5 px-4 cursor-pointer hover:text-slate-900" onClick={() => handleSort('data1Contato')}>
                <div className="flex items-center gap-1">
                  <span>1º Contato</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>

              <th className="py-3.5 px-4 text-center">
                <span>Tempo</span>
              </th>

              <th className="py-3.5 px-4 text-center cursor-pointer hover:text-slate-900" onClick={() => handleSort('respondeu')}>
                <span>Respondeu?</span>
              </th>

              <th className="py-3.5 px-4 cursor-pointer hover:text-slate-900" onClick={() => handleSort('dataFollowUp')}>
                <div className="flex items-center gap-1">
                  <span>Follow-up</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>

              <th className="py-3.5 px-4 text-center">
                <span>Tentativas</span>
              </th>

              <th className="py-3.5 px-4 cursor-pointer hover:text-slate-900" onClick={() => handleSort('prioridade')}>
                <div className="flex items-center gap-1">
                  <span>Prioridade</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>

              <th className="py-3.5 px-4 text-right">
                <span>Ações</span>
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100">
            {sortedLeads.length === 0 ? (
              <tr>
                <td colSpan={12} className="py-12 text-center text-slate-400 text-xs">
                  Nenhum lead encontrado com os filtros selecionados.
                </td>
              </tr>
            ) : (
              sortedLeads.map((lead) => {
                const daysInfo = formatDaysAgoText(lead.data1Contato);
                const followStatus = getFollowUpStatus(lead.dataFollowUp, lead.status, lead.data1Contato);
                const cleanHandle = (lead.instagram || '').replace('@', '').trim();
                const microMentor = getMicroMentorBadge(lead);

                return (
                  <tr
                    key={lead.id}
                    onClick={() => setSelectedLead(lead)}
                    className="hover:bg-slate-50/70 transition-colors cursor-pointer"
                  >
                    <td className="py-3 px-4 font-semibold text-slate-900 max-w-[260px]">
                      <div className="flex flex-wrap items-center gap-1.5">
                        <span className="truncate font-semibold hover:text-indigo-600 transition-colors max-w-[150px]">
                          {lead.nome || cleanHandle || 'Lead sem nome'}
                        </span>
                        {lead.id.startsWith('fb_') && (
                          <span className="inline-flex items-center gap-1 text-[9px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-1.5 py-0.5 rounded shadow-2xs flex-shrink-0">
                            <Sparkles className="w-2.5 h-2.5 text-emerald-600 animate-pulse" />
                            ✨ NOVO
                          </span>
                        )}
                        {microMentor && (
                          <span
                            className={`inline-flex items-center text-[9px] font-bold px-1.5 py-0.5 rounded shadow-2xs flex-shrink-0 ${
                              microMentor.isSmall
                                ? 'bg-cyan-50 text-cyan-800 border border-cyan-200'
                                : 'bg-slate-100 text-slate-600 border border-slate-200'
                            }`}
                          >
                            {microMentor.text}
                          </span>
                        )}
                      </div>
                      {lead.comoEncontrei && (
                        <div className="text-[10px] text-slate-400 font-normal truncate" title={lead.comoEncontrei}>
                          {lead.comoEncontrei}
                        </div>
                      )}
                    </td>

                    <td className="py-3 px-4">
                      {cleanHandle ? (
                        <div className="flex items-center gap-1.5" onClick={(e) => e.stopPropagation()}>
                          <a
                            href={`https://instagram.com/${cleanHandle}`}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1 font-medium text-slate-700 hover:text-slate-900 bg-slate-100/80 px-2 py-0.5 rounded border border-slate-200 transition-colors"
                          >
                            <InstagramIcon className="w-3 h-3 text-slate-400" />
                            @{cleanHandle}
                            <ExternalLink className="w-2.5 h-2.5 text-slate-400" />
                          </a>
                          <a
                            href={`https://ig.me/m/${cleanHandle}`}
                            target="_blank"
                            rel="noreferrer"
                            className="text-[10px] text-indigo-600 hover:text-indigo-800 bg-indigo-50 px-1 py-0.5 rounded font-medium border border-indigo-100"
                            title="Direct ✉️"
                          >
                            Direct
                          </a>
                        </div>
                      ) : (
                        <span className="text-slate-400">-</span>
                      )}
                    </td>

                    <td className="py-3 px-4">
                      {lead.nicho ? (
                        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
                          {lead.nicho}
                        </span>
                      ) : (
                        <span className="text-slate-400">-</span>
                      )}
                    </td>

                    <td className="py-3 px-4" onClick={(e) => e.stopPropagation()}>
                      <select
                        value={lead.status}
                        onChange={(e) => updateLeadStatus(lead.id, e.target.value as LeadStatus)}
                        className="bg-slate-50 border border-slate-200 hover:border-slate-300 text-slate-800 text-xs rounded px-2 py-1 outline-none cursor-pointer"
                      >
                        <option value="nao_contatado">Não Contatado</option>
                        <option value="contatado_aguardando">Aguardando Resposta</option>
                        <option value="em_conversa">Em Conversa</option>
                        <option value="reuniao_agendada">Reunião Agendada</option>
                        <option value="reuniao_realizada">Reunião Realizada</option>
                        <option value="fechado">Cliente Fechado</option>
                        <option value="arquivado">Arquivado</option>
                      </select>
                    </td>

                    {/* Ação Rápida 1-Clique na Tabela */}
                    <td className="py-3 px-4 text-center" onClick={(e) => e.stopPropagation()}>
                      {lead.status === 'nao_contatado' && (
                        <button
                          onClick={(e) => handleMarkContatado(lead.id, e)}
                          className="px-2 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[11px] font-bold inline-flex items-center gap-1 transition-all shadow-2xs"
                          title="Marcar como Contatado e Agendar Follow-up para +3 dias"
                        >
                          <CheckCircle2 className="w-3 h-3" />
                          <span>Contatei (+3d)</span>
                        </button>
                      )}

                      {lead.status === 'contatado_aguardando' && (
                        <div className="inline-flex items-center gap-1">
                          <button
                            onClick={(e) => handleFollowUpFeito(lead, e)}
                            className="px-1.5 py-0.5 bg-amber-50 hover:bg-amber-100 border border-amber-300 text-amber-900 rounded text-[10px] font-semibold flex items-center gap-1"
                            title="+1 Follow-up (+4d)"
                          >
                            <RefreshCw className="w-2.5 h-2.5 text-amber-700" />
                            <span>+4d</span>
                          </button>
                          <button
                            onClick={(e) => handleRespondeu(lead.id, e)}
                            className="px-1.5 py-0.5 bg-blue-600 hover:bg-blue-700 text-white rounded text-[10px] font-bold flex items-center gap-1"
                            title="Respondeu!"
                          >
                            <MessageCircle className="w-2.5 h-2.5" />
                            <span>Respondeu</span>
                          </button>
                        </div>
                      )}

                      {lead.status !== 'nao_contatado' && lead.status !== 'contatado_aguardando' && (
                        <span className="text-[10px] text-slate-400">Em andamento</span>
                      )}
                    </td>

                    <td className="py-3 px-4 font-mono text-slate-600">
                      {formatDateBR(lead.data1Contato)}
                    </td>

                    <td className="py-3 px-4 text-center font-medium text-slate-900">
                      {daysInfo.text}
                    </td>

                    <td className="py-3 px-4 text-center" onClick={(e) => e.stopPropagation()}>
                      <button
                        onClick={() => updateLead(lead.id, { respondeu: !lead.respondeu })}
                        className={`p-1 rounded transition-colors ${
                          lead.respondeu
                            ? 'text-emerald-600'
                            : 'text-slate-300 hover:text-slate-500'
                        }`}
                        title="Alternar resposta"
                      >
                        {lead.respondeu ? (
                          <CheckCircle className="w-4 h-4" />
                        ) : (
                          <XCircle className="w-4 h-4" />
                        )}
                      </button>
                    </td>

                    <td className="py-3 px-4">
                      {lead.dataFollowUp ? (
                        <span
                          className={`font-mono text-xs px-2 py-0.5 rounded ${
                            followStatus === 'hoje'
                              ? 'bg-amber-100 text-amber-900 border border-amber-300 font-bold animate-pulse'
                              : followStatus === 'atrasado'
                              ? 'bg-rose-100 text-rose-900 border border-rose-300 font-bold'
                              : 'text-slate-600 bg-slate-100 border border-slate-200'
                          }`}
                        >
                          {formatDateBR(lead.dataFollowUp)}
                        </span>
                      ) : (
                        <span className="text-slate-400">-</span>
                      )}
                    </td>

                    <td className="py-3 px-4 text-center font-semibold text-amber-700">
                      {lead.tentativasFollowUp || 0}x
                    </td>

                    <td className="py-3 px-4">
                      {lead.prioridade === 'alta' && (
                        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-rose-50 text-rose-700 border border-rose-200">Alta</span>
                      )}
                      {lead.prioridade === 'media' && (
                        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Média</span>
                      )}
                      {lead.prioridade === 'baixa' && (
                        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-600 border border-slate-200">Baixa</span>
                      )}
                    </td>

                    <td className="py-3 px-4 text-right space-x-1" onClick={(e) => e.stopPropagation()}>
                      <button
                        onClick={() => {
                          setEditingLead(lead);
                          setIsModalOpen(true);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-800 hover:bg-slate-100 rounded transition-colors"
                        title="Editar Lead"
                      >
                        <Edit2 className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => {
                          if (window.confirm(`Excluir o lead ${lead.nome || lead.instagram}?`)) {
                            deleteLead(lead.id);
                          }
                        }}
                        className="p-1 text-slate-400 hover:text-rose-600 hover:bg-slate-100 rounded transition-colors"
                        title="Excluir Lead"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
