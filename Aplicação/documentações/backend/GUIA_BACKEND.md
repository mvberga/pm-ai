# Guia do Backend

## Visão
Stack: FastAPI, Alembic, Pytest. Entrypoint: app/main.py. Configurações: app/settings.py.

## Estrutura de Módulos
- Routers: app/routers/*
- Models: app/models/*
- Schemas: app/schemas/*
- Services: app/services/*
- Repositories: app/repositories/*
- Middlewares: app/middlewares/*
- Tasks/Jobs: app/tasks/*
- Utils: app/utils/*

## API
- OpenAPI estática: Aplicação/backend/static_docs/openapi.json
- Redoc estático: Aplicação/backend/static_docs/redoc.html
- Como (re)gerar: python Aplicação/backend/generate_static_docs.py

## Banco de Dados
- Migrations: alembic/ e alembic.ini
- Aplicar migrations: alembic upgrade head
- Criar migration: alembic revision --autogenerate -m "descrição"

## Execução (PowerShell)
- Dev: uvicorn app.main:app --reload
- Testes: pytest -q --maxfail=1 --disable-warnings
- Cobertura: pytest --cov=app --cov-report=term-missing

## Deploy
- Dockerfile e docker-compose.*.yml
- Healthcheck: health_check.py
- Variáveis de ambiente: env.example, env.staging, env.production

## Observabilidade
- ELK (Filebeat/Logstash/Elasticsearch/Kibana) + APM
- Métricas/Logs configurados em Aplicação/logging/

## Qualidade
- Linters: ruff/flake8, black, isort, mypy
- Segurança: bandit
- Cobertura mínima sugerida: 80%
