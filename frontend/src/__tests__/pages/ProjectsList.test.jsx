import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProjectsList from '../../pages/ProjectsList'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn() }
}))

describe('ProjectsList', () => {
  it('lista projetos recebidos da API', async () => {
    api.get.mockResolvedValueOnce({ data: [
      { id: 1, name: 'Projeto A' },
      { id: 2, name: 'Projeto B' }
    ]})

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
    })
  })
})


