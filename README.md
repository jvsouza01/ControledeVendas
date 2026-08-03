# 🚀 Sistema de Controle de Vendas e Prospecção de Clientes (Plataforma Trajetória)

Sistema web moderno, automatizado e responsivo desenvolvido em **React + TypeScript + Vite** para substituição de planilhas de prospecção e controle de vendas no Instagram para a **Plataforma Trajetória**.

---

## 📌 Sobre o Projeto

O **Sistema de Prospecção & Vendas Trajetória** foi criado com o objetivo de eliminar a necessidade de controle manual via planilhas de Excel. O sistema automatiza o acompanhamento de leads prospectados no Instagram, calculando o tempo em contato, notificando sobre follow-ups pendentes e organizando todo o funil comercial.

---

## 🔥 Principais Funcionalidades

1. **📊 Automação do Tempo em Contato ("Há X dias")**:
   - Calcula dinamicamente o tempo decorrido desde o 1º contato com cada prospect.
2. **⏰ Central de Follow-ups Urgentes**:
   - Alertas para contatos com follow-up agendado para **Hoje** ou com **Data Atrasada**.
   - Contador de tentativas de follow-up (`+1 Tentativa`).
3. **🎯 Links Diretos para o Instagram**:
   - Botão em cada lead para abrir o perfil `@usuario` diretamente no Instagram em uma nova aba.
4. **🗂️ Visões Flexíveis**:
   - **Kanban Board**: Funil de vendas visual (*Não Contatado*, *Aguardando Resposta*, *Em Conversa*, *Reunião Agendada*, *Reunião Realizada*, *Cliente Fechado*, *Arquivado*).
   - **Tabela Interativa**: Visão estilo planilha com ordenação, busca textual rápida e filtro por nicho e prioridade.
   - **Metrics Dashboard**: Indicadores de taxa de resposta, total de prospecções, reuniões e vendas.
5. **📥 Importação e Exportação Excel (.xlsx / .csv)**:
   - Importador automático de planilhas existentes em Excel com mapeamento de colunas.
   - Exportador para baixar a base atualizada em `.xlsx` a qualquer momento.

---

## 💻 Como Rodar o Projeto Localmente

```bash
# 1. Instalar as dependências
npm install

# 2. Iniciar o servidor de desenvolvimento
npm run dev
```

Acesse o sistema em: `http://localhost:5173/`

---

## 🌐 Como Fazer Deploy Online (GitHub Pages ou Vercel)

### Opção 1: GitHub Pages

1. Inicialize o repositório git e suba para o GitHub:
   ```bash
   git init
   git add .
   git commit -m "feat: Sistema de Prospecção e Vendas Trajetória"
   git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
   git push -u origin main
   ```
2. Execute o comando de deploy automático:
   ```bash
   npm run deploy
   ```
   *O sistema será publicado automaticamente na branch `gh-pages`!*

### Opção 2: Vercel

1. Importe o repositório do GitHub diretamente na [Vercel](https://vercel.com).
2. O build será detectado automaticamente (`npm run build`) e o site estará online instantaneamente com HTTPS gratuito.

---

## 👥 Compartilhamento de Dados com Colegas

Por padrão, o sistema armazena as alterações diretamente no **LocalStorage do navegador** para garantir máxima velocidade e uso offline. 

- **Como compartilhar com colegas**:
  1. Seu colega pode acessar a URL do site e terá acesso a todos os leads pré-carregados da base inicial.
  2. Para sincronizar alterações feitas por você, basta clicar no botão **Exportar Excel** e enviar a planilha para ele importar no botão **Importar Excel**.

---

## 🛠️ Tecnologias Utilizadas

- **Core**: React 19 + TypeScript + Vite
- **Estilização**: Tailwind CSS v4 (Design System Clean Light Mode / Apple Style)
- **Ícones**: Lucide Icons
- **Manipulação de Excel**: SheetJS (xlsx) + PapaParse
- **Efeitos**: Canvas Confetti
