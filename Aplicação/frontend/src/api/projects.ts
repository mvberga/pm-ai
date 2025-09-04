import { useState } from 'react';
import api from './client';
import type { 
  Project, 
  ProjectWithActions, 
  ProjectFilters, 
  ProjectStats,
  PortfolioMetrics,
  ProjectCreateRequest,
  ProjectUpdateRequest 
} from '../types/portfolio';

// Tipos para requisições
export interface ProjectCreateRequest {
  name: string;
  municipio: string;
  entidade?: string;
  chamado_jira?: string;
  portfolio?: string;
  vertical?: string;
  product?: string;
  tipo: string;
  data_inicio: string;
  data_fim: string;
  etapa_atual?: string;
  valor_implantacao: number;
  valor_recorrente: number;
  recursos: number;
  status: string;
  gerente_projeto_id: number;
  gerente_portfolio_id: number;
  owner_id: number;
}

export interface ProjectUpdateRequest {
  name?: string;
  municipio?: string;
  entidade?: string;
  chamado_jira?: string;
  portfolio?: string;
  vertical?: string;
  product?: string;
  tipo?: string;
  data_inicio?: string;
  data_fim?: string;
  etapa_atual?: string;
  valor_implantacao?: number;
  valor_recorrente?: number;
  recursos?: number;
  status?: string;
  gerente_projeto_id?: number;
  gerente_portfolio_id?: number;
  owner_id?: number;
}

// Serviços de API para projetos
export const projectsApi = {
  // Listar todos os projetos
  async getAll(filters?: ProjectFilters): Promise<ProjectWithActions[]> {
    const params = new URLSearchParams();
    
    if (filters?.status) params.append('status', filters.status);
    if (filters?.portfolio) params.append('portfolio', filters.portfolio);
    if (filters?.vertical) params.append('vertical', filters.vertical);
    if (filters?.municipio) params.append('municipio', filters.municipio);
    if (filters?.search) params.append('search', filters.search);
    
    const response = await api.get(`/projects?${params.toString()}`);
    return response.data;
  },

  // Buscar projeto por ID
  async getById(id: number): Promise<ProjectWithActions> {
    const response = await api.get(`/projects/${id}`);
    return response.data;
  },

  // Criar novo projeto
  async create(data: ProjectCreateRequest): Promise<Project> {
    const response = await api.post('/projects', data);
    return response.data;
  },

  // Atualizar projeto
  async update(id: number, data: ProjectUpdateRequest): Promise<Project> {
    const response = await api.put(`/projects/${id}`, data);
    return response.data;
  },

  // Deletar projeto
  async delete(id: number): Promise<void> {
    await api.delete(`/projects/${id}`);
  },

  // Obter estatísticas dos projetos
  async getStats(): Promise<ProjectStats> {
    const response = await api.get('/projects/stats');
    return response.data;
  },

  // Obter projetos com contagem de action items
  async getWithActionItems(filters?: ProjectFilters): Promise<ProjectWithActions[]> {
    const params = new URLSearchParams();
    params.append('include_action_items', 'true');
    
    if (filters?.status) params.append('status', filters.status);
    if (filters?.portfolio) params.append('portfolio', filters.portfolio);
    if (filters?.vertical) params.append('vertical', filters.vertical);
    if (filters?.municipio) params.append('municipio', filters.municipio);
    if (filters?.search) params.append('search', filters.search);
    
    const response = await api.get(`/projects?${params.toString()}`);
    return response.data;
  },

  // Buscar projetos por texto
  async search(query: string): Promise<ProjectWithActions[]> {
    const response = await api.get(`/projects/search?q=${encodeURIComponent(query)}`);
    return response.data;
  },

  // Obter projetos por status
  async getByStatus(status: string): Promise<ProjectWithActions[]> {
    const response = await api.get(`/projects?status=${status}`);
    return response.data;
  },

  // Obter projetos por portfólio
  async getByPortfolio(portfolio: string): Promise<ProjectWithActions[]> {
    const response = await api.get(`/projects?portfolio=${encodeURIComponent(portfolio)}`);
    return response.data;
  },

  // Obter projetos por vertical
  async getByVertical(vertical: string): Promise<ProjectWithActions[]> {
    const response = await api.get(`/projects?vertical=${encodeURIComponent(vertical)}`);
    return response.data;
  },

  // Obter projetos por município
  async getByMunicipio(municipio: string): Promise<ProjectWithActions[]> {
    const response = await api.get(`/projects?municipio=${encodeURIComponent(municipio)}`);
    return response.data;
  }
};

// Hook personalizado para projetos (para uso em componentes React)
export const useProjects = () => {
  const [projects, setProjects] = useState<ProjectWithActions[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = async (filters?: ProjectFilters) => {
    try {
      setLoading(true);
      setError(null);
      const data = await projectsApi.getWithActionItems(filters);
      setProjects(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar projetos');
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (data: ProjectCreateRequest) => {
    try {
      setLoading(true);
      setError(null);
      const newProject = await projectsApi.create(data);
      setProjects(prev => [...prev, newProject]);
      return newProject;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar projeto');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateProject = async (id: number, data: ProjectUpdateRequest) => {
    try {
      setLoading(true);
      setError(null);
      const updatedProject = await projectsApi.update(id, data);
      setProjects(prev => prev.map(p => p.id === id ? updatedProject : p));
      return updatedProject;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar projeto');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteProject = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await projectsApi.delete(id);
      setProjects(prev => prev.filter(p => p.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao deletar projeto');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    projects,
    loading,
    error,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject,
  };
};



// Hook para métricas do portfólio
export const useProjectsMetrics = () => {
  const [metrics, setMetrics] = useState<PortfolioMetrics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/projects/metrics');
      setMetrics(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar métricas');
    } finally {
      setLoading(false);
    }
  };

  return {
    metrics,
    loading,
    error,
    fetchMetrics,
  };
};
