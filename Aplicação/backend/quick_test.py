#!/usr/bin/env python3
"""
Script para testes rápidos da API
Permite validar rapidamente se a aplicação está funcionando
"""

import requests
import json
import sys
from typing import Optional

BASE_URL = "http://localhost:8000"

def test_health():
    """Testa health check"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Health Check: Erro - {e}")
        return False

def test_docs():
    """Testa documentação"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"✅ Docs: {response.status_code}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Docs: Erro - {e}")
        return False

def test_openapi():
    """Testa OpenAPI schema"""
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        if response.status_code == 200:
            schema = response.json()
            print(f"✅ OpenAPI: {response.status_code} - {schema.get('info', {}).get('title', 'N/A')}")
            return True
        else:
            print(f"❌ OpenAPI: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ OpenAPI: Erro - {e}")
        return False

def test_auth():
    """Testa autenticação"""
    try:
        # Dados de teste (ajuste conforme necessário)
        auth_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=auth_data, timeout=5)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Auth: {response.status_code} - Token obtido: {token[:20] if token else 'N/A'}...")
            return token
        else:
            print(f"⚠️ Auth: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Auth: Erro - {e}")
        return None

def test_projects(token: Optional[str] = None):
    """Testa endpoints de projetos"""
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{BASE_URL}/api/v1/projects/", headers=headers, timeout=5)
        
        if response.status_code in [200, 401, 403]:  # 401/403 são esperados sem token válido
            print(f"✅ Projects: {response.status_code}")
            return True
        else:
            print(f"❌ Projects: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Projects: Erro - {e}")
        return False

def test_checklists(token: Optional[str] = None):
    """Testa endpoints de checklists"""
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{BASE_URL}/api/v1/checklists/", headers=headers, timeout=5)
        
        if response.status_code in [200, 401, 403]:
            print(f"✅ Checklists: {response.status_code}")
            return True
        else:
            print(f"❌ Checklists: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Checklists: Erro - {e}")
        return False

def test_portfolios(token: Optional[str] = None):
    """Testa endpoints de portfólios"""
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{BASE_URL}/api/v1/portfolios/", headers=headers, timeout=5)
        
        if response.status_code in [200, 401, 403]:
            print(f"✅ Portfolios: {response.status_code}")
            return True
        else:
            print(f"❌ Portfolios: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Portfolios: Erro - {e}")
        return False

def main():
    """Função principal"""
    print("🧪 Iniciando testes rápidos da API...")
    print(f"🌐 URL Base: {BASE_URL}")
    print("-" * 50)
    
    # Testes básicos
    health_ok = test_health()
    docs_ok = test_docs()
    openapi_ok = test_openapi()
    
    if not health_ok:
        print("\n❌ Aplicação não está rodando ou não está acessível!")
        print("💡 Dica: Execute 'uvicorn app.main:app --reload' para iniciar a aplicação")
        sys.exit(1)
    
    # Testes de autenticação
    token = test_auth()
    
    # Testes de endpoints
    projects_ok = test_projects(token)
    checklists_ok = test_checklists(token)
    portfolios_ok = test_portfolios(token)
    
    # Resumo
    print("-" * 50)
    print("📊 Resumo dos Testes:")
    print(f"  Health Check: {'✅' if health_ok else '❌'}")
    print(f"  Documentação: {'✅' if docs_ok else '❌'}")
    print(f"  OpenAPI: {'✅' if openapi_ok else '❌'}")
    print(f"  Autenticação: {'✅' if token else '⚠️'}")
    print(f"  Projetos: {'✅' if projects_ok else '❌'}")
    print(f"  Checklists: {'✅' if checklists_ok else '❌'}")
    print(f"  Portfólios: {'✅' if portfolios_ok else '❌'}")
    
    # Status final
    basic_tests = health_ok and docs_ok and openapi_ok
    endpoint_tests = projects_ok and checklists_ok and portfolios_ok
    
    if basic_tests and endpoint_tests:
        print("\n🎉 Todos os testes passaram! Aplicação funcionando corretamente.")
        print("🌐 Acesse http://localhost:8000/docs para testar interativamente")
    elif basic_tests:
        print("\n⚠️ Testes básicos passaram, mas alguns endpoints falharam.")
        print("💡 Verifique a configuração do banco de dados e autenticação")
    else:
        print("\n❌ Testes básicos falharam. Verifique se a aplicação está rodando.")
        print("💡 Execute 'uvicorn app.main:app --reload' para iniciar")

if __name__ == "__main__":
    main()
