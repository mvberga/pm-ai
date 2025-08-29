# 📋 Regras de Versionamento de Documentos - PM AI MVP

**Data de Criação:** 28 de Agosto de 2025  
**Última Atualização:** 28 de Agosto de 2025  
**Versão:** 1.0.0  
**Status:** ✅ Regras estabelecidas

---

## 🎯 **Objetivo**

Este documento estabelece regras claras para versionamento e identificação de documentos no projeto PM AI MVP, evitando confusões sobre qual versão é a mais recente e mantendo consistência na documentação.

---

## 📊 **Padrão de Cabeçalho Obrigatório**

### **Formato Padrão**
```markdown
# Título do Documento

**Data de Criação:** DD/MM/AAAA  
**Última Atualização:** DD/MM/AAAA  
**Versão:** X.Y.Z  
**Status:** ✅/🔄/📋/🧪/❌
```

### **Campos Obrigatórios**
1. **Data de Criação**: Data em que o documento foi criado
2. **Última Atualização**: Data da última modificação
3. **Versão**: Número de versão semântica (X.Y.Z)
4. **Status**: Emoji indicando o status atual

---

## 🔢 **Sistema de Versionamento Semântico**

### **Formato: X.Y.Z**
- **X (Major)**: Mudanças que quebram compatibilidade
- **Y (Minor)**: Novas funcionalidades mantendo compatibilidade
- **Z (Patch)**: Correções e melhorias menores

### **Exemplos de Versionamento**
| Tipo de Mudança | Exemplo | Descrição |
|-----------------|---------|-----------|
| **Major (X)** | 1.0.0 → 2.0.0 | Reestruturação completa, mudanças arquiteturais |
| **Minor (Y)** | 1.0.0 → 1.1.0 | Novas funcionalidades, seções adicionadas |
| **Patch (Z)** | 1.0.0 → 1.0.1 | Correções, atualizações de status, formatação |

---

## 📅 **Padrões de Data**

### **Formato Brasileiro (Recomendado)**
```markdown
**Data de Criação:** 28 de Agosto de 2025
**Última Atualização:** 28 de Agosto de 2025
```

### **Formato Internacional (Alternativo)**
```markdown
**Data de Criação:** 2025-08-28
**Última Atualização:** 2025-08-28
```

### **Regras de Atualização**
- **Sempre atualizar** a data de última atualização ao modificar
- **Manter** a data de criação original
- **Usar formato consistente** em todo o projeto

---

## 🎨 **Sistema de Status com Emojis**

### **Status Principais**
| Emoji | Status | Descrição |
|-------|--------|-----------|
| ✅ | Concluído | Documento completo e atualizado |
| 🔄 | Em Progresso | Documento sendo desenvolvido/modificado |
| 📋 | Planejado | Documento planejado mas não iniciado |
| 🧪 | Testando | Documento em fase de validação |
| ❌ | Bloqueado | Documento com problemas ou dependências |

### **Status Específicos**
| Emoji | Status | Descrição |
|-------|--------|-----------|
| 🆕 | Novo | Documento recém-criado |
| 🔧 | Manutenção | Documento sendo corrigido/atualizado |
| 📚 | Documentação | Documento de referência |
| 🚀 | Lançamento | Documento para nova versão |

---

## 📁 **Organização por Localização**

### **Estrutura de Pastas e Versionamento**
```
📦 Projeto/
├── 📚 documentações/           # Documentação técnica (versão mais recente)
│   ├── README.md              # v1.0.0 (28/08/2025) ✅
│   ├── REQUISITOS.md          # v1.0 (26/08/2025) ✅
│   └── [outros documentos]   # Versões atualizadas
├── README.md                  # v0.9.0 (Janeiro 2025) 🔄
└── [outros arquivos]         # Versões variadas
```

### **Regra de Prioridade**
1. **`Aplicação/documentações/`**: Documentação técnica mais recente
2. **Raiz do projeto**: Documentação geral e visão de alto nível
3. **Subpastas específicas**: Documentação especializada por área

---

