import React from 'react';
import { useLeads } from '../context/LeadContext';
import {
  formatDateBR,
  formatDaysAgoText,
  getFollowUpStatus,
} from '../utils/dateUtils';
import {
  X,
  ExternalLink,
  Edit2,
  Trash2,
  Clock,
  Calendar,
} from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';
import { getGoogleCalendarUrl } from '../utils/calendarUtils';

export const LeadDetailDrawer: React.FC = () => {
  const { selectedLead, setSelectedLead, setEditingLead, setIsModalOpen, deleteLead, incrementFollowUpAttempt } = useLeads();

  if (!selectedLead) return null;

  const daysInfo = formatDaysAgoText(selectedLead.data1Contato);
  const followStatus = getFollowUpStatus(selectedLead.dataFollowUp, selectedLead.status, selectedLead.data1Contato);

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-900/40 backdrop-blur-sm flex justify-end animate-fadeIn">
      <div className="w-full max-w-md bg-white border-l border-slate-200 h-full flex flex-col shadow-2xl overflow-hidden animate-slideLeft">
        
        <div className="p-4 border-b border-slate-200/80 bg-slate-50/50 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-slate-900 text-white flex items-center justify-center shadow-xs">
              <InstagramIcon className="w-4 h-4" />
            </div>
            <div className="overflow-hidden">
              <h3 className="font-semibold text-sm text-slate-900 truncate max-w-[200px]">
                {selectedLead.nome || 'Lead sem nome'}
              </h3>
              {selectedLead.instagram && (
                <a
                  href={`https://instagram.com/${selectedLead.instagram.replace('@', '')}`}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs text-slate-500 font-medium hover:text-slate-900 flex items-center gap-1"
                >
                  @{selectedLead.instagram.replace('@', '')}
                  <ExternalLink className="w-3 h-3 text-slate-400" />
                </a>
              )}
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={() => {
                setEditingLead(selectedLead);
                setIsModalOpen(true);
              }}
              className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
              title="Editar Lead"
            >
              <Edit2 className="w-4 h-4" />
            </button>
            <button
              onClick={() => setSelectedLead(null)}
              className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="p-5 overflow-y-auto flex-1 space-y-5 text-xs text-slate-700">
          
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200/80 space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-slate-400 font-medium uppercase tracking-wider text-[10px]">Indicador de Prospecção</span>
              <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-white text-slate-700 border border-slate-200">
                {selectedLead.status.replace('_', ' ').toUpperCase()}
              </span>
            </div>

            <div className="flex justify-between items-end pt-1">
              <div>
                <p className="text-[11px] text-slate-500">Primeiro contato:</p>
                <p className="text-xs font-semibold text-slate-900 mt-0.5">
                  {selectedLead.data1Contato ? formatDateBR(selectedLead.data1Contato) : 'Pendente'}
                </p>
              </div>

              <div className="text-right">
                <p className="text-[11px] text-slate-500">Tempo decorrido:</p>
                <p className="text-sm font-bold text-slate-900">
                  {daysInfo.text}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200/80 space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-xs text-slate-900 flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-slate-500" />
                Follow-up & Agendamento
              </h4>
              <button
                onClick={() => incrementFollowUpAttempt(selectedLead.id)}
                className="px-2.5 py-1 bg-white hover:bg-slate-100 text-slate-700 font-medium rounded-md text-[10px] border border-slate-200 transition-colors shadow-xs"
              >
                +1 Tentativa ({selectedLead.tentativasFollowUp}x)
              </button>
            </div>

            <div className="flex justify-between items-center text-xs pt-1">
              <span className="text-slate-500">Data Agendada:</span>
              <span className="font-mono font-medium text-slate-900">
                {selectedLead.dataFollowUp ? formatDateBR(selectedLead.dataFollowUp) : 'Não agendado'}
              </span>
            </div>

            {selectedLead.dataFollowUp && (
              <a
                href={getGoogleCalendarUrl(selectedLead, 'followup')}
                target="_blank"
                rel="noreferrer"
                className="w-full py-1.5 px-3 bg-white hover:bg-slate-100 border border-slate-300 text-slate-800 font-medium rounded-lg flex items-center justify-center gap-1.5 transition-all text-xs shadow-2xs"
              >
                <Calendar className="w-3.5 h-3.5 text-blue-600" />
                Agendar no Google Calendar
              </a>
            )}

            {selectedLead.dataReuniao && (
              <a
                href={getGoogleCalendarUrl(selectedLead, 'reuniao')}
                target="_blank"
                rel="noreferrer"
                className="w-full py-1.5 px-3 bg-blue-50 hover:bg-blue-100 border border-blue-200 text-blue-800 font-semibold rounded-lg flex items-center justify-center gap-1.5 transition-all text-xs shadow-2xs"
              >
                <Calendar className="w-3.5 h-3.5 text-blue-600" />
                Agendar Demo ({formatDateBR(selectedLead.dataReuniao)}) no Google Calendar
              </a>
            )}

            {followStatus === 'hoje' && (
              <div className="p-2 bg-amber-50 text-amber-800 font-medium text-center rounded-lg border border-amber-200">
                Follow-up agendado para hoje.
              </div>
            )}
            {followStatus === 'atrasado' && (
              <div className="p-2 bg-rose-50 text-rose-800 font-medium text-center rounded-lg border border-rose-200">
                Follow-up com data atrasada.
              </div>
            )}
          </div>

          <div className="space-y-2">
            <h4 className="font-semibold text-slate-400 uppercase tracking-wider text-[10px]">Informações Gerais</h4>
            <div className="grid grid-cols-2 gap-2.5 text-xs">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span className="text-slate-400 block text-[10px]">Nicho:</span>
                <span className="font-medium text-slate-900">{selectedLead.nicho || '-'}</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span className="text-slate-400 block text-[10px]">Como Encontrei:</span>
                <span className="font-medium text-slate-900">{selectedLead.comoEncontrei || '-'}</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span className="text-slate-400 block text-[10px]">Respondeu?</span>
                <span className={`font-medium ${selectedLead.respondeu ? 'text-emerald-600' : 'text-slate-600'}`}>
                  {selectedLead.respondeu ? 'Sim' : 'Não'}
                </span>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span className="text-slate-400 block text-[10px]">Prioridade:</span>
                <span className="font-medium text-slate-900 capitalize">{selectedLead.prioridade}</span>
              </div>
            </div>
          </div>

          {selectedLead.proximoPasso && (
            <div className="bg-slate-50 border border-slate-200/80 p-3 rounded-xl space-y-1">
              <span className="text-[10px] font-semibold uppercase text-slate-500 tracking-wider">Próximo Passo</span>
              <p className="text-slate-800 text-xs font-medium">{selectedLead.proximoPasso}</p>
            </div>
          )}

          {selectedLead.observacoes && (
            <div className="bg-slate-50 border border-slate-200/80 p-3 rounded-xl space-y-1">
              <span className="text-[10px] font-semibold uppercase text-slate-400 tracking-wider">Observações</span>
              <p className="text-slate-700 text-xs whitespace-pre-line">{selectedLead.observacoes}</p>
            </div>
          )}

          {selectedLead.instagram && (
            <a
              href={`https://instagram.com/${selectedLead.instagram.replace('@', '')}`}
              target="_blank"
              rel="noreferrer"
              className="w-full py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-xl flex items-center justify-center gap-2 transition-all text-xs shadow-xs"
            >
              <InstagramIcon className="w-3.5 h-3.5" />
              Abrir Perfil no Instagram (@{selectedLead.instagram.replace('@', '')})
            </a>
          )}
        </div>

        <div className="p-4 border-t border-slate-200 bg-slate-50/50 flex justify-between items-center">
          <button
            onClick={() => {
              if (window.confirm(`Tem certeza que deseja excluir o lead ${selectedLead.nome}?`)) {
                deleteLead(selectedLead.id);
              }
            }}
            className="text-xs text-rose-600 hover:text-rose-700 flex items-center gap-1 font-medium transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            Excluir Lead
          </button>
          <button
            onClick={() => setSelectedLead(null)}
            className="px-4 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium rounded-lg transition-colors"
          >
            Fechar
          </button>
        </div>

      </div>
    </div>
  );
};
