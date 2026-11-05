export interface MicroMentorInfo {
  text: string;
  isSmall: boolean;
}

export function getMicroMentorBadge(lead: {
  id?: string;
  observacoes?: string;
  comoEncontrei?: string;
}): MicroMentorInfo | null {
  const combined = `${lead.observacoes || ''} ${lead.comoEncontrei || ''}`;

  // 1. Regex para extrair contagem de seguidores explícita
  // Exemplos: "👥 ~2.300 seguidores", "(2.3k seg)", "3,064 Followers", "~1.5k seg", "850 seguidores"
  const followerRegex = /(?:👥\s*)?(?:~\s*)?(\d+(?:[.,]\d+)?\s*(?:k|mil)?)\s*(?:seguidores|followers|seg\b)/i;
  const match = combined.match(followerRegex);

  if (match) {
    const rawVal = match[1].toLowerCase().replace(/\s+/g, '');
    let num = 0;
    if (rawVal.includes('k')) {
      num = parseFloat(rawVal.replace('k', '')) * 1000;
    } else if (rawVal.includes('mil')) {
      num = parseFloat(rawVal.replace('mil', '')) * 1000;
    } else {
      num = parseFloat(rawVal.replace(/\./g, '').replace(',', '.'));
    }

    const formattedText = rawVal.includes('k')
      ? rawVal
      : num >= 1000
      ? `${(num / 1000).toFixed(1).replace('.0', '')}k`
      : `${Math.round(num)}`;

    if (num <= 15000) {
      return { text: `🌱 Micro-Mentor (~${formattedText} seg)`, isSmall: true };
    } else {
      return { text: `👥 ~${formattedText} seg`, isSmall: false };
    }
  }

  // 2. Se tiver marcado Porte: Fruta Baixa explicitamente
  if (combined.includes('Porte: Fruta Baixa') || combined.includes('Fruta Baixa')) {
    return { text: '🌱 Micro-Mentor (<10k seg)', isSmall: true };
  }

  // 3. Se for lead minerado do lote de frutas baixas (fb_)
  if (lead.id?.startsWith('fb_')) {
    return { text: '🌱 Micro-Mentor (<15k seg)', isSmall: true };
  }

  return null;
}
