# Documentação — Aplicação do Prompt ao HTML (Página Única)

Este documento consolida a **aplicação do prompt ajustado** sobre o arquivo HTML fornecido, produzindo:
1) uma **leitura técnica** do HTML e seus atributos/fluxos,
2) um **enquadramento** ao MVP conforme **README.md** e **SPEC.md** anexos,
3) uma **especificação de página** (React + TypeScript),
4) **integrações de API** mapeadas,
5) um **skeleton de código** pronto para colar,
6) um **plano de testes** e **boas práticas**,
7) itens a **remover/adiar** do HTML para aderir ao escopo do MVP,
8) **critérios de aceite** e próximos passos.

---

## 1) Leitura técnica do HTML (o que existe hoje)

### Arquitetura geral
- O arquivo implementa uma “**Dashboard Central**” com três telas navegáveis: seleção de portfólio → menu → duas apps internas: **ProjetosApp** e **StatusApp**.
- A troca de telas ocorre em `DOMContentLoaded`, alternando `display`/`hidden` e inicializando cada app sob demanda.
- Contêineres/IDs principais: `#portfolio-screen`, `#menu-screen`, `#projetos-app-container`, `#status-app-container`, além de botões para voltar e alternar apps.

### ProjetosApp (importador de planilha + visualizações)
- Estado interno extenso: dados de projeto/equipe/cliente/produtos/cronogramas, riscos, “lessons learned”, próximos passos, notas de produto, além de *instances* de gráficos (Chart.js).
- Parte do estado é persistida em **localStorage** (ex.: `projetos_lessonsLearnedData`, `projetos_nextStepsData`, `projetos_verticalsKanbanStatus`, `projetos_customTasks`, `projetos_productNotes`).
- Fluxo de importação: **drag & drop** ou file input → uso de **XLSX** para ler a planilha, reset de estruturas, mapeamento de **abas nomeadas** (e.g., “Dados Gerais”, “Equipe do Projeto”, “Dados Cliente”, “Produtos Contratados”, “Cronograma Macro”, “Cronograma - <Vertical>”, “Riscos”, “Documentos Chaves” etc.), normalização de cabeçalhos e conversão de datas Excel → ISO.
- Renderizações notáveis:
  - **Timeline** (cronograma) calculando progresso por **luxon** (hoje vs. início/fim), com barras e dias restantes.
  - Tabela de **Produtos Contratados** (Vertical, Produto, Entidade, Chamado, Senhas de Produção).
  - **Lessons Learned**: CRUD local com persistência em localStorage e botão “Remover”.
- Charts (Chart.js) para prioridades, origem, progresso de marcos e “verticals”.

### StatusApp (relatório executivo por planilha)
- Estruturas para agregação (inclui **pesos** por “etapa” para compor “score” de implantação) e normalização de *strings*.
- Fluxo similar ao de Projetos: importação de planilha (drag & drop, input change), **theme toggle** e **mobile sidebar**.

> **Observação de escopo:** grande parte do HTML atual depende de **upload de XLSX** e inclui features de **Gantt/Kanban, riscos e lessons** que **não fazem parte do MVP** descrito nos anexos. Essas funcionalidades devem seguir para backlog/fase futura.

---

## 2) Enquadramento ao MVP (README/SPEC)

- **Stack alvo (front):** React 18 + TypeScript com Vite, React Router e Axios/fetch.
- **Escopo funcional do MVP (front + API):**
  - **Projetos**: listar/criar/detalhar.
  - **Checklists**: grupos + itens com update.
  - **Central de Ações**: criar/listar/atualizar com filtro por tipo.
  - **Login Google** é *stub* no backend.
- **Fora do MVP agora:** Gantt/Kanban, Risks, Lessons Learned, Dashboard preditivo — manter como **backlog** e “*stubs*” visuais.
- **Decisão de recorte desta entrega:** transformar o HTML em **uma página React “Status Executivo de Projetos”** (rota `/projects/status`) que:
  1) lista projetos via **GET `/api/v1/projects`**,
  2) exibe indicadores simples (quantidade, % com ações pendentes, etc.),
  3) permite navegação para **detalhe** de projeto (`/projects/:id`),
  4) inclui um **painel de Ações** resumido por tipo (usa `/action-items`),
  5) **sem dependência de upload XLSX** (importador fica para fase/admin futura).

---

## 3) Especificação da Página (React + TS)

### Rota
- `/projects/status` — página única deste escopo.

