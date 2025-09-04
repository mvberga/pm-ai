# Runbooks de Operação

## Incidentes Comuns
- API fora do ar: verificar healthcheck, logs e APM
- Falhas de build/deploy: verificar pipelines e versões de imagem
- Erros 5xx: correlacionar com logs e métricas

## Procedimentos
- Rollback: restaurar versão anterior da imagem/compose
- Rotação de chaves: atualizar secrets e reiniciar serviços
- Backup/Restore de banco: conforme ambiente
