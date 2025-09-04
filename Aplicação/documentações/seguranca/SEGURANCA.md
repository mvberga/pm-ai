# Segurança

## Segredos
- Nunca commitar .env; usar env.example
- Usar secrets por ambiente (Actions, Vault)

## Scanners
- Backend: bandit, safety
- Frontend: npm audit, dependabot/snyk

## Hardening
- CORS, rate limiting, headers seguros
- Reduzir superfície de ataque em Docker (user não-root)
