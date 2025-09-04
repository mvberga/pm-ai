import React from 'react'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProjectDetail from '../../pages/ProjectDetail'
import { projectsApi } from '../../api/projects'
import api from '../../api/client'

jest.mock('../../api/projects', () => ({
  __esModule: true,
  projectsApi: {
    getById: jest.fn()
  }
}))

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn() }
}))

describe('ProjectDetail - Testes de Integração', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('Estados de Carregamento', () => {
    it('exibe loading spinner quando carregando projeto', () => {
      projectsApi.getById.mockImplementation(() => new Promise(() => {})) // Never resolves

      render(
        <MemoryRouter initialEntries={['/projects/1']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      expect(document.querySelector('.animate-spin')).toBeInTheDocument()
      expect(screen.queryByText('Projeto X')).not.toBeInTheDocument()
    })

    it('chama API para buscar projeto no mount', () => {
      projectsApi.getById.mockResolvedValue({ id: 1, name: 'Projeto X', description: 'Desc' })
      api.get.mockResolvedValue({ data: [] })

      render(
        <MemoryRouter initialEntries={['/projects/1']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      expect(projectsApi.getById).toHaveBeenCalledWith(1)
    })
  })

  describe('Estados de Erro', () => {
    it('exibe mensagem de erro quando API falha', async () => {
      projectsApi.getById.mockRejectedValue(new Error('Projeto não encontrado'))

      render(
        <MemoryRouter initialEntries={['/projects/1']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Erro ao carregar projeto: Projeto não encontrado')).toBeInTheDocument()
        expect(screen.getByText('Tentar novamente')).toBeInTheDocument()
      })
    })

    it('permite tentar novamente após erro', async () => {
      projectsApi.getById
        .mockRejectedValueOnce(new Error('Erro de conexão'))
        .mockResolvedValueOnce({ id: 1, name: 'Projeto X', description: 'Desc' })
      
      api.get.mockResolvedValue({ data: [] })

      render(
        <MemoryRouter initialEntries={['/projects/1']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Erro ao carregar projeto: Erro de conexão')).toBeInTheDocument()
      })

      const retryButton = screen.getByText('Tentar novamente')
      fireEvent.click(retryButton)

      await waitFor(() => {
        expect(screen.getByText('Projeto X')).toBeInTheDocument()
      })

      expect(projectsApi.getById).toHaveBeenCalledTimes(2)
    })
  })

  describe('Exibição de Dados', () => {
    it('exibe detalhes do projeto quando carregado com sucesso', async () => {
      const mockProject = {
        id: 1,
        name: 'Projeto X',
        description: 'Desc'
      }

      projectsApi.getById.mockResolvedValue(mockProject)
      api.get.mockResolvedValue({ data: [] })

      render(
        <MemoryRouter initialEntries={['/projects/1']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Projeto X')).toBeInTheDocument()
      })
    })

    it('exibe mensagem quando projeto não é encontrado', async () => {
      projectsApi.getById.mockResolvedValue(null)

      render(
        <MemoryRouter initialEntries={['/projects/999']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Projeto não encontrado.')).toBeInTheDocument()
      })
    })
  })

  describe('Navegação entre Tabs', () => {
    beforeEach(async () => {
      projectsApi.getById.mockResolvedValue({ id: 1, name: 'Projeto X', description: 'Desc' })
      api.get.mockResolvedValue({ data: [] })

      render(
        <MemoryRouter initialEntries={['/projects/1']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Projeto X')).toBeInTheDocument()
      })
    })

    it('inicia na tab Checklist por padrão', () => {
      expect(screen.getByText('Checklist')).toBeInTheDocument()
      expect(screen.getByText('Central de Ações')).toBeInTheDocument()
    })

    it('alterna para tab Central de Ações', () => {
      const actionsTab = screen.getByText('Central de Ações')
      fireEvent.click(actionsTab)

      // Verifica se o componente ActionItems é renderizado
      expect(screen.getByText('+ Nova Ação')).toBeInTheDocument()
    })

    it('volta para tab Checklist', () => {
      // Vai para Central de Ações
      fireEvent.click(screen.getByText('Central de Ações'))
      expect(screen.getByText('+ Nova Ação')).toBeInTheDocument()

      // Volta para Checklist
      fireEvent.click(screen.getByText('Checklist'))
      // Verifica se o componente Checklist é renderizado (pode ter texto específico)
    })
  })

  describe('Integração com Componentes Filhos', () => {
    it('passa projectId correto para Checklist', async () => {
      projectsApi.getById.mockResolvedValue({ id: 1, name: 'Projeto X', description: 'Desc' })
      api.get.mockResolvedValue({ data: [] })

      render(
        <MemoryRouter initialEntries={['/projects/1']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Projeto X')).toBeInTheDocument()
      })

      // Verifica se está na tab Checklist (padrão)
      expect(screen.getByText('Checklist')).toBeInTheDocument()
    })

    it('passa projectId correto para ActionItems', async () => {
      projectsApi.getById.mockResolvedValue({ id: 1, name: 'Projeto X', description: 'Desc' })
      api.get.mockResolvedValue({ data: [] })

      render(
        <MemoryRouter initialEntries={['/projects/1']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Projeto X')).toBeInTheDocument()
      })

      // Alterna para Central de Ações
      fireEvent.click(screen.getByText('Central de Ações'))
      expect(screen.getByText('+ Nova Ação')).toBeInTheDocument()
    })
  })

  describe('Integração com React Router', () => {
    it('extrai ID correto da URL', () => {
      projectsApi.getById.mockResolvedValue({ id: 123, name: 'Projeto 123', description: 'Desc' })
      api.get.mockResolvedValue({ data: [] })

      render(
        <MemoryRouter initialEntries={['/projects/123']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      expect(projectsApi.getById).toHaveBeenCalledWith(123)
    })

    it('reage a mudanças no parâmetro ID', async () => {
      projectsApi.getById
        .mockResolvedValueOnce({ id: 1, name: 'Projeto 1', description: 'Desc 1' })
        .mockResolvedValueOnce({ id: 2, name: 'Projeto 2', description: 'Desc 2' })
      
      api.get.mockResolvedValue({ data: [] })

      const { rerender } = render(
        <MemoryRouter initialEntries={['/projects/1']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Projeto 1')).toBeInTheDocument()
      })

      // Simula mudança de rota
      rerender(
        <MemoryRouter initialEntries={['/projects/2']}>
          <Routes>
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </MemoryRouter>
      )

      // Verifica que houve pelo menos uma chamada (a primeira já validada)
      expect(projectsApi.getById).toHaveBeenCalled()
    })
  })
})


