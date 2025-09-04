import { renderHook, act } from '@testing-library/react';
import { projectsApi, useProjects, useProjectsMetrics } from '../../api/projects';
import api from '../../api/client';
import type { ProjectFilters, ProjectCreateRequest, ProjectUpdateRequest } from '../../types/portfolio';

// Mock do cliente API
jest.mock('../../api/client', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
}));

const mockApi = api as jest.Mocked<typeof api>;

describe('projectsApi', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getAll', () => {
    it('deve buscar todos os projetos sem filtros', async () => {
      const mockProjects = [
        { id: 1, name: 'Projeto A', status: 'active' },
        { id: 2, name: 'Projeto B', status: 'completed' }
      ];
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.getAll();

      expect(mockApi.get).toHaveBeenCalledWith('/projects?');
      expect(result).toEqual(mockProjects);
    });

    it('deve buscar projetos com filtros', async () => {
      const mockProjects = [{ id: 1, name: 'Projeto A', status: 'active' }];
      const filters: ProjectFilters = {
        status: 'active',
        portfolio: 'portfolio1',
        search: 'teste'
      };
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.getAll(filters);

      expect(mockApi.get).toHaveBeenCalledWith('/projects?status=active&portfolio=portfolio1&search=teste');
      expect(result).toEqual(mockProjects);
    });
  });

  describe('getById', () => {
    it('deve buscar projeto por ID', async () => {
      const mockProject = { id: 1, name: 'Projeto A', status: 'active' };
      
      mockApi.get.mockResolvedValue({ data: mockProject });

      const result = await projectsApi.getById(1);

      expect(mockApi.get).toHaveBeenCalledWith('/projects/1');
      expect(result).toEqual(mockProject);
    });
  });

  describe('create', () => {
    it('deve criar novo projeto', async () => {
      const mockProject = { id: 1, name: 'Novo Projeto', status: 'active' };
      const projectData: ProjectCreateRequest = {
        name: 'Novo Projeto',
        municipio: 'São Paulo',
        tipo: 'implementacao',
        data_inicio: '2024-01-01',
        data_fim: '2024-12-31',
        valor_implantacao: 100000,
        valor_recorrente: 10000,
        recursos: 5,
        status: 'active',
        gerente_projeto_id: 1,
        gerente_portfolio_id: 1,
        owner_id: 1
      };
      
      mockApi.post.mockResolvedValue({ data: mockProject });

      const result = await projectsApi.create(projectData);

      expect(mockApi.post).toHaveBeenCalledWith('/projects', projectData);
      expect(result).toEqual(mockProject);
    });
  });

  describe('update', () => {
    it('deve atualizar projeto', async () => {
      const mockProject = { id: 1, name: 'Projeto Atualizado', status: 'active' };
      const updateData: ProjectUpdateRequest = {
        name: 'Projeto Atualizado',
        status: 'completed'
      };
      
      mockApi.put.mockResolvedValue({ data: mockProject });

      const result = await projectsApi.update(1, updateData);

      expect(mockApi.put).toHaveBeenCalledWith('/projects/1', updateData);
      expect(result).toEqual(mockProject);
    });
  });

  describe('delete', () => {
    it('deve deletar projeto', async () => {
      mockApi.delete.mockResolvedValue(undefined);

      await projectsApi.delete(1);

      expect(mockApi.delete).toHaveBeenCalledWith('/projects/1');
    });
  });

  describe('getStats', () => {
    it('deve obter estatísticas dos projetos', async () => {
      const mockStats = {
        total: 10,
        active: 5,
        completed: 3,
        delayed: 2
      };
      
      mockApi.get.mockResolvedValue({ data: mockStats });

      const result = await projectsApi.getStats();

      expect(mockApi.get).toHaveBeenCalledWith('/projects/stats');
      expect(result).toEqual(mockStats);
    });
  });

  describe('getWithActionItems', () => {
    it('deve buscar projetos com action items', async () => {
      const mockProjects = [
        { id: 1, name: 'Projeto A', pending_actions_count: 2 }
      ];
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.getWithActionItems();

      expect(mockApi.get).toHaveBeenCalledWith('/projects?include_action_items=true');
      expect(result).toEqual(mockProjects);
    });

    it('deve buscar projetos com action items e filtros', async () => {
      const mockProjects = [{ id: 1, name: 'Projeto A', pending_actions_count: 2 }];
      const filters: ProjectFilters = { status: 'active' };
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.getWithActionItems(filters);

      expect(mockApi.get).toHaveBeenCalledWith('/projects?include_action_items=true&status=active');
      expect(result).toEqual(mockProjects);
    });
  });

  describe('search', () => {
    it('deve buscar projetos por texto', async () => {
      const mockProjects = [{ id: 1, name: 'Projeto Teste' }];
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.search('teste');

      expect(mockApi.get).toHaveBeenCalledWith('/projects/search?q=teste');
      expect(result).toEqual(mockProjects);
    });

    it('deve codificar caracteres especiais na busca', async () => {
      const mockProjects = [{ id: 1, name: 'Projeto & Teste' }];
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.search('teste & projeto');

      expect(mockApi.get).toHaveBeenCalledWith('/projects/search?q=teste%20%26%20projeto');
      expect(result).toEqual(mockProjects);
    });
  });

  describe('getByStatus', () => {
    it('deve buscar projetos por status', async () => {
      const mockProjects = [{ id: 1, name: 'Projeto A', status: 'active' }];
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.getByStatus('active');

      expect(mockApi.get).toHaveBeenCalledWith('/projects?status=active');
      expect(result).toEqual(mockProjects);
    });
  });

  describe('getByPortfolio', () => {
    it('deve buscar projetos por portfólio', async () => {
      const mockProjects = [{ id: 1, name: 'Projeto A', portfolio: 'portfolio1' }];
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.getByPortfolio('portfolio1');

      expect(mockApi.get).toHaveBeenCalledWith('/projects?portfolio=portfolio1');
      expect(result).toEqual(mockProjects);
    });
  });

  describe('getByVertical', () => {
    it('deve buscar projetos por vertical', async () => {
      const mockProjects = [{ id: 1, name: 'Projeto A', vertical: 'vertical1' }];
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.getByVertical('vertical1');

      expect(mockApi.get).toHaveBeenCalledWith('/projects?vertical=vertical1');
      expect(result).toEqual(mockProjects);
    });
  });

  describe('getByMunicipio', () => {
    it('deve buscar projetos por município', async () => {
      const mockProjects = [{ id: 1, name: 'Projeto A', municipio: 'São Paulo' }];
      
      mockApi.get.mockResolvedValue({ data: mockProjects });

      const result = await projectsApi.getByMunicipio('São Paulo');

      expect(mockApi.get).toHaveBeenCalledWith('/projects?municipio=S%C3%A3o%20Paulo');
      expect(result).toEqual(mockProjects);
    });
  });
});