### Layout & componentes compartilhados
- **TopBar** (usuário, alternância de tema, link para docs).
- **SideNav** simples com entradas “Projetos” e “Ações”.
- **Breadcrumbs** opcionais (quando fizer sentido).
- **Cards de KPI** (Total de Projetos; % com ações pendentes; Itens por tipo).
- **Tabela de Projetos** com busca client-side (por nome) e coluna “Ações pendentes”.
- **Painel “Ações Recentes”** (lista filtrável por `type`).

### Dados & Hooks
- `useProjects()` → **GET /api/v1/projects**.
- `useActionItems(projectId?)` → **GET /api/v1/projects/{id}/action-items?type=...`.
- **Tipos TS** alinhados ao modelo do MVP (projects, action_items etc.).

### Acessibilidade & UX
- Estados vazios (“Nenhum projeto”), *loading skeleton*, erros com **retry**.
- Navegação por teclado e `aria-*` em botões/links/inputs.
- i18n simples (pt-BR) e formatação de datas/valores (Intl).

### Segurança & Não-funcionais
- Propagar `Authorization: Bearer ...` (login Google stub).
- CORS e **base URL** via ambiente: `VITE_API_URL`.
- RNFs: tipagem forte, lint/format (ESLint/Prettier), testes automatizados.

---

## 4) Integrações de API (contratos usados)

### Projetos
- `GET /api/v1/projects` — lista projetos.
- `GET /api/v1/projects/{id}` — detalhe do projeto.

### Ações (Action Items)
- `GET /api/v1/projects/{project_id}/action-items?type=...` — filtra e lista;
- `POST /api/v1/projects/{project_id}/action-items` — cria;
- `PUT /api/v1/action-items/{item_id}` — atualiza.

### Mapeamento HTML → MVP
- “Próximos Passos” e “Pendências” do HTML tornam-se **Action Items**.
- Gantt/Kanban/risks/lessons ficam **ocultos** na UI do MVP (backlog).

---

## 5) Skeleton de código (pronto para colar)

```tsx
// src/pages/ProjectsStatusPage.tsx
import { useEffect, useMemo, useState } from "react";
import { getProjects, getActionItems } from "../services/api";
import type { Project, ActionItem } from "../types";

