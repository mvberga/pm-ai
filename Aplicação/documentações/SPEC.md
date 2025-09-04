# SPEC.md — Ferramenta de Gestão de Projetos com IA (MVP)

**Data de Criação:** 18 de Agosto de 2025  
**Última Atualização:** 29 de Agosto de 2025  
**Versão:** 1.0.1  
**Status:** ✅ Aprovado para desenvolvimento do MVP

---

## 1) Visão & Objetivo

**Visão:** Centralizar a gestão de implantação de projetos (do entendimento inicial ao handover), reduzindo planilhas manuais e habilitando automações de IA (captura de transcrições, extração de ações e base de conhecimento para consulta/RAG).

**Objetivo do MVP:** Disponibilizar autenticação, cadastro/consulta de projetos, checklists por grupos (itens categorizados) e central de ações com filtros básicos, servindo de base para evoluções (Gantt, Kanban, RAG e histórico de eventos).

---

## 2) Escopo

### 2.1 Incluído (MVP)
- Login via Google (stub no backend; trocar por verificação real em produção).
- **Projetos:** listar, criar, detalhar.
- **Checklists:** grupos por projeto; itens classificados como **Ação** ou **Documentação**; atualização de item.
- **Central de Ações:** criação, listagem com filtro por tipo e atualização.

### 2.2 Excluído (Roadmap)
- Visualizações **Gantt** e **Kanban**.
- **Histórico de Eventos/Reuniões** com resumos.
- Pipeline de **IA/RAG** (ingestão de transcrições e base vetorial).
- **Dashboard** e modelos preditivos.

---

## 3) Arquitetura & Stack

| Camada       | Tecnologia                                    | Motivo                                                                 |
|--------------|-----------------------------------------------|------------------------------------------------------------------------|
| Frontend     | React + Vite + React Router + Axios           | Rapidez de dev, SPA leve, roteamento simples, fácil integração REST.  |
| Backend      | FastAPI (Python 3.11)                         | Alto desempenho, OpenAPI automático, tipagem moderna.                 |
| Banco        | PostgreSQL 16 + `pgvector`                    | Relacional + vetores (pronto para RAG futuro).                        |
| ORM          | SQLAlchemy 2.0 (assíncrono) + asyncpg         | Modelo moderno, sessions assíncronas.                                 |
| Auth         | JWT (stub Google Sign-In)                     | Autorização simples; trocar por verificação real do id_token.         |
| Infra        | Docker & Docker Compose                       | Ambientes reproduzíveis e padronizados.                               |
| Orquestração | n8n (futuro)                                  | Pipelines de ingestão/IA e integrações (Google, etc.).               |

**Portas padrão:** Backend `8000`, Frontend `5173`, Postgres `5432`.

---

## 4) API do MVP

Prefixo: `/api/v1`

```http
# Autenticação (stub)
POST /auth/google/login
Body: { "id_token": "string", "email": "user@dominio", "name": "Nome" }
-> 200: { access_token, token_type, user }
```

```http
# Projetos
GET  /projects
POST /projects
GET  /projects/{project_id}
```

```http
# Checklists
GET  /projects/{project_id}/checklist-groups
POST /projects/{project_id}/checklist-groups

POST /checklist-groups/{group_id}/items
PUT  /checklist-items/{item_id}
```

```http
# Central de Ações
GET  /projects/{project_id}/action-items?type=...
POST /projects/{project_id}/action-items
PUT  /action-items/{item_id}
```

> Observação: no MVP, `owner_id` do projeto está temporário (valor fixo). Em produção, deve vir do **sub** do JWT.

---

## 5) Modelo de Dados (alto nível)

Entidades principais (MVP):

- `users` (id, email, name, created_at)
- `projects` (id, name, description?, portfolio?, vertical?, product?, owner_id, created_at)
- `project_members` (id, project_id, user_id, role?)
- `checklist_groups` (id, project_id, name, created_at)
- `checklist_items` (id, group_id, title, type['Ação','Documentação'], notes?, is_done, created_at)
- `action_items` (id, project_id, title, type['Ação Pontual','Pendência','Chamado','Bug'], assignee_id?, due_date?, status, description?, created_at)

