# REQUISITOS — Agente & Plataforma de Gestão de Projetos com IA (MVP → Escala)

**Data de Criação:** 26 de Agosto de 2025  
**Última Atualização:** 26 de Agosto de 2025  
**Versão:** 1.0.0  
**Status:** ✅ Padrões técnicos estabelecidos  
**Documento:** Requisitos de Engenharia, Governança e Operação para o projeto FastAPI + React + Postgres (pgvector) + n8n (futuro)

---

## 1) Visão, Objetivos e Escopo

**Visão:** Plataforma SaaS interna que centraliza a implantação de projetos, substitui planilhas, automatiza captura de ações a partir de reuniões e forma uma base de conhecimento (RAG) para consultas.  
**Objetivo (MVP):** Entregar autenticação, CRUD de Projetos, Checklists (grupos/itens) e Central de Ações (filtros), com fundações sólidas para IA e governança.  
**Fora do MVP (Roadmap):** Gantt, Kanban, Histórico de Eventos/Meetings, ingestão de transcrições, RAG/embeddings, dashboards e modelos preditivos.

---

## 2) Papéis e Responsabilidades (RACI simplificado)

- **Product Owner (A/R):** priorização de backlog, aceite do escopo.  
- **Tech Lead (A/R):** padrões de arquitetura, revisões críticas, segurança e performance.  
- **Backend Dev (R):** APIs, modelos, migrations, testes.  
- **Frontend Dev (R):** UI/UX, rotas, integração API.  
- **Data/ML (C):** ingestão, embeddings, curadoria e avaliação de IA.  
- **DevOps (C/R):** CI/CD, observabilidade, infra, backups e DR.  
- **Security/Governança (C/A):** LGPD, auditoria, gestão de riscos, controle de acessos.

---

## 3) Requisitos Funcionais (RF)

