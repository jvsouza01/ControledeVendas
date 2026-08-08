import React, { useState } from 'react';
import { useLeads } from '../context/LeadContext';
import type { Lead, LeadStatus } from '../types/lead';
import {
  formatDateBR,
  formatDaysAgoText,
  getFollowUpStatus,
} from '../utils/dateUtils';
import {
  Edit2,
  Trash2,
  ExternalLink,
  ArrowUpDown,
  CheckCircle,
  XCircle,
} from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';

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

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-700 border-collapse min-w-[1200px]">
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

              <th className="py-3.5 px-4 cursor-pointer hover:text-slate-900" onClick={() => handleSort('data1Contato')}>
                <div className="flex items-center gap-1">
                  <span>Data 1º Contato</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>

              <th className="py-3.5 px-4 text-center">
                <span>Tempo Decorrido</span>
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

              <th className="py-3.5 px-4">
                <span>Próximo Passo / Obs</span>
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

                return (
                  <tr
                    key={lead.id}
                    className="hover:bg-slate-50/70 transition-colors"
                  >
                    <td className="py-3 px-4 font-semibold text-slate-900">
                      <button
                        onClick={() => setSelectedLead(lead)}
                        className="hover:text-slate-600 text-left font-semibold"
                      >
                        {lead.nome || 'Lead sem nome'}
                      </button>
                      {lead.comoEncontrei && (
                        <div className="text-[10px] text-slate-400 font-normal">{lead.comoEncontrei}</div>
                      )}
                    </td>

                    <td className="py-3 px-4">
                      {lead.instagram ? (
                        <a
                          href={`https://instagram.com/${lead.instagram.replace('@', '')}`}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1.5 font-medium text-slate-700 hover:text-slate-900 bg-slate-100/80 px-2 py-0.5 rounded border border-slate-200"
                        >
                          <InstagramIcon className="w-3 h-3 text-slate-400" />
                          @{lead.instagram.replace('@', '')}
                          <ExternalLink className="w-2.5 h-2.5 text-slate-400" />
                        </a>
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

                    <td className="py-3 px-4">
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

                    <td className="py-3 px-4 font-mono text-slate-600">
                      {formatDateBR(lead.data1Contato)}
                    </td>

                    <td className="py-3 px-4 text-center font-medium text-slate-900">
                      {daysInfo.text}
                    </td>

                    <td className="py-3 px-4 text-center">
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
                              ? 'bg-amber-50 text-amber-700 border border-amber-200 font-semibold'
                              : followStatus === 'atrasado'
                              ? 'bg-rose-50 text-rose-700 border border-rose-200 font-semibold'
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

                    <td className="py-3 px-4 max-w-[220px]">
                      <div className="truncate text-slate-600" title={lead.proximoPasso || lead.observacoes}>
                        {lead.proximoPasso || lead.observacoes || <span className="text-slate-400">-</span>}
                      </div>
                    </td>

                    <td className="py-3 px-4 text-right space-x-1">
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
