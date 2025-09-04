import { renderHook, act, waitFor } from '@testing-library/react';

// Mock do client.js
jest.mock('../../api/client', () => ({
  __esModule: true,
  default: {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  }
}));

import api from '../../api/client';
import { useProjects } from '../../api/projects';

const mockApi = jest.mocked(api);

describe('useProjects Error Handling', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('fetchProjects error handling', () => {
    it('deve tratar erro 404 ao buscar projetos', async () => {
      const error404 = new Error('Not found');
      mockApi.get.mockRejectedValueOnce(error404);

      const { result } = renderHook(() => useProjects());

      await act(async () => {
        await result.current.fetchProjects();
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe('Not found');
        expect(result.current.projects).toEqual([]);
      });
    });

    it('deve tratar erro de rede ao buscar projetos', async () => {
      const networkError = new Error('Network Error');
      mockApi.get.mockRejectedValueOnce(networkError);

      const { result } = renderHook(() => useProjects());

      await act(async () => {
        await result.current.fetchProjects();
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe('Network Error');
        expect(result.current.projects).toEqual([]);
      });
    });

    it('deve tratar erro 500 ao buscar projetos', async () => {
      const error500 = new Error('Internal server error');
      mockApi.get.mockRejectedValueOnce(error500);

      const { result } = renderHook(() => useProjects());

      await act(async () => {
        await result.current.fetchProjects();
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe('Internal server error');
        expect(result.current.projects).toEqual([]);
      });
    });

    it('deve limpar erro ao tentar buscar novamente', async () => {
      const error = new Error('Initial error');
      mockApi.get
        .mockRejectedValueOnce(error)
        .mockResolvedValueOnce({ data: [] });

      const { result } = renderHook(() => useProjects());

      // Primeira tentativa - erro
      await act(async () => {
        await result.current.fetchProjects();
      });

      await waitFor(() => {
        expect(result.current.error).toBe('Initial error');
      });

      // Segunda tentativa - sucesso
      await act(async () => {
        await result.current.fetchProjects();
      });

      await waitFor(() => {
        expect(result.current.error).toBe(null);
        expect(result.current.projects).toEqual([]);
      });
    });
  });

  describe('createProject error handling', () => {
    it('deve tratar erro 422 ao criar projeto', async () => {
      const error422 = new Error('Validation error');
      mockApi.post.mockRejectedValueOnce(error422);

      const { result } = renderHook(() => useProjects());

      const invalidData = {
        name: '',
        municipio: '',
        tipo: 'test',
        data_inicio: '2024-01-01',
        data_fim: '2024-12-31',
        valor_implantacao: 0,
        valor_recorrente: 0,
        recursos: 0,
        status: 'active',
        gerente_projeto_id: 1,
        gerente_portfolio_id: 1,
        owner_id: 1
      };

      await act(async () => {
        try {
          await result.current.createProject(invalidData);
        } catch (error) {
          // Esperado que lance erro
        }
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe('Validation error');
      });
    });

    it('deve tratar erro 409 ao criar projeto duplicado', async () => {
      const error409 = new Error('Project already exists');
      mockApi.post.mockRejectedValueOnce(error409);

      const { result } = renderHook(() => useProjects());

      const duplicateData = {
        name: 'Projeto Existente',
        municipio: 'Teste',
        tipo: 'test',
        data_inicio: '2024-01-01',
        data_fim: '2024-12-31',
        valor_implantacao: 1000,
        valor_recorrente: 100,
        recursos: 1,
        status: 'active',
        gerente_projeto_id: 1,
        gerente_portfolio_id: 1,
        owner_id: 1
      };

      await act(async () => {
        try {
          await result.current.createProject(duplicateData);
        } catch (error) {
          // Esperado que lance erro
        }
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe('Project already exists');
      });
    });
  });

  describe('updateProject error handling', () => {
    it('deve tratar erro 404 ao atualizar projeto inexistente', async () => {
      const error404 = new Error('Project not found');
      mockApi.put.mockRejectedValueOnce(error404);

      const { result } = renderHook(() => useProjects());

      const updateData = {
        name: 'Projeto Atualizado'
      };

      await act(async () => {
        try {
          await result.current.updateProject(999, updateData);
        } catch (error) {
          // Esperado que lance erro
        }
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe('Project not found');
      });
    });

    it('deve tratar erro 403 ao tentar atualizar projeto sem permissão', async () => {
      const error403 = new Error('Access denied');
      mockApi.put.mockRejectedValueOnce(error403);

      const { result } = renderHook(() => useProjects());

      const updateData = {
        name: 'Projeto Atualizado'
      };

      await act(async () => {
        try {
          await result.current.updateProject(1, updateData);
        } catch (error) {
          // Esperado que lance erro
        }
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe('Access denied');
      });
    });
  });

  describe('deleteProject error handling', () => {
    it('deve tratar erro 404 ao deletar projeto inexistente', async () => {
      const error404 = new Error('Project not found');
      mockApi.delete.mockRejectedValueOnce(error404);

      const { result } = renderHook(() => useProjects());

      await act(async () => {
        try {
          await result.current.deleteProject(999);
        } catch (error) {
          // Esperado que lance erro
        }
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe('Project not found');
      });
    });

    it('deve tratar erro 409 ao deletar projeto com dependências', async () => {
      const error409 = new Error('Cannot delete project with active action items');
      mockApi.delete.mockRejectedValueOnce(error409);

      const { result } = renderHook(() => useProjects());

      await act(async () => {
        try {
          await result.current.deleteProject(1);
        } catch (error) {
          // Esperado que lance erro
        }
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe('Cannot delete project with active action items');
      });
    });
  });

  describe('Filtros com valores inválidos', () => {
    it('deve tratar filtros com valores undefined', async () => {
      mockApi.get.mockResolvedValueOnce({ data: [] });

      const { result } = renderHook(() => useProjects());

      const invalidFilters = {
        status: undefined,
        portfolio: null,
        search: ''
      };

      await act(async () => {
        await result.current.fetchProjects(invalidFilters as any);
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe(null);
      });
    });

    it('deve tratar filtros com arrays vazios', async () => {
      mockApi.get.mockResolvedValueOnce({ data: [] });

      const { result } = renderHook(() => useProjects());

      const emptyFilters = {
        status: '',
        portfolio: '',
        vertical: '',
        municipio: '',
        search: ''
      };

      await act(async () => {
        await result.current.fetchProjects(emptyFilters);
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe(null);
      });
    });
  });

  describe('Estados de loading', () => {
    it('deve manter loading true durante operações assíncronas', async () => {
      let resolvePromise: (value: any) => void;
      const promise = new Promise((resolve) => {
        resolvePromise = resolve;
      });
      
      mockApi.get.mockReturnValueOnce(promise as any);

      const { result } = renderHook(() => useProjects());

      act(() => {
        result.current.fetchProjects();
      });

      expect(result.current.loading).toBe(true);

      await act(async () => {
        resolvePromise!([]);
        await promise;
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });
    });
  });
});
