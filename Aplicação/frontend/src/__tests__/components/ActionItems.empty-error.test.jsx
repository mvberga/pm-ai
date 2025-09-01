import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import ActionItems from '../../components/ActionItems'
import api from '../../api/client'

jest.mock('../../api/client', () => ({
  __esModule: true,
  default: { get: jest.fn() }
}))

describe('ActionItems - estados vazios e erro', () => {
  const projectId = '1'

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('lista vazia sem quebrar', async () => {
    api.get.mockResolvedValueOnce({ data: [] })
    render(<ActionItems projectId={projectId} />)
    await waitFor(() => {
      expect(screen.queryByRole('listitem')).not.toBeInTheDocument()
    })
  })

  it('faz catch de erro sem lançar', async () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
    api.get.mockRejectedValueOnce(new Error('falha'))
    render(<ActionItems projectId={projectId} />)
    // espera ciclo
    await new Promise(r => setTimeout(r, 0))
    consoleSpy.mockRestore()
  })
})


