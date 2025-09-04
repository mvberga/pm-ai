## Verificação de Comunicações - Frontend x Backend

Escopo: Report Executivo `/projects/status`

Base URL do cliente Axios: definida por `src/api/client.js`
- Testes (Jest): `http://localhost:8000/api/v1`
- Dev (Vite): `process.env.VITE_API_URL` se definido; fallback localhost
- Cypress (Docker): `http://backend:8000/api/v1`

Endpoints usados:
1. GET `/projects?include_action_items=true` — lista de projetos com contagem de ações
2. GET `/projects/{id}/action-items` — action items do projeto selecionado
3. Opcional: GET `/projects/metrics` — métricas agregadas (hook disponível)

E2E (mock vs live):
- Mock (padrão): intercepts direcionados a `/api/v1/**` com fixtures (`projects_status` e fluxos principais), garantindo estabilidade de CI.
- Live (opcional): `project_real_live.cy.js` acessa rotas reais quando `RUN_LIVE=1` e backend ativo.

Contratos esperados:
- `ProjectWithActions.pending_actions_count?: number`
- `ActionItem` com `status`, `priority`, `type`

Monitoramento/Erros:
- Estados de loading e erro cobertos na página e tabela
- Requisições idempotentes, sem mutações

# Checklist — Verificação de Comunicações e Aderência entre Camadas

Data: 03/09/2025
Escopo: Rota prioritária `/projects/status` (Report Executivo)

## Frontend
- [ ] `VITE_API_URL` configurado (.env/.env.local) e acessível no navegador
- [ ] `/projects/status` renderiza KPIs e tabela com dados reais
- [ ] Estados loading/vazio/erro cobertos; logs limpos no console
- [ ] Dark mode por classe e fonte Inter aplicados

## Backend (API)
- [ ] GET `/api/v1/projects` retorna 200 com lista
- [ ] GET `/api/v1/projects/{id}/action-items` retorna 200 com lista
- [ ] CORS habilitado para origem do frontend
- [ ] Autenticação (se ativa) aceita credenciais do frontend

## Banco de Dados
- [ ] Migrações aplicadas; dados seed de `projects` e `action_items`
- [ ] Índices por `project_id` em `action_items`

## Infra/Deploy
- [ ] Nginx/Proxy com upstream correto (headers CORS e segurança)
- [ ] Docker Compose expõe portas e redes corretas
- [ ] TLS/HTTPS no ambiente externo

## Testes e Observabilidade
- [ ] Jest/RTL para a página (KPIs, busca, estados)
- [ ] Cypress smoke para `/projects/status`
- [ ] Logs de erro no backend monitorados; sem 4xx/5xx inesperados

## Critérios de Aceite
- [ ] Página acessível, dados carregados, abas funcionais
- [ ] KPIs e tabela consistentes com a API
- [ ] Sem erros no console ou falhas de rede
