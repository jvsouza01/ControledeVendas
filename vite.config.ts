import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { execFile } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Plugin Vite customizado que expõe a rota GET /api/minerar executando busca_ao_vivo.py
function liveMinerPlugin(): Plugin {
  return {
    name: 'live-miner-api',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // Intercepta requisições para /api/minerar
        if (!req.url || !req.url.startsWith('/api/minerar')) {
          return next();
        }

        try {
          const parsedUrl = new URL(req.url, 'http://localhost');
          const q = parsedUrl.searchParams.get('q') || parsedUrl.searchParams.get('query') || '';
          const nicho = parsedUrl.searchParams.get('nicho') || 'Carreiras Policiais';

          const scriptPath = path.resolve(__dirname, 'minerador', 'busca_ao_vivo.py');
          const args = ['--query', q, '--nicho', nicho];

          execFile(
            'python',
            [scriptPath, ...args],
            { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 },
            (error, stdout, stderr) => {
              res.setHeader('Content-Type', 'application/json; charset=utf-8');

              if (error) {
                console.error('[LiveMinerAPI] Erro ao executar busca_ao_vivo.py:', error, stderr);
                res.statusCode = 500;
                res.end(JSON.stringify({ error: error.message, leads: [] }));
                return;
              }

              try {
                // Valida o JSON antes de devolver
                const jsonOutput = JSON.parse(stdout.trim());
                res.statusCode = 200;
                res.end(JSON.stringify(jsonOutput));
              } catch (parseErr) {
                console.error('[LiveMinerAPI] Formato inesperado de JSON retornado:', parseErr, stdout);
                res.statusCode = 200;
                res.end(stdout.trim());
              }
            }
          );
        } catch (err: any) {
          res.statusCode = 500;
          res.setHeader('Content-Type', 'application/json; charset=utf-8');
          res.end(JSON.stringify({ error: err?.message || 'Erro desconhecido', leads: [] }));
        }
      });
    },
  };
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(), liveMinerPlugin()],
  base: './', // Permite rodar no GitHub Pages sem problema de caminhos
});
