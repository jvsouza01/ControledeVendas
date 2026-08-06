import React, { useState } from 'react';
import { useLeads } from '../context/LeadContext';
import { X, Sparkles, Bookmark, Copy, Check, Zap } from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const InstagramCaptureModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const { addLead } = useLeads();
  const [urlOrHandle, setUrlOrHandle] = useState('');
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  // Extrai o @handle limpo da URL ou texto digitado
  const extractHandle = (input: string): string => {
    let clean = input.trim();
    if (!clean) return '';
    clean = clean.replace(/https?:\/\/(www\.)?instagram\.com\//i, '');
    clean = clean.split('/')[0].split('?')[0];
    clean = clean.replace('@', '');
    return clean;
  };

  const handleQuickCapture = (e: React.FormEvent) => {
    e.preventDefault();
    const handle = extractHandle(urlOrHandle);
    if (!handle) return;

    // Converte handle em nome amigável para o lead (ex: "mentoria_concursos_sp" -> "Mentoria Concursos Sp")
    const formattedName = handle
      .replace(/[._]/g, ' ')
      .replace(/\b\w/g, (char) => char.toUpperCase());

    // Salva o lead diretamente no CRM (na coluna Não Contatado)
    addLead({
      nome: formattedName,
      instagram: handle,
      nicho: 'Mentoria de Concursos',
      comoEncontrei: 'Instagram Outbound',
      status: 'nao_contatado',
      data1Contato: new Date().toISOString().split('T')[0],
      respondeu: false,
      data2Contato: '',
      dataFollowUp: new Date().toISOString().split('T')[0],
      tentativasFollowUp: 0,
      dataReuniao: '',
      reuniaoRealizada: false,
      prioridade: 'media',
      proximoPasso: 'Enviar Direct de apresentação da Trajetória',
      observacoes: `Lead capturado via Instagram (@${handle}).`,
      valorProposta: 0,
    });

    setUrlOrHandle('');
    onClose();
  };

  // Código do Bookmarklet para a barra de favoritos do navegador
  const appBaseUrl = window.location.origin + window.location.pathname;
  const bookmarkletCode = `javascript:(function(){
    var url = window.location.href;
    var match = url.match(/instagram\\.com\\/([^\\/?#]+)/);
    var handle = match ? match[1] : '';
    if(!handle || handle==='explore'||handle==='direct'||handle==='reels'){
      alert('Abra um perfil de Mentoria no Instagram antes de clicar!');
      return;
    }
    var title = document.title ? document.title.split('(')[0].replace('• Instagram photos and videos','').trim() : handle;
    var target = '${appBaseUrl}?instaHandle=' + encodeURIComponent(handle) + '&instaName=' + encodeURIComponent(title);
    window.open(target, '_blank');
  })();`;

  const copyBookmarklet = () => {
    navigator.clipboard.writeText(bookmarkletCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/50 backdrop-blur-xs flex items-start justify-center p-4 sm:p-6 animate-fadeIn">
      <div className="bg-white rounded-2xl max-w-lg w-full max-h-[85vh] flex flex-col border border-slate-200 shadow-2xl overflow-hidden my-auto">
        
        {/* Cabeçalho */}
        <div className="bg-gradient-to-r from-slate-900 to-slate-800 p-5 text-white flex items-center justify-between flex-shrink-0">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-white/10 rounded-xl backdrop-blur-md">
              <Zap className="w-5 h-5 text-amber-400" />
            </div>
            <div>
              <h3 className="font-semibold text-sm">Captura Rápida de Mentorias</h3>
              <p className="text-xs text-slate-300">Cadastre leads do Instagram em segundos</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6 text-xs text-slate-700 overflow-y-auto flex-1">
          
          {/* Método 1: Cole a URL / Handle */}
          <form onSubmit={handleQuickCapture} className="space-y-3 bg-slate-50 p-4 rounded-xl border border-slate-200/80">
            <label className="block font-semibold text-slate-900 flex items-center gap-1.5 text-xs">
              <InstagramIcon className="w-4 h-4 text-slate-700" />
              Opção 1: Cole a URL ou @handle do perfil
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Ex: instagram.com/mentoriaconcursos ou @mentoriaconcursos"
                value={urlOrHandle}
                onChange={(e) => setUrlOrHandle(e.target.value)}
                className="flex-1 bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs focus:ring-2 focus:ring-slate-900 focus:outline-none"
              />
              <button
                type="submit"
                disabled={!urlOrHandle.trim()}
                className="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold disabled:opacity-50 px-4 py-2 rounded-lg flex items-center gap-1.5 transition-all shadow-xs"
              >
                <Sparkles className="w-3.5 h-3.5 text-slate-950 fill-current" />
                Capturar
              </button>
            </div>
            <p className="text-[11px] text-slate-500">
              O lead será adicionado <strong>instantaneamente</strong> na coluna <em>"Não Contatado"</em> do seu Kanban!
            </p>
          </form>

          {/* Método 2: Botão Favorito no Navegador (Bookmarklet) */}
          <div className="space-y-3 bg-amber-50/60 p-4 rounded-xl border border-amber-200/80">
            <div className="flex items-center justify-between">
              <label className="font-semibold text-slate-900 flex items-center gap-1.5 text-xs">
                <Bookmark className="w-4 h-4 text-amber-600" />
                Opção 2: Botão Favorito no Navegador
              </label>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-200 text-amber-900">
                1-Clique
              </span>
            </div>

            <p className="text-[11px] text-slate-600 leading-relaxed">
              Arraste o botão abaixo para a sua <strong>Barra de Favoritos do navegador</strong>. Quando você estiver navegando em um perfil no Instagram, basta clicar no favorito!
            </p>

            <div className="flex flex-col sm:flex-row items-center gap-2 pt-1">
              <a
                href={bookmarkletCode}
                onClick={(e) => e.preventDefault()}
                className="w-full sm:w-auto px-4 py-2 bg-gradient-to-r from-amber-500 to-amber-600 text-white font-bold rounded-lg shadow-md hover:brightness-110 text-center cursor-grab active:cursor-grabbing text-xs flex items-center justify-center gap-2"
                title="Arraste este botão para a sua Barra de Favoritos do Navegador"
              >
                <Zap className="w-3.5 h-3.5 fill-current" />
                ➕ Salvar na Trajetória
              </a>

              <button
                type="button"
                onClick={copyBookmarklet}
                className="w-full sm:w-auto px-3 py-2 bg-white border border-amber-300 hover:bg-amber-100/50 text-amber-900 font-medium rounded-lg flex items-center justify-center gap-1.5 transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'Código Copiado!' : 'Copiar Código JS'}
              </button>
            </div>
            
            <div className="bg-white/80 p-2.5 rounded-lg border border-amber-200 text-[11px] text-slate-500 space-y-1">
              <p>💡 <strong>Como instalar no Chrome/Edge:</strong></p>
              <ol className="list-decimal list-inside space-y-0.5">
                <li>Pressione <kbd className="px-1 py-0.5 bg-slate-200 rounded text-[10px]">Ctrl + Shift + B</kbd> para mostrar a barra de favoritos.</li>
                <li>Arraste o botão <strong>"➕ Salvar na Trajetória"</strong> para a barra.</li>
                <li>No Instagram, abra a página do perfil da mentoria e clique no favorito!</li>
              </ol>
            </div>
          </div>

        </div>

        <div className="p-4 border-t border-slate-200 bg-slate-50 flex justify-end flex-shrink-0">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 rounded-xl font-medium transition-colors"
          >
            Fechar
          </button>
        </div>

      </div>
    </div>
  );
};
