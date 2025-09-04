import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProjectsList from '../../pages/ProjectsList'
import { useProjects } from '../../api/projects'

jest.mock('../../api/projects', () => ({
  __esModule: true,
  useProjects: jest.fn()
}))

describe('ProjectsList - estados vazios e erro', () => {
  it('exibe lista vazia sem quebrar', async () => {
    const mockUseProjects = {
      projects: [],
      loading: false,
      error: null,
      fetchProjects: jest.fn()
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
      // Sem itens na lista
      expect(screen.queryByRole('link')).not.toBeInTheDocument()
    })
  })

  it('exibe erro da API com botão para tentar novamente', async () => {
    const mockFetchProjects = jest.fn()
    const mockUseProjects = {
      projects: [],
      loading: false,
      error: 'Erro ao carregar projetos',
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

    expect(screen.getByText('Erro ao carregar projetos: Erro ao carregar projetos')).toBeInTheDocument()
    expect(screen.getByText('Tentar novamente')).toBeInTheDocument()
  })
})


