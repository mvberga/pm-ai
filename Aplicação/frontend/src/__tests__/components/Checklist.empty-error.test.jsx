import React from 'react'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import Checklist from '../../components/Checklist'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn(), post: jest.fn() }
}))

describe('Checklist - estados vazios e erro', () => {
  const projectId = '1'

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renderiza sem grupos (vazio)', async () => {
    api.get.mockResolvedValueOnce({ data: [] })
    render(<Checklist projectId={projectId} />)
    await waitFor(() => {
      // Sem qualquer grupo renderizado
      expect(screen.queryByText(/Itens aparecem/)).not.toBeInTheDocument()
      expect(screen.queryByText('+ Item')).not.toBeInTheDocument()
    })
  })

  it('não adiciona grupo com input vazio', async () => {
    api.get.mockResolvedValueOnce({ data: [] })
    render(<Checklist projectId={projectId} />)
    fireEvent.click(screen.getByText('Adicionar Grupo'))
    expect(api.post).not.toHaveBeenCalled()
  })
})


