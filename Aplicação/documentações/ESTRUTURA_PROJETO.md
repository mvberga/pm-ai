# 🏗️ Estrutura do Projeto PM AI MVP

**Data de Criação:** Janeiro 2025  
**Última Atualização:** Janeiro 2025  
**Versão:** 1.0.0  
**Status:** ✅ Estrutura reorganizada e documentada

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
- **Backend**: FastAPI com estrutura modular
- **Frontend**: React + Vite com componentes
- **Banco**: PostgreSQL + pgvector + migrations
- **Docker**: Configurações de ambiente

### **Status**
- ✅ **MVP 100% Estabilizado**
- ✅ **Padrões de código implementados**
- ✅ **Base sólida para evolução**

### **Estrutura Interna**
```
Aplicação/
├── backend/               # API FastAPI
│   ├── app/              # Código da aplicação
│   ├── Dockerfile        # Container do backend
│   └── requirements.txt  # Dependências Python
├── frontend/             # Interface React
│   ├── src/              # Código fonte
│   ├── Dockerfile        # Container do frontend
│   └── package.json      # Dependências Node.js
├── db/                   # Scripts de banco
├── docker-compose.yml    # Orquestração
└── README.md             # Documentação técnica
```

---

## 📋 **Backlog/ - Requisitos e Especificações**

### **Conteúdo**
- **Frontend**: Especificações de interface
- **Requisitos de IA**: Funcionalidades de inteligência artificial
- **Especificações técnicas**: Detalhes de implementação

### **Propósito**
- Referência para desenvolvimento de novas features
- Base para planejamento de sprints
- Documentação de requisitos não implementados

### **Estrutura Interna**
```
Backlog/
├── Frontend/             # Especificações de UI/UX
├── Requisitos/           # Requisitos funcionais
└── Especificações/       # Detalhes técnicos
```

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
3. **`regras.mdc`** - Regras do Cursor (este arquivo)

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

**📖 Para detalhes técnicos, consulte os documentos específicos em cada diretório!**