> Futuro (fora do MVP): `meetings`, `risks`, `lessons_learned`, `knowledge_base` (texto + vetor + metadados).

---

## 6) Requisitos

### 6.1 Funcionais
- RF01: Autenticação via Google (verificação real do `id_token` fora do MVP).
- RF02: CRUD básico de Projetos.
- RF03: CRUD de Grupos de Checklist e Itens; alteração de status/conteúdo do item.
- RF04: Central de Ações com filtro por tipo.
- RF05: Healthcheck `/api/v1/health`.

### 6.2 Não Funcionais
- RNF01: **Segurança** — usar HTTPS em produção; rotacionar `SECRET_KEY`; mínimo de permissões nos tokens.
- RNF02: **Desempenho** — P95 < 300ms nas rotas CRUD (ambiente padrão).
- RNF03: **CORS** — liberar apenas origens necessárias.
- RNF04: **Manutenibilidade** — tipagem, linting, testes unitários (a adicionar), migrations com Alembic.
- RNF05: **Observabilidade** — logs estruturados (a adicionar), `/health`.

---

## 7) Critérios de Aceite (MVP)

- Conseguir criar e listar **Projetos** via UI e via API.
- Conseguir criar **Grupos de Checklist** por projeto e adicionar **Itens**; atualizar item.
- Conseguir criar **Itens de Ação**, filtrar por **tipo** e atualizá-los.
- Persistência estável em Postgres; inicialização com `pgvector` sem erros.
- CORS configurado para a origem do frontend.
- Documentação OpenAPI acessível em `/docs`.

---

## 8) Configuração & Ambiente

### 8.1 Variáveis de Ambiente (raiz `.env`)
```env
# Postgres
POSTGRES_USER=pmapp
POSTGRES_PASSWORD=pmapp
POSTGRES_DB=pmdb

# Backend
SECRET_KEY=devsecret
CORS_ORIGINS=http://localhost:5173

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
```

### 8.2 Subir o ambiente (dev)
```bash
cp .env.example .env
docker compose up --build
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:5173
```

---

## 9) Roadmap de Evolução

- **Fase 2:** Gantt, Kanban, histórico de eventos (reuniões, resumos, anotações), ingestão de transcrições via n8n, embeddings e `knowledge_base`.
- **Ajuste de Navegação (Base HTML → React):**
  - Status (SideNav): Visão Geral, Cronograma e Financeiro (consolidado) — aplicado no HTML base como referência.
  - Projetos (SideNav): Visão Geral, Equipe de Projeto, Cliente, Produto Contratado, Cronograma, Kanban, Checklist de Implantação, Gestão de Riscos, Lições Aprendidas, Próximos Passos, Extração — aplicado no HTML base.
  - Preferências persistidas: última aba do Status e portfólio selecionado salvos em `localStorage` — aplicado no HTML base.
- **Fase 3:** Modelos de ML (predição de atraso, recomendação de ações/risks), RBAC, auditoria de mudanças, exportações avançadas, testes e observabilidade completa.

---

## 10) Decisões & Observações

- Autenticação Google encontra-se **stub** para acelerar o MVP; exige troca por verificação real do `id_token` (Google Identity) antes de ir a produção.
- `owner_id` fixo na criação de projeto — **trocar** para extrair do JWT.
- `pgvector` habilitado desde o início para simplificar a transição ao RAG.
- Frontend com UI mínima e sem lib de componentes para manter leveza no MVP.
- Governança de UI: decisões registradas em `Aplicação/documentações/adr/` (ex.: ADR-UI-0001), seguindo processo definido em `REQUISITOS.md` (seção UX/UI) e regras em `Aplicação/regras.mdc`.
 - Governança de UI: decisões registradas em `Aplicação/documentações/adr/` (ex.: ADR-UI-0001), seguindo processo definido em `REQUISITOS.md` (seção UX/UI) e regras em `Aplicação/regras.mdc`.
 - Layout/UX aprovado (MVP): TopBar fixa, SideNav colapsável, Breadcrumbs visível; tokens e componentes base descritos em `FRONTEND_ESTRUTURA.md`.
