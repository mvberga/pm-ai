## Guia Frontend - Report Executivo (/projects/status)

- Rota: `/projects/status`
- Tema: dark, fonte Inter, primária Tailwind `primary` (equivalente a #2563EB)
- Componentes: `TopBar`, `SideNav`, `Breadcrumbs`, `KPICard`, `ProjectsTable`
- Dados: hooks `useProjects()` e `useActionItems()`

Endpoints consumidos:
- GET `/projects?include_action_items=true`
- GET `/projects/{id}/action-items` (on-demand ao clicar em ações)

KPIs exibidos:
- Total de Projetos
- Projetos com Ações Pendentes
- Total de Ações Pendentes
- Valor Total dos Projetos (implantação)

Interações:
- Clique em projeto leva para `/projects/:id`
- Clique em “ações” abre painel com action items do projeto

Testes:
- Unit (Jest/RTL): `src/__tests__/pages/ProjectsStatusPage.test.tsx`
- E2E (Cypress): `cypress/e2e/projects_status.cy.js`
- E2E Live opcional: `cypress/e2e/project_real_live.cy.js` (executar com `npm run cypress:run:live`)

# GUIA — Frontend Report Executivo (Prioridade URGENTE)

Data: 03/09/2025
Status: Ativo (Prioridade urgente)

## Objetivo
Implementar a página “Report Executivo” no frontend (rota `/projects/status`) alinhada ao blueprint visual do `Backlog/frontend v3/Unificado.html` (módulo Status com 3 abas), consumindo a API real e cobrindo estados de loading/vazio/erro, com smoke E2E.

## Escopo (MVP da página)
- Sidebar fixa/drawer com 3 abas: Visão Geral, Cronograma, Financeiro.
- Visão Geral:
  - KPIs: Total de projetos; Ações pendentes; Última entrega (máx); % concluído.
  - Tabela com: Projeto, Cidade, Ações pendentes; busca por nome.
- Cronograma: barras de progresso por projeto (percentual simples).
- Financeiro: placeholder para dados financeiros (sem dependência de XLSX nesta fase).

## API (contratos)
- GET `/api/v1/projects`
  - Esperado: `[ { id, name, city, progress?, timeline? } ]`
- GET `/api/v1/projects/{id}/action-items`
  - Esperado: `[ { id, project_id, status, type?, due_date? } ]`

Notas:
- Backend deve habilitar CORS e expor base por `VITE_API_URL`.
- Autenticação: seguir fluxo atual (cookies/JWT, se aplicável).

## Implementação (arquivos)
- `src/pages/ProjectsStatusPage.jsx`: página principal (sidebar + conteúdo por abas).
- `src/services/api.js`: `getProjects()`, `getActionItems(projectId)`.
- Ajustes visuais globais:
  - `index.html`: classe `dark`, fonte Inter (já aplicado).
  - Tailwind: darkMode 'class'.

## Estilo e Layout
- Tema dark: backgrounds `bg-slate-900/800/700`, textos `text-slate-100/400`.
- Cor primária: `#0761FF` (links/realces).
- Fonte: Inter.
- Interações: hover consistente; navegação por teclado; ARIA em inputs/botões/links.

## Testes
- Unit (Jest/RTL):
  - KPIs renderizam com mocks.
  - Busca filtra tabela.
  - Estados loading/vazio/erro.
- E2E (Cypress, smoke):
  - Navegar para `/projects/status` e ver lista.
  - Filtrar por nome e manter renderização estável.

## Critérios de Aceite
- Página abre em `/projects/status` com layout dark e fonte Inter.
- KPIs corretas para dados mockados/da API.
- Tabela com coluna “Ações pendentes”.
- Abas funcionando (Visão Geral, Cronograma, Financeiro).
- Requests batem na API configurada via `VITE_API_URL`.
- Testes unit e smoke E2E passando.

## Riscos e Mitigações
- Ausência de dados financeiros: manter placeholder e planejar endpoints.
- CORS/Autenticação: validar no checklist de verificação entre camadas.
- Performance: projeto e ações carregados em paralelo; paginação futura se necessário.

## Referências
- `Backlog/frontend v3/Unificado.html` (módulo Status)
- `Backlog/frontend v3/documentacao_aplicacao_prompt_html.md`
