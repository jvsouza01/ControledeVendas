import React, { useState } from 'react';
import { useLeads } from '../context/LeadContext';
import { parseExcelFile } from '../utils/excelUtils';
import { X, FileSpreadsheet, Upload, AlertCircle, CheckCircle2 } from 'lucide-react';
import type { Lead } from '../types/lead';

export const ExcelImportModal: React.FC = () => {
  const { isImportModalOpen, setIsImportModalOpen, importLeads } = useLeads();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [parsedLeads, setParsedLeads] = useState<Lead[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [replaceMode, setReplaceMode] = useState(false);

  if (!isImportModalOpen) return null;

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;

    setFile(selected);
    setLoading(true);
    setError(null);

    try {
      const leads = await parseExcelFile(selected);
      if (leads.length === 0) {
        setError('Nenhum dado válido foi encontrado na planilha.');
      } else {
        setParsedLeads(leads);
      }
    } catch (err: any) {
      setError('Erro ao ler a planilha Excel/CSV: ' + (err.message || 'Formato inválido'));
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmImport = () => {
    if (parsedLeads.length > 0) {
      importLeads(parsedLeads, replaceMode);
      setIsImportModalOpen(false);
      setFile(null);
      setParsedLeads([]);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white border border-slate-200 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
        
        <div className="px-6 py-4 border-b border-slate-200/80 flex items-center justify-between bg-slate-50/50">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-slate-100 text-slate-700 rounded-lg border border-slate-200">
              <FileSpreadsheet className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-semibold text-sm text-slate-900">Importar Planilha Excel</h3>
              <p className="text-[11px] text-slate-500">Carregue arquivos .xlsx, .xls ou .csv</p>
            </div>
          </div>
          <button
            onClick={() => setIsImportModalOpen(false)}
            className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-6 space-y-4 text-xs text-slate-700">
          <div className="border-2 border-dashed border-slate-200 hover:border-slate-400 rounded-xl p-6 text-center bg-slate-50/50 transition-colors cursor-pointer relative group">
            <input
              type="file"
              accept=".xlsx, .xls, .csv"
              onChange={handleFileChange}
              className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
            />
            <Upload className="w-6 h-6 text-slate-400 mx-auto mb-2" />
            <p className="font-semibold text-slate-800 text-xs">
              {file ? file.name : 'Clique para selecionar a planilha'}
            </p>
            <p className="text-[11px] text-slate-400 mt-1">Suporta .xlsx e .csv</p>
          </div>

          {loading && (
            <div className="text-center py-2 text-slate-600 font-medium animate-pulse">
              Processando planilha...
            </div>
          )}

          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {parsedLeads.length > 0 && (
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2.5">
              <div className="flex items-center gap-2 text-slate-900 font-semibold text-xs">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>{parsedLeads.length} leads prontos para importar!</span>
              </div>
              <p className="text-[11px] text-slate-500">
                Reconhecemos automaticamente as colunas de Nome, Instagram (@), Nicho, Status e Datas.
              </p>

              <div className="pt-2 border-t border-slate-200 space-y-1.5">
                <label className="flex items-center gap-2 cursor-pointer text-slate-700 font-medium">
                  <input
                    type="radio"
                    name="importMode"
                    checked={!replaceMode}
                    onChange={() => setReplaceMode(false)}
                    className="text-slate-900 focus:ring-slate-400"
                  />
                  Adicionar aos leads existentes
                </label>
                <label className="flex items-center gap-2 cursor-pointer text-slate-700 font-medium">
                  <input
                    type="radio"
                    name="importMode"
                    checked={replaceMode}
                    onChange={() => setReplaceMode(true)}
                    className="text-slate-900 focus:ring-slate-400"
                  />
                  Substituir todos os leads atuais
                </label>
              </div>
            </div>
          )}

          <div className="pt-3 border-t border-slate-100 flex justify-end gap-2">
            <button
              onClick={() => setIsImportModalOpen(false)}
              className="px-4 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-lg transition-colors text-xs"
            >
              Cancelar
            </button>
            <button
              disabled={parsedLeads.length === 0}
              onClick={handleConfirmImport}
              className={`px-5 py-1.5 font-medium rounded-lg text-xs transition-all ${
                parsedLeads.length > 0
                  ? 'bg-slate-900 hover:bg-slate-800 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-400 cursor-not-allowed'
              }`}
            >
              Confirmar Importação ({parsedLeads.length})
            </button>
          </div>

        </div>
      </div>
    </div>
  );
};
