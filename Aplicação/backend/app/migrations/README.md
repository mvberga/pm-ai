# Migração de Dados - Arquitetura Expandida

Este diretório contém scripts para migrar dados existentes para a nova arquitetura expandida do backend.

## 📋 Visão Geral

A migração inclui:
- **Criação de novas tabelas** para os modelos expandidos
- **Migração de dados existentes** para os novos modelos
- **Validação da migração** para garantir integridade

## 🗂️ Arquivos

### Scripts de Migração
- `create_new_tables.py` - Cria as novas tabelas no banco de dados
- `data_migration.py` - Migra dados existentes para os novos modelos
- `run_migration.py` - Script principal que executa toda a migração
- `validate_migration.py` - Valida se a migração foi bem-sucedida

## 🚀 Como Executar

### 1. Migração Completa
```bash
cd Aplicação/backend
python -m app.migrations.run_migration
```

### 2. Apenas Criação de Tabelas
```bash
cd Aplicação/backend
python -m app.migrations.create_new_tables
```

### 3. Apenas Migração de Dados
```bash
cd Aplicação/backend
python -m app.migrations.data_migration
```

### 4. Validação
```bash
cd Aplicação/backend
python -m app.migrations.validate_migration
```

## 📊 O que é Migrado

### Portfólios
- **Fonte**: Valores únicos de `portfolio` na tabela `projects`
- **Destino**: Nova tabela `portfolios`
- **Lógica**: Cria um portfólio para cada valor único encontrado

### Membros da Equipe
- **Fonte**: Tabela `project_members`
- **Destino**: Nova tabela `team_members`
- **Lógica**: Migra cada `ProjectMember` para `TeamMember` com mapeamento de roles

### Clientes
- **Fonte**: Dados dos projetos (entidade, município)
- **Destino**: Nova tabela `clients`
- **Lógica**: Cria um cliente padrão para cada projeto sem cliente

### Riscos
- **Fonte**: Análise dos projetos
- **Destino**: Nova tabela `risks`
- **Lógica**: Cria riscos padrão para cada projeto (cronograma, escopo, técnico)

## 🔧 Configuração

### Pré-requisitos
- PostgreSQL rodando
- Banco de dados configurado
- Tabelas existentes com dados

### Variáveis de Ambiente
Certifique-se de que as seguintes variáveis estão configuradas:
```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

## 📈 Estatísticas da Migração

O script de migração gera estatísticas detalhadas:
- Número de portfólios criados
- Número de membros da equipe migrados
- Número de clientes criados
- Número de riscos criados
- Lista de erros encontrados

## ⚠️ Considerações Importantes

### Backup
**SEMPRE faça backup do banco de dados antes de executar a migração!**

### Rollback
Se algo der errado, você pode:
1. Restaurar o backup
2. Executar `DROP TABLE` nas novas tabelas
3. Reverter as mudanças manualmente

### Testes
Execute a migração primeiro em um ambiente de teste para validar o processo.

## 🐛 Troubleshooting

### Erro de Conexão
```
sqlalchemy.exc.OperationalError: connection refused
```
**Solução**: Verifique se o PostgreSQL está rodando e as credenciais estão corretas.

### Erro de Permissão
```
permission denied for table
```
**Solução**: Verifique se o usuário do banco tem permissões para criar tabelas.

### Erro de Chave Estrangeira
```
foreign key constraint fails
```
**Solução**: Verifique se as tabelas referenciadas existem e têm dados válidos.

## 📝 Logs

Todos os scripts geram logs detalhados:
- ✅ Operações bem-sucedidas
- ❌ Erros encontrados
- 📊 Estatísticas da migração
- 🔍 Detalhes de validação

## 🔄 Pós-Migração

Após a migração bem-sucedida:

1. **Valide os dados** usando o script de validação
2. **Teste a API** com os novos endpoints
3. **Atualize o frontend** para usar os novos recursos
4. **Monitore** o sistema por alguns dias

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs detalhados
2. Execute o script de validação
3. Consulte a documentação da API
4. Entre em contato com a equipe de desenvolvimento

---

**Última atualização**: 02/09/2025  
**Versão**: 1.0.0
