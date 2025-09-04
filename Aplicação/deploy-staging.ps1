# Script de Deploy para Staging - PM AI MVP
# Data: 03/09/2025

Write-Host "Iniciando Deploy em Staging - PM AI MVP" -ForegroundColor Green

# Verificar se Docker está rodando
Write-Host "Verificando Docker..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "Docker esta rodando" -ForegroundColor Green
} catch {
    Write-Host "Docker nao esta rodando. Inicie o Docker Desktop primeiro." -ForegroundColor Red
    exit 1
}

# Parar containers existentes
Write-Host "Parando containers existentes..." -ForegroundColor Yellow
docker-compose -f docker-compose.staging.yml --env-file env.staging down

# Limpar volumes se necessário (descomente se quiser resetar dados)
# Write-Host "Limpando volumes..." -ForegroundColor Yellow
# docker-compose -f docker-compose.staging.yml --env-file env.staging down -v

# Reconstruir imagens
Write-Host "Reconstruindo imagens..." -ForegroundColor Yellow
docker-compose -f docker-compose.staging.yml --env-file env.staging build --no-cache

# Iniciar serviços
Write-Host "Iniciando servicos..." -ForegroundColor Yellow
docker-compose -f docker-compose.staging.yml --env-file env.staging up -d

# Aguardar serviços ficarem prontos
Write-Host "Aguardando servicos ficarem prontos..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Verificar status dos containers
Write-Host "Verificando status dos containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.staging.yml --env-file env.staging ps

# Verificar logs do backend
Write-Host "Verificando logs do backend..." -ForegroundColor Yellow
docker-compose -f docker-compose.staging.yml --env-file env.staging logs backend --tail=20

# Testar conectividade
Write-Host "Testando conectividade..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "Frontend esta respondendo" -ForegroundColor Green
    }
} catch {
    Write-Host "Frontend nao esta respondendo ainda" -ForegroundColor Yellow
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost/api/v1/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "Backend esta respondendo" -ForegroundColor Green
    }
} catch {
    Write-Host "Backend nao esta respondendo ainda" -ForegroundColor Yellow
}

Write-Host "Deploy em staging concluido!" -ForegroundColor Green
Write-Host "URLs de acesso:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost" -ForegroundColor White
Write-Host "   Health Check: http://localhost/health" -ForegroundColor White
Write-Host "   Backend API: http://localhost/api/v1/" -ForegroundColor White

Write-Host "Comandos uteis:" -ForegroundColor Cyan
Write-Host "   Ver logs: docker-compose -f docker-compose.staging.yml --env-file env.staging logs [service]" -ForegroundColor White
Write-Host "   Parar: docker-compose -f docker-compose.staging.yml --env-file env.staging down" -ForegroundColor White
Write-Host "   Status: docker-compose -f docker-compose.staging.yml --env-file env.staging ps" -ForegroundColor White