import React from 'react'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { PortfolioOverview } from '../../components/dashboard/PortfolioOverview'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn() }
}))

describe('PortfolioOverview', () => {
  const metricsSample = {
    total_projects: 2,
    total_implantation: 100000,
    total_recurring: 5000,
    total_resources: 10,
    projects_by_status: { completed: 1, on_track: 1 },
    projects_by_municipio: { 'Florianópolis': 1, 'Joinville': 1 },
    projects_by_portfolio: {}
  }

  const projectsSample = [
    {
      id: 1,
      name: 'Projeto A',
      municipio: 'Florianópolis',
      status: 'completed',
      valor_implantacao: 60000,
      valor_recorrente: 3000,
      recursos: 5,
      data_inicio: '',
      data_fim: '',
      gerente_projeto: '',
      portfolio: 'Premium',
      vertical: 'TI',
      etapa_atual: ''
    },
    {
      id: 2,
      name: 'Projeto B',
      municipio: 'Joinville',
      status: 'on_track',
      valor_implantacao: 40000,
      valor_recorrente: 2000,
      recursos: 5,
      data_inicio: '',
      data_fim: '',
      gerente_projeto: '',
      portfolio: 'Premium',
      vertical: 'TI',
      etapa_atual: ''
    }
  ]

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renderiza métricas e lista de projetos após carregar', async () => {
    ;(api.get as jest.Mock)
      .mockResolvedValueOnce({ data: metricsSample })
      .mockResolvedValueOnce({ data: projectsSample })

    render(<PortfolioOverview />)

    await waitFor(() => {
      expect(screen.getByText('Portfólio Clientes Premium SC/MG')).toBeInTheDocument()
    })

    // KPIs presentes
    expect(screen.getByText('Total Projetos')).toBeInTheDocument()
    // "Implantação" aparece no KPI e também no cabeçalho da tabela; verifique presença sem exigir unicidade
    expect(screen.getAllByText('Implantação').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Recorrente').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Recursos').length).toBeGreaterThan(0)

    // Valores formatados
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(screen.getByText('R$ 100.000')).toBeInTheDocument()
    expect(screen.getByText('R$ 5.000')).toBeInTheDocument()
    expect(screen.getByText('10')).toBeInTheDocument()

    // Cidades agregadas e tabela (podem aparecer em cards e na tabela)
    expect(screen.getAllByText('Florianópolis').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Joinville').length).toBeGreaterThan(0)
    expect(screen.getByText('Todos os Projetos')).toBeInTheDocument()
    expect(screen.getByText('Projeto A')).toBeInTheDocument()
    expect(screen.getByText('Projeto B')).toBeInTheDocument()

    // Status traduzidos (podem aparecer em cards e na tabela)
    expect(screen.getAllByText('Concluído').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Em Dia').length).toBeGreaterThan(0)
  })

  it('exibe erro e permite tentar novamente', async () => {
    ;(api.get as jest.Mock)
      // Primeira tentativa: falha em uma das chamadas
      .mockRejectedValueOnce(new Error('network'))
      .mockResolvedValueOnce({ data: [] })
      // Retry: sucesso nas duas
      .mockResolvedValueOnce({ data: metricsSample })
      .mockResolvedValueOnce({ data: projectsSample })

    render(<PortfolioOverview />)

    await waitFor(() => {
      expect(screen.getByText('Erro ao carregar dados')).toBeInTheDocument()
    })

    fireEvent.click(screen.getByText('Tentar novamente'))

    await waitFor(() => {
      expect(screen.getByText('Portfólio Clientes Premium SC/MG')).toBeInTheDocument()
    })
  })

  it('lida com estados vazios (métricas zeradas e sem projetos)', async () => {
    const emptyMetrics = {
      total_projects: 0,
      total_implantation: 0,
      total_recurring: 0,
      total_resources: 0,
      projects_by_status: {},
      projects_by_municipio: {},
      projects_by_portfolio: {}
    }

    ;(api.get as jest.Mock)
      .mockResolvedValueOnce({ data: emptyMetrics })
      .mockResolvedValueOnce({ data: [] })

    render(<PortfolioOverview />)

    await waitFor(() => {
      expect(screen.getByText('Portfólio Clientes Premium SC/MG')).toBeInTheDocument()
    })

    expect(screen.getByText('Total Projetos')).toBeInTheDocument()
    expect(screen.getAllByText('0').length).toBeGreaterThan(0)
    expect(screen.getByText('Todos os Projetos')).toBeInTheDocument()
  })
})


