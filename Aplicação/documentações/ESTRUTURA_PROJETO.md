# 🏗️ Estrutura do Projeto PM AI MVP

**Data de Criação:** Janeiro 2025  
**Última Atualização:** 2 de Setembro de 2025  
**Versão:** 3.2.0  
**Status:** ✅ Arquitetura do backend expandida e documentada - Fase 2: Sistema Completo Baseado no Protótipo concluída

---

## 📁 **Visão Geral da Estrutura**

O projeto foi reorganizado em três diretórios principais para melhor organização e separação de responsabilidades:

```
📦 Cursor/
├── 🚀 Aplicação/          # Código fonte e aplicação
├── 📋 Backlog/            # Requisitos e especificações
└── 💬 Chats/              # Histórico e contexto
```

---

## 🚀 **Aplicação/ - Código Fonte**

### **Conteúdo**
- **Backend**: FastAPI com arquitetura expandida e modular
- **Frontend**: React + Vite com componentes
- **Banco**: PostgreSQL + pgvector + migrations
- **Docker**: Configurações de ambiente

### **Status**
- ✅ **MVP 100% Estabilizado**
- ✅ **Arquitetura do backend expandida e implementada**
- ✅ **Fase 2: Sistema Completo Baseado no Protótipo - CONCLUÍDA**
- ✅ **Padrões de código implementados**
- ✅ **Base sólida para evolução**
- ✅ **Análise do protótipo HTML unificado concluída**
- 🔄 **Próximo: Fase 3 - Sistema de Produção e Deploy**

### **Estrutura Interna**
```
Aplicação/
├── backend/               # API FastAPI
│   ├── app/              # Código da aplicação
│   ├── Dockerfile        # Container do backend
│   └── requirements.txt  # Dependências Python
├── frontend/             # Interface React
│   ├── src/              # Código fonte
│   │   ├── api/          # Cliente API e hooks
│   │   ├── types/        # Tipos TypeScript
│   │   ├── ui/           # Componentes e tokens
│   │   ├── pages/        # Páginas da aplicação
│   │   └── components/   # Componentes específicos
│   ├── Dockerfile        # Container do frontend
│   └── package.json      # Dependências Node.js
├── db/                   # Scripts de banco
├── docker-compose.yml    # Orquestração
└── README.md             # Documentação técnica
```

### **Nova Arquitetura do Backend (Implementada)**
```
Aplicação/backend/app/
├── core/                 # Configurações centrais
│   ├── config.py         # Configurações da aplicação
│   └── deps.py           # Dependências FastAPI
├── db/                   # Gerenciamento de banco
│   └── session.py        # Sessões SQLAlchemy
├── models/               # Modelos de dados (expandidos)
│   ├── user.py           # Usuários
│   ├── project.py        # Projetos
│   ├── checklist.py      # Checklists
│   ├── action_item.py    # Itens de ação
│   ├── portfolio.py      # Portfólios (NOVO)
│   ├── team_member.py    # Membros da equipe (NOVO)
│   ├── client.py         # Clientes (NOVO)
│   ├── risk.py           # Riscos (NOVO)
│   ├── lesson_learned.py # Lições aprendidas (NOVO)
│   └── next_step.py      # Próximos passos (NOVO)
├── routers/              # Rotas da API (expandidas)
│   ├── auth.py           # Autenticação
│   ├── projects.py       # Projetos
│   ├── checklists.py     # Checklists
│   ├── action_items.py   # Itens de ação
│   ├── portfolios.py     # Portfólios (NOVO)
│   ├── team_members.py   # Membros da equipe (NOVO)
│   ├── clients.py        # Clientes (NOVO)
│   └── risks.py          # Riscos (NOVO)
├── services/             # Lógica de negócio (NOVO)
│   ├── auth_service.py   # Serviços de autenticação
│   ├── project_service.py # Serviços de projeto
│   ├── checklist_service.py # Serviços de checklist
│   └── action_item_service.py # Serviços de item de ação
├── repositories/         # Camada de dados (NOVO)
│   ├── base_repository.py # Repositório base
│   ├── user_repository.py # Repositório de usuários
│   ├── project_repository.py # Repositório de projetos
│   ├── checklist_repository.py # Repositório de checklists
│   └── action_item_repository.py # Repositório de itens de ação
├── utils/                # Utilitários (NOVO)
│   ├── excel_parser.py   # Parser de Excel
│   ├── pdf_generator.py  # Gerador de PDF
│   └── ai_integration.py # Integração com IA (Gemini)
├── cache/                # Sistema de cache (NOVO)
│   ├── redis_client.py   # Cliente Redis
│   ├── cache_service.py  # Serviço de cache
│   └── cache_decorators.py # Decoradores de cache
├── tasks/                # Tarefas assíncronas (NOVO)
│   ├── celery_app.py     # Configuração Celery
│   ├── import_tasks.py   # Tarefas de importação
│   ├── report_tasks.py   # Tarefas de relatórios
│   └── ai_tasks.py       # Tarefas de IA
├── tests/                # Testes (expandidos)
│   ├── test_services.py  # Testes de serviços (NOVO)
│   ├── test_repositories.py # Testes de repositórios (NOVO)
│   ├── test_utils.py     # Testes de utilitários (NOVO)
│   └── [outros testes existentes]
├── middlewares/          # Middlewares
│   ├── error_handler.py  # Tratamento de erros
│   └── logging.py        # Logging
├── schemas/              # Schemas Pydantic (expandidos)
│   ├── user.py           # Schemas de usuário
│   ├── project.py        # Schemas de projeto
│   ├── checklist.py      # Schemas de checklist
│   ├── action_item.py    # Schemas de item de ação
│   ├── portfolio.py      # Schemas de portfólio (NOVO)
│   ├── team_member.py    # Schemas de membro da equipe (NOVO)
│   ├── client.py         # Schemas de cliente (NOVO)
│   ├── risk.py           # Schemas de risco (NOVO)
│   ├── lesson_learned.py # Schemas de lição aprendida (NOVO)
│   └── next_step.py      # Schemas de próximo passo (NOVO)
└── main.py               # Aplicação principal
```

