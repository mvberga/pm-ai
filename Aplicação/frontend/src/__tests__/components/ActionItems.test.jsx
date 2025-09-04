import React from 'react'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import ActionItems from '../../components/ActionItems'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn(), post: jest.fn() }
}))

describe('ActionItems', () => {
  const projectId = '1'

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('lista itens e filtra por tipo', async () => {
    // primeira listagem (sem filtro)
    api.get.mockResolvedValueOnce({ data: [
      { id: 1, title: 'Ação 1', type: 'Ação Pontual' },
      { id: 2, title: 'Bug 1', type: 'Bug' }
    ]})
    // listagem com filtro Bug
    api.get.mockResolvedValueOnce({ data: [
      { id: 2, title: 'Bug 1', type: 'Bug' }
    ]})

    render(<ActionItems projectId={projectId} />)

    await waitFor(() => {
      expect(screen.getByText('Ação 1')).toBeInTheDocument()
      expect(screen.getByText('Bug 1')).toBeInTheDocument()
    })

    fireEvent.change(screen.getByDisplayValue('Todos os tipos'), { target: { value: 'Bug' } })

    await waitFor(() => {
      expect(api.get).toHaveBeenLastCalledWith(`/projects/${projectId}/action-items?type=Bug`)
      expect(screen.queryByText('Ação 1')).not.toBeInTheDocument()
      expect(screen.getByText('Bug 1')).toBeInTheDocument()
    })
  })

  it('permite adicionar nova ação', async () => {
    // listagem inicial
    api.get.mockResolvedValueOnce({ data: [] })
    // post
    api.post.mockResolvedValueOnce({ data: { id: 3 } })
    // listagem após adicionar
    api.get.mockResolvedValueOnce({ data: [ { id: 3, title: 'Nova Ação', type: 'Ação Pontual' } ] })

    jest.spyOn(window, 'prompt').mockImplementation((msg, def) => {
      if (msg.startsWith('Título')) return 'Nova Ação'
      if (msg.startsWith("Tipo")) return 'Ação Pontual'
      return def
    })

    render(<ActionItems projectId={projectId} />)

    fireEvent.click(screen.getByText('+ Nova Ação'))

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith(`/projects/${projectId}/action-items`, { title: 'Nova Ação', type: 'Ação Pontual', status: 'open' })
      expect(screen.getByText('Nova Ação')).toBeInTheDocument()
    })
  })

  it('não adiciona ação quando título é cancelado', async () => {
    api.get.mockResolvedValueOnce({ data: [] })

    jest.spyOn(window, 'prompt').mockReturnValue(null) // Simula cancelar

    render(<ActionItems projectId={projectId} />)

    fireEvent.click(screen.getByText('+ Nova Ação'))

    await waitFor(() => {
      expect(api.post).not.toHaveBeenCalled()
    })
  })

  it('trata erro na listagem de itens', async () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
    api.get.mockRejectedValueOnce(new Error('Erro na API'))

    render(<ActionItems projectId={projectId} />)

    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith(expect.any(Error))
    })

    consoleSpy.mockRestore()
  })


})