1. **Autenticação Google** (MVP em stub; produção com verificação real do `id_token`).  
2. **Projetos:** listar, criar e detalhar.  
3. **Checklists:** grupos por projeto; itens com tipos **Ação**/**Documentação**; atualização de item.  
4. **Central de Ações:** criação, filtro por tipo, atualização.  
5. **Healthcheck:** `/api/v1/health` expõe status básico.  
6. **OpenAPI:** documentação atualizada e versionada.

---

## 4) Requisitos Não Funcionais (RNF)

- **Disponibilidade alvo (SLI/SLO):** 99.5% ambiente prod; janelas de manutenção comunicadas.  
- **Latência (P95):** < 300 ms em rotas CRUD; < 800 ms com agregações simples.  
- **Escalabilidade:** stateless no backend; banco com índices e plano de particionamento futuro.  
- **Confiabilidade:** testes automatizados; migrations versionadas; restauração validada.  
- **Usabilidade:** UI responsiva, feedback de erros de forma clara, i18n preparado.  
- **Aderência aos 12‑Factor Apps:** configs via env; logs stdout; build/run/release separados.

---

## 5) Arquitetura & Stack

| Camada | Tecnologia | Diretrizes |
|---|---|---|
| **Frontend** | React + Vite + React Router + Axios | SPA leve; tratamento de erros; fallback offline básico; .env para API. |
| **Backend** | FastAPI (Python 3.11) | Routers modulares; DI; validação Pydantic v2; async I/O. |
| **DB** | PostgreSQL 16 + `pgvector` | Base relacional + vetores para RAG; Alembic para migrations. |
| **ORM** | SQLAlchemy 2.0 (assíncrono) + asyncpg | Sessões com `async_sessionmaker`; transações explícitas. |
| **Cache** | Redis (futuro) | TTL para dados quentes; invalidação por chave. |
| **Jobs/Orquestração** | n8n (futuro) | Ingestão de transcrições; pipelines de limpeza → chunking → embeddings. |
| **Mensageria (opcional)** | Redis Streams / RabbitMQ | Desacoplar jobs pesados (transcrição/embedding). |
| **Observabilidade** | OpenTelemetry + Prometheus/Grafana + Loki | Tracing, métricas e logs estruturados JSON. |
| **Segurança** | JWT (RS256 em prod), Rate limit, CORS, CSP | Defesa de borda, política de chaves e rotação. |

**Ambientes:** `dev` (Docker Compose), `staging` e `prod`. **Infra como código** (compose; Terraform opcional em nuvem).

---

## 6) Padrões de Código (Python/FastAPI)

**Princípios do exemplo incorporados e expandidos:**

- **Estilo e Organização**
  - **Conciso, técnico e modular**; evitar duplicação; **RORO (receive object, return object)**.  
  - Funções puras com `def`, I/O assíncrono com `async def`.  
  - Tipagem em **todas** as assinaturas; **Pydantic v2** para IO; `Annotated`/`Field` quando útil.  
  - Nomes descritivos com verbos auxiliares: `is_active`, `has_permission`.  
  - **snake_case** para arquivos e diretórios (`routers/project_routes.py`).  
  - Exporte rotas e utilitários nomeados; evite classes desnecessárias.  
  - Use **lifespan** (context manager) ao invés de `@app.on_event` quando adequado.
- **Tratamento de Erros (guard clauses)**
  - Verifique precondições no início; **early return** para erros; evite aninhamentos profundos.  
  - **HTTPException** para erros esperados; middleware para exceções inesperadas (500).  
  - Erros consistentes com código, `detail`, `type`, `instance` (padrão Problem Details opcional).  
- **Desempenho**
  - Somente operações async em DB/API externas; evite bloqueios.  
  - Cache de leituras frequentes (Redis); **ETag / Cache-Control** quando couber.  
  - Paginação padrão e **lazy loading** em coleções grandes.
- **Estrutura Sugerida**
  ```text
  backend/app/
    main.py
    core/        # config, segurança, lifespan, rate-limit
    db/          # engine, session, migrations (alembic)
    routers/     # project, checklist, action_items, auth
    models/      # sqlalchemy
    schemas/     # pydantic v2
    services/    # lógica de domínio (funções puras)
    utils/       # helpers (hash, time, parsing, idempotency)
    middlewares/ # logging, errors, cors
    tests/       # unit, integration, contract
  ```

**Exemplo — DI + guard clause + RORO**:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from .deps import get_session
from ..schemas.project import ProjectIn, ProjectOut
from ..models.project import Project

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]

@router.post("/projects", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectIn, session: Session) -> ProjectOut:
    if not payload.name.strip():
        raise HTTPException(status_code=400, detail="name_required")
    project = Project(**payload.model_dump(), owner_id=...)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return ProjectOut.model_validate(project, from_attributes=True)
```

---

## 7) Convenções de API

- **Versionamento:** prefixo `/api/v1`; breaking changes em `/api/v2`.  
- **Padrões REST:** nouns, idempotência em PUT/DELETE; **Idempotency-Key** (header) em POST críticos.  
- **Paginação:** `?page=1&size=50` + `X-Total-Count`; limites e default configuráveis.  
- **Filtros/Ordenação:** `?q=...&sort=-created_at`.  
- **Erros:** JSON com `{ code, detail, fields? }`; tabela de erros documentada.  
- **Segurança:** JWT Bearer; escopos/roles (RBAC leve); **CORS** restrito; **rate limit** por IP/usuário.  
- **Observabilidade:** `X-Request-ID` em todas as respostas; correlação de logs/traces.  
- **Docs:** OpenAPI gerada + exemplos; regras de depreciação com sunset headers.

---

## 8) Segurança e Conformidade (LGPD)

- **Princípios LGPD:** minimização, finalidade, necessidade e transparência.  
- **Base legal:** consentimento explícito para gravações/transcrições; contratos para dados necessários.  
- **Dados Sensíveis:** anonimização/pseudonimização; **Data Masking** em logs.  
- **Criptografia:** TLS 1.2+ em trânsito; AES‑256 at rest (se suportado pelo provedor).  
- **Segredos:** sem `secrets` no repositório; uso de variáveis de ambiente ou secret manager; **rotação** semestral.  
- **Acesso:** MFA para admin; **principle of least privilege**; trilhas de auditoria.  
- **Retenção & Eliminação:** políticas por tabela (ex.: logs 90 dias; transcrições brutas 180 dias).  
- **Backups & DR:** snapshot diário; retenção 7/30/90; **teste de restauração trimestral**.  
- **Supply Chain:** pin de dependências; `pip-tools`/`uv` + hashes; **SCA** (Snyk/Dependabot/Renovate); **Bandit**.  
- **Hardening:** headers (CSP, HSTS, X‑Content‑Type‑Options), desativar directory listing, limitar upload.

---

## 9) Dados e Banco

- **Modelagem:** chaves surrogate (`bigserial`), timestamps com TZ, soft‑delete onde fizer sentido.  
- **Índices:** em FKs e colunas de filtro; análise de `EXPLAIN` para queries pesadas.  
- **Migrations:** **Alembic** versionado; regra: 1 PR = 1 migration coesa.  
- **Integridade:** FKs ON DELETE RESTRICT/SET NULL conforme domínio; constraints NOT NULL adequadas.  
- **`pgvector`:** tabela `knowledge_base(text, embedding, metadata)` para RAG.  
- **Políticas de dados:** classificação (Público, Interno, Confidencial), owners por tabela.

---

## 10) Desempenho e Caching

- **Cache**: Redis com TTL para listas de referência; invalidar na escrita.  
- **Evitando N+1:** `selectinload`/`joinedload` quando necessário.  
- **Limites:** `size` máximo por página; proteção contra payloads grandes; gzip.  
- **Medições:** APM + traces de queries; orçamentos de performance por rota.

---

## 11) Observabilidade

- **Logs:** JSON estruturado (nivel, ts, msg, request_id, user_id?); nunca logar PII bruta.  
- **Métricas:** HTTP (latência, taxa de erro), DB (pool usage), cache hit rate, filas.  
- **Tracing:** OpenTelemetry; propagação de contexto; amostragem ajustável.  
- **Alertas:** baseados em SLO (latência/erros); rotas de escalonamento.

---

## 12) CI/CD

- **Pipelines (GitHub Actions ou similar):**
  1. **Lint/Format:** `ruff`, `black --check`, `mypy`.
  2. **Tests:** `pytest -q --maxfail=1 --disable-warnings --cov=app --cov-fail-under=85`.
  3. **Security:** `bandit -r app`, SCA (Snyk/Dependabot/Renovate).
  4. **Build:** Docker multi-stage (slim), SBOM.
  5. **Scan de imagem:** trivy/grype.
  6. **Deploy:** `staging` → smoke tests → aprovação → `prod`.
- **Padrões Git:** Conventional Commits; **SemVer**; PR template; CODEOWNERS; regras de branch `main` protegida.
- **DORA:** medir Lead Time, Deployment Frequency, MTTR, Change Failure Rate.

---

## 13) Testes

- **Níveis:** unitários (funções puras), integração (DB/Redis), contrato (OpenAPI), E2E (UI → API).  
- **Ferramentas:** `pytest`, `httpx.AsyncClient`, `pytest-asyncio`, `factory_boy/faker`.  
- **Dados de teste:** fixtures isoladas; DB efêmero por test run.  
- **Cobertura:** alvo ≥ 85% linhas backend; criticar testes frágeis/flaky (quarentena).

---

## 14) Configuração & Ambientes

- `.env` por ambiente; **nunca** commitar `.env` real.  
- **Feature Flags:** Unleash/Config simples para ativar Gantt/Kanban por ambiente.  
- **Tarefas:** `Makefile` (ex.: `make dev`, `make test`, `make lint`, `make migrate`).  
- **Pre-commit:** hooks para `ruff`, `black`, `mypy`, `bandit`.

---

## 15) Governança de Mudanças e Releases

- **Change Management:** changelog por release; ADRs para decisões arquiteturais.  
- **Revisões:** 2 revisores (um tech lead) para mudanças de schema/segurança.  
- **Risco:** matriz de risco para mudanças altas; rollback plan documentado.  
- **Auditoria:** trilhas de quem/quando/qual mudança (migrations, configs).

---

## 16) Gestão de Dependências & Licenças

- **Pin e lock:** `requirements.txt` + `uv`/`pip-tools` com hashes.  
- **Revisão periódica:** dependências desatualizadas/removidas.  
- **Licenças:** inventário de terceiros; arquivo NOTICE; evitar copyleft forte sem aprovação.

---

## 17) Documentação

- **SPEC.md** (produto), **REQUISITOS.md** (este arquivo), **API.md** (contrato), **RUNBOOK.md** (operacional), **SECURITY.md**.  
- **Exemplos executáveis** no Swagger; snippets de integração.  
- **ADR** para escolhas (ex.: `pgvector`, Redis, rate limit).

---

## 18) Automação & Agentes (IA)

- **Agente Dev (Cursor):** seguir princípios (funcional, RORO, DI, guard clauses).  
- **Defesas:** validação de prompt/entrada (contra prompt injection); limitar escopos e ações de escrita.  
- **Privacidade:** evitar envio de PII para modelos; mascarar/omitir campos.  
- **Avaliação de IA:** métricas de precisão/recall de extração de ações; amostragens semanais.  
- **Proveniência:** logar origem de trechos usados em RAG (doc_id, chunk_id, score).

---

## 19) Definition of Ready / Done

**Ready:** escopo claro, critérios de aceite testáveis, riscos conhecidos, migrações definidas.  
**Done:** código revisado, testes verdes (≥85%), cobertura de logs, métricas adicionadas, documentação atualizada, migrações aplicadas/rollback testado, release anotada.

---

## 20) Checklists Práticos

- [ ] Endpoint novo tem **tipos Pydantic**, validação e **exemplos** no OpenAPI.  
- [ ] Tratamento de erros com **HTTPException** + middleware 500.  
- [ ] **Logs** estruturados com `request_id`.  
- [ ] **Métricas** de lat/erro exportadas.  
- [ ] **Migrations** e índices revisados.  
- [ ] **Rate limit** e CORS conferidos.  
- [ ] **Secrets** via env/secret manager.  
- [ ] **CI** com lint/test/security; **image scan** ok.  
- [ ] **LGPD:** minimização, retenção e masking de logs.  
- [ ] **Backups/Restore** testados no ciclo.

---

## 21) Sugestões Adicionais

- **Idempotency‑Key** para POSTs sensíveis e **Outbox Pattern** para garantir envio de eventos.  
- **Coroutines bound**: limite de concorrência para jobs (se usar mensageria).  
- **API Contracts** com Pact/E2E consumer-driven para integrações externas.  
- **Blue/Green** ou **Canary** para reduzir risco de release.  
- **Error Budgets** alinhados a SLO para priorizar débitos técnicos.
