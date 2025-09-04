#!/bin/bash

# Script de Deploy para Produção
# PM AI MVP API

set -e

echo "🚀 Iniciando deploy para produção..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    error "Docker não está instalado. Instale o Docker primeiro."
fi

if ! command -v docker-compose &> /dev/null; then
    error "Docker Compose não está instalado. Instale o Docker Compose primeiro."
fi

# Verificar se arquivo .env existe
if [ ! -f .env ]; then
    warning "Arquivo .env não encontrado. Criando arquivo de exemplo..."
    cat > .env << EOF
# Configurações de Produção
SECRET_KEY=your-super-secret-production-key-here-change-this
POSTGRES_PASSWORD=your-secure-postgres-password-here
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
EOF
    warning "Por favor, edite o arquivo .env com suas configurações antes de continuar."
    exit 1
fi

# Parar containers existentes
log "Parando containers existentes..."
docker-compose -f docker-compose.prod.yml down || true

# Remover imagens antigas
log "Removendo imagens antigas..."
docker-compose -f docker-compose.prod.yml down --rmi all || true

# Construir novas imagens
log "Construindo imagens de produção..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Executar migrações do banco
log "Executando migrações do banco de dados..."
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
log "Iniciando serviços de produção..."
docker-compose -f docker-compose.prod.yml up -d

# Aguardar serviços ficarem prontos
log "Aguardando serviços ficarem prontos..."
sleep 30

# Verificar saúde dos serviços
log "Verificando saúde dos serviços..."

# Verificar backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    success "Backend está funcionando!"
else
    error "Backend não está respondendo. Verifique os logs: docker-compose -f docker-compose.prod.yml logs backend"
fi

# Verificar banco de dados
if docker-compose -f docker-compose.prod.yml exec -T db pg_isready -U pmapp -d pmdb > /dev/null 2>&1; then
    success "Banco de dados está funcionando!"
else
    error "Banco de dados não está respondendo. Verifique os logs: docker-compose -f docker-compose.prod.yml logs db"
fi

# Verificar Redis
if docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
    success "Redis está funcionando!"
else
    error "Redis não está respondendo. Verifique os logs: docker-compose -f docker-compose.prod.yml logs redis"
fi

# Executar testes de integração
log "Executando testes de integração..."
if docker-compose -f docker-compose.prod.yml exec -T backend python -m pytest app/tests/test_integration/ --tb=no -q; then
    success "Todos os testes passaram!"
else
    warning "Alguns testes falharam. Verifique os logs para mais detalhes."
fi

# Mostrar status final
log "Status dos serviços:"
docker-compose -f docker-compose.prod.yml ps

success "🎉 Deploy para produção concluído com sucesso!"
success "🌐 API disponível em: http://localhost:8000"
success "📊 Health check: http://localhost:8000/health"
success "📚 Documentação: http://localhost:8000/docs"

echo ""
echo "Para ver os logs em tempo real:"
echo "docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "Para parar os serviços:"
echo "docker-compose -f docker-compose.prod.yml down"
