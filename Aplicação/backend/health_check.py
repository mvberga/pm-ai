#!/usr/bin/env python3
"""
Script para verificar a saúde do sistema após reconstrução
"""

import asyncio
import sys
import httpx
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.append(str(Path(__file__).parent))

from app.db.session import get_engine
from app.core.config import settings

async def check_database():
    """Verificar conexão com o banco de dados"""
    print("🔍 Verificando conexão com o banco de dados...")
    
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            if result.scalar() == 1:
                print("✅ Conexão com banco de dados OK")
                return True
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False
    finally:
        await engine.dispose()

async def check_api():
    """Verificar se a API está respondendo"""
    print("�� Verificando API...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ API respondendo corretamente")
                return True
            else:
                print(f"❌ API retornou status {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Erro ao conectar com API: {e}")
        return False

async def check_dependencies():
    """Verificar se todas as dependências estão instaladas"""
    print("�� Verificando dependências...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "sqlalchemy",
        "asyncpg",
        "alembic",
        "pytest",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NÃO ENCONTRADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Pacotes faltando: {', '.join(missing_packages)}")
        return False
    
    return True

async def main():
    """Executar todas as verificações"""
    print("🚀 Iniciando verificação de saúde do sistema...\n")
    
    checks = [
        ("Dependências", check_dependencies),
        ("Banco de Dados", check_database),
        ("API", check_api),
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        result = await check_func()
        results.append((name, result))
    
    print("\n" + "="*50)
    print("📊 RESUMO DOS RESULTADOS:")
    print("="*50)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 Todos os testes passaram! Sistema funcionando corretamente.")
    else:
        print("\n⚠️ Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
