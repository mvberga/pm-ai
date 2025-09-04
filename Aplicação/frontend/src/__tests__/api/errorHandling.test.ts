// Mock do client.js (ESM compatível)
jest.mock('../../api/client', () => ({
  __esModule: true,
  default: {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  }
}));

import { projectsApi } from '../../api/projects';
import api from '../../api/client';

const mockAxios = jest.mocked(api);

describe('API Error Handling', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('projectsApi.getAll', () => {
    it('deve tratar erro 404 corretamente', async () => {
      const error404 = {
        response: {
          status: 404,
          data: { detail: 'Not found' }
        }
      };
      mockAxios.get.mockRejectedValueOnce(error404);

      await expect(projectsApi.getAll()).rejects.toEqual(error404);
    });

    it('deve tratar erro 500 corretamente', async () => {
      const error500 = {
        response: {
          status: 500,
          data: { detail: 'Internal server error' }
        }
      };
      mockAxios.get.mockRejectedValueOnce(error500);

      await expect(projectsApi.getAll()).rejects.toEqual(error500);
    });

    it('deve tratar erro de rede corretamente', async () => {
      const networkError = new Error('Network Error');
      mockAxios.get.mockRejectedValueOnce(networkError);

      await expect(projectsApi.getAll()).rejects.toEqual(networkError);
    });

    it('deve tratar timeout corretamente', async () => {
      const timeoutError = {
        code: 'ECONNABORTED',
        message: 'timeout of 5000ms exceeded'
      };
      mockAxios.get.mockRejectedValueOnce(timeoutError);

      await expect(projectsApi.getAll()).rejects.toEqual(timeoutError);
    });
  });

  describe('projectsApi.getById', () => {
    it('deve tratar erro 404 para projeto não encontrado', async () => {
      const error404 = {
        response: {
          status: 404,
          data: { detail: 'Project not found' }
        }
      };
      mockAxios.get.mockRejectedValueOnce(error404);

      await expect(projectsApi.getById(999)).rejects.toEqual(error404);
    });

    it('deve tratar erro 403 para acesso negado', async () => {
      const error403 = {
        response: {
          status: 403,
          data: { detail: 'Access denied' }
        }
      };
      mockAxios.get.mockRejectedValueOnce(error403);

      await expect(projectsApi.getById(1)).rejects.toEqual(error403);
    });
  });

  describe('projectsApi.create', () => {
    it('deve tratar erro 422 para dados inválidos', async () => {
      const error422 = {
        response: {
          status: 422,
          data: { 
            detail: 'Validation error',
            errors: {
              name: ['This field is required'],
              municipio: ['This field is required']
            }
          }
        }
      };
      mockAxios.post.mockRejectedValueOnce(error422);

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

      await expect(projectsApi.create(invalidData)).rejects.toEqual(error422);
    });

    it('deve tratar erro 409 para conflito (projeto já existe)', async () => {
      const error409 = {
        response: {
          status: 409,
          data: { detail: 'Project already exists' }
        }
      };
      mockAxios.post.mockRejectedValueOnce(error409);

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

      await expect(projectsApi.create(duplicateData)).rejects.toEqual(error409);
    });
  });

  describe('projectsApi.update', () => {
    it('deve tratar erro 400 para dados malformados', async () => {
      const error400 = {
        response: {
          status: 400,
          data: { detail: 'Bad request' }
        }
      };
      mockAxios.put.mockRejectedValueOnce(error400);

      const malformedData = {
        name: null,
        valor_implantacao: 'invalid'
      };

      await expect(projectsApi.update(1, malformedData)).rejects.toEqual(error400);
    });
  });

  describe('projectsApi.delete', () => {
    it('deve tratar erro 404 para projeto não encontrado', async () => {
      const error404 = {
        response: {
          status: 404,
          data: { detail: 'Project not found' }
        }
      };
      mockAxios.delete.mockRejectedValueOnce(error404);

      await expect(projectsApi.delete(999)).rejects.toEqual(error404);
    });

    it('deve tratar erro 409 para projeto com dependências', async () => {
      const error409 = {
        response: {
          status: 409,
          data: { detail: 'Cannot delete project with active action items' }
        }
      };
      mockAxios.delete.mockRejectedValueOnce(error409);

      await expect(projectsApi.delete(1)).rejects.toEqual(error409);
    });
  });

  describe('Filtros com parâmetros inválidos', () => {
    it('deve tratar filtros com caracteres especiais', async () => {
      const filters = {
        search: 'test<script>alert("xss")</script>',
        municipio: 'São Paulo; DROP TABLE projects;'
      };

      mockAxios.get.mockResolvedValueOnce({ data: [] });

      await projectsApi.getAll(filters);

      expect(mockAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('search=test%3Cscript%3Ealert%28%22xss%22%29%3C%2Fscript%3E')
      );
    });

    it('deve tratar filtros com valores muito longos', async () => {
      const longString = 'a'.repeat(10000);
      const filters = {
        search: longString
      };

      mockAxios.get.mockResolvedValueOnce({ data: [] });

      await projectsApi.getAll(filters);

      expect(mockAxios.get).toHaveBeenCalledWith(
        expect.stringContaining(`search=${encodeURIComponent(longString)}`)
      );
    });
  });

  describe('Recuperação de erro', () => {
    it('deve retry em caso de erro temporário', async () => {
      const temporaryError = {
        response: {
          status: 503,
          data: { detail: 'Service temporarily unavailable' }
        }
      };

      mockAxios.get
        .mockRejectedValueOnce(temporaryError)
        .mockResolvedValueOnce({ data: [] });

      // Simula retry manual
      let result;
      try {
        result = await projectsApi.getAll();
      } catch (error) {
        // Primeira tentativa falha, tenta novamente
        result = await projectsApi.getAll();
      }

      expect(result).toEqual([]);
      expect(mockAxios.get).toHaveBeenCalledTimes(2);
    });
  });
});
