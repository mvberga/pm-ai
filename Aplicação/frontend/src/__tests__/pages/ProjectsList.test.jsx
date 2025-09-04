import React from 'react'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProjectsList from '../../pages/ProjectsList'
import { useProjects } from '../../api/projects'

jest.mock('../../api/projects', () => ({
  __esModule: true,
  useProjects: jest.fn()
}))

describe('ProjectsList - Testes de Integração', () => {
  const mockFetchProjects = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('Estados de Carregamento', () => {
    it('exibe loading spinner quando carregando', () => {
      const mockUseProjects = {
        projects: [],
        loading: true,
        error: null,
        fetchProjects: mockFetchProjects
      }

      useProjects.mockReturnValue(mockUseProjects)

      render(
        <MemoryRouter initialEntries={['/projects']}>
          <Routes>
            <Route path="/projects" element={<ProjectsList />} />
          </Routes>
        </MemoryRouter>
      )

      expect(document.querySelector('.animate-spin')).toBeInTheDocument()
      expect(screen.getByText('Projetos')).toBeInTheDocument()
    })

    it('chama fetchProjects no mount', () => {
      const mockUseProjects = {
        projects: [],
        loading: false,
        error: null,
        fetchProjects: mockFetchProjects
      }

      useProjects.mockReturnValue(mockUseProjects)

      render(
        <MemoryRouter initialEntries={['/projects']}>
          <Routes>
            <Route path="/projects" element={<ProjectsList />} />
          </Routes>
        </MemoryRouter>
      )

      expect(mockFetchProjects).toHaveBeenCalledTimes(1)
    })
  })

  describe('Estados de Erro', () => {
    it('exibe mensagem de erro quando API falha', () => {
      const mockUseProjects = {
        projects: [],
        loading: false,
        error: 'Erro de conexão',
        fetchProjects: mockFetchProjects
      }

      useProjects.mockReturnValue(mockUseProjects)

      render(
        <MemoryRouter initialEntries={['/projects']}>
          <Routes>
            <Route path="/projects" element={<ProjectsList />} />
          </Routes>
        </MemoryRouter>
      )

      expect(screen.getByText('Erro ao carregar projetos: Erro de conexão')).toBeInTheDocument()
      expect(screen.getByText('Tentar novamente')).toBeInTheDocument()
    })

    it('permite tentar novamente após erro', async () => {
      const mockUseProjects = {
        projects: [],
        loading: false,
        error: 'Erro de conexão',
        fetchProjects: mockFetchProjects
      }

      useProjects.mockReturnValue(mockUseProjects)

      render(
        <MemoryRouter initialEntries={['/projects']}>
          <Routes>
            <Route path="/projects" element={<ProjectsList />} />
          </Routes>
        </MemoryRouter>
      )

      const retryButton = screen.getByText('Tentar novamente')
      fireEvent.click(retryButton)

      expect(mockFetchProjects).toHaveBeenCalledTimes(2)
    })
  })

  describe('Listagem de Projetos', () => {
    it('lista projetos recebidos da API', async () => {
      const mockProjects = [
        { id: 1, name: 'Projeto A' },
        { id: 2, name: 'Projeto B' },
        { id: 3, name: 'Projeto C' }
      ]

      const mockUseProjects = {
        projects: mockProjects,
        loading: false,
        error: null,
        fetchProjects: mockFetchProjects
      }

      useProjects.mockReturnValue(mockUseProjects)

      render(
        <MemoryRouter initialEntries={['/projects']}>
          <Routes>
            <Route path="/projects" element={<ProjectsList />} />
          </Routes>
        </MemoryRouter>
      )

      expect(screen.getByText('Projetos')).toBeInTheDocument()

      await waitFor(() => {
        expect(screen.getByText('Projeto A')).toBeInTheDocument()
        expect(screen.getByText('Projeto B')).toBeInTheDocument()
        expect(screen.getByText('Projeto C')).toBeInTheDocument()
      })
    })

    it('exibe lista vazia quando não há projetos', () => {
      const mockUseProjects = {
        projects: [],
        loading: false,
        error: null,
        fetchProjects: mockFetchProjects
      }

      useProjects.mockReturnValue(mockUseProjects)

      render(
        <MemoryRouter initialEntries={['/projects']}>
          <Routes>
            <Route path="/projects" element={<ProjectsList />} />
          </Routes>
        </MemoryRouter>
      )

      expect(screen.getByText('Projetos')).toBeInTheDocument()
      expect(screen.getByRole('list')).toBeInTheDocument()
      expect(screen.queryByRole('listitem')).not.toBeInTheDocument()
    })

    it('cria links corretos para cada projeto', async () => {
      const mockProjects = [
        { id: 1, name: 'Projeto A' },
        { id: 2, name: 'Projeto B' }
      ]

      const mockUseProjects = {
        projects: mockProjects,
        loading: false,
        error: null,
        fetchProjects: mockFetchProjects
      }

      useProjects.mockReturnValue(mockUseProjects)

      render(
        <MemoryRouter initialEntries={['/projects']}>
          <Routes>
            <Route path="/projects" element={<ProjectsList />} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        const linkA = screen.getByRole('link', { name: 'Projeto A' })
        const linkB = screen.getByRole('link', { name: 'Projeto B' })
        
        expect(linkA).toHaveAttribute('href', '/projects/1')
        expect(linkB).toHaveAttribute('href', '/projects/2')
      })
    })
  })

  describe('Integração com React Router', () => {
    it('navega corretamente para detalhes do projeto', async () => {
      const mockProjects = [
        { id: 1, name: 'Projeto A' }
      ]

      const mockUseProjects = {
        projects: mockProjects,
        loading: false,
        error: null,
        fetchProjects: mockFetchProjects
      }

      useProjects.mockReturnValue(mockUseProjects)

      render(
        <MemoryRouter initialEntries={['/projects']}>
          <Routes>
            <Route path="/projects" element={<ProjectsList />} />
            <Route path="/projects/:id" element={<div>Detalhes do Projeto</div>} />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        const projectLink = screen.getByRole('link', { name: 'Projeto A' })
        expect(projectLink).toBeInTheDocument()
        expect(projectLink).toHaveAttribute('href', '/projects/1')
      })
    })
  })
})


