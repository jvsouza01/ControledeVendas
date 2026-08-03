import * as XLSX from 'xlsx';
import type { Lead, LeadPrioridade, LeadStatus } from '../types/lead';

/**
 * Exporta a lista de leads atual em arquivo .XLSX (Excel)
 */
export function exportLeadsToExcel(leads: Lead[]) {
  const dataToExport = leads.map((lead) => ({
    'Nome (Mentor/Professor)': lead.nome,
    '@ Instagram': lead.instagram,
    Nicho: lead.nicho,
    'Como encontrei': lead.comoEncontrei,
    'Status do lead': mapStatusToLabel(lead.status),
    'Data 1º contato (DM texto)': lead.data1Contato,
    'Respondeu?': lead.respondeu ? 'Sim' : 'Não',
    'Data 2º contato (DM c/ link)': lead.data2Contato,
    'Data follow-up agendado': lead.dataFollowUp,
    'Nº tentativas follow-up': lead.tentativasFollowUp,
    'Data reunião marcada': lead.dataReuniao,
    'Reunião realizada?': lead.reuniaoRealizada ? 'Sim' : 'Não',
    Prioridade: lead.prioridade ? lead.prioridade.toUpperCase() : 'MÉDIA',
    'Próximo passo': lead.proximoPasso,
    Observações: lead.observacoes,
    'Valor Proposta (R$)': lead.valorProposta || 0,
  }));

  const worksheet = XLSX.utils.json_to_sheet(dataToExport);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Prospecção e Vendas');

  const dateStr = new Date().toISOString().slice(0, 10);
  XLSX.writeFile(workbook, `controle_prospeccao_vendas_${dateStr}.xlsx`);
}

/**
 * Parseia arquivo Excel (.xlsx, .xls, .csv) enviado pelo usuário para formato Lead[]
 */
export async function parseExcelFile(file: File): Promise<Lead[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target?.result as ArrayBuffer);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const rawJson: any[] = XLSX.utils.sheet_to_json(worksheet, { defval: '' });

        const importedLeads: Lead[] = rawJson.map((row, index) => {
          const instagramRaw = String(
            row['@ Instagram'] || row['Instagram'] || row['@'] || row['Insta'] || ''
          ).trim().replace(/^@/, '');

          const nomeRaw = String(
            row['Nome (Mentor/professor)'] || row['Nome (Mentor/Professor)'] || row['Nome'] || instagramRaw || `Lead ${index + 1}`
          ).trim();

          const statusRaw = String(row['Status do lead'] || row['Status'] || '').toLowerCase();
          const status = parseStatus(statusRaw);

          const prioridadeRaw = String(row['Prioridade'] || '').toLowerCase();
          const prioridade = parsePrioridade(prioridadeRaw);

          const respondeuRaw = String(row['Respondeu?'] || row['Respondeu'] || '').toLowerCase();
          const respondeu = respondeuRaw === 'sim' || respondeuRaw === 's' || respondeuRaw === 'true';

          const reuniaoRealizadaRaw = String(row['Reunião realizada?'] || row['Reuniao realizada'] || '').toLowerCase();
          const reuniaoRealizada = reuniaoRealizadaRaw === 'sim' || reuniaoRealizadaRaw === 's' || reuniaoRealizadaRaw === 'true';

          return {
            id: `imported_${Date.now()}_${index}`,
            nome: nomeRaw,
            instagram: instagramRaw,
            nicho: String(row['Nicho'] || '').trim(),
            comoEncontrei: String(row['Como encontrei'] || row['Origem'] || 'Importado Excel').trim(),
            status,
            data1Contato: normalizeDateString(row['Data 1º contato (DM texto)'] || row['Data 1º contato'] || row['Data 1o contato']),
            respondeu,
            data2Contato: normalizeDateString(row['Data 2º contato (DM c/ link)'] || row['Data 2º contato']),
            dataFollowUp: normalizeDateString(row['Data follow-up agendado'] || row['Data follow-up'] || row['Follow up']),
            tentativasFollowUp: Number(row['Nº tentativas follow-up'] || row['Tentativas'] || 0),
            dataReuniao: normalizeDateString(row['Data reunião marcada'] || row['Data reunião'] || row['Reunião']),
            reuniaoRealizada,
            prioridade,
            proximoPasso: String(row['Próximo passo'] || '').trim(),
            observacoes: String(row['Observações'] || row['Observacao'] || '').trim(),
            valorProposta: Number(row['Valor Proposta (R$)'] || row['Valor'] || 0),
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          };
        });

        resolve(importedLeads.filter((l) => l.nome || l.instagram));
      } catch (err) {
        reject(err);
      }
    };

    reader.onerror = (error) => reject(error);
    reader.readAsArrayBuffer(file);
  });
}

function parseStatus(raw: string): LeadStatus {
  if (raw.includes('aguardando') || raw.includes('contatado')) return 'contatado_aguardando';
  if (raw.includes('conversa') || raw.includes('respondeu')) return 'em_conversa';
  if (raw.includes('marcada') || raw.includes('agendada')) return 'reuniao_agendada';
  if (raw.includes('realizada')) return 'reuniao_realizada';
  if (raw.includes('fechado') || raw.includes('venda')) return 'fechado';
  if (raw.includes('sem interesse') || raw.includes('arquivado') || raw.includes('perdido')) return 'arquivado';
  return 'nao_contatado';
}

function parsePrioridade(raw: string): LeadPrioridade {
  if (raw.includes('alt')) return 'alta';
  if (raw.includes('baix')) return 'baixa';
  return 'media';
}

function normalizeDateString(val: any): string {
  if (!val) return '';
  if (typeof val === 'number') {
    const date = new Date(Math.round((val - 25569) * 86400 * 1000));
    return date.toISOString().split('T')[0];
  }
  const str = String(val).trim();
  if (str.includes('/')) {
    const parts = str.split('/');
    if (parts.length === 3) {
      const day = parts[0].padStart(2, '0');
      const month = parts[1].padStart(2, '0');
      let year = parts[2];
      if (year.length === 2) year = '20' + year;
      return `${year}-${month}-${day}`;
    }
  }
  if (str.match(/^\d{4}-\d{2}-\d{2}$/)) {
    return str;
  }
  return '';
}

function mapStatusToLabel(status: LeadStatus): string {
  switch (status) {
    case 'nao_contatado': return 'Não contatado';
    case 'contatado_aguardando': return 'Contatado - aguardando resposta';
    case 'em_conversa': return 'Em conversa / Respondeu';
    case 'reuniao_agendada': return 'Reunião marcada';
    case 'reuniao_realizada': return 'Reunião realizada';
    case 'fechado': return 'Cliente Fechado';
    case 'arquivado': return 'Arquivado / Sem interesse';
  }
}
