import React from 'react'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProjectDetail from '../../pages/ProjectDetail'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn() }
}))

describe('ProjectDetail', () => {
  it('exibe detalhes do projeto e alterna tabs', async () => {
    // 1) Detalhes do projeto
    api.get.mockResolvedValueOnce({ data: { id: 1, name: 'Projeto X', description: 'Desc' } })
    // 2) Checklist groups (vazio)
    api.get.mockResolvedValueOnce({ data: [] })
    // 3) Action items (vazio)
    api.get.mockResolvedValueOnce({ data: [] })

    render(
      <MemoryRouter initialEntries={['/projects/1']}>
        <Routes>
          <Route path="/projects/:id" element={<ProjectDetail />} />
        </Routes>
      </MemoryRouter>
    )

    expect(screen.getByText('Carregando...')).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText('Projeto X')).toBeInTheDocument()
      expect(screen.getByText('Desc')).toBeInTheDocument()
    })

    // Tabs
    fireEvent.click(screen.getByText('Central de Ações'))
    expect(screen.getByText('+ Nova Ação')).toBeInTheDocument()
  })
})


