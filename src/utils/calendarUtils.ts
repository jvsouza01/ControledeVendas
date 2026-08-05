import type { Lead } from '../types/lead';

/**
 * Gera URL direta para criar um evento no Google Calendar para o Follow-up ou Reunião de um lead.
 */
export function getGoogleCalendarUrl(lead: Lead, type: 'followup' | 'reuniao' = 'followup'): string {
  const dateStr = type === 'reuniao' && lead.dataReuniao ? lead.dataReuniao : lead.dataFollowUp;
  if (!dateStr) return '';

  // dateStr está no formato YYYY-MM-DD
  const cleanDate = dateStr.replace(/-/g, '');
  
  // Evento das 09:00 às 09:30 BRT (12:00 às 12:30 UTC)
  const startIso = `${cleanDate}T120000Z`;
  const endIso = `${cleanDate}T123000Z`;

  const instaHandle = lead.instagram ? `@${lead.instagram.replace('@', '')}` : '';
  const title = type === 'reuniao'
    ? `Reunião Demo Trajetória: ${lead.nome || 'Mentoria'} (${instaHandle})`
    : `Follow-up Trajetória: ${lead.nome || 'Mentoria'} (${instaHandle})`;

  const detailsLines = [
    `🎯 Mentoria / Lead: ${lead.nome}`,
    lead.instagram ? `📸 Instagram: https://instagram.com/${lead.instagram.replace('@', '')}` : '',
    `📊 Nicho: ${lead.nicho || 'Mentoria de Concursos'}`,
    `📌 Status no CRM: ${lead.status.replace('_', ' ').toUpperCase()}`,
    lead.proximoPasso ? `🚀 Próximo Passo: ${lead.proximoPasso}` : '',
    lead.observacoes ? `📝 Observações: ${lead.observacoes}` : '',
    `\n---\nCadastrado via Plataforma Trajetória (Controle de Vendas)`,
  ].filter(Boolean);

  const details = detailsLines.join('\n');

  const params = new URLSearchParams({
    action: 'TEMPLATE',
    text: title,
    dates: `${startIso}/${endIso}`,
    details: details,
    location: lead.instagram ? `https://instagram.com/${lead.instagram.replace('@', '')}` : 'Google Meet / Instagram Direct',
  });

  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}
