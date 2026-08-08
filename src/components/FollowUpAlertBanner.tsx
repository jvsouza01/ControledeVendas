import React from 'react';
import { useLeads } from '../context/LeadContext';
import { getFollowUpStatus, formatDateBR } from '../utils/dateUtils';
import { Bell, AlertCircle, CheckCircle2, Calendar } from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';
import { getGoogleCalendarUrl } from '../utils/calendarUtils';

export const FollowUpAlertBanner: React.FC = () => {
  const { leads, setSelectedLead, filters, setFilters } = useLeads();

  const urgentLeads = leads.filter((lead) => {
    const status = getFollowUpStatus(lead.dataFollowUp, lead.status, lead.data1Contato);
    return status === 'hoje' || status === 'atrasado';
  });

  const hojeCount = leads.filter(l => getFollowUpStatus(l.dataFollowUp, l.status, l.data1Contato) === 'hoje').length;
  const atrasadosCount = leads.filter(l => getFollowUpStatus(l.dataFollowUp, l.status, l.data1Contato) === 'atrasado').length;

  if (urgentLeads.length === 0) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-3.5 flex items-center justify-between shadow-xs mb-6 text-slate-700">
        <div className="flex items-center gap-3">
          <div className="p-1.5 bg-emerald-50 text-emerald-600 rounded-lg border border-emerald-200/60">
            <CheckCircle2 className="w-4 h-4" />
          </div>
          <div>
            <h4 className="font-semibold text-xs text-slate-900">Follow-ups em dia</h4>
            <p className="text-[11px] text-slate-500">Nenhum contato pendente para hoje ou com data em atraso.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs mb-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-amber-50 text-amber-600 rounded-lg border border-amber-200/60">
            <Bell className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h4 className="font-semibold text-xs text-slate-900">
                Central de Follow-ups Urgentes
              </h4>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-amber-50 text-amber-700 border border-amber-200">
                {urgentLeads.length} pendentes
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              {hojeCount > 0 && <span>{hojeCount} agendados para hoje</span>}
              {hojeCount > 0 && atrasadosCount > 0 && <span> • </span>}
              {atrasadosCount > 0 && <span className="text-rose-600 font-medium">{atrasadosCount} atrasados</span>}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() =>
              setFilters((prev) => ({
                ...prev,
                apenasFollowUpHojeOuAtrasado: !prev.apenasFollowUpHojeOuAtrasado,
              }))
            }
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
              filters.apenasFollowUpHojeOuAtrasado
                ? 'bg-slate-900 text-white font-semibold shadow-xs'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200/80'
            }`}
          >
            <AlertCircle className="w-3.5 h-3.5" />
            {filters.apenasFollowUpHojeOuAtrasado ? 'Mostrando Apenas Urgentes' : 'Filtrar Urgentes'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5 mt-3 pt-3 border-t border-slate-100">
        {urgentLeads.slice(0, 3).map((lead) => {
          const fStatus = getFollowUpStatus(lead.dataFollowUp, lead.status, lead.data1Contato);
          const isAtrasado = fStatus === 'atrasado';
          return (
            <div
              key={lead.id}
              className="bg-slate-50 border border-slate-200/80 hover:border-slate-300 p-2.5 rounded-lg flex items-center justify-between text-xs transition-all"
            >
              <div className="overflow-hidden mr-2 cursor-pointer" onClick={() => setSelectedLead(lead)}>
                <div className="font-semibold text-slate-900 truncate hover:text-slate-700">
                  {lead.nome}
                </div>
                <div className="text-[11px] text-slate-500 flex items-center gap-1 truncate font-medium">
                  <InstagramIcon className="w-3 h-3 text-slate-400 flex-shrink-0" />
                  @{lead.instagram || 'sem_handle'}
                </div>
              </div>

              <div className="flex items-center gap-1.5 flex-shrink-0">
                <span
                  className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${
                    isAtrasado
                      ? 'bg-rose-50 text-rose-700 border border-rose-200'
                      : 'bg-amber-50 text-amber-700 border border-amber-200'
                  }`}
                >
                  {isAtrasado ? 'Atrasado' : 'Hoje'} ({formatDateBR(lead.dataFollowUp)})
                </span>
                <a
                  href={getGoogleCalendarUrl(lead, 'followup')}
                  target="_blank"
                  rel="noreferrer"
                  className="p-1 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors"
                  title="Agendar no Google Calendar"
                >
                  <Calendar className="w-3.5 h-3.5" />
                </a>
                <a
                  href={`https://instagram.com/${lead.instagram.replace('@', '')}`}
                  target="_blank"
                  rel="noreferrer"
                  className="p-1 text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 rounded transition-colors"
                  title="Abrir Instagram"
                >
                  <InstagramIcon className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
