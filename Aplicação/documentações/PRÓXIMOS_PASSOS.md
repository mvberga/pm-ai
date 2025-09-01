# 🚀 Próximos Passos - PM AI MVP

##  **Status Atual: Backend 100% (Unit + Integração + Carga) e Frontend priorizando reestruturação com testes essenciais**

### ✅ **Concluído:**
- **Backend 100% funcional** (54 testes unitários passando)
- **Testes de performance** (6/6 testes passando)
- **API robusta** com CRUD completo
- **Infraestrutura sólida** e isolada

###  **Em Andamento:**
- **Reestruturação do Frontend** (camadas `src/api`, `src/types`, `src/ui`)
- **Manutenção de testes essenciais** (páginas principais e `PortfolioOverview` em estados base)
- **E2E (smoke) via Docker Compose** — execução sob demanda

## 🎯 **Próximos Passos (Prioridade Alta):**

### **1. Frontend — Reestruturação (SEMANA ATUAL E PRÓXIMA)**
- [ ] Criar camadas base:
  - `src/api/` (cliente + adaptadores)
  - `src/types/` (contratos com backend)
  - `src/ui/` (tokens/componentes base)
- [ ] Migrar `PortfolioOverview.tsx` para o novo padrão
- [ ] Manter testes essenciais nesta tela (carregando, erro, vazio, populado)
- [ ] Congelar expansão de cobertura neste ciclo (sem `coverageThreshold`)

### **2. Testes (mínimo necessário)**
- [ ] Manter testes de páginas principais (`ProjectsList`, `ProjectDetail`)
- [ ] Rodar 1–2 specs E2E “smoke” no compose para validar navegação e integração
- [ ] Adiar aumento de cobertura/branches até estabilizar a nova arquitetura

### **3. Consolidação (depois da migração das principais telas)**
- [ ] Retomar metas de cobertura (≥80% geral, branches ≥70–80%)
- [ ] Ampliar E2E real (2–4 fluxos completos)
- [ ] Casos negativos e de recuperação

## 📈 **Métricas de Progresso:**

| **Fase** | **Status** | **Progresso** | **Prazo** |
|----------|------------|---------------|-----------|
| **Backend** | ✅ Completo | 100% | Concluído |
| **Performance** | ✅ Completo | 100% | Concluído |
| **Integração** | ✅ Completo | 100% | Concluído |
| **Frontend** | 🔄 Reestruturação | Testes essenciais mantidos | Esta/Próxima semana |
| **E2E** | 🔄 Smoke sob demanda | 3 specs (mock) + 1 real | Após migração |

##  **Objetivos da Semana:**

### **Meta 1: Reestruturação do Frontend**
– **Ações**: Criar base `api/types/ui`, migrar `PortfolioOverview`, manter suíte verde

### **Meta 2: Sistema 100% Testado**
- **Backend**: ✅ 100%
- **Integração**: ✅ 100%
- **Frontend**: 🔄 Reestruturação com testes essenciais
- **E2E**: 🔄 Smoke sob demanda

##  **Riscos Identificados:**

### **Alto:**
- Divergência temporária entre UI antiga e nova (fase de transição)

### **Médio:**
- Ajustes de contrato de API durante migração
- Potenciais quebras visuais ao extrair componentes base

### **Baixo:**
- Testes de performance já estão estáveis
- Backend está 100% funcional

---

*Última atualização: 30/08/2025 (priorização de reestruturação do frontend)*
*Responsável: Equipe de Desenvolvimento PM AI MVP*
