import React, { useState, useEffect } from 'react';
import { useLeads } from '../context/LeadContext';
import type { Lead, LeadPrioridade, LeadStatus } from '../types/lead';
import { getTodayString } from '../utils/dateUtils';
import { X, Save, User } from 'lucide-react';

export const LeadModal: React.FC = () => {
  const { isModalOpen, setIsModalOpen, editingLead, addLead, updateLead } = useLeads();

  const [formData, setFormData] = useState<Partial<Lead>>({
    nome: '',
    instagram: '',
    nicho: '',
    comoEncontrei: 'Instagram - prospecção',
    status: 'nao_contatado',
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
    valorProposta: 0,
  });

  useEffect(() => {
    if (editingLead) {
      setFormData(editingLead);
    } else {
      setFormData({
        nome: '',
        instagram: '',
        nicho: '',
        comoEncontrei: 'Instagram - prospecção',
        status: 'nao_contatado',
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
        valorProposta: 0,
      });
    }
  }, [editingLead, isModalOpen]);

  if (!isModalOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const cleanData = {
      nome: formData.nome || '',
      instagram: (formData.instagram || '').replace(/^@/, '').trim(),
      nicho: formData.nicho || '',
      comoEncontrei: formData.comoEncontrei || 'Instagram - prospecção',
      status: (formData.status as LeadStatus) || 'nao_contatado',
      data1Contato: formData.data1Contato || '',
      respondeu: Boolean(formData.respondeu),
      data2Contato: formData.data2Contato || '',
      dataFollowUp: formData.dataFollowUp || '',
      tentativasFollowUp: Number(formData.tentativasFollowUp || 0),
      dataReuniao: formData.dataReuniao || '',
      reuniaoRealizada: Boolean(formData.reuniaoRealizada),
      prioridade: (formData.prioridade as LeadPrioridade) || 'media',
      proximoPasso: formData.proximoPasso || '',
      observacoes: formData.observacoes || '',
      valorProposta: Number(formData.valorProposta || 0),
    };

    if (editingLead && editingLead.id) {
      updateLead(editingLead.id, cleanData);
    } else {
      addLead(cleanData);
    }

    setIsModalOpen(false);
  };

  const handlePreencherHoje = (campo: 'data1Contato' | 'data2Contato' | 'dataFollowUp' | 'dataReuniao') => {
    setFormData((prev) => ({ ...prev, [campo]: getTodayString() }));
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto flex items-start justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white border border-slate-200 rounded-2xl w-full max-w-3xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden my-auto">
        
        <div className="px-6 py-4 border-b border-slate-200/80 flex items-center justify-between bg-slate-50/50">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-slate-100 text-slate-700 rounded-lg border border-slate-200">
              <User className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-semibold text-sm text-slate-900">
                {editingLead && editingLead.id ? 'Editar Prospect' : 'Novo Prospect'}
              </h3>
              <p className="text-[11px] text-slate-500">Preencha os dados do cliente</p>
            </div>
          </div>
          <button
            onClick={() => setIsModalOpen(false)}
            className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 overflow-y-auto space-y-5 flex-1 text-xs">
          
          <div className="space-y-3">
            <h4 className="font-semibold text-slate-500 uppercase tracking-wider text-[10px] border-b border-slate-100 pb-1">
              1. Identificação do Lead
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
              <div>
                <label className="block text-slate-700 font-medium mb-1">Nome (Mentor / Professor)</label>
                <input
                  type="text"
                  placeholder="Ex: Prof. Santiago do rumo"
                  value={formData.nome || ''}
                  onChange={(e) => setFormData((prev) => ({ ...prev, nome: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none transition-all"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-medium mb-1">@ Instagram (sem @)</label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 font-medium">@</span>
                  <input
                    type="text"
                    placeholder="profexemplo"
                    value={formData.instagram || ''}
                    onChange={(e) => setFormData((prev) => ({ ...prev, instagram: e.target.value }))}
                    className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg pl-7 pr-3 py-1.5 text-slate-900 outline-none transition-all"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-700 font-medium mb-1">Nicho</label>
                <input
                  type="text"
                  placeholder="Ex: Concurso Policial, Advogados..."
                  value={formData.nicho || ''}
                  onChange={(e) => setFormData((prev) => ({ ...prev, nicho: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none transition-all"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-medium mb-1">Como Encontrei</label>
                <input
                  type="text"
                  placeholder="Ex: Instagram - hashtag, prospecção..."
                  value={formData.comoEncontrei || ''}
                  onChange={(e) => setFormData((prev) => ({ ...prev, comoEncontrei: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none transition-all"
                />
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-slate-500 uppercase tracking-wider text-[10px] border-b border-slate-100 pb-1">
              2. Estágio e Prioridade
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
              <div>
                <label className="block text-slate-700 font-medium mb-1">Status do Lead</label>
                <select
                  value={formData.status || 'nao_contatado'}
                  onChange={(e) => setFormData((prev) => ({ ...prev, status: e.target.value as LeadStatus }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none transition-all"
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

              <div>
                <label className="block text-slate-700 font-medium mb-1">Prioridade</label>
                <select
                  value={formData.prioridade || 'media'}
                  onChange={(e) => setFormData((prev) => ({ ...prev, prioridade: e.target.value as LeadPrioridade }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none transition-all"
                >
                  <option value="alta">Alta</option>
                  <option value="media">Média</option>
                  <option value="baixa">Baixa</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-700 font-medium mb-1">Valor da Proposta (R$)</label>
                <input
                  type="number"
                  placeholder="0,00"
                  value={formData.valorProposta || 0}
                  onChange={(e) => setFormData((prev) => ({ ...prev, valorProposta: Number(e.target.value) }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none font-mono transition-all"
                />
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-slate-500 uppercase tracking-wider text-[10px] border-b border-slate-100 pb-1">
              3. Datas e Agendamentos
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-slate-700 font-medium">Data 1º Contato</label>
                  <button
                    type="button"
                    onClick={() => handlePreencherHoje('data1Contato')}
                    className="text-[10px] text-slate-500 hover:text-slate-900 underline"
                  >
                    Hoje
                  </button>
                </div>
                <input
                  type="date"
                  value={formData.data1Contato || ''}
                  onChange={(e) => setFormData((prev) => ({ ...prev, data1Contato: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none font-mono transition-all"
                />
              </div>

              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-slate-700 font-medium">Data Follow-up Agendado</label>
                  <button
                    type="button"
                    onClick={() => handlePreencherHoje('dataFollowUp')}
                    className="text-[10px] text-amber-600 hover:text-amber-700 underline"
                  >
                    Hoje
                  </button>
                </div>
                <input
                  type="date"
                  value={formData.dataFollowUp || ''}
                  onChange={(e) => setFormData((prev) => ({ ...prev, dataFollowUp: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none font-mono transition-all"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-medium mb-1">Nº Tentativas</label>
                <input
                  type="number"
                  min="0"
                  value={formData.tentativasFollowUp || 0}
                  onChange={(e) => setFormData((prev) => ({ ...prev, tentativasFollowUp: Number(e.target.value) }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none transition-all"
                />
              </div>

              <div className="flex items-center gap-4 pt-4">
                <label className="flex items-center gap-2 cursor-pointer text-slate-700 font-medium">
                  <input
                    type="checkbox"
                    checked={formData.respondeu || false}
                    onChange={(e) => setFormData((prev) => ({ ...prev, respondeu: e.target.checked }))}
                    className="w-3.5 h-3.5 rounded border-slate-300 text-slate-900 focus:ring-slate-400"
                  />
                  Respondeu ao contato?
                </label>

                <label className="flex items-center gap-2 cursor-pointer text-slate-700 font-medium">
                  <input
                    type="checkbox"
                    checked={formData.reuniaoRealizada || false}
                    onChange={(e) => setFormData((prev) => ({ ...prev, reuniaoRealizada: e.target.checked }))}
                    className="w-3.5 h-3.5 rounded border-slate-300 text-slate-900 focus:ring-slate-400"
                  />
                  Reunião Realizada?
                </label>
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-slate-500 uppercase tracking-wider text-[10px] border-b border-slate-100 pb-1">
              4. Próximos Passos e Notas
            </h4>
            <div className="space-y-3">
              <div>
                <label className="block text-slate-700 font-medium mb-1">Próximo Passo</label>
                <input
                  type="text"
                  placeholder="Ex: Reenviar mensagem caso não responda até 06/08"
                  value={formData.proximoPasso || ''}
                  onChange={(e) => setFormData((prev) => ({ ...prev, proximoPasso: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg px-3 py-1.5 text-slate-900 outline-none transition-all"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-medium mb-1">Observações</label>
                <textarea
                  rows={3}
                  placeholder="Perfil ativo, ~15k seguidores..."
                  value={formData.observacoes || ''}
                  onChange={(e) => setFormData((prev) => ({ ...prev, observacoes: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-slate-400 focus:bg-white rounded-lg p-2.5 text-slate-900 outline-none resize-none transition-all"
                />
              </div>
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100 flex justify-end gap-2">
            <button
              type="button"
              onClick={() => setIsModalOpen(false)}
              className="px-4 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-lg transition-colors text-xs"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-lg flex items-center gap-1.5 transition-all text-xs shadow-xs"
            >
              <Save className="w-3.5 h-3.5" />
              Salvar Lead
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
