# Contrato da API

## Fontes
- OpenAPI (JSON): Aplicação/backend/static_docs/openapi.json
- Redoc (HTML): Aplicação/backend/static_docs/redoc.html

## Geração
- Atualizar documentação estática: python Aplicação/backend/generate_static_docs.py

## Versionamento
- Versionar breaking changes (ex.: /v1, /v2) e manter compatibilidade quando possível
- Documentar códigos de erro, payloads e exemplos

## Segurança
- Autenticação (ex.: Bearer), CORS, rate limit e políticas de acesso
