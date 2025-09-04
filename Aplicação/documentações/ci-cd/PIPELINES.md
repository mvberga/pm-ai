# Pipelines CI/CD

## Workflows
- .github/workflows/frontend-ci.yml
- .github/workflows/backend-ci.yml
- .github/workflows/e2e-real.yml
- .github/workflows/deploy-staging.yml
- .github/workflows/deploy-production.yml
- .github/workflows/performance-tests.yml

## Gates de Qualidade
- Lint, testes, cobertura mínima, build
- Scans de segurança e SCA
- Validação de compose e Dockerfile

## Segredos
- Armazenados em GitHub Actions Secrets
- Princípio do menor privilégio
