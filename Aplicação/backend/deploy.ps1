# Script de Deploy para Produção - PowerShell
# PM AI MVP API

param(
    [switch]$SkipTests,
    [switch]$Force
)

# Configurar cores para output
$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    switch ($Level) {
        "ERROR" { Write-Host "[$timestamp] [ERROR] $Message" -ForegroundColor Red }
        "SUCCESS" { Write-Host "[$timestamp] [SUCCESS] $Message" -ForegroundColor Green }
        "WARNING" { Write-Host "[$timestamp] [WARNING] $Message" -ForegroundColor Yellow }
        default { Write-Host "[$timestamp] [INFO] $Message" -ForegroundColor Blue }
    }
}

Write-Log "🚀 Iniciando deploy para produção..."

# Verificar se Docker está instalado
try {
    $dockerVersion = docker --version
    Write-Log "Docker encontrado: $dockerVersion"
} catch {
    Write-Log "Docker não está instalado. Instale o Docker Desktop primeiro." "ERROR"
    exit 1
}

try {
    $composeVersion = docker-compose --version
    Write-Log "Docker Compose encontrado: $composeVersion"
} catch {
    Write-Log "Docker Compose não está instalado. Instale o Docker Compose primeiro." "ERROR"
    exit 1
}

# Verificar se arquivo .env existe
if (-not (Test-Path ".env")) {
    Write-Log "Arquivo .env não encontrado. Criando arquivo de exemplo..." "WARNING"
    @"
# Configurações de Produção
SECRET_KEY=your-super-secret-production-key-here-change-this
POSTGRES_PASSWORD=your-secure-postgres-password-here
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Log "Por favor, edite o arquivo .env com suas configurações antes de continuar." "WARNING"
    exit 1
}

# Parar containers existentes
Write-Log "Parando containers existentes..."
try {
    docker-compose -f docker-compose.prod.yml down
} catch {
    Write-Log "Nenhum container em execução para parar." "WARNING"
}

# Remover imagens antigas se Force estiver habilitado
if ($Force) {
    Write-Log "Removendo imagens antigas..."
    try {
        docker-compose -f docker-compose.prod.yml down --rmi all
    } catch {
        Write-Log "Nenhuma imagem para remover." "WARNING"
    }
}

# Construir novas imagens
Write-Log "Construindo imagens de produção..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Executar migrações do banco
Write-Log "Executando migrações do banco de dados..."
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
Write-Log "Iniciando serviços de produção..."
docker-compose -f docker-compose.prod.yml up -d

# Aguardar serviços ficarem prontos
Write-Log "Aguardando serviços ficarem prontos..."
Start-Sleep -Seconds 30

# Verificar saúde dos serviços
Write-Log "Verificando saúde dos serviços..."

# Verificar backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Log "Backend está funcionando!" "SUCCESS"
    } else {
        Write-Log "Backend retornou status: $($response.StatusCode)" "ERROR"
    }
} catch {
    Write-Log "Backend não está respondendo. Verifique os logs: docker-compose -f docker-compose.prod.yml logs backend" "ERROR"
}

# Verificar banco de dados
try {
    $dbCheck = docker-compose -f docker-compose.prod.yml exec -T db pg_isready -U pmapp -d pmdb
    if ($LASTEXITCODE -eq 0) {
        Write-Log "Banco de dados está funcionando!" "SUCCESS"
    } else {
        Write-Log "Banco de dados não está respondendo." "ERROR"
    }
} catch {
    Write-Log "Erro ao verificar banco de dados." "ERROR"
}

# Verificar Redis
try {
    $redisCheck = docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping
    if ($redisCheck -eq "PONG") {
        Write-Log "Redis está funcionando!" "SUCCESS"
    } else {
        Write-Log "Redis não está respondendo." "ERROR"
    }
} catch {
    Write-Log "Erro ao verificar Redis." "ERROR"
}

# Executar testes de integração se não for pulado
if (-not $SkipTests) {
    Write-Log "Executando testes de integração..."
    try {
        docker-compose -f docker-compose.prod.yml exec -T backend python -m pytest app/tests/test_integration/ --tb=no -q
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Todos os testes passaram!" "SUCCESS"
        } else {
            Write-Log "Alguns testes falharam. Verifique os logs para mais detalhes." "WARNING"
        }
    } catch {
        Write-Log "Erro ao executar testes." "WARNING"
    }
}

# Mostrar status final
Write-Log "Status dos serviços:"
docker-compose -f docker-compose.prod.yml ps

Write-Log "🎉 Deploy para produção concluído com sucesso!" "SUCCESS"
Write-Log "🌐 API disponível em: http://localhost:8000" "SUCCESS"
Write-Log "📊 Health check: http://localhost:8000/health" "SUCCESS"
Write-Log "📚 Documentação: http://localhost:8000/docs" "SUCCESS"

Write-Host ""
Write-Host "Para ver os logs em tempo real:" -ForegroundColor Cyan
Write-Host "docker-compose -f docker-compose.prod.yml logs -f" -ForegroundColor White
Write-Host ""
Write-Host "Para parar os serviços:" -ForegroundColor Cyan
Write-Host "docker-compose -f docker-compose.prod.yml down" -ForegroundColor White