### **Estrutura Futura (Baseada no Protótipo)**
```
Aplicação/
├── backend/               # API FastAPI (expandida) ✅ IMPLEMENTADA
│   ├── app/              # Código da aplicação
│   │   ├── routers/      # Rotas da API ✅ IMPLEMENTADA
│   │   ├── models/       # Modelos de dados ✅ IMPLEMENTADA
│   │   ├── services/     # Lógica de negócio ✅ IMPLEMENTADA
│   │   ├── repositories/ # Camada de dados ✅ IMPLEMENTADA
│   │   ├── utils/        # Utilitários ✅ IMPLEMENTADA
│   │   ├── cache/        # Sistema de cache ✅ IMPLEMENTADA
│   │   ├── tasks/        # Tarefas assíncronas ✅ IMPLEMENTADA
│   │   └── tests/        # Testes ✅ IMPLEMENTADA
│   └── ...
├── frontend/             # Interface React (sistema completo)
│   ├── src/              # Código fonte
│   │   ├── apps/         # Aplicações principais
│   │   │   ├── auth/     # Sistema de autenticação
│   │   │   ├── projects/ # App de Projetos
│   │   │   ├── status/   # App de Status
│   │   │   └── importers/# App de Importadores
│   │   ├── shared/       # Componentes compartilhados
│   │   │   ├── components/# Componentes reutilizáveis
│   │   │   ├── hooks/    # Hooks customizados
│   │   │   ├── utils/    # Utilitários
│   │   │   └── types/    # Tipos TypeScript
│   │   └── ...
│   └── ...
└── ...
```

---

## 📋 **Backlog/ - Requisitos e Especificações**

### **Conteúdo**
- **Frontend**: Especificações de interface
- **Requisitos de IA**: Funcionalidades de inteligência artificial
- **Especificações técnicas**: Detalhes de implementação
- **Protótipo HTML Unificado**: Sistema completo de gestão de projetos

### **Propósito**
- Referência para desenvolvimento de novas features
- Base para planejamento de sprints
- Documentação de requisitos não implementados
- **Blueprint para implementação do sistema completo**

### **Estrutura Interna**
```
Backlog/
├── Frontend/             # Especificações de UI/UX
├── frontend v3/          # Protótipo HTML unificado
│   └── Unificado.html    # Sistema completo de gestão
├── Requisitos/           # Requisitos funcionais
└── Especificações/       # Detalhes técnicos
```

### **Protótipo HTML Unificado**
- **Localização**: `Backlog/frontend v3/Unificado.html`
- **Conteúdo**: Sistema completo com 3 aplicações principais
- **Status**: ✅ Analisado e documentado
- **Próximo**: Implementação baseada no protótipo

---

## 💬 **Chats/ - Histórico e Contexto**

### **Conteúdo**
- **Resumos de conversas**: Decisões arquiteturais
- **Contexto histórico**: Evolução do projeto
- **Decisões técnicas**: Justificativas de escolhas

### **Propósito**
- Manter contexto histórico do projeto
- Referência para decisões arquiteturais
- Base para onboarding de novos desenvolvedores

### **Estrutura Interna**
```
Chats/
├── chat_início_do_projeto.md    # Contexto inicial
├── CHAT_RESUMO.md               # Resumo de decisões
└── [outros chats]               # Conversas específicas
```

---

## 📚 **Documentação de Referência**

### **Para Desenvolvimento Diário**
1. **`Aplicação/README.md`** - Setup e arquitetura
2. **`Aplicação/REQUISITOS.md`** - Padrões técnicos
3. **`Aplicação/FRONTEND_ESTRUTURA.md`** - Arquitetura do frontend e UX/Layout aprovados
4. **`regras.mdc`** - Regras do Cursor (este arquivo)

