import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProjectDetail from '../../pages/ProjectDetail'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn() }
}))

describe('ProjectDetail - estados vazios e erro', () => {
  it('exibe carregando e não quebra em erro de detalhes', async () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
    api.get.mockRejectedValueOnce(new Error('falha'))

    render(
      <MemoryRouter initialEntries={['/projects/1']}>
        <Routes>
          <Route path="/projects/:id" element={<ProjectDetail />} />
        </Routes>
      </MemoryRouter>
    )

    expect(screen.getByText('Carregando...')).toBeInTheDocument()

    // aguarda efeito terminar
    await new Promise(r => setTimeout(r, 0))

    consoleSpy.mockRestore()
  })
})


