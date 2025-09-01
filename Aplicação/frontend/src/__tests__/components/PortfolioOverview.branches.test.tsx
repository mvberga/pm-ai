import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { PortfolioOverview } from '../../components/dashboard/PortfolioOverview'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn() }
}))

describe('PortfolioOverview - branches', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('cobre mapeamentos de status (including default Desconhecido)', async () => {
    const metricsAllStatuses = {
      total_projects: 5,
      total_implantation: 0,
      total_recurring: 0,
      total_resources: 0,
      projects_by_status: {
        completed: 1,
        on_track: 1,
        warning: 1,
        delayed: 1,
        not_started: 1,
        unknown_status: 1
      },
      projects_by_municipio: {},
      projects_by_portfolio: {}
    }

    ;(api.get as jest.Mock)
      .mockResolvedValueOnce({ data: metricsAllStatuses })
      .mockResolvedValueOnce({ data: [] })

    render(<PortfolioOverview />)

    await waitFor(() => {
      expect(screen.getByText('Portfólio Clientes Premium SC/MG')).toBeInTheDocument()
    })

    // Textos traduzidos dos status
    expect(screen.getAllByText('Concluído').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Em Dia').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Atenção').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Atrasado').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Não Iniciado').length).toBeGreaterThan(0)
    // default branch
    expect(screen.getAllByText('Desconhecido').length).toBeGreaterThan(0)
  })

  it("exibe 'N/A' quando campos estão vazios e recorrente é zero", async () => {
    const metrics = {
      total_projects: 1,
      total_implantation: 1000,
      total_recurring: 0,
      total_resources: 1,
      projects_by_status: {},
      projects_by_municipio: { 'Cidade Z': 1 },
      projects_by_portfolio: {}
    }

    const projects = [
      {
        id: 9,
        name: 'Projeto Z',
        municipio: 'Cidade Z',
        status: 'not_started',
        valor_implantacao: 1000,
        valor_recorrente: 0,
        recursos: 1,
        data_inicio: '',
        data_fim: '',
        gerente_projeto: '',
        portfolio: '',
        vertical: '',
        etapa_atual: ''
      }
    ]

    ;(api.get as jest.Mock)
      .mockResolvedValueOnce({ data: metrics })
      .mockResolvedValueOnce({ data: projects })

    render(<PortfolioOverview />)

    await waitFor(() => {
      expect(screen.getByText('Todos os Projetos')).toBeInTheDocument()
    })

    expect(screen.getByText('Projeto Z')).toBeInTheDocument()
    // existem múltiplas ocorrências de 'N/A' (etapa, recorrente, portfólio, vertical)
    expect(screen.getAllByText('N/A').length).toBeGreaterThanOrEqual(4)
  })
})
