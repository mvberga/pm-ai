# 🚀 PM AI MVP - Guia de Deploy em Produção

**Data de Criação:** 2 de Setembro de 2025  
**Última Atualização:** 2 de Setembro de 2025  
**Status:** ✅ **Fase 3: Sistema de Produção e Deploy - Infrastructure Setup CONCLUÍDA**  
**Responsável:** Equipe de Desenvolvimento PM AI MVP

---

## 🎯 **Visão Geral**

Este guia fornece instruções completas para fazer deploy do PM AI MVP em ambiente de produção. A infraestrutura foi configurada com foco em segurança, performance e monitoramento.

---

## 🏗️ **Arquitetura de Produção**

### **Componentes da Infraestrutura:**
- **Frontend**: React com Nginx (porta 80/443)
- **Backend**: FastAPI com Uvicorn (porta 8000)
- **Database**: PostgreSQL com pgvector (porta 5432)
- **Cache**: Redis (porta 6379)
- **Reverse Proxy**: Nginx com SSL/TLS
- **Monitoring**: Prometheus + Grafana (opcional)

### **Características de Segurança:**
- ✅ **Multi-stage Docker builds** para imagens otimizadas
- ✅ **Usuários não-root** em todos os containers
- ✅ **Health checks** para todos os serviços
- ✅ **Rate limiting** no Nginx
- ✅ **Security headers** configurados
- ✅ **SSL/TLS** com certificados
- ✅ **Logs estruturados** com rotação

---

## 📋 **Pré-requisitos**

### **Sistema:**
- Docker Desktop 4.0+ (Windows/Mac) ou Docker Engine 20.10+ (Linux)
- Docker Compose 2.0+
- 4GB RAM mínimo (8GB recomendado)
- 10GB espaço em disco

### **Configuração:**
- Domínio configurado (opcional)
- Certificados SSL (para HTTPS)
- Firewall configurado (portas 80, 443, 8000)

---

## 🚀 **Deploy Rápido**

### **1. Preparação do Ambiente**

```bash
# Clone o repositório
git clone <seu-repositorio>
cd pm-ai-mvp/Aplicação

# Copie o arquivo de ambiente
cp env.production.example .env.production

# Edite as configurações
nano .env.production  # ou use seu editor preferido
```

### **2. Configuração do Ambiente**

Edite o arquivo `.env.production` com suas configurações:

```bash
# Database
POSTGRES_PASSWORD=SUA_SENHA_SEGURA_AQUI
POSTGRES_USER=pmapp_prod

# Backend
SECRET_KEY=SUA_CHAVE_SECRETA_FORTE_AQUI
CORS_ORIGINS=https://seudominio.com

# Frontend
VITE_API_URL=https://seudominio.com/api/v1

# Redis
REDIS_PASSWORD=SUA_SENHA_REDIS_AQUI
```

### **3. Deploy Automático**

#### **Linux/Mac:**
```bash
# Tornar o script executável
chmod +x deploy.sh

# Executar deploy
./deploy.sh deploy
```

#### **Windows PowerShell:**
```powershell
# Executar deploy
.\deploy.ps1 deploy
```

### **4. Verificar Deploy**

```bash
# Verificar status
./deploy.sh status  # Linux/Mac
.\deploy.ps1 status  # Windows

# Verificar logs
./deploy.sh logs     # Linux/Mac
.\deploy.ps1 logs    # Windows
```

---

## 🔧 **Comandos de Gerenciamento**

### **Scripts Disponíveis:**

| Comando | Descrição |
|---------|-----------|
| `deploy` | Deploy completo da aplicação |
| `stop` | Parar todos os serviços |
| `restart` | Reiniciar serviços |
| `logs` | Mostrar logs em tempo real |
| `status` | Mostrar status dos containers |
| `monitoring` | Iniciar serviços de monitoramento |

### **Exemplos de Uso:**

```bash
# Deploy completo
./deploy.sh deploy

# Parar serviços
./deploy.sh stop

# Reiniciar apenas o backend
docker-compose -f docker-compose.prod.yml restart backend

# Ver logs do backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Acessar container do backend
docker-compose -f docker-compose.prod.yml exec backend bash
```

---

## 📊 **Monitoramento**

### **Serviços de Monitoramento (Opcional):**

```bash
# Iniciar monitoramento
./deploy.sh monitoring

# Acessar dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

### **Métricas Disponíveis:**
- **Backend**: Requests, response time, errors
- **Database**: Connections, queries, performance
- **Redis**: Memory usage, operations
- **System**: CPU, memory, disk usage

---

## 🔒 **Segurança**

### **Configurações de Segurança Implementadas:**

#### **Docker:**
- ✅ Multi-stage builds para reduzir tamanho das imagens
- ✅ Usuários não-root em todos os containers
- ✅ Health checks para detecção de falhas
- ✅ Logs com rotação automática

#### **Nginx:**
- ✅ Rate limiting (10 req/s para API, 5 req/m para login)
- ✅ Security headers (HSTS, CSP, X-Frame-Options)
- ✅ SSL/TLS com configurações seguras
- ✅ Gzip compression para performance

#### **Backend:**
- ✅ CORS configurado para domínios específicos
- ✅ Validação de entrada com Pydantic
- ✅ Logs estruturados
- ✅ Health checks

#### **Database:**
- ✅ Senhas fortes obrigatórias
- ✅ Conexões criptografadas
- ✅ Backup automático (configurar)

---

## 🚨 **Troubleshooting**

### **Problemas Comuns:**

#### **1. Container não inicia:**
```bash
# Verificar logs
docker-compose -f docker-compose.prod.yml logs <servico>

