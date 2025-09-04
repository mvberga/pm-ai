# 🌐 Guia de Testes via Navegador - PM AI MVP API

## 📋 Visão Geral

Este guia mostra como testar e validar a aplicação PM AI MVP API diretamente através do navegador, incluindo como gerar documentação estática para visualização offline.

## 🚀 Acessando a Aplicação

### 🌐 Método 1: Aplicação Local (Recomendado)

```bash
# No diretório backend
cd Aplicação/backend

# Iniciar a aplicação
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**URLs disponíveis:**
- **📚 Documentação Interativa (Swagger)**: `http://localhost:8000/docs`
- **📖 Documentação ReDoc**: `http://localhost:8000/redoc`
- **🔍 Health Check**: `http://localhost:8000/health`
- **📋 OpenAPI Schema**: `http://localhost:8000/openapi.json`

### 🐳 Método 2: Via Docker (Produção)

```bash
# Iniciar containers
docker-compose -f docker-compose.prod.yml up -d

# Acessar via navegador
# http://localhost:8000/docs
```

## 🧪 Testando Funcionalidades via Navegador

### 🎯 Swagger UI - Interface de Testes

1. **Acesse**: `http://localhost:8000/docs`
2. **Funcionalidades disponíveis**:
   - ✅ **Testar todos os endpoints** diretamente no navegador
   - ✅ **Autenticação** com tokens JWT
   - ✅ **Validação de dados** em tempo real
   - ✅ **Visualização de respostas** da API
   - ✅ **Download de schemas** OpenAPI

### 🔐 Como Testar Autenticação

1. **No Swagger UI** (`/docs`):
   - Clique em **"Authorize"** (🔒)
   - Use o endpoint `/api/v1/auth/login` para obter token
   - Cole o token no campo "Bearer Token"
   - Agora pode testar endpoints protegidos

### 📋 Testando Endpoints Principais

```bash
# Exemplos de URLs para testar:
http://localhost:8000/api/v1/projects/          # Listar projetos
http://localhost:8000/api/v1/checklists/        # Listar checklists
http://localhost:8000/api/v1/portfolios/        # Listar portfólios
http://localhost:8000/api/v1/team-members/      # Listar membros
```

## 📄 Gerando Documentação Estática

### 🛠️ Script de Geração

Crie um arquivo `generate_static_docs.py` no diretório `Aplicação/backend/`:

```python
#!/usr/bin/env python3
"""
Script para gerar documentação estática da API
Permite visualizar a documentação sem precisar rodar a aplicação
"""

import json
import os
from pathlib import Path
from fastapi.openapi.utils import get_openapi
from app.main import app

def generate_static_docs():
    """Gera documentação estática da API"""
    
    # Criar diretório para documentação estática
    docs_dir = Path("static_docs")
    docs_dir.mkdir(exist_ok=True)
    
    print("🚀 Gerando documentação estática...")
    
    # 1. Gerar OpenAPI Schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Salvar schema OpenAPI
    with open(docs_dir / "openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    
    print("✅ OpenAPI schema salvo em: static_docs/openapi.json")
    
    # 2. Gerar HTML com Swagger UI
    swagger_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app.title} - Documentação</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
    <style>
        html {{
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }}
        *, *:before, *:after {{
            box-sizing: inherit;
        }}
        body {{
            margin:0;
            background: #fafafa;
        }}
        .swagger-ui .topbar {{
            background-color: #2c3e50;
        }}
        .swagger-ui .topbar .download-url-wrapper {{
            display: none;
        }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            const ui = SwaggerUIBundle({{
                url: './openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                validatorUrl: null,
                tryItOutEnabled: true,
                requestInterceptor: function(request) {{
                    // Adicionar headers padrão se necessário
                    return request;
                }}
            }});
        }};
    </script>
</body>
</html>
"""
    
    with open(docs_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(swagger_html)
    
    print("✅ Swagger UI salvo em: static_docs/index.html")
    
    # 3. Gerar HTML com ReDoc
    redoc_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app.title} - ReDoc</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
        }}
    </style>
</head>
<body>
    <redoc spec-url='./openapi.json'></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js"></script>
</body>
</html>
"""
    
    with open(docs_dir / "redoc.html", "w", encoding="utf-8") as f:
        f.write(redoc_html)
    
    print("✅ ReDoc salvo em: static_docs/redoc.html")
    
    # 4. Gerar README para documentação estática
    readme_content = f"""# 📚 Documentação Estática - {app.title}

Esta pasta contém a documentação estática da API que pode ser visualizada sem precisar rodar a aplicação.

## 📋 Arquivos Disponíveis

- **`index.html`** - Swagger UI interativo
- **`redoc.html`** - ReDoc (documentação alternativa)
- **`openapi.json`** - Schema OpenAPI completo

## 🚀 Como Usar

### Opção 1: Abrir Diretamente
```bash
# Abrir no navegador
open static_docs/index.html    # macOS
start static_docs/index.html   # Windows
xdg-open static_docs/index.html # Linux
```

### Opção 2: Servidor Local Simples
```bash
# Python 3
python -m http.server 8001 --directory static_docs

