import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProjectsList from '../../pages/ProjectsList'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn() }
}))

describe('ProjectsList - estados vazios e erro', () => {
  it('exibe lista vazia sem quebrar', async () => {
    api.get.mockResolvedValueOnce({ data: [] })

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

  it('faz catch de erro da API sem lançar', async () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
    api.get.mockRejectedValueOnce(new Error('falha'))

    render(
      <MemoryRouter initialEntries={['/projects']}>
        <Routes>
          <Route path="/projects" element={<ProjectsList />} />
        </Routes>
      </MemoryRouter>
    )

    expect(screen.getByText('Projetos')).toBeInTheDocument()

    await waitFor(() => {
      // Continua renderizando sem links
      expect(screen.queryByRole('link')).not.toBeInTheDocument()
    })

    consoleSpy.mockRestore()
  })
})