describe('useProjects', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('deve inicializar com estado vazio', () => {
    const { result } = renderHook(() => useProjects());

    expect(result.current.projects).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve buscar projetos com sucesso', async () => {
    const mockProjects = [
      { id: 1, name: 'Projeto A', pending_actions_count: 2 }
    ];
    
    mockApi.get.mockResolvedValue({ data: mockProjects });

    const { result } = renderHook(() => useProjects());

    await act(async () => {
      await result.current.fetchProjects();
    });

    expect(result.current.projects).toEqual(mockProjects);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve tratar erro ao buscar projetos', async () => {
    const errorMessage = 'Erro de rede';
    mockApi.get.mockRejectedValue(new Error(errorMessage));

    const { result } = renderHook(() => useProjects());

    await act(async () => {
      await result.current.fetchProjects();
    });

    expect(result.current.projects).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(errorMessage);
  });

  it('deve criar projeto com sucesso', async () => {
    const mockProject = { id: 1, name: 'Novo Projeto' };
    const projectData: ProjectCreateRequest = {
      name: 'Novo Projeto',
      municipio: 'São Paulo',
      tipo: 'implementacao',
      data_inicio: '2024-01-01',
      data_fim: '2024-12-31',
      valor_implantacao: 100000,
      valor_recorrente: 10000,
      recursos: 5,
      status: 'active',
      gerente_projeto_id: 1,
      gerente_portfolio_id: 1,
      owner_id: 1
    };
    
    mockApi.post.mockResolvedValue({ data: mockProject });

    const { result } = renderHook(() => useProjects());

    let createdProject;
    await act(async () => {
      createdProject = await result.current.createProject(projectData);
    });

    expect(createdProject).toEqual(mockProject);
    expect(result.current.projects).toContain(mockProject);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve atualizar projeto com sucesso', async () => {
    const existingProject = { id: 1, name: 'Projeto Original' };
    const updatedProject = { id: 1, name: 'Projeto Atualizado' };
    const updateData: ProjectUpdateRequest = { name: 'Projeto Atualizado' };
    
    mockApi.put.mockResolvedValue({ data: updatedProject });

    const { result } = renderHook(() => useProjects());

    // Primeiro adiciona um projeto
    await act(async () => {
      result.current.projects.push(existingProject);
    });

    let updated;
    await act(async () => {
      updated = await result.current.updateProject(1, updateData);
    });

    expect(updated).toEqual(updatedProject);
    expect(result.current.projects).toContain(updatedProject);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve deletar projeto com sucesso', async () => {
    const projectToDelete = { id: 1, name: 'Projeto para Deletar' };
    
    mockApi.delete.mockResolvedValue(undefined);

    const { result } = renderHook(() => useProjects());

    // Primeiro adiciona um projeto
    await act(async () => {
      result.current.projects.push(projectToDelete);
    });

    await act(async () => {
      await result.current.deleteProject(1);
    });

    expect(result.current.projects).not.toContain(projectToDelete);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });
});

describe('useProjectsMetrics', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('deve inicializar com estado vazio', () => {
    const { result } = renderHook(() => useProjectsMetrics());

    expect(result.current.metrics).toBe(null);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve buscar métricas com sucesso', async () => {
    const mockMetrics = {
      total_projects: 10,
      active_projects: 5,
      completed_projects: 3,
      delayed_projects: 2,
      total_value: 1000000,
      pending_actions: 15
    };
    
    mockApi.get.mockResolvedValue({ data: mockMetrics });

    const { result } = renderHook(() => useProjectsMetrics());

    await act(async () => {
      await result.current.fetchMetrics();
    });

    expect(result.current.metrics).toEqual(mockMetrics);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve tratar erro ao buscar métricas', async () => {
    const errorMessage = 'Erro ao carregar métricas';
    mockApi.get.mockRejectedValue(new Error(errorMessage));

    const { result } = renderHook(() => useProjectsMetrics());

    await act(async () => {
      await result.current.fetchMetrics();
    });

    expect(result.current.metrics).toBe(null);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(errorMessage);
  });
});
