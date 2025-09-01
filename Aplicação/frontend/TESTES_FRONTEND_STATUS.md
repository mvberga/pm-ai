# Status dos Testes de Frontend - PM AI MVP

**Data de Criação:** 28 de Agosto de 2025  
**Última Atualização:** 30 de Agosto de 2025  
**Status Atual:** 🧪 Reestruturação priorizada — Jest verde (suítes essenciais), E2E (smoke) sob demanda  
**Ação Atual:** Manter testes essenciais e congelar aumento de cobertura até estabilizar a nova arquitetura

---

## 🎯 **Visão Geral dos Testes de Frontend**

Infraestrutura de testes configurada (Jest + RTL). Durante a reestruturação, mantemos testes essenciais em páginas principais e `PortfolioOverview`.

---

## 📊 **Status Atual dos Testes de Frontend**

### **📌 Status Atual**
- **Infraestrutura**: Configurada (Jest + RTL)
- **Framework de Teste**: Jest + Testing Library (ativo)
- **Cobertura** (Jest): Stmts ~94.6% • Branches ~84.1% • Funcs ~92.3% • Lines ~96.1%
- **PortfolioOverview.tsx**: 100% Stmts/Funcs/Lines; Branches ~92.85%
- **Testes E2E**: Cypress (smoke, fluxo mockado, erros; 1 fluxo real)

### **📁 Estrutura Atual**
```
frontend/
├── src/
│   ├── __tests__/               # ✅ Testes essenciais
│   ├── api/                     # 🔄 (novo) cliente + adaptadores
│   ├── types/                   # 🔄 (novo) contratos com backend
│   └── ui/                      # 🔄 (novo) tokens/componentes base
├── jest.config.js
├── cypress/
└── cypress.config.js
```

---

## 🚀 **Roadmap (revisado)**

### **Fase 1: Configuração da Infraestrutura (Concluída)**

#### **1.1 Dependências de Teste**
- [x] **Jest**: Framework de teste principal
- [x] **@testing-library/react**
- [x] **@testing-library/jest-dom**
- [x] **@testing-library/user-event**

#### **1.2 Configuração**
- [x] **jest.config.js**
- [x] **setupTests.ts**
- [x] **scripts npm**

### **Fase 2: Reestruturação (agora)**

#### **2.1 Ações**
- [ ] Criar `src/api`, `src/types`, `src/ui`
- [ ] Migrar `PortfolioOverview.tsx` para o novo padrão
- [ ] Manter testes essenciais (carregando, erro, vazio, populado)
- [ ] Rodar 1–2 specs E2E smoke no compose

#### **2.2 Testes de Hooks e Utilitários**
- [ ] **Hooks customizados**: Lógica de estado e efeitos
- [ ] **Funções utilitárias**: Formatação, validação, etc.
- [ ] **Contextos**: Gerenciamento de estado global

### **Fase 3: Migração de Telas**

#### **3.1 Ações**
- [ ] Migrar `ProjectsList` e `ProjectDetail`
- [ ] Ajustar testes essenciais por tela migrada
- [ ] Garantir suíte verde a cada etapa

#### **3.2 Testes de Estado**
- [ ] **Gerenciamento de estado**: Context, Redux, etc.
- [ ] **Persistência**: LocalStorage, SessionStorage
- [ ] **Sincronização**: Estado entre componentes

---

## 🛠️ **Configuração**

### **Jest Configuration (Ativa)**
```javascript
// jest.config.js (planejado)
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/main.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

### **Testing Library Setup**
```typescript
// src/setupTests.ts (planejado)
import '@testing-library/jest-dom';
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### **Scripts NPM (Ativos)**
```json
// package.json scripts (planejado)
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci --coverage --watchAll=false"
  }
}
```

---

## 📋 **Comandos**

### **Testes Unitários**
```bash
cd Aplicação/frontend

# Executar todos os testes
npm test

# Testes em modo watch
npm run test:watch

# Testes com cobertura
npm run test:coverage

# Testes em modo CI
npm run test:ci
```