### **Para Implementação do Sistema Completo**
1. **`ANÁLISE_PROTÓTIPO_HTML.md`** - Análise detalhada do protótipo vs implementação atual
2. **`Backlog/frontend v3/Unificado.html`** - Protótipo completo do sistema
3. **`PRÓXIMOS_PASSOS.md`** - Plano de implementação em fases

> **Atualização**: O protótipo HTML unificado (`Backlog/frontend v3/Unificado.html`) representa um sistema completo de gestão de projetos com 3 aplicações principais (Projetos, Status, Importadores), autenticação, importação de planilhas, gráficos interativos, gestão de riscos com IA, e muito mais. Este arquivo serve como blueprint para implementação completa do sistema.

### **Para Planejamento**
1. **`Aplicação/PRÓXIMOS_PASSOS.md`** - Roadmap e cronograma
2. **`Aplicação/SPEC.md`** - Especificações do produto
3. **`Backlog/`** - Requisitos detalhados

### **Para Contexto Histórico**
1. **`Chats/`** - Decisões e evolução do projeto

---

## 🔄 **Fluxo de Trabalho Recomendado**

### **Desenvolvimento de Nova Feature**
1. **Análise**: Consultar `Backlog/` e `SPEC.md`
2. **Desenvolvimento**: Seguir padrões de `REQUISITOS.md`
3. **Implementação**: Código em `Aplicação/`
4. **Documentação**: Atualizar documentação relevante

### **Implementação do Sistema Completo**
1. **Análise**: Consultar `ANÁLISE_PROTÓTIPO_HTML.md`
2. **Planejamento**: Seguir fases em `PRÓXIMOS_PASSOS.md`
3. **Desenvolvimento**: Implementar baseado no protótipo HTML
4. **Validação**: Comparar com protótipo e documentar progresso

### **Correção de Bugs**
1. **Identificação**: Reproduzir em `Aplicação/`
2. **Correção**: Seguir padrões existentes
3. **Teste**: Validar em ambiente local
4. **Deploy**: Apenas após validação

### **Atualização de Documentação**
1. **Identificação**: Mudança que afeta documentação
2. **Atualização**: Modificar arquivo relevante
3. **Validação**: Verificar consistência entre documentos
4. **Commit**: Incluir na mesma PR da funcionalidade

---

## 🎯 **Padrões de Organização**

### **Nomenclatura**
- **Arquivos**: `snake_case.md` para documentação
- **Pastas**: `PascalCase` para diretórios principais
- **Código**: Seguir padrões específicos de cada linguagem

### **Versionamento**
- **Documentação**: Atualizar com cada mudança significativa
- **Código**: Commits atômicos e descritivos
- **Releases**: Tagging semântico (SemVer)

### **Manutenção**
- **Revisão periódica**: Mensal para documentação
- **Atualização**: Sempre que houver mudanças
- **Validação**: Verificar links e referências

---

## 🚨 **Regras Importantes**

### **Nunca Fazer**
- ❌ Mover arquivos sem atualizar referências
- ❌ Deletar documentação sem backup
- ❌ Ignorar inconsistências entre documentos

### **Sempre Fazer**
- ✅ Atualizar documentação com mudanças
- ✅ Manter links funcionando
- ✅ Seguir padrões estabelecidos
- ✅ Validar consistência

---

## 📊 **Métricas de Organização**

### **Indicadores de Qualidade**
- **Documentação atualizada**: 100% dos arquivos
- **Links funcionando**: Zero links quebrados
- **Consistência**: Documentos alinhados
- **Cobertura**: Todas as funcionalidades documentadas

### **Acompanhamento**
- **Revisão mensal**: Estrutura e organização
- **Validação trimestral**: Links e referências
- **Atualização contínua**: Com mudanças no projeto

---

## 🎉 **Conclusão**

A nova estrutura organizacional oferece:

1. **Separação clara** de responsabilidades
2. **Fácil navegação** entre diferentes tipos de conteúdo
3. **Manutenção simplificada** da documentação
4. **Contexto preservado** para novos desenvolvedores
5. **Base sólida** para crescimento do projeto
6. **Blueprint completo** para implementação do sistema de gestão de projetos
7. **Arquitetura do backend expandida** com padrões enterprise (Services, Repositories, Cache, Tasks)

### **Próximos Passos**
- **Fase 3: Sistema de Produção e Deploy** - Infrastructure Setup
- **CI/CD Pipeline**: Implementar GitHub Actions, testes automatizados
- **Monitoring & Logging**: Implementar logging estruturado, métricas, alertas
- **Production Deployment**: Deploy em staging e produção
- **Performance Testing**: Testes de carga e otimizações
- **Security Audit**: Auditoria de segurança

**📖 Para detalhes técnicos, consulte os documentos específicos em cada diretório!**
