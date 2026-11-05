import React, { useState } from 'react';
import { useLeads } from '../context/LeadContext';
import {
  formatDateBR,
  formatDaysAgoText,
  getFollowUpStatus,
  getTodayString,
  addDaysToDate,
} from '../utils/dateUtils';
import {
  X,
  ExternalLink,
  Edit2,
  Trash2,
  Clock,
  Calendar,
  MessageSquare,
  ShoppingBag,
  Link as LinkIcon,
  Copy,
  Check,
  CheckCircle2,
  RefreshCw,
  Sparkles,
} from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';
import { getGoogleCalendarUrl } from '../utils/calendarUtils';

export const LeadDetailDrawer: React.FC = () => {
  const {
    selectedLead,
    setSelectedLead,
    setEditingLead,
    setIsModalOpen,
    deleteLead,
    incrementFollowUpAttempt,
    updateLead,
  } = useLeads();

  const [copiedTemplateId, setCopiedTemplateId] = useState<number | null>(null);

  if (!selectedLead) return null;

  const daysInfo = formatDaysAgoText(selectedLead.data1Contato);
  const followStatus = getFollowUpStatus(selectedLead.dataFollowUp, selectedLead.status, selectedLead.data1Contato);
  const cleanHandle = (selectedLead.instagram || '').replace('@', '').trim();

  // Extração de primeiro nome para templates
  const getFirstName = (fullName?: string) => {
    if (!fullName) return 'Professor(a)';
    const clean = fullName.replace(/^(Prof\.|Profª\.|Professor|Professora)\s+/i, '').trim();
    return clean.split(' ')[0] || 'Professor(a)';
  };

  const mentorFirstName = getFirstName(selectedLead.nome);
  const mentorNiche = selectedLead.nicho || 'concursos públicos';

  // Detecção de links ricos em observações e dados
  const extractUrls = (text?: string) => {
    if (!text) return [];
    const urlRegex = /(https?:\/\/[^\s"'<>]+)/g;
    return text.match(urlRegex) || [];
  };

  const allUrls = extractUrls(selectedLead.observacoes);
  const whatsappUrl = allUrls.find((u) => u.includes('wa.me') || u.includes('whatsapp.com'));
  const checkoutUrl = allUrls.find(
    (u) => u.includes('kiwify.com.br') || u.includes('hotmart.com') || u.includes('eduzz.com')
  );
  const bioLinkUrl = allUrls.find(
    (u) => u.includes('linktr.ee') || u.includes('beacons.ai') || u.includes('bio.site')
  );
  const extraSiteUrl = allUrls.find(
    (u) =>
      u !== whatsappUrl &&
      u !== checkoutUrl &&
      u !== bioLinkUrl &&
      !u.includes('instagram.com') &&
      !u.includes('youtube.com')
  );

  // Ações Rápidas de 1 Clique
  const handleMarkContatado = () => {
    const today = getTodayString();
    const nextFollow = addDaysToDate(3);
    updateLead(selectedLead.id, {
      status: 'contatado_aguardando',
      data1Contato: today,
      dataFollowUp: nextFollow,
      proximoPasso: 'Fazer 1º Follow-up no Direct/WhatsApp',
    });
  };

  const handleFollowUpFeito = () => {
    const today = getTodayString();
    const nextFollow = addDaysToDate(4);
    updateLead(selectedLead.id, {
      tentativasFollowUp: (selectedLead.tentativasFollowUp || 0) + 1,
      data2Contato: today,
      dataFollowUp: nextFollow,
      proximoPasso: 'Aguardando resposta do Follow-up',
    });
  };

  const handleRespondeu = () => {
    updateLead(selectedLead.id, {
      status: 'em_conversa',
      respondeu: true,
      proximoPasso: 'Desenvolver conversa / sondar dores da plataforma',
    });
  };

  // Playbook de Abordagem
  const PLAYBOOK_TEMPLATES = [
    {
      id: 1,
      titulo: '1. Quebra-Gelo Direct (Natural / Sem parecer bot)',
      canal: 'Instagram Direct',
      texto: `Olá ${mentorFirstName}, tudo bem? Vi seu trabalho incrível com mentoria para ${mentorNiche}.\n\nQueria te fazer uma pergunta rápida: hoje você entrega os cronogramas e o acompanhamento de questões para os seus alunos em planilha/PDF ou já usa uma plataforma própria?`,
    },
    {
      id: 2,
      titulo: '2. Ângulo Dor da Planilha & Kiwify/Hotmart',
      canal: 'Direct ou WhatsApp',
      texto: `Fala ${mentorFirstName}! Notei que sua mentoria de ${mentorNiche} tem bastante procura.\n\nMuitos mentores me relatam que perdem horas atualizando planilhas no Excel e tirando dúvidas de questões manualmente no WhatsApp. Nós criamos uma solução whitelabel onde seu aluno tem cronograma automatizado + edital verticalizado inteligente com a SUA marca.\n\nTeria 5 minutinhos essa semana para ver uma demo rápida?`,
    },
    {
      id: 3,
      titulo: '3. Abordagem WhatsApp Comercial',
      canal: 'WhatsApp',
      texto: `Oi ${mentorFirstName}, como vai? Te mandei uma mensagem no Direct do Insta sobre a sua mentoria de ${mentorNiche}.\n\nSou da Trajetória e ajudamos mentores independentes a terem sua própria plataforma de estudos com cronograma inteligente e edital verticalizado para os alunos. Quando teria um tempinho para batermos um papo rápido?`,
    },
    {
      id: 4,
      titulo: '4. Follow-up Rápido (+3 dias)',
      canal: 'Follow-up',
      texto: `Oi ${mentorFirstName}, tudo bem? Sei que a sua rotina com os alunos de ${mentorNiche} deve estar bem corrida!\n\nPassando só para saber se conseguiu dar uma olhada na mensagem anterior. Abraço!`,
    },
  ];

  const handleCopyTemplate = (id: number, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedTemplateId(id);
    setTimeout(() => setCopiedTemplateId(null), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-900/40 backdrop-blur-sm flex justify-end animate-fadeIn">
      <div className="w-full max-w-lg bg-white border-l border-slate-200 h-full flex flex-col shadow-2xl overflow-hidden animate-slideLeft">
        
        {/* Cabeçalho */}
        <div className="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-slate-900 text-white flex items-center justify-center shadow-xs">
              <InstagramIcon className="w-4 h-4" />
            </div>
            <div className="overflow-hidden">
              <h3 className="font-bold text-sm text-slate-900 truncate max-w-[240px]">
                {selectedLead.nome || 'Lead sem nome'}
              </h3>
              {cleanHandle && (
                <div className="flex items-center gap-2 mt-0.5">
                  <a
                    href={`https://instagram.com/${cleanHandle}`}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-slate-500 font-medium hover:text-indigo-600 flex items-center gap-1 transition-colors"
                  >
                    @{cleanHandle}
                    <ExternalLink className="w-3 h-3 text-slate-400" />
                  </a>
                  <a
                    href={`https://ig.me/m/${cleanHandle}`}
                    target="_blank"
                    rel="noreferrer"
                    className="text-[10px] text-indigo-600 hover:text-indigo-800 bg-indigo-50 px-1.5 py-0.2 rounded font-semibold border border-indigo-100"
                  >
                    Abrir Direct ✉️
                  </a>
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={() => {
                setEditingLead(selectedLead);
                setIsModalOpen(true);
              }}
              className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 rounded-lg transition-colors"
              title="Editar Lead"
            >
              <Edit2 className="w-4 h-4" />
            </button>
            <button
              onClick={() => setSelectedLead(null)}
              className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 rounded-lg transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Conteúdo com Scroll */}
        <div className="p-5 overflow-y-auto flex-1 space-y-5 text-xs text-slate-700">
          
          {/* BOTÕES DE AÇÃO RÁPIDA 1-CLIQUE NO TOPO DO DRAWER */}
          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Ações de Fluxo Rápido</span>
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-white text-slate-700 border border-slate-200">
                {selectedLead.status.replace('_', ' ').toUpperCase()}
              </span>
            </div>

            {selectedLead.status === 'nao_contatado' && (
              <button
                onClick={handleMarkContatado}
                className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 active:scale-98 text-white rounded-lg text-xs font-bold flex items-center justify-center gap-2 transition-all shadow-xs"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>✅ Marcar como Contatado (+3d Follow-up)</span>
              </button>
            )}

            {selectedLead.status === 'contatado_aguardando' && (
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={handleFollowUpFeito}
                  className="py-1.5 px-3 bg-amber-50 hover:bg-amber-100 border border-amber-300 text-amber-900 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-all"
                >
                  <RefreshCw className="w-3.5 h-3.5 text-amber-700" />
                  <span>Follow-up Feito (+4d)</span>
                </button>
                <button
                  onClick={handleRespondeu}
                  className="py-1.5 px-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold flex items-center justify-center gap-1.5 transition-all shadow-xs"
                >
                  <MessageSquare className="w-3.5 h-3.5" />
                  <span>💬 Mentor Respondeu!</span>
                </button>
              </div>
            )}
          </div>

          {/* BOTÕES DE CONTATO DETECTADOS (WHATSAPP, CHECKOUT, LINKTREE) */}
          {(whatsappUrl || checkoutUrl || bioLinkUrl || extraSiteUrl || cleanHandle) && (
            <div className="space-y-1.5">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">
                Canais e Links Detectados
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {cleanHandle && (
                  <a
                    href={`https://ig.me/m/${cleanHandle}`}
                    target="_blank"
                    rel="noreferrer"
                    className="p-2 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 text-indigo-900 rounded-lg font-semibold flex items-center justify-between text-xs transition-colors"
                  >
                    <span className="flex items-center gap-1.5">
                      <InstagramIcon className="w-3.5 h-3.5 text-indigo-600" />
                      Direct do Instagram
                    </span>
                    <ExternalLink className="w-3 h-3 text-indigo-400" />
                  </a>
                )}

                {whatsappUrl && (
                  <a
                    href={whatsappUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="p-2 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 text-emerald-900 rounded-lg font-semibold flex items-center justify-between text-xs transition-colors"
                  >
                    <span className="flex items-center gap-1.5">
                      💬 Chamar WhatsApp
                    </span>
                    <ExternalLink className="w-3 h-3 text-emerald-400" />
                  </a>
                )}

                {checkoutUrl && (
                  <a
                    href={checkoutUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="p-2 bg-purple-50 hover:bg-purple-100 border border-purple-200 text-purple-900 rounded-lg font-semibold flex items-center justify-between text-xs transition-colors"
                  >
                    <span className="flex items-center gap-1.5">
                      <ShoppingBag className="w-3.5 h-3.5 text-purple-600" />
                      Página / Checkout
                    </span>
                    <ExternalLink className="w-3 h-3 text-purple-400" />
                  </a>
                )}

                {bioLinkUrl && (
                  <a
                    href={bioLinkUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="p-2 bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-800 rounded-lg font-semibold flex items-center justify-between text-xs transition-colors"
                  >
                    <span className="flex items-center gap-1.5">
                      <LinkIcon className="w-3.5 h-3.5 text-slate-600" />
                      Bio / Linktree
                    </span>
                    <ExternalLink className="w-3 h-3 text-slate-400" />
                  </a>
                )}

                {extraSiteUrl && (
                  <a
                    href={extraSiteUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="p-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-800 rounded-lg font-semibold flex items-center justify-between text-xs transition-colors col-span-1 sm:col-span-2"
                  >
                    <span className="flex items-center gap-1.5 truncate">
                      🌐 {extraSiteUrl.replace('https://', '').replace('http://', '').split('/')[0]}
                    </span>
                    <ExternalLink className="w-3 h-3 text-slate-400 flex-shrink-0" />
                  </a>
                )}
              </div>
            </div>
          )}

          {/* PLAYBOOK DE ABORDAGEM (1-CLICK COPY) */}
          <div className="bg-gradient-to-br from-indigo-50/50 to-slate-50 p-4 rounded-xl border border-indigo-100 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-indigo-600" />
                <h4 className="font-bold text-xs text-indigo-950">Playbook de Abordagem (1-Click Copy)</h4>
              </div>
              <span className="text-[10px] text-indigo-600 font-medium">Personalizado para {mentorFirstName}</span>
            </div>

            <div className="space-y-2.5">
              {PLAYBOOK_TEMPLATES.map((tpl) => (
                <div key={tpl.id} className="bg-white p-3 rounded-lg border border-indigo-100/80 shadow-2xs space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-[11px] text-slate-800">{tpl.titulo}</span>
                    <button
                      onClick={() => handleCopyTemplate(tpl.id, tpl.texto)}
                      className="px-2 py-0.5 rounded text-[10px] font-bold transition-all flex items-center gap-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200"
                    >
                      {copiedTemplateId === tpl.id ? (
                        <>
                          <Check className="w-3 h-3 text-emerald-600" />
                          <span className="text-emerald-700">Copiado!</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3 text-indigo-500" />
                          <span>Copiar</span>
                        </>
                      )}
                    </button>
                  </div>
                  <p className="text-[11px] text-slate-600 whitespace-pre-line leading-relaxed bg-slate-50 p-2 rounded border border-slate-100 font-mono">
                    {tpl.texto}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Informações de Follow-up e Agendamento */}
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
                +1 Tentativa ({selectedLead.tentativasFollowUp || 0}x)
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

            {followStatus === 'hoje' && (
              <div className="p-2 bg-amber-100 text-amber-900 font-bold text-center rounded-lg border border-amber-300 animate-pulse">
                ⏰ Follow-up agendado para HOJE!
              </div>
            )}
            {followStatus === 'atrasado' && (
              <div className="p-2 bg-rose-100 text-rose-900 font-bold text-center rounded-lg border border-rose-300">
                ⚠️ Follow-up atrasado! Faça contato agora.
              </div>
            )}
          </div>

          {/* Dados Gerais */}
          <div className="space-y-2">
            <h4 className="font-semibold text-slate-400 uppercase tracking-wider text-[10px]">Dados do Prospect</h4>
            <div className="grid grid-cols-2 gap-2.5 text-xs">
              <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200/80">
                <span className="text-slate-400 block text-[10px]">Nicho:</span>
                <span className="font-medium text-slate-900">{selectedLead.nicho || '-'}</span>
              </div>
              <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200/80">
                <span className="text-slate-400 block text-[10px]">Como Encontrei:</span>
                <span className="font-medium text-slate-900">{selectedLead.comoEncontrei || '-'}</span>
              </div>
              <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200/80">
                <span className="text-slate-400 block text-[10px]">1º Contato / Tempo:</span>
                <span className="font-medium text-slate-900">{formatDateBR(selectedLead.data1Contato)} ({daysInfo.text})</span>
              </div>
              <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200/80">
                <span className="text-slate-400 block text-[10px]">Prioridade:</span>
                <span className="font-medium text-slate-900 capitalize">{selectedLead.prioridade}</span>
              </div>
            </div>
          </div>

          {/* Próximo Passo */}
          {selectedLead.proximoPasso && (
            <div className="bg-slate-50 border border-slate-200/80 p-3 rounded-xl space-y-1">
              <span className="text-[10px] font-semibold uppercase text-slate-500 tracking-wider">Próximo Passo</span>
              <p className="text-slate-800 text-xs font-medium">{selectedLead.proximoPasso}</p>
            </div>
          )}

          {/* Observações */}
          {selectedLead.observacoes && (
            <div className="bg-slate-50 border border-slate-200/80 p-3 rounded-xl space-y-1">
              <span className="text-[10px] font-semibold uppercase text-slate-400 tracking-wider">Observações & Links</span>
              <p className="text-slate-700 text-xs whitespace-pre-line leading-relaxed">{selectedLead.observacoes}</p>
            </div>
          )}

          {/* Botão Aberto do Perfil */}
          {cleanHandle && (
            <a
              href={`https://instagram.com/${cleanHandle}`}
              target="_blank"
              rel="noreferrer"
              className="w-full py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-xl flex items-center justify-center gap-2 transition-all text-xs shadow-xs"
            >
              <InstagramIcon className="w-3.5 h-3.5" />
              Abrir Perfil Completo (@{cleanHandle})
            </a>
          )}
        </div>

        {/* Rodapé do Drawer */}
        <div className="p-4 border-t border-slate-200 bg-slate-50 flex justify-between items-center">
          <button
            onClick={() => {
              if (window.confirm(`Tem certeza que deseja excluir o lead ${selectedLead.nome || selectedLead.instagram}?`)) {
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
            className="px-4 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium rounded-lg transition-colors border border-slate-200"
          >
            Fechar
          </button>
        </div>

      </div>
    </div>
  );
};
