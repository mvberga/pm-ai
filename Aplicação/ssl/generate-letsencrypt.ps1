# Script para Gerar Certificados Let's Encrypt - PM AI MVP
# Data: 03/09/2025

param(
    [Parameter(Mandatory=$true)]
    [string]$Domain,
    
    [Parameter(Mandatory=$false)]
    [string]$Email = "admin@pm-ai-mvp.com"
)

Write-Host "Gerando Certificados Let's Encrypt para $Domain" -ForegroundColor Green

# Verificar se certbot está disponível
try {
    $certbotVersion = certbot --version
    Write-Host "Certbot encontrado: $certbotVersion" -ForegroundColor Green
} catch {
    Write-Host "Certbot nao encontrado. Instalando via winget..." -ForegroundColor Yellow
    winget install Certbot.Certbot
    Write-Host "Certbot instalado. Reinicie o terminal e execute novamente." -ForegroundColor Yellow
    exit 1
}

# Criar diretório para certificados
$certDir = "ssl/letsencrypt"
if (!(Test-Path $certDir)) {
    New-Item -ItemType Directory -Path $certDir -Force
    Write-Host "Diretorio $certDir criado" -ForegroundColor Yellow
}

# Gerar certificado Let's Encrypt
Write-Host "Gerando certificado Let's Encrypt para $Domain..." -ForegroundColor Yellow
Write-Host "Email: $Email" -ForegroundColor Cyan

# Comando para gerar certificado (modo standalone)
$certbotCmd = "certbot certonly --standalone --non-interactive --agree-tos --email $Email -d $Domain --cert-path $certDir --key-path $certDir --fullchain-path $certDir --config-dir $certDir --work-dir $certDir --logs-dir $certDir"

Write-Host "Executando: $certbotCmd" -ForegroundColor Cyan

try {
    Invoke-Expression $certbotCmd
    
    # Verificar se os certificados foram gerados
    $certFile = "$certDir/live/$Domain/fullchain.pem"
    $keyFile = "$certDir/live/$Domain/privkey.pem"
    
    if (Test-Path $certFile -and Test-Path $keyFile) {
        Write-Host "Certificados Let's Encrypt gerados com sucesso!" -ForegroundColor Green
        Write-Host "Arquivos criados:" -ForegroundColor Cyan
        Write-Host "  - $certFile" -ForegroundColor White
        Write-Host "  - $keyFile" -ForegroundColor White
        
        # Copiar para localização padrão do Nginx
        Copy-Item $certFile "ssl/ssl-cert.pem" -Force
        Copy-Item $keyFile "ssl/ssl-cert.key" -Force
        Write-Host "Certificados copiados para ssl/ssl-cert.*" -ForegroundColor Green
        
    } else {
        Write-Host "Erro: Certificados nao foram gerados corretamente" -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host "Erro ao gerar certificados Let's Encrypt: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Verifique se:" -ForegroundColor Yellow
    Write-Host "  1. O dominio $Domain aponta para este servidor" -ForegroundColor White
    Write-Host "  2. As portas 80 e 443 estao abertas" -ForegroundColor White
    Write-Host "  3. Nenhum servidor web esta rodando nas portas 80/443" -ForegroundColor White
    exit 1
}

# Mostrar informações do certificado
Write-Host "Informacoes do certificado:" -ForegroundColor Cyan
openssl x509 -in ssl/ssl-cert.pem -text -noout | Select-String -Pattern "Subject:", "Not Before:", "Not After:"

Write-Host "Certificados Let's Encrypt prontos para uso!" -ForegroundColor Green
Write-Host "Lembre-se de configurar renovacao automatica:" -ForegroundColor Yellow
Write-Host "certbot renew --dry-run" -ForegroundColor White
