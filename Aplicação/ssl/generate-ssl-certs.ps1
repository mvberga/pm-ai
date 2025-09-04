# Script para Gerar Certificados SSL - PM AI MVP
# Data: 03/09/2025

Write-Host "Gerando Certificados SSL para PM AI MVP" -ForegroundColor Green

# Criar diretório SSL se não existir
if (!(Test-Path "ssl")) {
    New-Item -ItemType Directory -Path "ssl" -Force
    Write-Host "Diretorio SSL criado" -ForegroundColor Yellow
}

# Verificar se OpenSSL está disponível
try {
    $opensslVersion = openssl version
    Write-Host "OpenSSL encontrado: $opensslVersion" -ForegroundColor Green
} catch {
    Write-Host "OpenSSL nao encontrado. Instalando via winget..." -ForegroundColor Yellow
    winget install OpenSSL.OpenSSL
    Write-Host "OpenSSL instalado. Reinicie o terminal e execute novamente." -ForegroundColor Yellow
    exit 1
}

# Gerar chave privada
Write-Host "Gerando chave privada..." -ForegroundColor Yellow
openssl genrsa -out ssl/ssl-cert.key 2048

# Criar arquivo de configuração OpenSSL
$opensslConfig = @"
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = BR
ST = SP
L = SaoPaulo
O = PM-AI-MVP
OU = IT
CN = localhost

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.localhost
IP.1 = 127.0.0.1
"@

$opensslConfig | Out-File -FilePath "ssl/openssl.conf" -Encoding ASCII

# Gerar certificado auto-assinado
Write-Host "Gerando certificado auto-assinado..." -ForegroundColor Yellow
openssl req -new -x509 -key ssl/ssl-cert.key -out ssl/ssl-cert.pem -days 365 -config ssl/openssl.conf -extensions v3_req

# Verificar certificados
Write-Host "Verificando certificados gerados..." -ForegroundColor Yellow
if ((Test-Path "ssl/ssl-cert.key") -and (Test-Path "ssl/ssl-cert.pem")) {
    Write-Host "Certificados SSL gerados com sucesso!" -ForegroundColor Green
    Write-Host "Arquivos criados:" -ForegroundColor Cyan
    Write-Host "  - ssl/ssl-cert.key (chave privada)" -ForegroundColor White
    Write-Host "  - ssl/ssl-cert.pem (certificado)" -ForegroundColor White
} else {
    Write-Host "Erro ao gerar certificados SSL" -ForegroundColor Red
    exit 1
}

# Mostrar informações do certificado
Write-Host "Informacoes do certificado:" -ForegroundColor Cyan
openssl x509 -in ssl/ssl-cert.pem -text -noout | Select-String -Pattern "Subject:", "Not Before:", "Not After:"

Write-Host "Certificados SSL prontos para uso!" -ForegroundColor Green
