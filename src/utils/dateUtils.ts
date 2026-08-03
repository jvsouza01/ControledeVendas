/**
 * Formata data no padrão brasileiro DD/MM/YYYY
 */
export function formatDateBR(dateStr?: string): string {
  if (!dateStr) return '-';
  const cleanStr = dateStr.split('T')[0];
  const parts = cleanStr.split('-');
  if (parts.length !== 3) return dateStr;
  const [year, month, day] = parts;
  return `${day.padStart(2, '0')}/${month.padStart(2, '0')}/${year}`;
}

/**
 * Retorna a data de hoje no formato YYYY-MM-DD
 */
export function getTodayString(): string {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Calcula a diferença de dias entre duas datas (YYYY-MM-DD).
 * Se data2 não for informada, usa Hoje.
 */
export function getDaysDifference(dateStr?: string, targetDateStr?: string): number | null {
  if (!dateStr) return null;

  const date1Parts = dateStr.split('-');
  if (date1Parts.length !== 3) return null;
  const date1 = new Date(Number(date1Parts[0]), Number(date1Parts[1]) - 1, Number(date1Parts[2]));

  let date2: Date;
  if (targetDateStr) {
    const date2Parts = targetDateStr.split('-');
    date2 = new Date(Number(date2Parts[0]), Number(date2Parts[1]) - 1, Number(date2Parts[2]));
  } else {
    const today = new Date();
    date2 = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  }

  const diffTime = date2.getTime() - date1.getTime();
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

/**
 * Retorna o status do follow-up:
 * 'hoje': agendado para a data atual
 * 'atrasado': a data de follow-up passou e ainda não foi realizado
 * 'futuro': agendado para data futura
 * 'sem_followup': sem data agendada
 */
export function getFollowUpStatus(dataFollowUp?: string, statusLead?: string): 'hoje' | 'atrasado' | 'futuro' | 'sem_followup' {
  if (!dataFollowUp) return 'sem_followup';
  if (statusLead === 'fechado' || statusLead === 'arquivado') return 'sem_followup';

  const todayStr = getTodayString();
  const daysDiff = getDaysDifference(dataFollowUp, todayStr);

  if (daysDiff === null) return 'sem_followup';

  if (dataFollowUp === todayStr) {
    return 'hoje';
  } else if (dataFollowUp < todayStr) {
    return 'atrasado';
  } else {
    return 'futuro';
  }
}

/**
 * Retorna o texto formatado "Há X dias" ou "Hoje" ou "Amanhã"
 */
export function formatDaysAgoText(dateStr?: string): { text: string; days: number | null } {
  if (!dateStr) return { text: 'Nunca contatado', days: null };

  const days = getDaysDifference(dateStr);
  if (days === null) return { text: '-', days: null };

  if (days === 0) return { text: 'Hoje', days: 0 };
  if (days === 1) return { text: 'Há 1 dia', days: 1 };
  if (days > 1) return { text: `Há ${days} dias`, days };
  if (days === -1) return { text: 'Amanhã', days: -1 };
  return { text: `Em ${Math.abs(days)} dias`, days };
}
