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

## Testes durante a migração
- Manter apenas cenários essenciais por tela.
- Evitar snapshots frágeis; usar `getByRole`/`getByText` com nomes estáveis.
- Rodar 1–2 E2E smoke no compose para detectar regressões de navegação.

## Critérios de pronto (fase)
- `api/types/ui` criados e utilizados por `PortfolioOverview`.
- Suíte Jest verde (sem thresholds), smoke E2E sem falhas.
- Documentação atualizada.

---
Última atualização: 30/08/2025

