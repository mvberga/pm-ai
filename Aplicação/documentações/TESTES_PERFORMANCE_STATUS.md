# Status dos Testes de Performance - PM AI MVP

**Data de Criação:** 28 de Agosto de 2025  
**Última Atualização:** 28 de Agosto de 2025  
**Versão:** 1.0.0  
**Status:** ✅ Smoke de performance básico passando (backend)

---

## 🎯 **Visão Geral dos Testes de Performance**

Os testes de performance estão planejados para a Fase 4 do projeto, após a implementação completa dos testes de backend, frontend e integração. Estes testes validarão a capacidade do sistema de lidar com carga, latência e escalabilidade, garantindo que as metas de performance sejam atendidas.

---

## 📊 **Status Atual dos Testes de Performance**

### ✅ Smoke executado na suíte (backend)
- **Carga E2E**: 30 operações simultâneas com 100% sucesso
- **Tempo total**: ~1.1–1.5s (ambiente local)
- **Taxa**: 20–36 ops/s (variável)

### **📋 Próxima etapa (Fase 4)**
- **Infraestrutura**: Docker Compose dedicado a performance
- **Framework**: Locust/Artillery
- **Cobertura**: APIs principais sob carga
- **Ambiente**: Monitoração (Prometheus/Grafana)

### **📁 Estrutura Planejada**
```
Aplicação/
├── tests/
│   ├── performance/              # 📋 Testes de performance (planejado)
│   │   ├── load/                 # 📋 Testes de carga
│   │   ├── stress/               # 📋 Testes de estresse
│   │   ├── spike/                # 📋 Testes de pico
│   │   └── endurance/            # 📋 Testes de resistência
│   ├── fixtures/                 # 📋 Dados de teste para carga
│   ├── scenarios/                # 📋 Cenários de teste
│   └── config/                   # 📋 Configurações de performance
├── docker-compose.performance.yml # 📋 Ambiente de teste de performance
└── locustfile.py                 # 📋 Configuração Locust (planejado)
```

---

## 🚀 **Roadmap de Testes de Performance**

### **Fase 1: Preparação da Infraestrutura (1 semana)**

#### **1.1 Ambiente de Teste de Performance**
- [ ] **Docker Compose para Performance**: Ambiente escalável
- [ ] **Banco de Teste**: PostgreSQL com dados de carga
- [ ] **Backend de Teste**: FastAPI com métricas habilitadas
- [ ] **Monitoramento**: Prometheus + Grafana (planejado)

#### **1.2 Configuração de Ferramentas**
- [ ] **Locust**: Para testes de carga Python
- [ ] **Artillery**: Alternativa para testes de carga Node.js
- [ ] **JMeter**: Para testes mais complexos (opcional)
- [ ] **K6**: Para testes de performance modernos (opcional)

### **Fase 2: Testes de Carga (1 semana)**

#### **2.1 APIs Principais**
- [ ] **Projetos**: CRUD com múltiplos usuários simultâneos
- [ ] **Checklists**: Criação e leitura em massa
- [ ] **Action Items**: Operações concorrentes
- [ ] **Autenticação**: Login simultâneo de usuários

#### **2.2 Cenários de Carga**
- [ ] **Carga Normal**: 100 usuários simultâneos
- [ ] **Carga Alta**: 500 usuários simultâneos
- [ ] **Carga Extrema**: 1000+ usuários simultâneos
- [ ] **Carga Sustentada**: 30 minutos de carga constante

### **Fase 3: Testes de Estresse e Escalabilidade (1 semana)**

#### **3.1 Testes de Estresse**
- [ ] **Limite de Capacidade**: Identificar ponto de quebra
- [ ] **Recuperação**: Sistema após sobrecarga
- [ ] **Degradação Graceful**: Performance sob estresse
- [ ] **Timeout Handling**: Respostas em cenários extremos

