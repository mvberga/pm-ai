#!/bin/bash

# ===========================================
# SCRIPT DE DEPLOY - PM AI MVP
# ===========================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se Docker está instalado
check_docker() {
    log "Verificando se Docker está instalado..."
    if ! command -v docker &> /dev/null; then
        error "Docker não está instalado. Por favor, instale o Docker primeiro."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
        exit 1
    fi
    
    success "Docker e Docker Compose estão instalados"
}

# Verificar se arquivo de ambiente existe
check_env() {
    log "Verificando arquivo de ambiente..."
    if [ ! -f ".env.production" ]; then
        warning "Arquivo .env.production não encontrado. Copiando do exemplo..."
        cp env.production.example .env.production
        warning "IMPORTANTE: Edite o arquivo .env.production com suas configurações antes de continuar!"
        read -p "Pressione Enter para continuar após editar o arquivo..."
    fi
    success "Arquivo de ambiente encontrado"
}

# Parar containers existentes
stop_containers() {
    log "Parando containers existentes..."
    docker-compose -f docker-compose.prod.yml down --remove-orphans || true
    success "Containers parados"
}

# Limpar imagens antigas
cleanup_images() {
    log "Limpando imagens antigas..."
    docker image prune -f || true
    success "Imagens antigas removidas"
}

# Build das imagens
build_images() {
    log "Construindo imagens Docker..."
    docker-compose -f docker-compose.prod.yml build --no-cache
    success "Imagens construídas com sucesso"
}

# Iniciar serviços
start_services() {
    log "Iniciando serviços..."
    docker-compose -f docker-compose.prod.yml up -d
    success "Serviços iniciados"
}

# Aguardar serviços ficarem prontos
wait_for_services() {
    log "Aguardando serviços ficarem prontos..."
    
    # Aguardar banco de dados
    log "Aguardando banco de dados..."
    timeout 60 bash -c 'until docker-compose -f docker-compose.prod.yml exec -T db pg_isready -U ${POSTGRES_USER:-pmapp_prod}; do sleep 2; done'
    
    # Aguardar Redis
    log "Aguardando Redis..."
    timeout 30 bash -c 'until docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping; do sleep 2; done'
    
    # Aguardar backend
    log "Aguardando backend..."
    timeout 60 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done'
    
    # Aguardar frontend
    log "Aguardando frontend..."
    timeout 30 bash -c 'until curl -f http://localhost:80/health; do sleep 2; done'
    
    success "Todos os serviços estão prontos"
}

# Executar migrações
run_migrations() {
    log "Executando migrações do banco de dados..."
    docker-compose -f docker-compose.prod.yml exec -T backend python -m app.migrations.run_migration
    success "Migrações executadas"
}

# Verificar saúde dos serviços
health_check() {
    log "Verificando saúde dos serviços..."
    
    # Backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        success "Backend está saudável"
    else
        error "Backend não está respondendo"
        return 1
    fi
    
    # Frontend
    if curl -f http://localhost:80/health > /dev/null 2>&1; then
        success "Frontend está saudável"
    else
        error "Frontend não está respondendo"
        return 1
    fi
    
    success "Todos os serviços estão saudáveis"
}

# Mostrar status dos containers
show_status() {
    log "Status dos containers:"
    docker-compose -f docker-compose.prod.yml ps
    
    echo ""
    log "URLs de acesso:"
    echo "  - Frontend: http://localhost"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Health Check: http://localhost/health"
    
    if docker-compose -f docker-compose.prod.yml ps | grep -q "prometheus"; then
        echo "  - Prometheus: http://localhost:9090"
    fi
    
    if docker-compose -f docker-compose.prod.yml ps | grep -q "grafana"; then
        echo "  - Grafana: http://localhost:3000"
    fi
}

# Função principal
main() {
    log "Iniciando deploy do PM AI MVP..."
    
    check_docker
    check_env
    stop_containers
    cleanup_images
    build_images
    start_services
    wait_for_services
    run_migrations
    health_check
    show_status
    
    success "Deploy concluído com sucesso!"
    log "A aplicação está disponível em http://localhost"
}

# Verificar argumentos
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "stop")
        log "Parando todos os serviços..."
        docker-compose -f docker-compose.prod.yml down
        success "Serviços parados"
        ;;
    "restart")
        log "Reiniciando serviços..."
        docker-compose -f docker-compose.prod.yml restart
        success "Serviços reiniciados"
        ;;
    "logs")
        docker-compose -f docker-compose.prod.yml logs -f
        ;;
    "status")
        show_status
        ;;
    "monitoring")
        log "Iniciando serviços de monitoramento..."
        docker-compose -f docker-compose.prod.yml --profile monitoring up -d
        success "Serviços de monitoramento iniciados"
        ;;
    *)
        echo "Uso: $0 {deploy|stop|restart|logs|status|monitoring}"
        echo ""
        echo "Comandos disponíveis:"
        echo "  deploy     - Deploy completo da aplicação"
        echo "  stop       - Parar todos os serviços"
        echo "  restart    - Reiniciar serviços"
        echo "  logs       - Mostrar logs em tempo real"
        echo "  status     - Mostrar status dos containers"
        echo "  monitoring - Iniciar serviços de monitoramento"
        exit 1
        ;;
esac
