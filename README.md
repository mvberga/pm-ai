# 🚀 PM AI MVP - Ferramenta de Gestão de Projetos com IA

**Data de Criação:** Janeiro 2025  
**Última Atualização:** 05 de Setembro de 2025  
**Versão:** 1.2.0  
**Status:** ✅ Sistema de Autenticação e Testes Corrigidos

> Frente Prioritária URGENTE: Report Executivo (Frontend)
>
> - Rota alvo: `/projects/status`
> - Guia: `Aplicação/documentações/frontend/GUIA_FRONTEND_REPORT_EXECUTIVO.md`
> - Verificação entre camadas: `Aplicação/documentações/engenharia/VERIFICACAO_COMUNICACOES.md`
> - Protótipo visual de referência: `Backlog/frontend v3/Unificado.html` (Status – 3 abas)

---

## 🎯 **Visão Geral**

O **PM AI MVP** é uma ferramenta de gestão de projetos com FastAPI, React e PostgreSQL (pgvector), projetada para centralizar a implantação de projetos, substituir planilhas manuais e habilitar automações de IA.

### **✅ Status Atual**
- **MVP Completamente Estabilizado** seguindo padrões de engenharia robustos
- **Sistema de Autenticação Funcionando** com JWT e proteção de endpoints
- **Testes de Integração Corrigidos** e passando com sucesso
- **Base sólida** para desenvolvimento contínuo
- **Pronto para evolução** funcional e escalabilidade

### **📚 Documentação Organizada**
- **Versão mais recente**: `Aplicação/documentações/README.md`
- **Navegação rápida**: `Aplicação/documentações/ÍNDICE_DOCUMENTAÇÃO.md`
- **Regras de versionamento**: `Aplicação/documentações/REGRAS_VERSIONAMENTO.md`

---

## 📁 **Estrutura do Projeto**

```
📦 PM AI MVP/
├── 🚀 Aplicação/          # Código fonte e aplicação
│   ├── backend/           # API FastAPI (Python)
│   ├── frontend/          # Interface React (JavaScript)
│   ├── db/                # Scripts de banco PostgreSQL
│   └── docker-compose.yml # Ambiente de desenvolvimento
├── 📋 Backlog/            # Requisitos e especificações
│   ├── Frontend/          # Especificações de UI/UX
│   └── Requisitos/        # Requisitos funcionais
├── 💬 Chats/              # Histórico e contexto
│   ├── chat_início_do_projeto.md
│   └── CHAT_RESUMO.md
└── 📚 Documentação/       # Documentos organizados e versionados
    ├── Aplicação/documentações/  # Documentação técnica completa
    └── README.md          # Este arquivo (visão geral)
```

---

## 🚀 **Início Rápido**

### **Pré-requisitos**
- Docker e Docker Compose
- Portas 8000 (backend) e 5174 (frontend via compose) livres

### **Subir o ambiente (Docker Compose)**
```bash
# Navegar para o diretório da aplicação
cd Aplicação/

# Copiar variáveis de ambiente
cp env.example .env

# Subir todos os serviços (detached)
docker compose up -d --build
```

### **Acessos**
- **Backend API (Swagger)**: http://localhost:8000/docs
- **Frontend (Compose)**: http://localhost:5174
- **Health Check**: http://localhost:8000/api/v1/health

---

## 📚 **Documentação por Propósito**

### **🚀 Para Desenvolvedores**
- **`Aplicação/documentações/README.md`** - Setup, arquitetura e comandos (versão mais recente)
- **`Aplicação/documentações/REQUISITOS.md`** - Padrões técnicos e convenções
- **`Aplicação/documentações/REGRAS_VERSIONAMENTO.md`** - Regras de versionamento
- **`Aplicação/regras.mdc`** - Regras do projeto (Cursor) e diretrizes resumidas
- **`Aplicação/documentações/adr/`** - ADRs de UI (decisões de layout)
- **`Aplicação/documentações/ÍNDICE_DOCUMENTAÇÃO.md`** - Navegação rápida por toda documentação