#### **3.2 Testes de Escalabilidade**
- [ ] **Horizontal Scaling**: Múltiplas instâncias
- [ ] **Vertical Scaling**: Recursos de máquina
- [ ] **Database Scaling**: Conexões e queries
- [ ] **Cache Scaling**: Redis e memória

---

## 🛠️ **Configuração Planejada**

### **Docker Compose para Performance**
```yaml
# docker-compose.performance.yml (planejado)
version: '3.8'
services:
  performance-db:
    image: postgres:16
    environment:
      POSTGRES_DB: pm_ai_performance
      POSTGRES_USER: perf_user
      POSTGRES_PASSWORD: perf_pass
    ports:
      - "5434:5432"
    volumes:
      - ./db/init:/docker-entrypoint-initdb.d
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'

  performance-backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://perf_user:perf_pass@performance-db:5432/pm_ai_performance
      PERFORMANCE_TESTING: true
      LOG_LEVEL: INFO
    depends_on:
      - performance-db
    ports:
      - "8002:8000"
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'

  locust:
    image: locustio/locust
    ports:
      - "8089:8089"
    volumes:
      - ./tests/performance:/locust
    command: -f /locust/locustfile.py --host=http://performance-backend:8000
    depends_on:
      - performance-backend

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./tests/performance/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana-storage:/var/lib/grafana

volumes:
  grafana-storage:
```

### **Locust Configuration**
```python
# tests/performance/locustfile.py (planejado)
from locust import HttpUser, task, between
import json
import random

class PMAIUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login do usuário no início do teste"""
        login_data = {
            "email": f"user{random.randint(1, 1000)}@test.com",
            "id_token": f"token_{random.randint(1000, 9999)}"
        }
        
        response = self.client.post("/api/v1/auth/google/login", json=login_data)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def get_projects(self):
        """Listar projetos (alta frequência)"""
        self.client.get("/api/v1/projects", headers=self.headers)
    
    @task(2)
    def create_project(self):
        """Criar projeto (média frequência)"""
        project_data = {
            "name": f"Performance Project {random.randint(1, 10000)}",
            "description": "Project created during performance testing",
            "municipio": "São Paulo",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        self.client.post("/api/v1/projects", 
                        json=project_data, 
                        headers=self.headers)
    
    @task(1)
    def get_project_detail(self):
        """Obter detalhes de projeto (baixa frequência)"""
        project_id = random.randint(1, 100)
        self.client.get(f"/api/v1/projects/{project_id}", 
                       headers=self.headers)
```

### **Artillery Configuration**
```yaml
# tests/performance/artillery-config.yml (planejado)
config:
  target: 'http://localhost:8002'
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 300
      arrivalRate: 50
      name: "Normal load"
    - duration: 180
      arrivalRate: 100
      name: "High load"
    - duration: 120
      arrivalRate: 200
      name: "Peak load"
  
  defaults:
    headers:
      Content-Type: 'application/json'
      Authorization: 'Bearer {{ $randomString() }}'

scenarios:
  - name: "Projects CRUD"
    weight: 70
    flow:
      - get:
          url: "/api/v1/projects"
      - think: 2
      - post:
          url: "/api/v1/projects"
          json:
            name: "Performance Project {{ $randomString() }}"
            description: "Created during performance test"
            municipio: "São Paulo"
            gerente_projeto_id: 1
            gerente_portfolio_id: 1
  
  - name: "Authentication"
    weight: 30
    flow:
      - post:
          url: "/api/v1/auth/google/login"
          json:
            email: "user{{ $randomNumber(1, 1000) }}@test.com"
            id_token: "token_{{ $randomNumber(1000, 9999) }}"
```

---

## 📋 **Comandos Planejados**

### **Testes de Performance**
```bash
# Subir ambiente de performance
docker-compose -f docker-compose.performance.yml up -d

# Testes com Locust
docker-compose -f docker-compose.performance.yml run locust

# Testes com Artillery
npm run test:performance:artillery

# Testes de carga específicos
npm run test:performance:load
npm run test:performance:stress
npm run test:performance:spike

# Monitoramento
open http://localhost:9090  # Prometheus
open http://localhost:3000  # Grafana
open http://localhost:8089  # Locust UI
```