### **Testes E2E — Execução Visual (Docker + Cypress GUI)**
1) Subir a stack (db, backend, frontend):
```powershell
cd C:\Users\mvber\Desktop\Cursor\Aplicação
docker compose up -d --build
```
2) Abrir a aplicação (opcional):
```powershell
Start-Process http://localhost:5174
```
3) Abrir Cypress GUI localmente:
```powershell
cd C:\Users\mvber\Desktop\Cursor\Aplicação\frontend
npm install
$env:CYPRESS_BASE_URL='http://localhost:5174'; $env:CYPRESS_API='http://localhost:8000/api/v1'; npm run cypress:open
```
4) No Cypress, selecione E2E Testing → navegador → execute `smoke.cy.js` / `project_real.cy.js` / `project_flow.cy.js` / `errors.cy.js`.

### **Testes E2E — Execução Headless via Compose**
- O serviço `cypress` está sob o profile `e2e` e pausado por padrão. Para executar em CI/headless:
```powershell
cd C:\Users\mvber\Desktop\Cursor\Aplicação
docker compose --profile e2e up -d cypress
docker compose logs -f cypress
# para parar
docker compose stop cypress
```

### **E2E real (Docker Compose + CI)**
- Compose: `Aplicação/docker-compose.yml` (db, backend, frontend:5174)
- CI: `.github/workflows/e2e-real.yml`
- Local: set `CYPRESS_BASE_URL=http://localhost:5174` e rode `npm run cypress:run`

---

## 🎯 **Metas (temporárias)**

### **Cobertura de Testes**
- **Curto prazo**: arquitetura `api/types/ui` implementada; `PortfolioOverview` migrado; suíte verde
- **Após migração**: retomar metas de cobertura e ampliar E2E

### **Tipos de Teste**
- **Unitários**: Componentes individuais
- **Integração**: Interação entre componentes
- **E2E**: Fluxos completos do usuário
- **Performance**: Renderização e re-renderização

---

## 🔧 **Dependências Planejadas**

### **Dependências de Desenvolvimento (principais)**
```json
{
  "devDependencies": {
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "@testing-library/user-event": "^14.0.0",
    "jest": "^29.0.0",
    "jest-environment-jsdom": "^29.0.0",
    "ts-jest": "^29.0.0",
    "cypress": "^13.0.0"
  }
}
```

### **Configurações Adicionais**
- **MSW (Mock Service Worker)**: Para mockar APIs
- **React Testing Library**: Para testar componentes
- **Jest DOM**: Para matchers de DOM
- **User Event**: Para simular interações

---

## 🎯 **Próximos Passos**

### **Imediato**
1. **Aumentar branch coverage (≥70%)** com cenários adicionais no `PortfolioOverview.tsx`
2. **Preparar E2E com Cypress** (compose + 1 fluxo real adicional)

### **Médio Prazo**
1. **Testes de integração (páginas)**
2. **E2E com Cypress** (CI headless)
3. **Cobertura ≥80% (branches)**

---

## 📚 **Recursos e Referências**

### **Documentação**
- [Jest](https://jestjs.io/docs/getting-started)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Testing Library Jest DOM](https://github.com/testing-library/jest-dom)
- [Cypress](https://docs.cypress.io/)

### **Exemplos e Tutoriais**
- [Testing React Components](https://react.dev/learn/testing)
- [Jest with TypeScript](https://jestjs.io/docs/getting-started#using-typescript)
- [Testing Library Best Practices](https://testing-library.com/docs/guiding-principles)

---

## 🚀 **Conclusão**

Durante a reestruturação do frontend, os testes continuam como rede de segurança mínima. A expansão de cobertura fica pausada até estabilizarmos a nova arquitetura; depois, retomamos metas e ampliamos E2E.

---

## 🔗 **Links Relacionados**

- **📋 Status Geral dos Testes:** [../TESTES_GERAL.md](../TESTES_GERAL.md)
- **🧪 Status dos Testes Backend:** [../backend/TESTES_BACKEND_STATUS.md](../backend/TESTES_BACKEND_STATUS.md)
- **🚀 Próximos Passos:** [../PRÓXIMOS_PASSOS.md](../PRÓXIMOS_PASSOS.md)

