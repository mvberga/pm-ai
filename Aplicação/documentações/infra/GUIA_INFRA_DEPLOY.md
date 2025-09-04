# Guia de Infra e Deploy

## Compose por Ambiente
- Arquivos: docker-compose.simple.yml, docker-compose.staging.yml, docker-compose.production.yml, docker-compose.elk.yml
- Validação: docker compose -f <arquivo> config --quiet

## Nginx
- Arquivos: Aplicação/nginx/*.conf
- TLS e redirecionamentos por ambiente

## Observabilidade
- ELK (Filebeat, Logstash, Elasticsearch, Kibana, APM)
- Prometheus e Grafana (Aplicação/monitoring)

## Runbooks de Deploy (PowerShell)
- Staging: ./deploy-staging.ps1
- Produção: ./deploy-production.ps1
- ELK: ./deploy-elk.ps1

## Boas Práticas
- Imagens versionadas e reprodutíveis
- Healthchecks e retries
- Segredos via variáveis/secret manager
