import React from 'react'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import Checklist from '../../components/Checklist'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn(), post: jest.fn() }
}))

describe('Checklist', () => {
  const projectId = '1'

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('lista grupos ao montar e permite adicionar grupo', async () => {
    api.get.mockResolvedValueOnce({ data: [{ id: 10, name: 'Inicial' }] })
    api.post.mockResolvedValueOnce({ data: { id: 11, name: 'Novo' } })
    api.get.mockResolvedValueOnce({ data: [{ id: 10, name: 'Inicial' }, { id: 11, name: 'Novo' }] })

    render(<Checklist projectId={projectId} />)

    // lista inicial
    await waitFor(() => {
      expect(screen.getByText('Inicial')).toBeInTheDocument()
    })

    // adiciona
    fireEvent.change(screen.getByPlaceholderText('Novo grupo'), { target: { value: 'Novo' } })
    fireEvent.click(screen.getByText('Adicionar Grupo'))

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith(`/projects/${projectId}/checklist-groups`, { name: 'Novo' })
      expect(screen.getByText('Novo')).toBeInTheDocument()
    })
  })

  it('adiciona item ao clicar em + Item (usando prompts)', async () => {
    api.get.mockResolvedValueOnce({ data: [{ id: 10, name: 'Grupo' }] })
    api.post.mockResolvedValueOnce({})
    api.get.mockResolvedValueOnce({ data: [{ id: 10, name: 'Grupo' }] })

    jest.spyOn(window, 'prompt').mockReturnValue('Título Teste')
    jest.spyOn(window, 'confirm').mockReturnValue(true)

    render(<Checklist projectId={projectId} />)

    await waitFor(() => {
      expect(screen.getByText('Grupo')).toBeInTheDocument()
    })

    fireEvent.click(screen.getByText('+ Item'))

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith(`/checklist-groups/10/items`, { title: 'Título Teste', type: 'Documentação', notes: '' })
    })
  })

  it('não adiciona grupo quando nome está vazio', async () => {
    api.get.mockResolvedValueOnce({ data: [] })

    render(<Checklist projectId={projectId} />)

    fireEvent.click(screen.getByText('Adicionar Grupo'))

    await waitFor(() => {
      expect(api.post).not.toHaveBeenCalled()
    })
  })

  it('não adiciona item quando título é cancelado', async () => {
    api.get.mockResolvedValueOnce({ data: [{ id: 10, name: 'Grupo' }] })

    jest.spyOn(window, 'prompt').mockReturnValue(null) // Simula cancelar

    render(<Checklist projectId={projectId} />)

    await waitFor(() => {
      expect(screen.getByText('Grupo')).toBeInTheDocument()
    })

    fireEvent.click(screen.getByText('+ Item'))

    await waitFor(() => {
      expect(api.post).not.toHaveBeenCalled()
    })
  })

  it('adiciona item como Ação quando confirm é false', async () => {
    api.get.mockResolvedValueOnce({ data: [{ id: 10, name: 'Grupo' }] })
    api.post.mockResolvedValueOnce({})
    api.get.mockResolvedValueOnce({ data: [{ id: 10, name: 'Grupo' }] })

    jest.spyOn(window, 'prompt').mockReturnValue('Título Teste')
    jest.spyOn(window, 'confirm').mockReturnValue(false) // Não é documentação

    render(<Checklist projectId={projectId} />)

    await waitFor(() => {
      expect(screen.getByText('Grupo')).toBeInTheDocument()
    })

    fireEvent.click(screen.getByText('+ Item'))

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith(`/checklist-groups/10/items`, { title: 'Título Teste', type: 'Ação', notes: '' })
    })
  })

  it('trata erro na listagem de grupos', async () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
    api.get.mockRejectedValueOnce(new Error('Erro na API'))

    render(<Checklist projectId={projectId} />)

    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith(expect.any(Error))
    })

    consoleSpy.mockRestore()
  })


})


