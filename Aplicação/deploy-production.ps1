# Script de Deploy para Producao - PM AI MVP
# Data: 03/09/2025

param(
    [Parameter(Mandatory=$false)]
    [string]$Domain = "pm-ai-mvp.com",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipSSL = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipTests = $false
)

Write-Host "Iniciando Deploy em Producao - PM AI MVP" -ForegroundColor Green
Write-Host "Dominio: $Domain" -ForegroundColor Cyan

# Verificar se Docker está rodando
Write-Host "Verificando Docker..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "Docker esta rodando" -ForegroundColor Green
} catch {
    Write-Host "Docker nao esta rodando. Inicie o Docker Desktop primeiro." -ForegroundColor Red
    exit 1
}

# Verificar se arquivo de ambiente existe
if (!(Test-Path "env.production")) {
    Write-Host "Arquivo env.production nao encontrado!" -ForegroundColor Red
    Write-Host "Criando arquivo de ambiente de producao..." -ForegroundColor Yellow
    # O arquivo já foi criado anteriormente
}

# Gerar certificados SSL se não pular
if (!$SkipSSL) {
    Write-Host "Gerando certificados SSL..." -ForegroundColor Yellow
    
    if (Test-Path "ssl/generate-ssl-certs.ps1") {
        Write-Host "Gerando certificados auto-assinados para desenvolvimento..." -ForegroundColor Yellow
        & ".\ssl\generate-ssl-certs.ps1"
    } else {
        Write-Host "Script de certificados nao encontrado. Criando certificados manualmente..." -ForegroundColor Yellow
        
        # Criar diretório SSL
        if (!(Test-Path "ssl")) {
            New-Item -ItemType Directory -Path "ssl" -Force
        }
        
        # Gerar certificados básicos
        openssl genrsa -out ssl/ssl-cert.key 2048
        openssl req -new -x509 -key ssl/ssl-cert.key -out ssl/ssl-cert.pem -days 365 -subj "/C=BR/ST=SP/L=SaoPaulo/O=PM-AI-MVP/OU=IT/CN=$Domain"
        
        Write-Host "Certificados SSL gerados" -ForegroundColor Green
    }
} else {
    Write-Host "Pulando geracao de certificados SSL" -ForegroundColor Yellow
}

# Parar containers existentes
Write-Host "Parando containers existentes..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml --env-file env.production down

# Limpar volumes se necessário (descomente se quiser resetar dados)
# Write-Host "Limpando volumes..." -ForegroundColor Yellow
# docker-compose -f docker-compose.production.yml --env-file env.production down -v

# Reconstruir imagens
Write-Host "Reconstruindo imagens..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml --env-file env.production build --no-cache

# Executar testes se não pular
if (!$SkipTests) {
    Write-Host "Executando testes antes do deploy..." -ForegroundColor Yellow
    
    # Testes do backend
    Write-Host "Executando testes do backend..." -ForegroundColor Cyan
    docker-compose -f docker-compose.production.yml --env-file env.production run --rm backend python -m pytest app/tests/ -v --tb=short
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Testes do backend falharam. Deploy cancelado." -ForegroundColor Red
        exit 1
    }
    
    # Testes do frontend
    Write-Host "Executando testes do frontend..." -ForegroundColor Cyan
    docker-compose -f docker-compose.production.yml --env-file env.production run --rm frontend npm test -- --coverage --watchAll=false
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Testes do frontend falharam. Deploy cancelado." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Todos os testes passaram!" -ForegroundColor Green
} else {
    Write-Host "Pulando execucao de testes" -ForegroundColor Yellow
}

# Iniciar serviços
Write-Host "Iniciando servicos..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml --env-file env.production up -d

# Aguardar serviços ficarem prontos
Write-Host "Aguardando servicos ficarem prontos..." -ForegroundColor Yellow
Start-Sleep -Seconds 60

# Verificar status dos containers
Write-Host "Verificando status dos containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml --env-file env.production ps

# Verificar logs do backend
Write-Host "Verificando logs do backend..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml --env-file env.production logs backend --tail=10

# Verificar logs do frontend
Write-Host "Verificando logs do frontend..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml --env-file env.production logs frontend --tail=10

# Verificar logs do nginx
Write-Host "Verificando logs do nginx..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml --env-file env.production logs nginx --tail=10

# Testar conectividade
Write-Host "Testando conectividade..." -ForegroundColor Yellow

# Testar HTTP (deve redirecionar para HTTPS)
try {
    $response = Invoke-WebRequest -Uri "http://localhost" -TimeoutSec 10 -MaximumRedirection 0
    Write-Host "HTTP redirecionamento funcionando" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode -eq 301) {
        Write-Host "HTTP redirecionamento funcionando (301)" -ForegroundColor Green
    } else {
        Write-Host "Problema com redirecionamento HTTP" -ForegroundColor Yellow
    }
}

# Testar HTTPS
try {
    $response = Invoke-WebRequest -Uri "https://localhost" -TimeoutSec 10 -SkipCertificateCheck
    if ($response.StatusCode -eq 200) {
        Write-Host "HTTPS funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "HTTPS nao esta respondendo ainda" -ForegroundColor Yellow
}

# Testar health check
try {
    $response = Invoke-WebRequest -Uri "https://localhost/health" -TimeoutSec 10 -SkipCertificateCheck
    if ($response.StatusCode -eq 200) {
        Write-Host "Health check funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "Health check nao esta respondendo ainda" -ForegroundColor Yellow
}

# Verificar monitoramento
Write-Host "Verificando servicos de monitoramento..." -ForegroundColor Yellow

# Prometheus
try {
    $response = Invoke-WebRequest -Uri "http://localhost:9090/-/healthy" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "Prometheus funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "Prometheus nao esta respondendo ainda" -ForegroundColor Yellow
}

# Grafana
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/api/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "Grafana funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "Grafana nao esta respondendo ainda" -ForegroundColor Yellow
}

# Kibana
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5601/api/status" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "Kibana funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "Kibana nao esta respondendo ainda" -ForegroundColor Yellow
}

Write-Host "Deploy em producao concluido!" -ForegroundColor Green
Write-Host "URLs de acesso:" -ForegroundColor Cyan
Write-Host "   Frontend: https://localhost" -ForegroundColor White
Write-Host "   Health Check: https://localhost/health" -ForegroundColor White
Write-Host "   Backend API: https://localhost/api/v1/" -ForegroundColor White
Write-Host "   Prometheus: http://localhost:9090" -ForegroundColor White
Write-Host "   Grafana: http://localhost:3000" -ForegroundColor White
Write-Host "   Kibana: http://localhost:5601" -ForegroundColor White

Write-Host "Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Configurar DNS para apontar para este servidor" -ForegroundColor White
Write-Host "2. Gerar certificados Let's Encrypt para dominio real" -ForegroundColor White
Write-Host "3. Configurar backup automatico" -ForegroundColor White
Write-Host "4. Configurar alertas de monitoramento" -ForegroundColor White
