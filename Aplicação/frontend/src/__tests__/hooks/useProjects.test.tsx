import { renderHook, act } from '@testing-library/react'
import { useProjects, useProjectsMetrics } from '../../api/projects'
import api from '../../api/client'

// Mock do cliente API
jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn(), post: jest.fn(), put: jest.fn(), delete: jest.fn() }
}))

describe('useProjects Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('inicializa com estado vazio', () => {
    const { result } = renderHook(() => useProjects())

    expect(result.current.projects).toEqual([])
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
  })

  it('busca projetos com sucesso', async () => {
    const mockProjects = [
      { id: 1, name: 'Projeto 1', municipio: 'Cidade A', status: 'on_track' },
      { id: 2, name: 'Projeto 2', municipio: 'Cidade B', status: 'completed' }
    ]

    ;(api.get as jest.Mock).mockResolvedValueOnce({ data: mockProjects })

    const { result } = renderHook(() => useProjects())

    await act(async () => {
      await result.current.fetchProjects()
    })

    expect(result.current.projects).toEqual(mockProjects)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
  })

  it('busca projetos com filtros', async () => {
    const mockProjects = [
      { id: 1, name: 'Projeto 1', municipio: 'Cidade A', status: 'on_track' }
    ]

    ;(api.get as jest.Mock).mockResolvedValueOnce({ data: mockProjects })

    const { result } = renderHook(() => useProjects())

    const filters = { status: 'on_track', portfolio: 'Premium' }

    await act(async () => {
      await result.current.fetchProjects(filters)
    })

    expect(api.get).toHaveBeenCalledWith('/projects?include_action_items=true&status=on_track&portfolio=Premium')
    expect(result.current.projects).toEqual(mockProjects)
  })

  it('trata erro ao buscar projetos', async () => {
    const errorMessage = 'Erro na API'
    ;(api.get as jest.Mock).mockRejectedValueOnce(new Error(errorMessage))

    const { result } = renderHook(() => useProjects())

    await act(async () => {
      await result.current.fetchProjects()
    })

    expect(result.current.projects).toEqual([])
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(errorMessage)
  })

  it('cria projeto com sucesso', async () => {
    const newProject = { id: 3, name: 'Novo Projeto', municipio: 'Cidade C' }
    const projectData = {
      name: 'Novo Projeto',
      municipio: 'Cidade C',
      tipo: 'Implantação',
      data_inicio: '2024-01-01',
      data_fim: '2024-12-31',
      valor_implantacao: 100000,
      valor_recorrente: 10000,
      recursos: 5,
      status: 'not_started',
      gerente_projeto_id: 1,
      gerente_portfolio_id: 1,
      owner_id: 1
    }

    ;(api.post as jest.Mock).mockResolvedValueOnce({ data: newProject })

    const { result } = renderHook(() => useProjects())

    let createdProject
    await act(async () => {
      createdProject = await result.current.createProject(projectData)
    })

    expect(createdProject).toEqual(newProject)
    expect(result.current.projects).toContain(newProject)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
  })

  it('atualiza projeto com sucesso', async () => {
    const existingProject = { id: 1, name: 'Projeto Original', municipio: 'Cidade A' }
    const updatedProject = { id: 1, name: 'Projeto Atualizado', municipio: 'Cidade A' }
    const updateData = { name: 'Projeto Atualizado' }

    const { result } = renderHook(() => useProjects())

    // Primeiro, adicionar um projeto existente
    ;(api.get as jest.Mock).mockResolvedValueOnce({ data: [existingProject] })
    
    await act(async () => {
      await result.current.fetchProjects()
    })

    // Agora atualizar o projeto
    ;(api.put as jest.Mock).mockResolvedValueOnce({ data: updatedProject })

    let updated
    await act(async () => {
      updated = await result.current.updateProject(1, updateData)
    })

    expect(updated).toEqual(updatedProject)
    expect(result.current.projects).toContain(updatedProject)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
  })

  it('deleta projeto com sucesso', async () => {
    const existingProject = { id: 1, name: 'Projeto para Deletar', municipio: 'Cidade A' }

    const { result } = renderHook(() => useProjects())
    
    // Primeiro, adicionar um projeto existente
    ;(api.get as jest.Mock).mockResolvedValueOnce({ data: [existingProject] })
    
    await act(async () => {
      await result.current.fetchProjects()
    })

    // Agora deletar o projeto
    ;(api.delete as jest.Mock).mockResolvedValueOnce({})

    await act(async () => {
      await result.current.deleteProject(1)
    })

    expect(result.current.projects).not.toContain(existingProject)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
  })

  it('trata erro ao criar projeto', async () => {
    const errorMessage = 'Erro ao criar projeto'
    const projectData = {
      name: 'Novo Projeto',
      municipio: 'Cidade C',
      tipo: 'Implantação',
      data_inicio: '2024-01-01',
      data_fim: '2024-12-31',
      valor_implantacao: 100000,
      valor_recorrente: 10000,
      recursos: 5,
      status: 'not_started',
      gerente_projeto_id: 1,
      gerente_portfolio_id: 1,
      owner_id: 1
    }

    ;(api.post as jest.Mock).mockRejectedValueOnce(new Error(errorMessage))

    const { result } = renderHook(() => useProjects())

    await act(async () => {
      try {
        await result.current.createProject(projectData)
      } catch (err) {
        // Esperado que lance erro
      }
    })

    expect(result.current.projects).toEqual([])
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(errorMessage)
  })
})

describe('useProjectsMetrics Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('inicializa com estado vazio', () => {
    const { result } = renderHook(() => useProjectsMetrics())

    expect(result.current.metrics).toBe(null)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
  })

  it('busca métricas com sucesso', async () => {
    const mockMetrics = {
      total_projects: 10,
      total_implantation: 1000000,
      total_recurring: 100000,
      total_resources: 50,
      projects_by_status: {
        completed: 3,
        on_track: 5,
        warning: 1,
        delayed: 1
      },
      projects_by_municipio: {
        'Cidade A': 5,
        'Cidade B': 3,
        'Cidade C': 2
      },
      projects_by_portfolio: {
        'Premium': 8,
        'Standard': 2
      }
    }

    ;(api.get as jest.Mock).mockResolvedValueOnce({ data: mockMetrics })

    const { result } = renderHook(() => useProjectsMetrics())

    await act(async () => {
      await result.current.fetchMetrics()
    })

    expect(result.current.metrics).toEqual(mockMetrics)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
  })

  it('trata erro ao buscar métricas', async () => {
    const errorMessage = 'Erro ao carregar métricas'
    ;(api.get as jest.Mock).mockRejectedValueOnce(new Error(errorMessage))

    const { result } = renderHook(() => useProjectsMetrics())

    await act(async () => {
      await result.current.fetchMetrics()
    })

    expect(result.current.metrics).toBe(null)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(errorMessage)
  })

  it('trata erro não-Error object', async () => {
    ;(api.get as jest.Mock).mockRejectedValueOnce('String error')

    const { result } = renderHook(() => useProjectsMetrics())

    await act(async () => {
      await result.current.fetchMetrics()
    })

    expect(result.current.metrics).toBe(null)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe('Erro ao carregar métricas')
  })
})
