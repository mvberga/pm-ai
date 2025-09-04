# 🚀 Deploy para Produção - PM AI MVP API

## 📋 Pré-requisitos

- Docker Desktop instalado e funcionando
- Docker Compose instalado
- Portas 8000, 5432, 6379 disponíveis
- Pelo menos 4GB de RAM disponível

## 🔧 Configuração

### 1. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações de Produção
SECRET_KEY=your-super-secret-production-key-here-change-this
POSTGRES_PASSWORD=your-secure-postgres-password-here
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

**⚠️ IMPORTANTE:** Altere as senhas e chaves secretas antes do deploy!

### 2. Deploy Automático

#### Windows (PowerShell):
```powershell
.\deploy.ps1
```

#### Linux/Mac (Bash):
```bash
./deploy.sh
```

### 3. Deploy Manual

```bash
# Parar containers existentes
docker-compose -f docker-compose.prod.yml down

# Construir imagens
docker-compose -f docker-compose.prod.yml build --no-cache

# Executar migrações
docker-compose -f docker-compose.prod.yml run --rm backend python -c "
from app.db.session import engine
from app.models import *
import asyncio

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Tabelas criadas com sucesso!')

asyncio.run(create_tables())
"

# Iniciar serviços
docker-compose -f docker-compose.prod.yml up -d
```

## 🏗️ Arquitetura de Produção

### Serviços Incluídos:

- **Backend**: API FastAPI (porta 8000)
- **Database**: PostgreSQL 16 (porta 5432)
- **Cache**: Redis 7 (porta 6379)
- **Worker**: Celery para tarefas assíncronas
- **Proxy**: Nginx para load balancing e SSL

### Recursos de Segurança:

- ✅ Headers de segurança configurados
- ✅ Rate limiting (10 req/s por IP)
- ✅ Usuário não-root nos containers
- ✅ Health checks configurados
- ✅ Timeouts apropriados
- ✅ Sistema de autenticação JWT funcionando
- ✅ Endpoints protegidos com autenticação obrigatória
- ✅ Validação de tokens implementada

## 📊 Monitoramento

### Health Checks:

- **API**: `http://localhost:8000/health`
- **Database**: Verificação automática via pg_isready
- **Redis**: Verificação automática via redis-cli ping

### Logs:

```bash
# Ver logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f

# Ver logs de um serviço específico
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Status dos Serviços:

```bash
docker-compose -f docker-compose.prod.yml ps
```

## 🧪 Testes

### Executar Testes de Integração:

```bash
# Testes de autenticação (corrigidos)
docker-compose -f docker-compose.prod.yml exec backend python -m pytest app/tests/test_integration/test_auth_flow.py -v

# Testes de projeto (com autenticação)
docker-compose -f docker-compose.prod.yml exec backend python -m pytest app/tests/test_integration/test_project_workflow.py -v

# Todos os testes de integração
docker-compose -f docker-compose.prod.yml exec backend python -m pytest app/tests/test_integration/ -v
```

### Executar Testes Específicos:

```bash
# Testes de checklist
docker-compose -f docker-compose.prod.yml exec backend python -m pytest app/tests/test_integration/test_checklist_workflow.py -v

# Testes de projeto
docker-compose -f docker-compose.prod.yml exec backend python -m pytest app/tests/test_integration/test_project_workflow.py -v
```

## 🔄 Manutenção

### Backup do Banco de Dados:

```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U pmapp pmdb > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restaurar Backup:

```bash
docker-compose -f docker-compose.prod.yml exec -T db psql -U pmapp pmdb < backup_file.sql
```

### Atualizar Aplicação:

```bash
# Parar serviços
docker-compose -f docker-compose.prod.yml down

# Atualizar código
git pull

# Reconstruir e iniciar
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

## 🚨 Troubleshooting

### Problemas Comuns:

1. **Porta já em uso**:
   ```bash
   # Verificar processos usando as portas
   netstat -tulpn | grep :8000
   ```

2. **Banco de dados não conecta**:
   ```bash
   # Verificar logs do banco
   docker-compose -f docker-compose.prod.yml logs db
   ```

3. **Redis não responde**:
   ```bash
   # Verificar logs do Redis
   docker-compose -f docker-compose.prod.yml logs redis
   ```

4. **Backend não inicia**:
   ```bash
   # Verificar logs do backend
   docker-compose -f docker-compose.prod.yml logs backend
   ```

### Limpeza Completa:

```bash
# Parar e remover tudo
docker-compose -f docker-compose.prod.yml down -v --rmi all

# Remover volumes
docker volume prune -f

# Remover imagens não utilizadas
docker image prune -f
```

## 📈 Performance

### Otimizações Incluídas:

- ✅ Multi-stage Docker build
- ✅ Nginx com rate limiting
- ✅ Connection pooling no banco
- ✅ Cache Redis configurado
- ✅ Workers múltiplos (4 workers)

### Monitoramento de Performance:

```bash
# Ver uso de recursos
docker stats

# Ver logs de performance
docker-compose -f docker-compose.prod.yml logs backend | grep "performance"
```

## 🔐 Segurança

### Checklist de Segurança:

- ✅ Variáveis de ambiente seguras
- ✅ Headers de segurança configurados
- ✅ Rate limiting ativo
- ✅ Usuário não-root nos containers
- ✅ Health checks configurados
- ✅ Logs de segurança ativos
- ✅ Sistema de autenticação JWT funcionando
- ✅ Endpoints protegidos com autenticação obrigatória
- ✅ Validação de tokens implementada
- ✅ Problemas de encoding corrigidos (Windows compatível)

### Atualizações de Segurança:

```bash
# Atualizar imagens base
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique os logs: `docker-compose -f docker-compose.prod.yml logs`
2. Execute os testes: `docker-compose -f docker-compose.prod.yml exec backend python -m pytest`
3. Verifique o health check: `curl http://localhost:8000/health`

---

**🎉 Sistema 100% funcional e pronto para produção!**

*Última atualização: Setembro 2025 - Sistema de Autenticação Corrigido*