### 🔥 Frente Prioritária do Frontend
- **Report Executivo (rota `/projects/status`)** — Implementar layout e componentes conforme o blueprint Status do `Unificado.html`, consumindo a API real. Consulte:
  - `Aplicação/documentações/frontend/GUIA_FRONTEND_REPORT_EXECUTIVO.md`
  - `Aplicação/documentações/engenharia/VERIFICACAO_COMUNICACOES.md`

### **📋 Para Planejamento**
- **`Aplicação/documentações/PRÓXIMOS_PASSOS.md`** - Roadmap e cronograma
- **`Aplicação/documentações/SPEC.md`** - Especificações do produto
- **`Backlog/`** - Requisitos detalhados por área

### **💬 Para Contexto**
- **`Chats/`** - Histórico de decisões e evolução
- **`Aplicação/documentações/ESTRUTURA_PROJETO.md`** - Organização do projeto
 - **`Aplicação/regras.mdc`** - Regras do projeto (Cursor)
 - **`Aplicação/documentações/adr/`** - ADRs de UI

---

## 🎯 **Funcionalidades (MVP)**

### **✅ Implementado**
- **Autenticação**: Google Sign-In com JWT e proteção de endpoints
- **Projetos**: CRUD completo com metadados e autenticação
- **Checklists**: Grupos e itens tipificados (Ação/Documentação)
- **Central de Ações**: Criação, filtros e atualização
- **Testes**: Suite completa de testes de integração funcionando
- **Segurança**: Endpoints protegidos com autenticação obrigatória

### **🚀 Próximas Fases**
- **Fase 2**: Gantt, Kanban, sistema de reuniões, pipeline de IA
- **Fase 3**: Modelos ML, RBAC avançado, dashboards
- **Fase 4**: CI/CD, observabilidade completa, produção

---

## 🛠️ **Stack Tecnológica**

| Camada | Tecnologia | Versão |
|--------|------------|---------|
| **Frontend** | React + Vite | 18.x |
| **Backend** | FastAPI (Python) | 3.11+ |
| **Banco** | PostgreSQL + pgvector | 16.x |
| **ORM** | SQLAlchemy 2.0 | Assíncrono |
| **Containerização** | Docker + Docker Compose | - |
| **Autenticação** | JWT (Google Identity) | OAuth 2.0 |

---

## 🔧 **Desenvolvimento**

### **Comandos úteis**
```bash
# Backend
cd Aplicação/backend
python -m pytest            # Executar testes
python -m ruff check app/   # Verificar código
python -m ruff format app/  # Formatar código

# Frontend
cd Aplicação/frontend
npm test                     # Executar testes
npm run lint                 # Verificar código
```

### **Como rodar testes e cobertura (Windows PowerShell)**
```powershell
cd "C:\Users\<SEU_USUARIO>\Desktop\Cursor\Aplicação\backend"

# 1) Criar e usar venv
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2) Rodar testes
.\.venv\Scripts\python.exe -m pytest -v -s

# 3) Cobertura + HTML
.\.venv\Scripts\python.exe -m pytest -v -s --cov=app --cov-report=term-missing --cov-report=html
start .\htmlcov\index.html
```

### **Padrões de Código**
- **Backend**: RORO, Guard Clauses, tipagem completa, injeção de dependência
- **Frontend**: Componentes funcionais, hooks, tratamento de erros
- **Qualidade**: Cobertura de testes ≥85%, linting automático

---

## 📊 **Métricas e Qualidade**

### **KPIs de Desenvolvimento**
- **Cobertura de testes**: ≥85%
- **Latência P95**: <300ms (rotas CRUD)
- **Disponibilidade**: 99.5% (produção)
- **Zero erros críticos**

### **Padrões de Qualidade**
- **Linting**: ruff, black, mypy
- **Segurança**: bandit, dependabot
- **CI/CD**: GitHub Actions (futuro)
- **Code Review**: 2 revisores para mudanças críticas

---

## 🤝 **Contribuição**

### **Fluxo de Desenvolvimento**
1. **Análise**: Consultar documentação relevante
2. **Desenvolvimento**: Seguir padrões estabelecidos
3. **Testes**: Cobertura ≥85%, testes de integração
4. **Review**: Code review com 2 revisores
5. **Deploy**: Apenas após validação completa