# Acessar: http://localhost:8001
```

### Opção 3: Servidor com CORS (para testes)
```bash
# Instalar http-server globalmente
npm install -g http-server

# Executar com CORS habilitado
http-server static_docs -p 8001 --cors

# Acessar: http://localhost:8001
```

## 🎯 Funcionalidades

- ✅ **Visualização completa** da API
- ✅ **Testes interativos** (limitados sem servidor)
- ✅ **Documentação offline**
- ✅ **Compartilhamento fácil**

## ⚠️ Limitações

- **Testes de API**: Requer servidor rodando para funcionar completamente
- **Autenticação**: Tokens precisam ser válidos do servidor ativo
- **Dados**: Não consegue fazer requisições reais sem backend

## 🔄 Atualizando

Para atualizar a documentação estática:

```bash
python generate_static_docs.py
```

---
*Gerado automaticamente em: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(docs_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README salvo em: static_docs/README.md")
    
    print(f"""
🎉 Documentação estática gerada com sucesso!

📁 Localização: {docs_dir.absolute()}
🌐 Para visualizar: Abra static_docs/index.html no navegador
📖 Alternativa: Abra static_docs/redoc.html para ReDoc

💡 Dica: Use um servidor local para funcionalidade completa:
   python -m http.server 8001 --directory static_docs
""")

if __name__ == "__main__":
    generate_static_docs()
```

### 🚀 Executando o Script

```bash
# No diretório backend
python generate_static_docs.py
```

### 📁 Visualizando a Documentação Estática

```bash
# Opção 1: Abrir diretamente
open static_docs/index.html    # macOS
start static_docs/index.html   # Windows

# Opção 2: Servidor local (recomendado)
python -m http.server 8001 --directory static_docs
# Acessar: http://localhost:8001
```

## 🧪 Scripts de Automação para Testes

### 📝 Script de Teste Rápido

Crie um arquivo `quick_test.py`:

```python
#!/usr/bin/env python3
"""
Script para testes rápidos da API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Testa health check"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.status_code} - {response.json()}")

def test_docs():
    """Testa documentação"""
    response = requests.get(f"{BASE_URL}/docs")
    print(f"Docs: {response.status_code}")

def test_openapi():
    """Testa OpenAPI schema"""
    response = requests.get(f"{BASE_URL}/openapi.json")
    print(f"OpenAPI: {response.status_code}")

def test_auth():
    """Testa autenticação"""
    # Dados de teste (ajuste conforme necessário)
    auth_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=auth_data)
    print(f"Auth: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Token obtido: {token[:20]}...")
        return token
    return None

def test_projects(token=None):
    """Testa endpoints de projetos"""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.get(f"{BASE_URL}/api/v1/projects/", headers=headers)
    print(f"Projects: {response.status_code}")

if __name__ == "__main__":
    print("🧪 Iniciando testes rápidos...")
    
    test_health()
    test_docs()
    test_openapi()
    
    token = test_auth()
    test_projects(token)
    
    print("✅ Testes concluídos!")
```

## 📊 Checklist de Validação via Navegador

### ✅ Funcionalidades Básicas
- [ ] Health check responde
- [ ] Documentação carrega
- [ ] OpenAPI schema válido
- [ ] Autenticação funciona
- [ ] Endpoints protegidos funcionam

### ✅ Funcionalidades Avançadas
- [ ] Criação de projetos
- [ ] Criação de checklists
- [ ] Criação de action items
- [ ] Gestão de portfólios
- [ ] Gestão de equipes
- [ ] Validação de dados
- [ ] Tratamento de erros

### ✅ Melhorias a Validar
- [ ] Performance dos endpoints
- [ ] Validação de entrada
- [ ] Mensagens de erro claras
- [ ] Documentação dos campos
- [ ] Exemplos de uso
- [ ] Códigos de status corretos

## 🎯 Resumo das Opções

### 🌐 Para Testes Interativos
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 📄 Para Documentação Offline
- **Gerar estática**: `python generate_static_docs.py`
- **Visualizar**: `static_docs/index.html`

### 🧪 Para Testes Automatizados
- **Script rápido**: `python quick_test.py`
- **Testes completos**: `python -m pytest app/tests/ -v`

## 🔧 Troubleshooting

### ❌ Problemas Comuns

1. **Aplicação não inicia**:
   ```bash
   # Verificar se as dependências estão instaladas
   pip install -r requirements.txt
   
   # Verificar se o banco está configurado
   python migrate_database.py
   ```

2. **Documentação não carrega**:
   ```bash
   # Verificar se a aplicação está rodando
   curl http://localhost:8000/health
   
   # Verificar logs
   uvicorn app.main:app --reload --log-level debug
   ```

3. **Testes falham**:
   ```bash
   # Verificar configuração do banco de teste
   python -m pytest app/tests/ -v --tb=short
   ```

### 💡 Dicas de Uso

- **Use o Swagger UI** para testes interativos
- **Gere documentação estática** para compartilhamento
- **Execute testes automatizados** para validação rápida
- **Monitore logs** para identificar problemas

---

**🎉 Agora você pode testar e validar melhorias diretamente no navegador, com ou sem a aplicação rodando!**

*Última atualização: Setembro 2024*
