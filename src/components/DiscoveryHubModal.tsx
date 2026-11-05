import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import {
  X,
  ExternalLink,
  Target,
  Sparkles,
  Copy,
  Check,
  Search,
  Loader2,
  Plus,
  CheckCircle2,
  Compass,
} from 'lucide-react';
import { InstagramIcon } from './InstagramIcon';
import { useLeads } from '../context/LeadContext';

interface DiscoveryHubModalProps {
  isOpen: boolean;
  onClose: () => void;
}

type NicheArea =
  | 'Todas as Áreas'
  | 'Carreiras Policiais'
  | 'Tribunais / Jurídica'
  | 'Fiscal / Controle'
  | 'Administrativo / INSS'
  | 'Bancos / Caixa / BB'
  | 'Saúde / Enfermagem'
  | 'Educação / Pedagogia'
  | 'Militar'
  | 'Redação & Isoladas';

interface DorkItem {
  id: string;
  canal: 'checkout' | 'linktree' | 'meta_ads' | 'instagram' | 'telegram_youtube';
  title: string;
  description: string;
  query: string;
  url: string;
  badge: string;
}

export const DiscoveryHubModal: React.FC<DiscoveryHubModalProps> = ({ isOpen, onClose }) => {
  const { addLead } = useLeads();
  const [selectedArea, setSelectedArea] = useState<NicheArea>('Todas as Áreas');
  const [copiedQueryId, setCopiedQueryId] = useState<string | null>(null);

  // Estados da Mineração Ao Vivo
  const [termoBusca, setTermoBusca] = useState('mentoria pm');
  const [nichoBusca, setNichoBusca] = useState('Carreiras Policiais');
  const [isMining, setIsMining] = useState(false);
  const [minedResults, setMinedResults] = useState<any[]>([]);
  const [miningStatusMsg, setMiningStatusMsg] = useState<string | null>(null);
  const [importedSet, setImportedSet] = useState<Set<string>>(new Set());

  if (!isOpen) return null;

  const handleCopyQuery = (id: string, query: string, e: React.MouseEvent) => {
    e.stopPropagation();
    navigator.clipboard.writeText(query);
    setCopiedQueryId(id);
    setTimeout(() => setCopiedQueryId(null), 2000);
  };

  // Mineração ao vivo via backend
  const handleBuscarAoVivo = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const termo = termoBusca.trim();
    if (!termo) return;

    setIsMining(true);
    setMiningStatusMsg('Buscando perfis reais de mentores na web...');
    try {
      const res = await fetch(
        `/api/minerar?q=${encodeURIComponent(termo)}&nicho=${encodeURIComponent(nichoBusca)}`
      );
      if (!res.ok) {
        throw new Error(`Serviço de mineração respondeu com código ${res.status}`);
      }
      const data = await res.json();
      const list = Array.isArray(data) ? data : (data.leads || []);
      setMinedResults(list);
      if (list.length === 0) {
        setMiningStatusMsg('Nenhum mentor encontrado para essa busca. Tente outro termo (ex: "mentoria policia civil", "cronograma concurso").');
      } else {
        setMiningStatusMsg(`${list.length} perfis reais encontrados!`);
      }
    } catch (err: any) {
      console.error('Erro na mineração ao vivo:', err);
      setMiningStatusMsg(`Falha na busca ao vivo: ${err.message || 'API offline'}. Você pode usar as Dorks Prontas abaixo enquanto o minerador sincroniza.`);
    } finally {
      setIsMining(false);
    }
  };

  const handleImportLead = (lead: any) => {
    const handle = (lead.instagram || '').replace(/[@\s]/g, '').trim();
    if (!handle) return;

    addLead({
      nome: lead.nome || handle,
      instagram: handle,
      nicho: lead.nicho || nichoBusca || 'Mentoria de Concursos',
      comoEncontrei: lead.comoEncontrei || 'Mineração Web Ao Vivo',
      status: 'nao_contatado',
      data1Contato: '',
      respondeu: false,
      data2Contato: '',
      dataFollowUp: '',
      tentativasFollowUp: 0,
      dataReuniao: '',
      reuniaoRealizada: false,
      prioridade: lead.prioridade || 'alta',
      proximoPasso: 'Enviar Direct de apresentação da Trajetória (Playbook)',
      observacoes: lead.observacoes || `Lead minerado ao vivo via Web Search (${termoBusca}).`,
      valorProposta: 0,
    });

    setImportedSet((prev) => new Set([...prev, handle.toLowerCase()]));
  };

  const handleImportAll = () => {
    minedResults.forEach((lead) => {
      const handle = (lead.instagram || '').replace(/[@\s]/g, '').trim().toLowerCase();
      if (handle && !importedSet.has(handle)) {
        handleImportLead(lead);
      }
    });
  };

  // Gerador dinâmico de Dorks baseado na área selecionada
  const getNicheKeywords = (area: NicheArea) => {
    switch (area) {
      case 'Carreiras Policiais':
        return '(policial OR "policia civil" OR "policia militar" OR "policia penal" OR GCM OR PMESP OR PMMG OR PCSP OR PCPR)';
      case 'Tribunais / Jurídica':
        return '(tribunal OR "TJSP" OR "TRT" OR "TRE" OR "TRF" OR juiz OR defensoria OR delegado OR escrevente)';
      case 'Fiscal / Controle':
        return '("auditor fiscal" OR SEFAZ OR "receita federal" OR ISS OR "tribunal de contas" OR TCE OR TCU)';
      case 'Administrativo / INSS':
        return '("INSS" OR "carreiras administrativas" OR "tecnico do seguro social" OR "CNU")';
      case 'Bancos / Caixa / BB':
        return '("caixa economica" OR "banco do brasil" OR "carreiras bancarias" OR BNB OR escriturario)';
      case 'Saúde / Enfermagem':
        return '(enfermagem OR "concurso saude" OR EBSERH OR "residencia enfermagem")';
      case 'Educação / Pedagogia':
        return '(pedagogia OR professor OR "concurso educacao" OR magistério OR "BNCC")';
      case 'Militar':
        return '(ESA OR EsPCEx OR "carreira militar" OR EEAR OR sargento)';
      case 'Redação & Isoladas':
        return '("redacao para concurso" OR discursiva OR "portugues para concurso" OR RLM)';
      default:
        return 'concurso';
    }
  };

  const currentNicheTerm = getNicheKeywords(selectedArea);

  // URLs codificadas para busca direta
  const googleSearchUrl = (query: string) => `https://www.google.com/search?q=${encodeURIComponent(query)}`;
  
  // Meta Ads Library com filtro Brasil, Todos os Anúncios e busca pelo nicho
  const getMetaAdsUrl = () => {
    const metaTerm = selectedArea === 'Todas as Áreas' ? 'mentoria concurso' : `mentoria ${selectedArea.toLowerCase()}`;
    return `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q=${encodeURIComponent(metaTerm)}&search_type=keyword_unordered&media_type=all`;
  };

  const DORKS: DorkItem[] = [
    {
      id: 'kiwify_hotmart',
      canal: 'checkout',
      title: '🔥 Checkouts Kiwify & Hotmart',
      description: 'Encontra páginas de checkout e vendas de mentoria e cronogramas que expõem WhatsApp ou Instagram do mentor.',
      query: `site:kiwify.com.br OR site:hotmart.com "mentoria" ${currentNicheTerm} ("instagram.com" OR "wa.me")`,
      url: googleSearchUrl(`site:kiwify.com.br OR site:hotmart.com "mentoria" ${currentNicheTerm} ("instagram.com" OR "wa.me")`),
      badge: 'Alta Conversão',
    },
    {
      id: 'linktree_beacons',
      canal: 'linktree',
      title: '🔗 Bios Linktree & Beacons.ai',
      description: 'Mapeia árvores de links de mentores independentes com botões de mentoria, cronograma, WhatsApp e Direct.',
      query: `site:linktr.ee OR site:beacons.ai "mentoria" ${currentNicheTerm} "instagram.com"`,
      url: googleSearchUrl(`site:linktr.ee OR site:beacons.ai "mentoria" ${currentNicheTerm} "instagram.com"`),
      badge: 'Contato Direto',
    },
    {
      id: 'meta_ads',
      canal: 'meta_ads',
      title: '💰 Meta Ads Library (Anúncios Ativos)',
      description: 'Abre a Biblioteca de Anúncios do Instagram/Facebook buscando mentores que estão investindo em tráfego pago hoje.',
      query: `Anúncios ativos no Brasil: "mentoria ${selectedArea}"`,
      url: getMetaAdsUrl(),
      badge: 'Investindo em Anúncios',
    },
    {
      id: 'instagram_filtrado',
      canal: 'instagram',
      title: '📸 Instagram Filtrado (Anti-Studygram)',
      description: 'Busca biografias de mentores de concursos eliminando grandes cursinhos e studygrams que não vendem nada.',
      query: `site:instagram.com ("mentoria" OR "cronograma de estudos") ${currentNicheTerm} -estrategia -gran -alfacon -direcao -qconcursos -ceisc`,
      url: googleSearchUrl(`site:instagram.com ("mentoria" OR "cronograma de estudos") ${currentNicheTerm} -estrategia -gran -alfacon -direcao -qconcursos -ceisc`),
      badge: 'Anti-Gigantes',
    },
    {
      id: 'telegram_youtube',
      canal: 'telegram_youtube',
      title: '✈️ YouTube & Telegram de Mentores',
      description: 'Acha canais do YouTube e grupos do Telegram de pequenos mentores que deixam o link de mentoria na descrição.',
      query: `site:youtube.com "mentoria" ${currentNicheTerm} ("instagram.com" OR "wa.me" OR "kiwify")`,
      url: googleSearchUrl(`site:youtube.com "mentoria" ${currentNicheTerm} ("instagram.com" OR "wa.me" OR "kiwify")`),
      badge: 'Autoridade Local',
    },
  ];

  const AREAS: NicheArea[] = [
    'Todas as Áreas',
    'Carreiras Policiais',
    'Tribunais / Jurídica',
    'Fiscal / Controle',
    'Administrativo / INSS',
    'Bancos / Caixa / BB',
    'Saúde / Enfermagem',
    'Educação / Pedagogia',
    'Militar',
    'Redação & Isoladas',
  ];

  return createPortal(
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-3 sm:p-5 animate-fadeIn">
      <div className="bg-white rounded-2xl border border-slate-200 w-full max-w-4xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Cabeçalho */}
        <div className="px-6 py-4 border-b border-slate-200 bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950 text-white flex items-center justify-between flex-shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-400 text-slate-950 flex items-center justify-center font-bold shadow-md">
              <Target className="w-5 h-5 text-slate-950" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold tracking-tight text-white">
                  Radar de Leads & Mineração Web
                </h2>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-400/20 text-emerald-300 border border-emerald-400/30">
                  Ao Vivo & Dorks
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Minere perfis reais na web ou use buscas avançadas para encontrar mentores na Kiwify, Hotmart e Instagram
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Corpo do Modal com Scroll Suave */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          
          {/* SEÇÃO 1: MINERADOR AO VIVO */}
          <div className="bg-gradient-to-br from-slate-900 via-slate-850 to-indigo-950 p-5 rounded-2xl text-white shadow-md border border-slate-700/60 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="p-1.5 bg-amber-400 text-slate-950 rounded-lg">
                  <Compass className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-xs font-bold uppercase tracking-wider text-amber-300">
                    🔍 Minerar Novos Leads na Web Agora
                  </h3>
                  <p className="text-[11px] text-slate-300">
                    Busca automatizada em páginas de vendas, Linktrees e Instagram
                  </p>
                </div>
              </div>
              <span className="text-[10px] px-2 py-0.5 bg-indigo-500/30 text-indigo-200 border border-indigo-400/30 rounded-full font-medium">
                Live Engine
              </span>
            </div>

            <form onSubmit={handleBuscarAoVivo} className="space-y-3">
              <div className="grid grid-cols-1 sm:grid-cols-12 gap-2">
                <div className="sm:col-span-7">
                  <label className="text-[10px] font-semibold text-slate-300 block mb-1">
                    Termo ou Palavra-chave:
                  </label>
                  <div className="relative">
                    <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                    <input
                      type="text"
                      value={termoBusca}
                      onChange={(e) => setTermoBusca(e.target.value)}
                      placeholder='Ex: "mentoria pm", "mentoria tribunais", "cronograma concurso"'
                      className="w-full bg-slate-800/90 border border-slate-700 focus:border-amber-400 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-400 outline-none transition-all"
                    />
                  </div>
                </div>

                <div className="sm:col-span-3">
                  <label className="text-[10px] font-semibold text-slate-300 block mb-1">
                    Nicho / Categoria:
                  </label>
                  <select
                    value={nichoBusca}
                    onChange={(e) => setNichoBusca(e.target.value)}
                    className="w-full bg-slate-800/90 border border-slate-700 focus:border-amber-400 rounded-xl px-3 py-2 text-xs text-white outline-none transition-all cursor-pointer"
                  >
                    <option value="Carreiras Policiais">Carreiras Policiais</option>
                    <option value="Tribunais / Jurídica">Tribunais / Jurídica</option>
                    <option value="Fiscal / Controle">Fiscal / Controle</option>
                    <option value="Administrativo / INSS">Administrativo / INSS</option>
                    <option value="Bancos / Caixa / BB">Bancos / Caixa / BB</option>
                    <option value="Saúde / Enfermagem">Saúde / Enfermagem</option>
                    <option value="Educação / Pedagogia">Educação / Pedagogia</option>
                    <option value="Militar">Militar</option>
                    <option value="Mentoria de Concursos">Concursos Gerais</option>
                  </select>
                </div>

                <div className="sm:col-span-2 flex items-end">
                  <button
                    type="submit"
                    disabled={isMining || !termoBusca.trim()}
                    className="w-full bg-amber-400 hover:bg-amber-300 disabled:opacity-50 text-slate-950 font-bold px-3 py-2 rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all shadow-md active:scale-95 cursor-pointer"
                  >
                    {isMining ? (
                      <>
                        <Loader2 className="w-3.5 h-3.5 animate-spin text-slate-950" />
                        <span>Buscando...</span>
                      </>
                    ) : (
                      <>
                        <Search className="w-3.5 h-3.5 text-slate-950" />
                        <span>Buscar</span>
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Sugestões rápidas de busca */}
              <div className="flex flex-wrap items-center gap-1.5 pt-1">
                <span className="text-[10px] text-slate-400">Sugestões rápidas:</span>
                {[
                  { label: '👮 PM & Policiais', q: 'mentoria pm', n: 'Carreiras Policiais' },
                  { label: '⚖️ Tribunais & TJ', q: 'mentoria tribunais', n: 'Tribunais / Jurídica' },
                  { label: '📅 Cronogramas', q: 'cronograma concurso', n: 'Carreiras Policiais' },
                  { label: '🕵️ Polícia Civil', q: 'mentoria policia civil', n: 'Carreiras Policiais' },
                  { label: '💼 Fiscal & SEFAZ', q: 'mentoria fiscal auditor', n: 'Fiscal / Controle' },
                ].map((s) => (
                  <button
                    type="button"
                    key={s.label}
                    onClick={() => {
                      setTermoBusca(s.q);
                      setNichoBusca(s.n);
                    }}
                    className="px-2 py-0.5 rounded-md text-[10px] bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
                  >
                    {s.label}
                  </button>
                ))}
              </div>
            </form>

            {/* Mensagem de status */}
            {miningStatusMsg && (
              <div className="text-[11px] px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/80 text-slate-300 flex items-center gap-2">
                <Sparkles className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />
                <span>{miningStatusMsg}</span>
              </div>
            )}

            {/* Resultados Minerados com Botões de Importação */}
            {minedResults.length > 0 && (
              <div className="space-y-2.5 bg-slate-950/60 p-3.5 rounded-xl border border-slate-800">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-emerald-400">
                      🎯 {minedResults.length} Perfis Encontrados
                    </span>
                    <span className="text-[11px] text-slate-400">
                      (clique para importar diretamente para a coluna "Não Contatado")
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={handleImportAll}
                    className="px-3 py-1 bg-emerald-500 hover:bg-emerald-400 active:scale-95 text-slate-950 text-xs font-bold rounded-lg flex items-center gap-1.5 transition-all shadow-xs"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>➕ Importar Todos ({minedResults.length})</span>
                  </button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 max-h-60 overflow-y-auto pr-1">
                  {minedResults.map((lead, idx) => {
                    const handle = (lead.instagram || '').replace(/[@\s]/g, '').trim();
                    const isImported = importedSet.has(handle.toLowerCase());

                    return (
                      <div
                        key={handle || idx}
                        className="bg-slate-900 p-3 rounded-lg border border-slate-800 flex flex-col justify-between gap-2 hover:border-slate-700 transition-all"
                      >
                        <div>
                          <div className="flex items-start justify-between gap-2">
                            <span className="font-semibold text-xs text-white truncate">
                              {lead.nome || handle}
                            </span>
                            <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-300 border border-slate-700 truncate max-w-[120px]">
                              {lead.nicho || nichoBusca}
                            </span>
                          </div>

                          {handle && (
                            <a
                              href={`https://instagram.com/${handle}`}
                              target="_blank"
                              rel="noreferrer"
                              className="inline-flex items-center gap-1 text-[11px] font-medium text-amber-300 hover:text-amber-200 mt-0.5"
                            >
                              <InstagramIcon className="w-3 h-3" />
                              @{handle}
                              <ExternalLink className="w-2.5 h-2.5" />
                            </a>
                          )}

                          {lead.observacoes && (
                            <p className="text-[11px] text-slate-400 line-clamp-2 mt-1">
                              {lead.observacoes}
                            </p>
                          )}
                        </div>

                        <button
                          type="button"
                          disabled={isImported}
                          onClick={() => handleImportLead(lead)}
                          className={`w-full py-1.5 px-2 rounded-md text-xs font-semibold flex items-center justify-center gap-1.5 transition-all ${
                            isImported
                              ? 'bg-emerald-950 text-emerald-300 border border-emerald-800 cursor-default'
                              : 'bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white shadow-2xs'
                          }`}
                        >
                          {isImported ? (
                            <>
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                              <span>✓ Importado para Não Contatado</span>
                            </>
                          ) : (
                            <>
                              <Plus className="w-3.5 h-3.5" />
                              <span>➕ Importar para Não Contatado</span>
                            </>
                          )}
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          {/* SEÇÃO 2: DICAS PRÁTICAS */}
          <div className="bg-amber-50/70 border border-amber-200/90 rounded-xl p-3.5 flex items-start gap-3">
            <Sparkles className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div className="text-xs text-amber-900 space-y-1">
              <span className="font-bold text-amber-950">Como validar uma "Fruta Baixa" em 5 segundos no Instagram:</span>
              <ul className="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-1 text-[11px] text-amber-800">
                <li className="bg-white/80 p-2 rounded-lg border border-amber-200/60">
                  <strong>👤 1.5k a 30k seguidores:</strong> O próprio mentor cuida e responde os Directs pessoalmente.
                </li>
                <li className="bg-white/80 p-2 rounded-lg border border-amber-200/60">
                  <strong>🛒 Vende na Kiwify/Hotmart:</strong> Entrega cronogramas em planilha/PDF ou mentoria sem plataforma própria.
                </li>
                <li className="bg-white/80 p-2 rounded-lg border border-amber-200/60">
                  <strong>🎯 Dor imediata:</strong> Sofre para cobrar, gerenciar alunos manualmente e enviar simulados em PDF.
                </li>
              </ul>
            </div>
          </div>

          {/* SEÇÃO 3: FILTRO DE ÁREA PARA AS DORKS */}
          <div>
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 block">
              Explorar Dorks Prontas por Área de Concurso
            </label>
            <div className="flex flex-wrap gap-1.5">
              {AREAS.map((area) => (
                <button
                  key={area}
                  onClick={() => setSelectedArea(area)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    selectedArea === area
                      ? 'bg-slate-900 text-white shadow-xs font-semibold'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200'
                  }`}
                >
                  {area}
                </button>
              ))}
            </div>
          </div>

          {/* SEÇÃO 4: LISTA DE DORKS */}
          <div className="space-y-3">
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
              Canais de Descoberta Calibrados (Clique para abrir a busca pronta no Google)
            </label>

            <div className="grid grid-cols-1 gap-3">
              {DORKS.map((dork) => (
                <div
                  key={dork.id}
                  className="bg-slate-50 hover:bg-white border border-slate-200 hover:border-slate-300 rounded-xl p-4 transition-all group flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-2xs hover:shadow-xs"
                >
                  <div className="space-y-1.5 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-xs text-slate-900 group-hover:text-indigo-600 transition-colors">
                        {dork.title}
                      </span>
                      <span className="px-1.5 py-0.2 rounded text-[10px] font-medium bg-indigo-50 text-indigo-700 border border-indigo-200">
                        {dork.badge}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-500">
                      {dork.description}
                    </p>
                    <div className="font-mono text-[10px] text-slate-600 bg-white px-2.5 py-1 rounded border border-slate-200/80 truncate max-w-xl">
                      {dork.query}
                    </div>
                  </div>

                  <div className="flex items-center gap-2 flex-shrink-0 pt-2 sm:pt-0">
                    <button
                      onClick={(e) => handleCopyQuery(dork.id, dork.query, e)}
                      className="px-2.5 py-1.5 bg-white hover:bg-slate-100 text-slate-700 text-xs font-medium rounded-lg border border-slate-200 flex items-center gap-1 transition-colors"
                      title="Copiar comando de busca"
                    >
                      {copiedQueryId === dork.id ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-emerald-600" />
                          <span className="text-emerald-700">Copiado</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5 text-slate-400" />
                          <span>Copiar</span>
                        </>
                      )}
                    </button>

                    <a
                      href={dork.url}
                      target="_blank"
                      rel="noreferrer"
                      className="px-3 py-1.5 bg-slate-900 hover:bg-indigo-600 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-all shadow-xs"
                    >
                      <span>Abrir Busca</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Rodapé */}
        <div className="p-4 border-t border-slate-200 bg-slate-50 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-600 flex-shrink-0">
          <div className="flex items-center gap-2">
            <InstagramIcon className="w-4 h-4 text-slate-400" />
            <span>Encontrou um mentor? Use o botão <strong>"+ Capturar"</strong> no cabeçalho ou importe os resultados acima!</span>
          </div>

          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-white hover:bg-slate-100 text-slate-800 text-xs font-medium rounded-lg border border-slate-300 transition-colors"
          >
            Fechar Radar
          </button>
        </div>

      </div>
    </div>,
    document.body
  );
};