## 🔄 **Fluxo de Atualização de Documentos**

### **Processo de Modificação**
1. **Identificar** o documento a ser atualizado
2. **Fazer as alterações** necessárias
3. **Atualizar** a data de última atualização
4. **Incrementar** a versão conforme o tipo de mudança
5. **Atualizar** o status se necessário
6. **Atualizar** o `ÍNDICE_DOCUMENTAÇÃO.md`

### **Exemplo de Atualização**
```markdown
# Antes
**Última Atualização:** 28 de Agosto de 2025  
**Versão:** 1.0.0  
**Status:** ✅

# Depois (após correção)
**Última Atualização:** 28 de Agosto de 2025  
**Versão:** 1.0.1  
**Status:** ✅
```

---

## 📋 **Regras Específicas por Tipo de Documento**

### **Documentos Técnicos**
- **REQUISITOS.md**: Incrementar versão major para mudanças arquiteturais
- **SPEC.md**: Incrementar versão minor para novas funcionalidades
- **README.md**: Incrementar versão patch para atualizações de status

### **Documentos de Status**
- **TESTES_*.md**: Atualizar data e status, manter versão
- **PRÓXIMOS_PASSOS.md**: Incrementar versão minor para novas fases
- **CHAT_RESUMO.md**: Atualizar data, manter versão

### **Documentos de Navegação**
- **ÍNDICE_DOCUMENTAÇÃO.md**: Atualizar data e referências
- **ESTRUTURA_PROJETO.md**: Incrementar versão minor para mudanças estruturais

---

## 🚨 **Regras Críticas**

### **Nunca Fazer**
- ❌ Modificar documentos sem atualizar versão
- ❌ Ignorar atualização de data de última modificação
- ❌ Manter documentos duplicados com versões diferentes
- ❌ Usar formatos de data inconsistentes

### **Sempre Fazer**
- ✅ Atualizar versão ao modificar conteúdo
- ✅ Manter datas de criação e atualização
- ✅ Usar sistema de status com emojis
- ✅ Atualizar índices e referências
- ✅ Seguir padrão semântico de versionamento

---

## 📊 **Exemplo de Aplicação**

### **Cenário: Atualização de Status dos Testes**
```markdown
# TESTES_GERAL.md

**Data de Criação:** 28 de Agosto de 2025  
**Última Atualização:** 28 de Agosto de 2025  
**Versão:** 1.0.0  
**Status:** 🧪

# Após implementação dos testes
**Data de Criação:** 28 de Agosto de 2025  
**Última Atualização:** 29 de Agosto de 2025  
**Versão:** 1.1.0  
**Status:** ✅
```

---

## 🔍 **Verificação de Consistência**

### **Checklist de Validação**
- [ ] Cabeçalho com todos os campos obrigatórios
- [ ] Data de última atualização atualizada
- [ ] Versão incrementada conforme mudanças
- [ ] Status atualizado com emoji apropriado
- [ ] Índice de documentação atualizado
- [ ] Referências cruzadas verificadas

### **Comando de Verificação**
```bash
# Verificar documentos sem versionamento
grep -L "Versão:" Aplicação/documentações/*.md

# Verificar documentos desatualizados
grep -L "Última Atualização:" Aplicação/documentações/*.md
```

---

## 🎉 **Benefícios do Sistema**

### **Para Desenvolvedores**
- **Identificação clara** da versão mais recente
- **Histórico de mudanças** através de versionamento
- **Consistência** na documentação
- **Facilidade** para encontrar informações atualizadas

### **Para o Projeto**
- **Qualidade** da documentação
- **Manutenibilidade** dos documentos
- **Profissionalismo** na apresentação
- **Rastreabilidade** de mudanças

---

## 📖 **Resumo**

Este sistema de versionamento garante:

1. **Identificação clara** da versão mais recente
2. **Consistência** na documentação
3. **Rastreabilidade** de mudanças
4. **Qualidade** e manutenibilidade
5. **Profissionalismo** na apresentação

**Sempre siga estas regras ao criar ou modificar documentos!** 🚀
