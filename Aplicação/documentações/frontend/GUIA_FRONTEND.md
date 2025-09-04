# Guia do Frontend

## Visão
Stack: Vite, React, TypeScript, Tailwind. Entrypoint: src/main.tsx.

## Estrutura
- Componentes, páginas, hooks, serviços (HTTP), assets
- Rotas e estado (definir padrão – ex.: React Router, Zustand/Redux)

## Build e Testes
- Build: npm run build
- Testes unitários: npm test -- --watch=false
- E2E: npx cypress run
- Cobertura: consultar pasta coverage/

## Integração com API
- Base URL, interceptors, autenticação (bearer), tratamento de erros
- Variáveis de ambiente (Vite): VITE_*

## Qualidade
- ESLint e Prettier
- depcheck e ts-prune para detectar dependências e exports não usados
- Cobertura mínima sugerida: 80%

## Frente Prioritária URGENTE: Report Executivo
- Rota `/projects/status` com layout e componentes alinhados ao protótipo `Backlog/frontend v3/Unificado.html` (módulo Status, 3 abas).
- Consulte `Aplicação/documentações/frontend/GUIA_FRONTEND_REPORT_EXECUTIVO.md` para escopo, API, testes e critérios de aceite.