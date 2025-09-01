# ADR-UI-0001 — Diretrizes de Layout V1 (PM AI MVP)

Data: 2025-08-29  
Status: Aceito  
Decisores: PO, Tech Lead, UX  
Revisão: trimestral (ou a cada release menor)

---

## 1) Contexto

Consolidar o layout V1 funcional e escalável para o SaaS de gestão de projetos, conciliando três visões: Gerencial (executivo/portfólio), Operacional (equipes) e Gestão de Projetos (GP). Há protótipos HTML iniciais ("importador.html" e "Status V1.html") que inspiram interações; formalizamos decisões antes de transpor para React e integrar com Backend/DB.

Referências:
- Backlog/Fontend v2/importador.html
- Backlog/Fontend v2/Status V1.html
- Aplicação/documentações/REQUISITOS.md (UX/UI e Backend/DB)
- Aplicação/regras.mdc (diretrizes resumidas)

---

## 2) Decisão

Arquitetura: Header + Sidebar colapsável + Breadcrumbs, com três áreas principais:
- Portfolio (Gerencial)
- Projects (Operacional)
- Project Detail (Gestão de Projetos)

Padrões V1 obrigatórios:
- Breakpoints: sm 640, md 768, lg 1024, xl 1280, 2xl 1536
- Acessibilidade: teclado/ARIA/contraste ≥ 4.5:1
- Estados: loading (skeleton), empty (CTA), error (retry)
- Componentização: cards adaptativos, DataTable (página/ordenar/filtrar), Charts encapsulados
- Tema: dark/light (preferência do sistema + toggle)

Processo antes de codar:
- Wireframes → Validação rápida → Mockups (Figma) → Kit de componentes
- Design Review semanal (30–45 min) com registro em ADR-UI + links nos PRs

---

## 3) Escopo V1 (UI)
- Portfolio Overview (cards + KPIs) e Timeline resumida
- Projects List e Project Detail (checklists, action items, documentos, timeline simplificada)
- Fundações: Header/Sidebar/Breadcrumbs; tema; grid/tokens de design

Fora de V1 (roadmap): Kanban completo, Gantt detalhado, relatórios executivos, Meetings+IA, Knowledge Base (RAG), analytics preditivo.

---

## 4) Impactos e Consequências
- Benefícios: consistência visual, melhor onboarding, evolução ágil
- Custos: discovery/design upfront, disciplina de ADR/Design Review
- Riscos: divergência mockups × dados reais → mitigar com contrato de API e seeds

---

## 5) Alternativas Consideradas
- Codar sem ciclo de design: descartado (alto retrabalho)
- UI monolítica: descartado (baixa reutilização)
- Lib de componentes pesada agora: adiado (manter leveza do MVP)

---

## 6) Plano de Validação
- Checklist por tela: estados, responsividade, acessibilidade
- Validação quinzenal com stakeholders
- Telemetria mínima de navegação/ações principais

---

## 7) Métricas de Sucesso
- Task Completion Rate > 95%
- −30% tempo de tarefas vs. protótipo
- Satisfação interna > 4.5/5

---

## 8) Roadmap e Versionamento
- V1.0: fundações + Portfolio + Projects + Project Detail básico
- V1.1: Kanban por vertical/projeto, filtros avançados, saved views
- V1.2: Gantt completo, relatórios executivos, exportações ricas
- Mudanças relevantes registradas em ADR-UI-00xx

---

## 9) Integração Backend/DB
- Confirmar contrato de dados da V1 antes de codar UI
- Alembic: 1 PR = 1 migration; rollback testado; API estável em /api/v1
- Performance: índices; paginação; limites de payload
- Segurança/LGPD: JWT escopado; CORS restrito; masking; retenção

---

## 10) Riscos e Mitigações
- Dados incompletos → seeds/mocks
- Responsividade complexa → grid com auto-fit ≥ 300px
- Acessibilidade negligenciada → checklist a11y nos PRs (linter futuro)

---

## 11) Ações
- Wireframes + mockups (Portfolio, Projects, Project Detail)
- Tokens de design e kit base
- Alinhar contrato de API com backend antes da UI
- Telemetria mínima habilitada
