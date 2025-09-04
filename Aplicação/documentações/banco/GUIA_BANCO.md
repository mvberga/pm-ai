# Guia do Banco de Dados

## Visão
Fontes de schema: db/init/*.sql e Alembic (ORM). Ambientes e credenciais definidas via .env e compose.

## Modelo de Dados
- Tabelas, chaves e relacionamentos (manter ERD atualizado)
- Convenções de nomenclatura (snake_case, sufixos _id, _at, etc.)

## Migrations (Alembic)
- Criar: alembic revision --autogenerate -m "descrição"
- Aplicar: alembic upgrade head
- Reverter: alembic downgrade -1

## Operações
- Backup/Restore conforme ambiente
- Estratégia de versionamento de schema
- Dados de seed/fixtures quando necessário