### **Análise de Resultados**
```bash
# Gerar relatórios de performance
npm run test:performance:report

# Análise de métricas
npm run test:performance:analyze

# Comparação entre execuções
npm run test:performance:compare
```

---

## 🎯 **Metas de Performance**

### **Latência (P95)**
- **APIs CRUD**: <300ms
- **APIs de Leitura**: <200ms
- **Autenticação**: <500ms
- **Relatórios**: <1000ms

### **Throughput**
- **Usuários Simultâneos**: 1000+
- **Requests por Segundo**: 500+
- **Transações por Segundo**: 100+

### **Recursos**
- **CPU**: <80% sob carga normal
- **Memória**: <2GB por instância
- **Disco**: <100MB/s de I/O
- **Rede**: <50MB/s de throughput

---

## 🔧 **Dependências Planejadas**

### **Dependências de Teste**
```json
{
  "devDependencies": {
    "artillery": "^2.0.0",
    "locust": "^2.0.0",
    "k6": "^0.45.0",
    "jmeter": "^5.5.0",
    "prometheus": "^2.45.0",
    "grafana": "^10.0.0"
  }
}
```

### **Configurações Adicionais**
- **Docker**: Para ambiente escalável
- **PostgreSQL**: Banco de teste com dados de carga
- **Redis**: Cache para testes de performance
- **Nginx**: Load balancer (se necessário)

---

## 🎯 **Próximos Passos**

### **Imediato (Fases 1-3)**
1. **Implementar testes de backend** (2-3 horas)
2. **Implementar testes de frontend** (1-2 semanas)
3. **Implementar testes de integração** (1-2 semanas)
4. **Preparar infraestrutura de performance** (1 semana)

### **Médio Prazo (Fase 4)**
1. **Testes de carga** (1 semana)
2. **Testes de estresse** (1 semana)
3. **Metas de performance validadas** (meta atingida)

---

## 📚 **Recursos e Referências**

### **Documentação**
- [Locust](https://docs.locust.io/)
- [Artillery](https://www.artillery.io/docs/)
- [K6](https://k6.io/docs/)
- [JMeter](https://jmeter.apache.org/usermanual/)

### **Exemplos e Tutoriais**
- [Performance Testing Best Practices](https://www.guru99.com/performance-testing.html)
- [Load Testing Strategies](https://www.blazemeter.com/blog/load-testing-strategies)
- [Performance Metrics](https://www.datadoghq.com/blog/engineering/performance-metrics/)

---

## 🚀 **Conclusão**

Os testes de performance estão **planejados para a Fase 4** do projeto. Com a infraestrutura de testes de backend, frontend e integração implementada, o foco será:

1. **Preparar ambiente escalável** (Docker + monitoramento)
2. **Implementar testes de carga** (Locust/Artillery)
3. **Validar metas de performance** (latência <300ms, 1000+ usuários)
4. **Garantir escalabilidade** (horizontal e vertical)

O projeto está no caminho certo para se tornar uma ferramenta robusta com testes completos em todas as camadas e validação de performance!

---

## 🔗 **Links Relacionados**

- **📋 Status Geral dos Testes:** [TESTES_GERAL.md](TESTES_GERAL.md)
- **🧪 Status dos Testes Backend:** [backend/TESTES_BACKEND_STATUS.md](backend/TESTES_BACKEND_STATUS.md)
- **🖥️ Status dos Testes Frontend:** [frontend/TESTES_FRONTEND_STATUS.md](frontend/TESTES_FRONTEND_STATUS.md)
- **🔗 Status dos Testes Integração:** [TESTES_INTEGRACAO_STATUS.md](TESTES_INTEGRACAO_STATUS.md)
- **🚀 Próximos Passos:** [PRÓXIMOS_PASSOS.md](PRÓXIMOS_PASSOS.md)
