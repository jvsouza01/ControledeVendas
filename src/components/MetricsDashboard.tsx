import React from 'react';
import { useLeads } from '../context/LeadContext';
import { getFollowUpStatus } from '../utils/dateUtils';
import {
  Users,
  MessageSquare,
  Trophy,
  AlertCircle,
  TrendingUp,
  Target,
  ArrowUpRight,
} from 'lucide-react';

export const MetricsDashboard: React.FC = () => {
  const { leads, setFilters, setViewMode } = useLeads();

  const totalLeads = leads.length;
  const contatados = leads.filter((l) => l.status !== 'nao_contatado');
  const contatadosCount = contatados.length;
  const taxaContatados = totalLeads > 0 ? Math.round((contatadosCount / totalLeads) * 100) : 0;

  const responderam = leads.filter((l) => l.respondeu || l.status === 'em_conversa' || l.status === 'reuniao_agendada' || l.status === 'reuniao_realizada' || l.status === 'fechado');
  const taxaResposta = contatadosCount > 0 ? Math.round((responderam.length / contatadosCount) * 100) : 0;

  const reunioesMarcadas = leads.filter((l) => l.status === 'reuniao_agendada' || l.status === 'reuniao_realizada' || l.dataReuniao).length;
  const fechados = leads.filter((l) => l.status === 'fechado');
  const valorTotalVendas = fechados.reduce((acc, l) => acc + (l.valorProposta || 0), 0);

  const followUpHoje = leads.filter((l) => getFollowUpStatus(l.dataFollowUp, l.status, l.data1Contato) === 'hoje').length;
  const followUpAtrasado = leads.filter((l) => getFollowUpStatus(l.dataFollowUp, l.status, l.data1Contato) === 'atrasado').length;

  const nichosMap: Record<string, number> = {};
  leads.forEach((l) => {
    const n = l.nicho || 'Sem Nicho';
    nichosMap[n] = (nichosMap[n] || 0) + 1;
  });
  const topNichos = Object.entries(nichosMap)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  const funil = [
    { label: 'Não Contatados', count: leads.filter((l) => l.status === 'nao_contatado').length, color: 'bg-slate-300' },
    { label: 'Aguardando Resposta', count: leads.filter((l) => l.status === 'contatado_aguardando').length, color: 'bg-amber-400' },
    { label: 'Em Conversa', count: leads.filter((l) => l.status === 'em_conversa').length, color: 'bg-blue-500' },
    { label: 'Reunião Agendada/Realizada', count: leads.filter((l) => l.status === 'reuniao_agendada' || l.status === 'reuniao_realizada').length, color: 'bg-purple-500' },
    { label: 'Clientes Fechados', count: fechados.length, color: 'bg-emerald-500' },
  ];

  return (
    <div className="space-y-5 pb-12 animate-fadeIn">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Total em Prospecção</p>
              <h3 className="text-2xl font-bold text-slate-900 mt-1">{totalLeads}</h3>
            </div>
            <div className="p-2.5 bg-slate-100 text-slate-700 rounded-lg border border-slate-200">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
            <span className="text-emerald-600 font-semibold flex items-center gap-0.5">
              <TrendingUp className="w-3.5 h-3.5" />
              {taxaContatados}%
            </span>
            <span>contatados ({contatadosCount} de {totalLeads})</span>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Taxa de Resposta</p>
              <h3 className="text-2xl font-bold text-slate-900 mt-1">{taxaResposta}%</h3>
            </div>
            <div className="p-2.5 bg-slate-100 text-slate-700 rounded-lg border border-slate-200">
              <MessageSquare className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
            <span className="text-slate-900 font-medium">{responderam.length} responderam</span>
            <span>do total contatado</span>
          </div>
        </div>

        <div
          onClick={() => {
            setFilters((prev) => ({ ...prev, apenasFollowUpHojeOuAtrasado: true }));
            setViewMode('kanban');
          }}
          className="bg-white border border-slate-200 hover:border-slate-300 rounded-xl p-4 shadow-xs cursor-pointer transition-all"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Follow-ups Urgentes</p>
              <h3 className="text-2xl font-bold text-amber-600 mt-1">{followUpHoje + followUpAtrasado}</h3>
            </div>
            <div className="p-2.5 bg-amber-50 text-amber-600 rounded-lg border border-amber-200">
              <AlertCircle className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center justify-between text-xs">
            <span className="text-slate-600">{followUpHoje} para hoje</span>
            <span className="text-rose-600 font-medium">{followUpAtrasado} atrasados</span>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Clientes Fechados</p>
              <h3 className="text-2xl font-bold text-emerald-600 mt-1">{fechados.length}</h3>
            </div>
            <div className="p-2.5 bg-emerald-50 text-emerald-600 rounded-lg border border-emerald-200">
              <Trophy className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
            <span>Reuniões marcadas: <strong className="text-slate-900">{reunioesMarcadas}</strong></span>
            {valorTotalVendas > 0 && (
              <span className="text-emerald-600 font-semibold">R$ {valorTotalVendas.toLocaleString('pt-BR')}</span>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div className="lg:col-span-2 bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-sm font-semibold text-slate-900 flex items-center gap-2">
                <Target className="w-4 h-4 text-slate-500" />
                Funil de Conversão
              </h3>
              <p className="text-xs text-slate-500">Distribuição dos prospects por estágio</p>
            </div>
          </div>

          <div className="space-y-3.5">
            {funil.map((f, idx) => {
              const pct = totalLeads > 0 ? Math.round((f.count / totalLeads) * 100) : 0;
              return (
                <div key={idx} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-700 font-medium">{f.label}</span>
                    <span className="text-slate-500 font-mono">
                      {f.count} lead(s) <span className="text-slate-400">({pct}%)</span>
                    </span>
                  </div>
                  <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden p-0.5 border border-slate-200">
                    <div
                      className={`h-full ${f.color} rounded-full transition-all duration-300`}
                      style={{ width: `${Math.max(pct, 2)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-1">Top Nichos</h3>
            <p className="text-xs text-slate-500 mb-4">Volume por nicho de atuação</p>

            <div className="space-y-3">
              {topNichos.map(([nicho, count]) => {
                const max = topNichos[0][1] || 1;
                const percentage = Math.round((count / max) * 100);
                return (
                  <div key={nicho} className="space-y-1">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-700 truncate max-w-[180px]">{nicho}</span>
                      <span className="text-slate-900 font-semibold">{count}</span>
                    </div>
                    <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden border border-slate-200">
                      <div
                        className="bg-slate-700 h-full rounded-full"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="mt-5 pt-3 border-t border-slate-100">
            <button
              onClick={() => setViewMode('kanban')}
              className="w-full py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium rounded-lg flex items-center justify-center gap-1 transition-colors"
            >
              <span>Ver Kanban Completo</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