### **Padrões Git**
- **Commits**: Conventional Commits
- **Branches**: Feature branches para novas funcionalidades
- **PRs**: Template padronizado, revisão obrigatória

---

## 📈 **Roadmap Atualizado**

### **✅ Fase 1: MVP Estabilizado (CONCLUÍDA)**
- ✅ Estrutura reorganizada seguindo padrões
- ✅ Padrões de código implementados
- ✅ Observabilidade configurada
- ✅ Base sólida estabelecida
- ✅ Sistema de autenticação corrigido e funcionando
- ✅ Testes de integração corrigidos e passando
- ✅ Endpoints protegidos com autenticação adequada

### **🚀 Fase 2: Evolução Funcional (PRIORIDADE ATUAL)**
- 🔥 Prioridade URGENTE: Report Executivo (rota `/projects/status`)
  - Layout dark, fonte Inter e cor primária `#0761FF` alinhados ao `Unificado.html`
  - KPIs, tabela de projetos com ações pendentes, abas Visão Geral / Cronograma / Financeiro
  - Consumo de API: `GET /api/v1/projects`, `GET /api/v1/projects/{id}/action-items`
  - Testes unit (Jest/RTL) e smoke E2E (Cypress) para a rota
  - Checklist de verificação entre camadas concluído
  
  Próximas frentes (não urgentes):
  - 📊 Gantt e Kanban
  - 📝 Sistema de reuniões e transcrições
  - 🤖 Pipeline de IA com embeddings
  - 📚 Base de conhecimento vetorial

### **🔮 Fases Futuras**
- **Fase 3**: Escalabilidade e modelos ML
- **Fase 4**: Produção e CI/CD completo

---

## 📞 **Suporte e Contato**

### **Documentação**
- **Técnica**: `Aplicação/documentações/README.md` (versão mais recente)
- **Padrões**: `Aplicação/documentações/REQUISITOS.md`
- **Versionamento**: `Aplicação/documentações/REGRAS_VERSIONAMENTO.md`
- **Navegação**: `Aplicação/documentações/ÍNDICE_DOCUMENTAÇÃO.md`

---

## 🧭 **Governança (Arquitetura e UI)**

- **Regras do Projeto (Cursor)**: `Aplicação/regras.mdc` — padrões de dev, QA e diretrizes resumidas de UX/UI.
- **ADRs de UI**: `Aplicação/documentações/adr/` — decisões de layout; ver `ADR-UI-0001-layout-v1.md`.
- **Processo de UI/UX**: definido em `Aplicação/documentações/REQUISITOS.md` (seção UX/UI — processo, padrões e governança).
- **SPEC**: referência às ADRs e regras (governança de UI) em `Aplicação/documentações/SPEC.md`.

### **Desenvolvimento**
- **Issues**: GitHub Issues
- **Discussões**: GitHub Discussions
- **Documentação**: Swagger em `/docs`

---

## 🎉 **Conclusão**

O **PM AI MVP** está **100% estabilizado** e pronto para evolução funcional. A nova estrutura organizacional oferece:

1. **Separação clara** de responsabilidades
2. **Documentação organizada** por propósito
3. **Padrões estabelecidos** para desenvolvimento
4. **Base sólida** para crescimento contínuo
5. **Roadmap claro** para próximas fases

**🚀 O projeto está no caminho certo para se tornar uma ferramenta robusta de gestão de projetos com IA!**

---

## 📖 **Próximos Passos**

1. **Leia** `Aplicação/documentações/REGRAS_VERSIONAMENTO.md` para entender o versionamento
2. **Explore** `Aplicação/documentações/README.md` para setup e desenvolvimento (versão mais recente)
3. **Consulte** `Aplicação/documentações/PRÓXIMOS_PASSOS.md` para roadmap
4. **Navegue** `Aplicação/documentações/ÍNDICE_DOCUMENTAÇÃO.md` para encontrar documentos
5. **Contribua** seguindo os padrões estabelecidos

**Bem-vindo ao desenvolvimento do PM AI MVP! 🎯**