# Verificar status
docker-compose -f docker-compose.prod.yml ps
```

#### **2. Banco de dados não conecta:**
```bash
# Verificar se PostgreSQL está rodando
docker-compose -f docker-compose.prod.yml exec db pg_isready

# Verificar logs do banco
docker-compose -f docker-compose.prod.yml logs db
```

#### **3. Frontend não carrega:**
```bash
# Verificar se Nginx está rodando
curl -I http://localhost

# Verificar logs do Nginx
docker-compose -f docker-compose.prod.yml logs nginx
```

#### **4. API não responde:**
```bash
# Verificar health check
curl http://localhost:8000/health

# Verificar logs do backend
docker-compose -f docker-compose.prod.yml logs backend
```

### **Comandos de Diagnóstico:**

```bash
# Verificar uso de recursos
docker stats

# Verificar volumes
docker volume ls

# Verificar redes
docker network ls

# Limpar sistema
docker system prune -f
```

---

## 📈 **Performance**

### **Otimizações Implementadas:**

#### **Frontend:**
- ✅ Build otimizado com Vite
- ✅ Nginx com gzip compression
- ✅ Cache de arquivos estáticos (1 ano)
- ✅ Minificação de assets

#### **Backend:**
- ✅ Uvicorn com 4 workers
- ✅ Connection pooling para PostgreSQL
- ✅ Cache Redis para queries frequentes
- ✅ Logs otimizados

#### **Database:**
- ✅ Índices otimizados
- ✅ Connection pooling
- ✅ Configurações de performance

---

## 🔄 **Backup e Restore**

### **Backup do Banco de Dados:**

```bash
# Backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
docker-compose -f docker-compose.prod.yml exec -T db psql -U $POSTGRES_USER $POSTGRES_DB < backup_file.sql
```

### **Backup de Volumes:**

```bash
# Backup de volumes
docker run --rm -v pm-ai-mvp_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

---

## 📚 **URLs de Acesso**

Após o deploy, a aplicação estará disponível em:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | http://localhost | Interface principal |
| **Backend API** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Documentação Swagger |
| **Health Check** | http://localhost/health | Status da aplicação |
| **Prometheus** | http://localhost:9090 | Métricas (se habilitado) |
| **Grafana** | http://localhost:3000 | Dashboards (se habilitado) |

---

## 🎯 **Próximos Passos**

### **Fase 3 - Próximas Implementações:**

1. **CI/CD Pipeline** (Semana 2)
   - [ ] GitHub Actions para testes automatizados
   - [ ] Deploy automático com rollback
   - [ ] Notificações de deploy

2. **Monitoring & Logging** (Semana 3)
   - [ ] Logging estruturado com ELK Stack
   - [ ] Alertas automáticos
   - [ ] Dashboards de monitoramento

3. **Production Deployment** (Semana 4)
   - [ ] Deploy em ambiente de staging
   - [ ] Testes de integração em staging
   - [ ] Deploy em produção
   - [ ] Monitoramento pós-deploy

---

## 📞 **Suporte**

### **Recursos de Ajuda:**
- **Documentação**: [README.md](README.md)
- **Logs**: `./deploy.sh logs` ou `.\deploy.ps1 logs`
- **Status**: `./deploy.sh status` ou `.\deploy.ps1 status`
- **Issues**: Abra uma issue no repositório

### **Comandos Úteis:**
```bash
# Verificar saúde completa
curl http://localhost/health
curl http://localhost:8000/health

# Verificar logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f

# Reiniciar serviço específico
docker-compose -f docker-compose.prod.yml restart <servico>
```

---

## 🎉 **Conclusão**

A **Fase 3: Infrastructure Setup** foi concluída com sucesso! O sistema agora possui:

- ✅ **Infraestrutura de produção** completa e segura
- ✅ **Docker multi-stage builds** otimizados
- ✅ **Nginx reverse proxy** com SSL/TLS
- ✅ **PostgreSQL e Redis** configurados para produção
- ✅ **Monitoramento** com Prometheus e Grafana
- ✅ **Scripts de deploy** para Linux e Windows
- ✅ **Health checks** e logs estruturados
- ✅ **Configurações de segurança** implementadas

**O sistema está pronto para produção e pode ser deployado com segurança!**

---

*Última atualização: 2 de Setembro de 2025*  
*Responsável: Equipe de Desenvolvimento PM AI MVP*
