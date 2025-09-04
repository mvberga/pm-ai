import api from '../../api/client';

// Mock do axios
jest.mock('axios', () => ({
  create: jest.fn(() => ({
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  })),
}));

describe('API Client', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('deve configurar baseURL corretamente para ambiente de teste', () => {
    // Simula ambiente de teste
    const originalEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'test';

    // Re-importa o módulo para testar a configuração
    jest.resetModules();
    const axios = require('axios');
    const apiClient = require('../../api/client').default;

    expect(axios.create).toHaveBeenCalledWith({
      baseURL: 'http://localhost:8000/api/v1'
    });

    // Restaura o ambiente original
    process.env.NODE_ENV = originalEnv;
  });

  it('deve configurar baseURL corretamente para ambiente de desenvolvimento', () => {
    // Simula ambiente de desenvolvimento
    const originalEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'development';

    // Re-importa o módulo para testar a configuração
    jest.resetModules();
    const axios = require('axios');
    const apiClient = require('../../api/client').default;

    expect(axios.create).toHaveBeenCalledWith({
      baseURL: 'http://localhost:8000/api/v1'
    });

    // Restaura o ambiente original
    process.env.NODE_ENV = originalEnv;
  });

  it('deve configurar baseURL corretamente para ambiente de produção', () => {
    // Simula ambiente de produção
    const originalEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'production';

    // Re-importa o módulo para testar a configuração
    jest.resetModules();
    const axios = require('axios');
    const apiClient = require('../../api/client').default;

    expect(axios.create).toHaveBeenCalledWith({
      baseURL: 'http://localhost:8000/api/v1'
    });

    // Restaura o ambiente original
    process.env.NODE_ENV = originalEnv;
  });

  it('deve exportar instância do axios', () => {
    expect(api).toBeDefined();
    expect(typeof api.get).toBe('function');
    expect(typeof api.post).toBe('function');
    expect(typeof api.put).toBe('function');
    expect(typeof api.delete).toBe('function');
  });
});
