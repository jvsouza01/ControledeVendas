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
 * Adiciona X dias a uma data base (ou Hoje se omitido) e retorna no formato YYYY-MM-DD
 */
export function addDaysToDate(days: number, baseDateStr?: string): string {
  let date: Date;
  if (baseDateStr) {
    const parts = baseDateStr.split('-');
    if (parts.length === 3) {
      date = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
    } else {
      date = new Date();
    }
  } else {
    date = new Date();
  }

  date.setDate(date.getDate() + days);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
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
export function getFollowUpStatus(
  dataFollowUp?: string,
  statusLead?: string,
  data1Contato?: string
): 'hoje' | 'atrasado' | 'futuro' | 'sem_followup' {
  if (statusLead === 'nao_contatado' || statusLead === 'fechado' || statusLead === 'arquivado') {
    return 'sem_followup';
  }

  const todayStr = getTodayString();

  if (dataFollowUp) {
    if (dataFollowUp === todayStr) return 'hoje';
    if (dataFollowUp < todayStr) return 'atrasado';
    return 'futuro';
  }

  if (
    (statusLead === 'contatado_aguardando' || statusLead === 'em_conversa') &&
    data1Contato
  ) {
    const daysSinceContact = getDaysDifference(data1Contato);
    if (daysSinceContact !== null && daysSinceContact >= 3) return 'atrasado';
    if (daysSinceContact !== null && daysSinceContact > 0) return 'futuro';
  }

  return 'sem_followup';
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
