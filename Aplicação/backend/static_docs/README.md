# 📚 Documentação Estática - PM AI MVP API

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
*Gerado automaticamente em: 2025-09-03 02:31:32*
