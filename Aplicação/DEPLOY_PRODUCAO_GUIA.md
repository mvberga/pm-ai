# 🚀 Guia de Deploy em Produção - PM AI MVP

**Data:** 03/09/2025  
**Status:** 🔄 Em Andamento  
**Responsável:** Equipe de Desenvolvimento

---

## 📋 **Status Atual**

### ✅ **Concluído:**
- ✅ Análise do status de staging
- ✅ Correção das dependências do backend (pandas, reportlab, python-jose)
- ✅ Criação do arquivo de ambiente de staging (`env.staging`)
- ✅ Criação do script de deploy automatizado (`deploy-staging.ps1`)
- ✅ Configuração do Nginx para staging (sem SSL)

### ✅ **Concluído:**
- ✅ Deploy em staging (CONCLUÍDO COM SUCESSO)
- ✅ Docker Desktop iniciado
- ✅ Todos os containers funcionando
- ✅ Sistema estável em staging

### ⏳ **Próximos Passos:**
- ⏳ Configurar SSL/TLS para produção
- ⏳ Deploy em produção com monitoramento
- ⏳ Executar testes de carga

---

## 🐳 **Pré-requisitos**

### **1. Docker Desktop**
- **Status:** ✅ Funcionando perfeitamente
- **Versão:** Docker Desktop 4.44.3 (202357)
- **Verificação:** `docker version` - OK

### **2. Arquivos de Configuração**
- ✅ `env.staging` - Variáveis de ambiente para staging
- ✅ `docker-compose.staging.yml` - Configuração dos serviços
- ✅ `nginx/nginx-staging.conf` - Configuração do Nginx
- ✅ `deploy-staging.ps1` - Script de deploy automatizado

---

## 🚀 **Passos para Deploy**

### **Passo 1: ✅ Docker Desktop (CONCLUÍDO)**
```powershell
# Docker está funcionando perfeitamente
docker version
# ✅ Client: Version 28.3.2
# ✅ Server: Docker Desktop 4.44.3 (202357)
```

### **Passo 2: ✅ Deploy em Staging (CONCLUÍDO)**
```powershell
# Deploy executado com sucesso
cd Aplicação
.\deploy-staging.ps1
# ✅ Todos os containers funcionando
# ✅ Sistema estável em staging
```

### **Passo 3: ✅ Verificar Status (CONCLUÍDO)**
```powershell
# Status dos containers - TODOS HEALTHY
docker-compose -f docker-compose.staging.yml --env-file env.staging ps
# ✅ pm-ai-backend-staging    Healthy
# ✅ pm-ai-db-staging         Healthy  
# ✅ pm-ai-frontend-staging   Healthy
# ✅ pm-ai-nginx-staging      Healthy
# ✅ pm-ai-redis-staging      Healthy
```

### **Passo 4: ✅ Testar Conectividade (CONCLUÍDO)**
```powershell
# Frontend funcionando
Invoke-WebRequest -Uri "http://localhost/health"
# ✅ Status 200 - "healthy"

# Sistema estável e funcionando
```

---

## 🔧 **Troubleshooting**

### **Problema: Docker não está rodando**
**Erro:** `error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine"`
**Solução:**
1. Iniciar Docker Desktop
2. Aguardar inicialização completa
3. Verificar com `docker version`

### **Problema: Containers não iniciam**
**Possíveis causas:**
- Portas em uso (80, 443, 5432, 6379)
- Volumes com permissões incorretas
- Dependências faltando

**Soluções:**
```powershell
# Parar todos os containers
docker-compose -f docker-compose.staging.yml --env-file env.staging down

# Limpar volumes (cuidado: apaga dados)
docker-compose -f docker-compose.staging.yml --env-file env.staging down -v

# Reconstruir imagens
docker-compose -f docker-compose.staging.yml --env-file env.staging build --no-cache
```

### **Problema: Backend não responde**
**Verificações:**
1. Logs do backend: `docker-compose -f docker-compose.staging.yml --env-file env.staging logs backend`
2. Dependências: Verificar se pandas, reportlab, python-jose estão instalados
3. Banco de dados: Verificar se PostgreSQL está rodando

---

## 📊 **URLs de Acesso (Staging)**

- **Frontend:** http://localhost
- **Health Check:** http://localhost/health
- **Backend API:** http://localhost/api/v1/
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379
- **Prometheus:** http://localhost:9090 (opcional)
- **Grafana:** http://localhost:3000 (opcional)

---

## 🔒 **Configuração para Produção**

### **SSL/TLS**
- Configurar certificados SSL
- Atualizar `nginx.conf` para HTTPS
- Configurar redirecionamento HTTP → HTTPS

### **Domínio**
- Configurar DNS
- Atualizar `CORS_ORIGINS` no arquivo de ambiente
- Configurar `VITE_API_URL`

### **Monitoramento**
- ELK Stack para logs
- Prometheus + Grafana para métricas
- Alertas configurados

---

## 📋 **Comandos Úteis**

```powershell
# Status dos containers
docker-compose -f docker-compose.staging.yml --env-file env.staging ps

# Logs de um serviço específico
docker-compose -f docker-compose.staging.yml --env-file env.staging logs [service]

# Parar todos os serviços
docker-compose -f docker-compose.staging.yml --env-file env.staging down

# Reiniciar um serviço específico
docker-compose -f docker-compose.staging.yml --env-file env.staging restart [service]

# Executar comandos dentro de um container
docker-compose -f docker-compose.staging.yml --env-file env.staging exec backend python -m pytest

# Verificar uso de recursos
docker stats
```

---

## 🎯 **Próximos Passos**

### **Imediato (CONCLUÍDO):**
1. ✅ Iniciar Docker Desktop
2. ✅ Executar deploy em staging
3. ✅ Verificar funcionamento
4. ✅ Executar testes de integração

### **Curto Prazo (Esta Semana):**
1. ⏳ Configurar SSL/TLS
2. ⏳ Deploy em produção
3. ⏳ Configurar monitoramento
4. ⏳ Executar testes de carga

### **Médio Prazo (Próximas Semanas):**
1. ⏳ Implementar funcionalidades avançadas
2. ⏳ Integração com IA (Gemini API)
3. ⏳ Sistema completo de gestão de projetos

---

## 📞 **Suporte**

Em caso de problemas:
1. Verificar logs dos containers
2. Consultar este guia de troubleshooting
3. Verificar documentação técnica
4. Contatar equipe de desenvolvimento

---

*Última atualização: 03/09/2025*  
*Responsável: Equipe de Desenvolvimento PM AI MVP*