export default function ProjectsStatusPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [actions, setActions] = useState<ActionItem[]>([]);
  const [q, setQ] = useState("");

  useEffect(() => {
    getProjects().then(setProjects).catch(console.error);
  }, []);

  useEffect(() => {
    // opcional: carregar itens globais de ação (sem project_id) se existir endpoint
    Promise.all(projects.map(p => getActionItems(p.id)))
      .then(results => setActions(results.flat()))
      .catch(console.error);
  }, [projects]);

  const filtered = useMemo(
    () => projects.filter(p => p.name.toLowerCase().includes(q.toLowerCase())),
    [projects, q]
  );

  return (
    <div className="container">
      <header className="flex items-center justify-between">
        <h1>Status Executivo</h1>
        <input
          aria-label="Buscar projeto"
          placeholder="Buscar projeto..."
          value={q}
          onChange={e => setQ(e.target.value)}
        />
      </header>

      <section className="kpis">
        <div className="kpi">Projetos: {projects.length}</div>
        <div className="kpi">
          Ações pendentes: {actions.filter(a => a.status !== "done").length}
        </div>
      </section>

      <table>
        <thead><tr><th>Projeto</th><th>Ações pendentes</th></tr></thead>
        <tbody>
          {filtered.map(p => {
            const pending = actions.filter(a => a.project_id === p.id && a.status !== "done").length;
            return (
              <tr key={p.id}>
                <td><a href={`/projects/${p.id}`}>{p.name}</a></td>
                <td>{pending}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
```

```ts
// src/services/api.ts
export async function getProjects() {
  const r = await fetch(`${import.meta.env.VITE_API_URL}/projects`, {
    credentials: "include",
    headers: { "Accept": "application/json" }
  });
  if (!r.ok) throw new Error("Falha ao carregar projetos");
  return r.json();
}

export async function getActionItems(projectId: number) {
  const r = await fetch(`${import.meta.env.VITE_API_URL}/projects/${projectId}/action-items`, {
    credentials: "include",
    headers: { "Accept": "application/json" }
  });
  if (!r.ok) throw new Error("Falha ao carregar ações");
  return r.json();
}
```

**Observações do skeleton**
- Segue o **escopo do MVP** e evita dependência de XLSX.
- Usa **variável de ambiente** `VITE_API_URL` para a base da API.
- Prevê **acessibilidade** básica (aria-label no input de busca).

---

## 6) Plano de testes

### Unitários (front)
- `getProjects` retorna lista e trata erro (mock `fetch`).
- `getActionItems` retorna lista e trata erro (mock `fetch`).
- `ProjectsStatusPage` renderiza KPIs corretas para dados simulados.
- Filtro por busca (`q`) reduz linhas da tabela.

### Integração/E2E (front)
- Usuário acessa `/projects/status`, vê lista com KPIs.
- Filtra por nome.
- Navega para `/projects/:id` (quando a página de detalhe existir).

### Aceite (MVP)
- Criar/listar **Projetos**.
- Criar/listar/atualizar **Ações**.
- (**Checklists** serão cobertos em outra página/escopo).

---

## 7) Boas práticas aplicadas

- **Escopo MVP**: esconder funcionalidades de planilha/Gantt/Kanban até a fase apropriada; não expor botões que não chamem API real.
- **Componentização** clara, nomes descritivos, props enxutas (preferir objetos tipados).
- **Hooks customizados** para dados (ex.: `useProjects`, `useActionItems`) isolando Axios/fetch, erros e retries.
- **Gerência de efeitos** idempotente; cancelar requests em unmount; **debounce** em buscas/filtros.
- **Estados derivados** calculados (evitar duplicidade da fonte de verdade).
- **Loading skeletons** e **ARIA** corretos; foco após ações; **toasts** não bloqueantes.
- **Tratamento de erros** com UX de fallback (“tentar novamente”) e telemetria futura.
- **Sem segredos no código**; configs via `.env` e variáveis `VITE_*`.
- **Lint/format**: ESLint + Prettier; convenções de commits e branches.
- **Testes**: jest/RTL unit + cypress E2E cobrindo rotas, estados e fluxos críticos.

---

## 8) Itens a remover/adiar do HTML para aderência ao MVP

- **Remover da UI do MVP** (deixar como backlog):
  - Upload/parse de **XLSX** e telas dependentes;
  - **Gantt/Kanban**, **Risks**, **Lessons Learned**, **Documents**;
  - Gráficos específicos de “prioridade/origem” se não houver dados expostos pela API.
- **Justificativa:** fora do escopo do MVP (conforme planejamento/roadmap nos anexos).

---

## 9) Seletores/IDs críticos (referência para migração)

- Telas: `#portfolio-screen`, `#menu-screen`, `#projetos-app-container`, `#status-app-container`.
- Projetos (import): `#projetos_importer-screen`, `#projetos_drop-zone`, `#projetos_file-input`, `#projetos_loading-container`, `#projetos_import-status`, `#projetos_dashboard-container`.
- Projetos (features): `#projetos_lessons-table-body`, `#projetos_add-lesson-btn`, filtros de riscos, contêineres de timeline.
- Status: `#status_import-screen`, `#status_drop-zone`, `#status_file-input`, `#status_dashboard-container`, `#status_page-container`.

---

## 10) Critérios de aceite (para esta página)

- A página cumpre seu propósito e **usa os endpoints corretos** do MVP (listar/criar/atualizar conforme o caso).
- Estados **loading / vazio / erro** cobertos, com mensagens acessíveis.
- Navegação por **rota** funciona (deep-link e histórico do navegador).
- **Aderência ao modelo de dados** (IDs e campos) previsto na SPEC.
- **Testes** definidos/executáveis (unit/E2E) alinhados às práticas do repositório.

---

## 11) Próximos passos sugeridos

1. Criar interface **Project** e **ActionItem** em `src/types` com base nos contratos reais do backend.
2. Conectar autenticação **stub JWT/Google** (se necessário) e propagar `Authorization: Bearer ...` no `fetch`/Axios.
3. Implementar página de **detalhe do projeto** (`/projects/:id`) com painel de **Action Items** e, em fase posterior, **Checklists**.
4. Prever **feature flags** para gradualmente reintroduzir importação de planilha e visões Gantt/Kanban assim que estiverem disponíveis.
5. Adicionar **telemetria** básica (erros do front) e coleta de métricas de UX (latência de páginas, falhas por endpoint).

---

> **Resumo:** O HTML foi interpretado e convertido em uma **página única** compatível com o **MVP**. O resultado inclui especificação pronta, código base, plano de testes e critérios de aceite — tudo sem dependência de upload de XLSX nesta fase, garantindo entrega rápida e aderência ao escopo.
