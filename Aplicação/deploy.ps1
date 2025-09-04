# ===========================================
# SCRIPT DE DEPLOY - PM AI MVP (PowerShell)
# ===========================================

param(
    [Parameter(Position=0)]
    [ValidateSet("deploy", "stop", "restart", "logs", "status", "monitoring")]
    [string]$Action = "deploy"
)

# Função para logging
function Write-Log {
    param([string]$Message)
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Verificar se Docker está instalado
function Test-Docker {
    Write-Log "Verificando se Docker está instalado..."
    
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Error "Docker não está instalado. Por favor, instale o Docker Desktop primeiro."
        exit 1
    }
    
    if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Error "Docker Compose não está instalado. Por favor, instale o Docker Desktop primeiro."
        exit 1
    }
    
    Write-Success "Docker e Docker Compose estão instalados"
}

# Verificar se arquivo de ambiente existe
function Test-EnvironmentFile {
    Write-Log "Verificando arquivo de ambiente..."
    
    if (-not (Test-Path ".env.production")) {
        Write-Warning "Arquivo .env.production não encontrado. Copiando do exemplo..."
        Copy-Item "env.production.example" ".env.production"
        Write-Warning "IMPORTANTE: Edite o arquivo .env.production com suas configurações antes de continuar!"
        Read-Host "Pressione Enter para continuar após editar o arquivo"
    }
    
    Write-Success "Arquivo de ambiente encontrado"
}

# Parar containers existentes
function Stop-Containers {
    Write-Log "Parando containers existentes..."
    try {
        docker-compose -f docker-compose.prod.yml down --remove-orphans
    } catch {
        # Ignorar erros se não houver containers rodando
    }
    Write-Success "Containers parados"
}

# Limpar imagens antigas
function Clear-OldImages {
    Write-Log "Limpando imagens antigas..."
    try {
        docker image prune -f
    } catch {
        # Ignorar erros
    }
    Write-Success "Imagens antigas removidas"
}

# Build das imagens
function Build-Images {
    Write-Log "Construindo imagens Docker..."
    docker-compose -f docker-compose.prod.yml build --no-cache
    Write-Success "Imagens construídas com sucesso"
}

# Iniciar serviços
function Start-Services {
    Write-Log "Iniciando serviços..."
    docker-compose -f docker-compose.prod.yml up -d
    Write-Success "Serviços iniciados"
}

# Aguardar serviços ficarem prontos
function Wait-ForServices {
    Write-Log "Aguardando serviços ficarem prontos..."
    
    # Aguardar banco de dados
    Write-Log "Aguardando banco de dados..."
    $timeout = 60
    $elapsed = 0
    do {
        Start-Sleep -Seconds 2
        $elapsed += 2
        try {
            $result = docker-compose -f docker-compose.prod.yml exec -T db pg_isready -U $env:POSTGRES_USER
            if ($LASTEXITCODE -eq 0) { break }
        } catch {
            # Continuar tentando
        }
    } while ($elapsed -lt $timeout)
    
    # Aguardar Redis
    Write-Log "Aguardando Redis..."
    $timeout = 30
    $elapsed = 0
    do {
        Start-Sleep -Seconds 2
        $elapsed += 2
        try {
            $result = docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping
            if ($LASTEXITCODE -eq 0) { break }
        } catch {
            # Continuar tentando
        }
    } while ($elapsed -lt $timeout)
    
    # Aguardar backend
    Write-Log "Aguardando backend..."
    $timeout = 60
    $elapsed = 0
    do {
        Start-Sleep -Seconds 2
        $elapsed += 2
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) { break }
        } catch {
            # Continuar tentando
        }
    } while ($elapsed -lt $timeout)
    
    # Aguardar frontend
    Write-Log "Aguardando frontend..."
    $timeout = 30
    $elapsed = 0
    do {
        Start-Sleep -Seconds 2
        $elapsed += 2
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:80/health" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) { break }
        } catch {
            # Continuar tentando
        }
    } while ($elapsed -lt $timeout)
    
    Write-Success "Todos os serviços estão prontos"
}

# Executar migrações
function Invoke-Migrations {
    Write-Log "Executando migrações do banco de dados..."
    docker-compose -f docker-compose.prod.yml exec -T backend python -m app.migrations.run_migration
    Write-Success "Migrações executadas"
}

# Verificar saúde dos serviços
function Test-Health {
    Write-Log "Verificando saúde dos serviços..."
    
    # Backend
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Success "Backend está saudável"
        } else {
            Write-Error "Backend não está respondendo corretamente"
            return $false
        }
    } catch {
        Write-Error "Backend não está respondendo"
        return $false
    }
    
    # Frontend
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:80/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Success "Frontend está saudável"
        } else {
            Write-Error "Frontend não está respondendo corretamente"
            return $false
        }
    } catch {
        Write-Error "Frontend não está respondendo"
        return $false
    }
    
    Write-Success "Todos os serviços estão saudáveis"
    return $true
}

# Mostrar status dos containers
function Show-Status {
    Write-Log "Status dos containers:"
    docker-compose -f docker-compose.prod.yml ps
    
    Write-Host ""
    Write-Log "URLs de acesso:"
    Write-Host "  - Frontend: http://localhost" -ForegroundColor Cyan
    Write-Host "  - Backend API: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "  - Health Check: http://localhost/health" -ForegroundColor Cyan
    
    $containers = docker-compose -f docker-compose.prod.yml ps
    if ($containers -match "prometheus") {
        Write-Host "  - Prometheus: http://localhost:9090" -ForegroundColor Cyan
    }
    
    if ($containers -match "grafana") {
        Write-Host "  - Grafana: http://localhost:3000" -ForegroundColor Cyan
    }
}

# Função principal
function Start-Deploy {
    Write-Log "Iniciando deploy do PM AI MVP..."
    
    Test-Docker
    Test-EnvironmentFile
    Stop-Containers
    Clear-OldImages
    Build-Images
    Start-Services
    Wait-ForServices
    Invoke-Migrations
    if (Test-Health) {
        Show-Status
        Write-Success "Deploy concluído com sucesso!"
        Write-Log "A aplicação está disponível em http://localhost"
    } else {
        Write-Error "Deploy falhou - alguns serviços não estão saudáveis"
        exit 1
    }
}

# Executar ação baseada no parâmetro
switch ($Action) {
    "deploy" {
        Start-Deploy
    }
    "stop" {
        Write-Log "Parando todos os serviços..."
        docker-compose -f docker-compose.prod.yml down
        Write-Success "Serviços parados"
    }
    "restart" {
        Write-Log "Reiniciando serviços..."
        docker-compose -f docker-compose.prod.yml restart
        Write-Success "Serviços reiniciados"
    }
    "logs" {
        docker-compose -f docker-compose.prod.yml logs -f
    }
    "status" {
        Show-Status
    }
    "monitoring" {
        Write-Log "Iniciando serviços de monitoramento..."
        docker-compose -f docker-compose.prod.yml --profile monitoring up -d
        Write-Success "Serviços de monitoramento iniciados"
    }
    default {
        Write-Host "Uso: .\deploy.ps1 {deploy|stop|restart|logs|status|monitoring}"
        Write-Host ""
        Write-Host "Comandos disponíveis:"
        Write-Host "  deploy     - Deploy completo da aplicação"
        Write-Host "  stop       - Parar todos os serviços"
        Write-Host "  restart    - Reiniciar serviços"
        Write-Host "  logs       - Mostrar logs em tempo real"
        Write-Host "  status     - Mostrar status dos containers"
        Write-Host "  monitoring - Iniciar serviços de monitoramento"
        exit 1
    }
}
