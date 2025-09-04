import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProjectDetail from '../../pages/ProjectDetail'
import { projectsApi } from '../../api/projects'

jest.mock('../../api/projects', () => ({
  __esModule: true,
  projectsApi: {
    getById: jest.fn()
  }
}))

describe('ProjectDetail - estados vazios e erro', () => {
  it('exibe erro ao carregar projeto', async () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
    projectsApi.getById.mockRejectedValueOnce(new Error('falha'))

    render(
      <MemoryRouter initialEntries={['/projects/1']}>
        <Routes>
          <Route path="/projects/:id" element={<ProjectDetail />} />
        </Routes>
      </MemoryRouter>
    )

    // Primeiro carrega
    expect(document.querySelector('.animate-spin')).toBeInTheDocument()

    // Depois mostra erro
    await waitFor(() => {
      expect(screen.getByText(/Erro ao carregar projeto/)).toBeInTheDocument()
      expect(screen.getByText('Tentar novamente')).toBeInTheDocument()
    })

    consoleSpy.mockRestore()
  })
})


