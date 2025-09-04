# Guia de Estrutura do Frontend (api/types/ui)

## Objetivo
Padronizar a arquitetura do frontend para reduzir acoplamento, facilitar testes e acelerar a evolução das telas.

## Camadas

### 1) `src/api/`
- `client.ts`: configuração de HTTP (ex.: axios/fetch) com interceptors (auth, erros).
- `adapters/`: mapeia contratos do backend para tipos internos (normalização, defaults).
- `services/`: funções de alto nível usadas por páginas/containers.

### 2) `src/types/`
- Tipos compartilhados com o backend (domínio: `Project`, `Checklist`, etc.).
- Tipos derivados para UI (ex.: `PortfolioMetricsView`).

### 3) `src/ui/`
- Tokens (cores, espaçamentos, tipografia) e helpers de estilo.
- Componentes base (Button, Card, Table, EmptyState, ErrorState, Spinner).

## Padrões
- Páginas importam apenas `services` e `ui` (evitar `client` direto).
- Adaptadores isolam diferenças de API/versões, preservando testes.
- Testes focam em comportamento (DOM), não em implementação.

## Migração sugerida
1. Criar diretórios `api/`, `types/`, `ui/`.
2. Extrair tipos de `PortfolioOverview.tsx` para `src/types/`.
3. Criar `api/services/portfolio.ts` com `getMetrics()` e `getProjects()`.
4. Ajustar `PortfolioOverview.tsx` para usar os services e componentes `ui` (Spinner, ErrorState, EmptyState, Card, KPI).
5. Garantir suíte verde (testes essenciais: loading/erro/vazio/populado).
6. Repetir para `ProjectsList` e `ProjectDetail`.

## Frente Prioritária: Report Executivo
- Rota: `/projects/status` (Status Executivo)
- Layout: Sidebar simples (Visão Geral, Cronograma, Financeiro) + conteúdo em cards, tema dark (`slate-*`), cor primária `#0761FF`, fonte Inter.
- API: `GET /api/v1/projects`, `GET /api/v1/projects/{id}/action-items`.
- Componentização: KPIs (cards), tabela de projetos com coluna “Ações pendentes”, switch de abas local.
- Testes: unit com estados loading/vazio/erro; smoke E2E com navegação.

## Testes durante a migração
- Manter apenas cenários essenciais por tela.
- Evitar snapshots frágeis; usar `getByRole`/`getByText` com nomes estáveis.
- Rodar 1–2 E2E smoke no compose para detectar regressões de navegação.

## Critérios de pronto (fase)
- `api/types/ui` criados e utilizados por `PortfolioOverview`.
- Suíte Jest verde (sem thresholds), smoke E2E sem falhas.
- Documentação atualizada.

## Layout & UX (Aprovado)

### Padrão de Layout
- TopBar fixa no topo (64px): logo Betha, título de página, ações (tema, docs, usuário).
- SideNav à esquerda (w-64), colapsável em desktop e drawer em mobile.
- Breadcrumbs sempre visível no topo do conteúdo para orientar a navegação.
- Conteúdo principal em cards: KPIs no topo, tabela/listas abaixo.

```
┌─────────────────────────────────────────────────────────┐
│ TopBar                                                  │
├─────────────┬───────────────────────────────────────────┤
│ SideNav     │ Breadcrumbs                               │
│ (w-64)      │ KPIs (grid responsivo)                    │
│             │ Tabela/Listas                             │
└─────────────┴───────────────────────────────────────────┘
```

### Responsividade e Acessibilidade
- Breakpoints: mobile (<768px), tablet (768–1024px), desktop (>1024px).
- SideNav vira overlay/drawer em mobile (botão hamburger).
- Navegação por teclado, ARIA em botões/links/inputs.
- Skeletons para estados de loading; mensagens claras para vazio/erro.

### Cores e Tokens (tema dark)
- Primary (Betha): `#0761FF`.
- Background: slate-900/800/700; Texto: slate-100/400.
- Status (semântico): success, warning, error, info.
- Fonte da verdade em `src/ui/tokens/colors.ts`.

### Interações
- Hover consistente em itens clicáveis (links, botões, linhas da tabela).
- Breadcrumbs navegável; SideNav destaca item ativo.
- Tabela com busca, filtros e ordenação por coluna.

### Componentes implementados (referência)
- TopBar: `src/ui/components/Layout/TopBar.tsx`
- SideNav: `src/ui/components/Layout/SideNav.tsx`
- Breadcrumbs: `src/ui/components/Layout/Breadcrumbs.tsx`
- KPICard: `src/ui/components/Cards/KPICard.tsx`
- ProjectsTable: `src/ui/components/Tables/ProjectsTable.tsx`
- Tokens de cor/utilidades: `src/ui/tokens/colors.ts`

### Página do MVP
- Status Executivo: rota `/projects/status` (`src/pages/ProjectsStatusPage.tsx`).

---
Última atualização: 01/09/2025

