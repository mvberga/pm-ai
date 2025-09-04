# Script para reconstruir o backend com dependências atualizadas
# Executar no PowerShell como administrador

Write-Host "🚀 Iniciando reconstrução do backend PM AI MVP..." -ForegroundColor Green

# Verificar se o Python está instalado
try {
    $pythonVersion = python --version
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado. Instale o Python 3.11+ primeiro." -ForegroundColor Red
    exit 1
}

# Criar ambiente virtual se não existir
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv .venv
}

# Ativar ambiente virtual
Write-Host "🔧 Ativando ambiente virtual..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Atualizar pip
Write-Host "⬆️ Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Limpar cache do pip
Write-Host "🧹 Limpando cache do pip..." -ForegroundColor Yellow
pip cache purge

# Desinstalar dependências antigas
Write-Host "🗑️ Removendo dependências antigas..." -ForegroundColor Yellow
pip freeze | ForEach-Object { pip uninstall -y $_.Split('==')[0] }

# Instalar dependências atualizadas
Write-Host "📥 Instalando dependências atualizadas..." -ForegroundColor Yellow
pip install -r requirements.txt

# Verificar instalação
Write-Host "🔍 Verificando instalação..." -ForegroundColor Yellow
pip list

# Executar testes básicos
Write-Host "🧪 Executando testes básicos..." -ForegroundColor Yellow
python -m pytest app/tests/test_basic.py -v

# Verificar se o servidor inicia
Write-Host "🚀 Testando inicialização do servidor..." -ForegroundColor Yellow
try {
    $process = Start-Process python -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 5
    
    # Testar endpoint de health
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Servidor iniciado com sucesso!" -ForegroundColor Green
    }
    
    # Parar o servidor
    Stop-Process -Id $process.Id -Force
} catch {
    Write-Host "❌ Erro ao testar servidor: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "🎉 Reconstrução do backend concluída!" -ForegroundColor Green
Write-Host "📋 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Execute 'python -m uvicorn app.main:app --reload' para iniciar o servidor" -ForegroundColor White
Write-Host "   2. Acesse http://localhost:8000/docs para ver a documentação da API" -ForegroundColor White
Write-Host "   3. Execute 'python -m pytest' para rodar todos os testes" -ForegroundColor White