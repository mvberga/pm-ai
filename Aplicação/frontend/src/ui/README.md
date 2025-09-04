# UI Components - PM AI MVP

Esta pasta contém os componentes de interface do usuário organizados por categoria e seguindo as boas práticas definidas no projeto.

## 📁 Estrutura

```
src/ui/
├── components/
│   ├── Layout/          # Componentes de layout (TopBar, SideNav, Breadcrumbs)
│   ├── Cards/           # Componentes de cards (KPICard)
│   └── Tables/          # Componentes de tabelas (ProjectsTable)
├── tokens/
│   └── colors.ts        # Tokens de design (cores, utilitários)
└── README.md           # Esta documentação
```

## 🎨 Design System

### Cores
Baseado no HTML unificado fornecido, utilizando:
- **Primary**: #0761FF (azul Betha)
- **Background**: Tons de slate (900, 800, 700)
- **Text**: Tons de slate (100, 400, 500)
- **Status**: Cores semânticas para diferentes estados

### Componentes

#### Layout
- **TopBar**: Barra superior com logo, título e ações do usuário
- **SideNav**: Navegação lateral com ícones e badges
- **Breadcrumbs**: Navegação hierárquica

#### Cards
- **KPICard**: Card para exibir métricas e KPIs com suporte a:
  - Ícones personalizados
  - Estados de loading
  - Tendências (positiva/negativa)
  - Cores semânticas por status

#### Tables
- **ProjectsTable**: Tabela de projetos com:
  - Busca e filtros
  - Ordenação por colunas
  - Estados de loading e vazio
  - Ações personalizadas

## 🚀 Uso

### Importação
```typescript
import { TopBar, SideNav, KPICard, ProjectsTable } from '../ui/components';
import { colors, getStatusColor } from '../ui/tokens/colors';
```

### Exemplo de uso do KPICard
```typescript
<KPICard
  title="Total de Projetos"
  value={42}
  icon={KPIIcons.Projects}
  status="info"
  trend={{
    value: 12,
    isPositive: true,
    label: "vs mês anterior"
  }}
/>
```

### Exemplo de uso do ProjectsTable
```typescript
<ProjectsTable
  projects={projects}
  loading={loading}
  onProjectClick={handleProjectClick}
  onActionItemsClick={handleActionItemsClick}
  searchQuery={searchQuery}
  onSearchChange={setSearchQuery}
/>
```

## 🎯 Características

- **TypeScript**: Tipagem forte em todos os componentes
- **Acessibilidade**: Suporte a ARIA labels e navegação por teclado
- **Responsivo**: Design adaptável para diferentes tamanhos de tela
- **Tema Dark**: Otimizado para o tema escuro do projeto
- **Loading States**: Estados de carregamento em todos os componentes
- **Error Handling**: Tratamento de erros com feedback visual

## 🔧 Customização

### Cores
As cores podem ser customizadas editando `tokens/colors.ts`:

```typescript
export const colors = {
  primary: {
    500: '#0761FF', // Cor principal
    // ... outras variações
  },
  // ... outras cores
};
```

### Componentes
Todos os componentes aceitam `className` para customização adicional:

```typescript
<KPICard
  title="Custom Card"
  value={100}
  className="border-2 border-blue-500"
/>
```

## 📱 Responsividade

Os componentes são responsivos por padrão:
- **Mobile**: Layout em coluna única
- **Tablet**: Layout adaptativo
- **Desktop**: Layout completo com sidebar

## ♿ Acessibilidade

- Suporte a navegação por teclado
- ARIA labels apropriados
- Contraste adequado
- Foco visível
- Screen reader friendly

## 🧪 Testes

Os componentes foram projetados para serem facilmente testáveis:
- Props bem definidas
- Estados isolados
- Hooks customizados para lógica de negócio
- Mocks simples para dependências externas
