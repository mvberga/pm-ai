import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import ProjectsStatusPage from '../../pages/ProjectsStatusPage'

// Mock dos hooks de dados
jest.mock('../../api/projects', () => ({
  useProjects: () => ({
    projects: [
      { id: 1, name: 'Projeto A', municipio: 'Cidade X', valor_implantacao: 1000, valor_recorrente: 100, recursos: 1, status: 'on_track', tipo: 'implantacao', data_inicio: '2025-01-01', data_fim: '2025-12-31', gerente_projeto_id: 1, gerente_portfolio_id: 1, owner_id: 1, created_at: '2025-01-01', updated_at: '2025-01-02', pending_actions_count: 2 },
      { id: 2, name: 'Projeto B', municipio: 'Cidade Y', valor_implantacao: 2000, valor_recorrente: 200, recursos: 2, status: 'completed', tipo: 'implantacao', data_inicio: '2025-01-01', data_fim: '2025-12-31', gerente_projeto_id: 1, gerente_portfolio_id: 1, owner_id: 1, created_at: '2025-01-01', updated_at: '2025-01-02', pending_actions_count: 0 }
    ],
    loading: false,
    error: null,
    fetchProjects: jest.fn()
  })
}))

jest.mock('../../api/actionItems', () => ({
  useActionItems: () => ({
    actionItems: [],
    loading: false,
    error: null,
    fetchActionItems: jest.fn()
  })
}))

jest.mock('../../ui/components/Layout/TopBar', () => ({
  TopBar: ({ title }: { title: string }) => <div data-testid="topbar">{title}</div>
}))

jest.mock('../../ui/components/Layout/SideNav', () => ({
  SideNav: ({}) => <nav data-testid="sidenav" />,
  NavIcons: {}
}))

jest.mock('../../ui/components/Layout/Breadcrumbs', () => ({
  Breadcrumbs: ({}) => <div data-testid="breadcrumbs" />
}))

jest.mock('../../ui/components/Cards/KPICard', () => ({
  KPICard: ({ title, value }: { title: string, value: any }) => (
    <div role="status" aria-label={title}>{String(value)}</div>
  ),
  KPIIcons: {}
}))

jest.mock('../../ui/components/Tables/ProjectsTable', () => ({
  ProjectsTable: ({ projects }: { projects: any[] }) => (
    <table>
      <tbody>
        {projects.map(p => <tr key={p.id}><td>{p.name}</td></tr>)}
      </tbody>
    </table>
  )
}))

const renderPage = () => render(
  <BrowserRouter>
    <ProjectsStatusPage />
  </BrowserRouter>
)

describe('ProjectsStatusPage', () => {
  it('renderiza título, KPIs e tabela', async () => {
    renderPage()

    expect(screen.getByTestId('topbar')).toHaveTextContent('Status Executivo de Projetos')
    expect(screen.getByTestId('breadcrumbs')).toBeInTheDocument()
    expect(screen.getByTestId('sidenav')).toBeInTheDocument()

    // KPIs básicos
    expect(screen.getByRole('status', { name: 'Total de Projetos' })).toHaveTextContent('2')
    expect(screen.getByRole('status', { name: 'Total de Ações Pendentes' })).toHaveTextContent('2')

    // Tabela com projetos
    expect(screen.getByText('Projeto A')).toBeInTheDocument()
    expect(screen.getByText('Projeto B')).toBeInTheDocument()
  })
})
