import React, { useState } from 'react';
import { useLeads } from '../context/LeadContext';
import { X, Sparkles, Copy, Check, Zap, CheckCircle2, ChevronRight } from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const InstagramCaptureModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const { addLead } = useLeads();
  const [urlOrHandle, setUrlOrHandle] = useState('');
  const [copied, setCopied] = useState(false);
  const [saved, setSaved] = useState(false);

  if (!isOpen) return null;

  const extractHandle = (input: string): string => {
    let clean = input.trim();
    if (!clean) return '';
    clean = clean.replace(/https?:\/\/(www\.)?instagram\.com\//i, '');
    clean = clean.split('/')[0].split('?')[0];
    clean = clean.replace('@', '').trim();
    return clean;
  };

  const handleQuickCapture = (e: React.FormEvent) => {
    e.preventDefault();
    const handle = extractHandle(urlOrHandle);
    if (!handle) return;

    const formattedName = handle
      .replace(/[._]/g, ' ')
      .replace(/\b\w/g, (char) => char.toUpperCase());

    addLead({
      nome: formattedName,
      instagram: handle,
      nicho: 'Mentoria de Concursos',
      comoEncontrei: 'Instagram Outbound',
      status: 'nao_contatado',
      data1Contato: '',
      respondeu: false,
      data2Contato: '',
      dataFollowUp: '',
      tentativasFollowUp: 0,
      dataReuniao: '',
      reuniaoRealizada: false,
      prioridade: 'media',
      proximoPasso: 'Enviar Direct de apresentação da Trajetória',
      observacoes: `Lead capturado via Instagram (@${handle}).`,
      valorProposta: 0,
    });

    setUrlOrHandle('');
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  // Código do script de extensão do Chrome (Tampermonkey / extensão própria)
  // Este código pode ser usado como UserScript no Tampermonkey
  const appBaseUrl = window.location.origin + window.location.pathname.replace(/\/$/, '');
  const userScript = `// ==UserScript==
// @name         Salvar na Trajetória
// @namespace    trajetoria-crm
// @version      1.0
// @description  Captura perfis do Instagram e salva direto no CRM Trajetória
// @match        https://www.instagram.com/*
// @grant        none
// ==/UserScript==

(function() {
  'use strict';
  // Adiciona botão flutuante na página do Instagram
  const btn = document.createElement('button');
  btn.textContent = '➕ Salvar na Trajetória';
  btn.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:9999;background:#f59e0b;color:#000;font-weight:bold;padding:10px 16px;border:none;border-radius:8px;cursor:pointer;font-size:13px;box-shadow:0 4px 12px rgba(0,0,0,0.3);';
  document.body.appendChild(btn);
  btn.onclick = function() {
    var match = location.href.match(/instagram\\.com\\/([^\\/\\?#]+)/);
    var handle = match ? match[1] : '';
    if (!handle || ['explore','direct','reels','p','stories','accounts'].includes(handle)) {
      alert('Abra o perfil de uma mentoria antes de clicar!');
      return;
    }
    var title = document.querySelector('h2')?.textContent || handle;
    window.open('${appBaseUrl}?instaHandle=' + encodeURIComponent(handle) + '&instaName=' + encodeURIComponent(title), '_blank');
  };
})();`;

  const copyScript = () => {
    navigator.clipboard.writeText(userScript);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    // Overlay: inset-0 sem flex, overflow-y-auto para permitir scroll quando necessário
    <div
      className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/50 backdrop-blur-sm animate-fadeIn"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      {/* Centralizador: min-h-full com flex e py para garantir espaço no topo */}
      <div className="flex min-h-full items-center justify-center p-4 py-8">
        {/* Modal */}
        <div className="bg-white rounded-2xl w-full max-w-lg border border-slate-200 shadow-2xl overflow-hidden">

          {/* Cabeçalho */}
          <div className="bg-gradient-to-r from-slate-900 to-slate-800 px-6 py-5 text-white flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-white/10 rounded-xl">
                <Zap className="w-5 h-5 text-amber-400" />
              </div>
              <div>
                <h3 className="font-semibold text-sm">Captura Rápida de Mentorias</h3>
                <p className="text-xs text-slate-300 mt-0.5">Cadastre leads do Instagram em segundos</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="p-6 space-y-5">

            {/* === OPÇÃO 1: Cole a URL === */}
            <div className="space-y-3 bg-slate-50 p-4 rounded-xl border border-slate-200">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-slate-900 text-white text-[10px] font-bold flex items-center justify-center flex-shrink-0">1</span>
                <span className="font-semibold text-slate-900 text-xs flex items-center gap-1.5">
                  <InstagramIcon className="w-4 h-4" />
                  Cole o link ou @handle do perfil
                </span>
              </div>
              <form onSubmit={handleQuickCapture} className="flex gap-2">
                <input
                  type="text"
                  placeholder="@mentoriaconcursos  ou  instagram.com/mentoriaconcursos"
                  value={urlOrHandle}
                  onChange={(e) => setUrlOrHandle(e.target.value)}
                  autoFocus
                  className="flex-1 bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs focus:ring-2 focus:ring-amber-400 focus:border-amber-400 focus:outline-none transition-all"
                />
                <button
                  type="submit"
                  disabled={!urlOrHandle.trim()}
                  className="bg-amber-500 hover:bg-amber-600 active:scale-95 text-slate-950 font-bold disabled:opacity-40 px-4 py-2 rounded-lg flex items-center gap-1.5 transition-all shadow-sm flex-shrink-0 text-xs"
                >
                  {saved ? (
                    <><CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" /> Salvo!</>
                  ) : (
                    <><Sparkles className="w-3.5 h-3.5" /> Capturar</>
                  )}
                </button>
              </form>
              <p className="text-[11px] text-slate-500">
                O lead vai direto para a coluna <strong>"Não Contatado"</strong> do seu Kanban!
              </p>
            </div>

            {/* === OPÇÃO 2: Tampermonkey === */}
            <div className="space-y-3 bg-amber-50/60 p-4 rounded-xl border border-amber-200/80">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-amber-500 text-white text-[10px] font-bold flex items-center justify-center flex-shrink-0">2</span>
                  <span className="font-semibold text-slate-900 text-xs">Botão 1-Clique no Instagram (Tampermonkey)</span>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-200 text-amber-900">Avançado</span>
              </div>

              <div className="text-[11px] text-slate-600 space-y-1 leading-relaxed">
                <p>Use o <strong>Tampermonkey</strong> (extensão gratuita do Chrome) para colocar um botão <em>"Salvar na Trajetória"</em> diretamente na página do Instagram. Basta:</p>
                <div className="space-y-0.5 mt-2">
                  {[
                    'Instale a extensão "Tampermonkey" no Chrome (gratuito)',
                    'Abra o Tampermonkey > "Criar novo script"',
                    'Apague tudo e cole o código abaixo',
                    'Salve com Ctrl+S — pronto!',
                  ].map((step, i) => (
                    <div key={i} className="flex items-start gap-1.5">
                      <ChevronRight className="w-3 h-3 text-amber-600 mt-0.5 flex-shrink-0" />
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              </div>

              <button
                onClick={copyScript}
                className="w-full py-2 px-3 bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold rounded-lg flex items-center justify-center gap-2 transition-all text-xs"
              >
                {copied ? <><Check className="w-3.5 h-3.5 text-emerald-800" /> Código Copiado!</> : <><Copy className="w-3.5 h-3.5" /> Copiar Código do Script</>}
              </button>

              <a
                href="https://www.tampermonkey.net/"
                target="_blank"
                rel="noreferrer"
                className="block text-center text-[11px] text-blue-600 hover:underline"
              >
                → Baixar Tampermonkey (tampermonkey.net)
              </a>
            </div>

          </div>

          <div className="px-6 py-4 border-t border-slate-200 bg-slate-50 flex justify-end">
            <button
              onClick={onClose}
              className="px-5 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 rounded-xl font-medium transition-colors text-xs"
            >
              Fechar
            </button>
          </div>

        </div>
      </div>
    </div>
  );
};
