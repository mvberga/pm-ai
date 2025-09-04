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
