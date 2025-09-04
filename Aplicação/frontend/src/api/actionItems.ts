import api from './client';
import type { 
  ActionItem, 
  ActionItemFilters, 
  ActionItemCreateRequest, 
  ActionItemUpdateRequest,
  ActionItemStats,
  ProjectActionItemSummary 
} from '../types/actionItems';

// Serviços de API para action items
export const actionItemsApi = {
  // Listar todos os action items
  async getAll(filters?: ActionItemFilters): Promise<ActionItem[]> {
    const params = new URLSearchParams();
    
    if (filters?.type) params.append('type', filters.type);
    if (filters?.status) params.append('status', filters.status);
    if (filters?.priority) params.append('priority', filters.priority);
    if (filters?.project_id) params.append('project_id', filters.project_id.toString());
    
    const response = await api.get(`/action-items?${params.toString()}`);
    return response.data;
  },

  // Buscar action item por ID
  async getById(id: number): Promise<ActionItem> {
    const response = await api.get(`/action-items/${id}`);
    return response.data;
  },

  // Criar novo action item
  async create(data: ActionItemCreateRequest): Promise<ActionItem> {
    const response = await api.post('/action-items', data);
    return response.data;
  },

  // Atualizar action item
  async update(id: number, data: ActionItemUpdateRequest): Promise<ActionItem> {
    const response = await api.put(`/action-items/${id}`, data);
    return response.data;
  },

  // Deletar action item
  async delete(id: number): Promise<void> {
    await api.delete(`/action-items/${id}`);
  },

  // Obter action items de um projeto específico
  async getByProject(projectId: number, filters?: Omit<ActionItemFilters, 'project_id'>): Promise<ActionItem[]> {
    const params = new URLSearchParams();
    
    if (filters?.type) params.append('type', filters.type);
    if (filters?.status) params.append('status', filters.status);
    if (filters?.priority) params.append('priority', filters.priority);
    
    const response = await api.get(`/projects/${projectId}/action-items?${params.toString()}`);
    return response.data;
  },

  // Obter estatísticas dos action items
  async getStats(projectId?: number): Promise<ActionItemStats> {
    const url = projectId 
      ? `/projects/${projectId}/action-items/stats`
      : '/action-items/stats';
    
    const response = await api.get(url);
    return response.data;
  },

  // Obter resumo de action items por projeto
  async getProjectSummary(): Promise<ProjectActionItemSummary[]> {
    const response = await api.get('/action-items/project-summary');
    return response.data;
  },

  // Buscar action items por texto
  async search(query: string, projectId?: number): Promise<ActionItem[]> {
    const url = projectId 
      ? `/projects/${projectId}/action-items/search?q=${encodeURIComponent(query)}`
      : `/action-items/search?q=${encodeURIComponent(query)}`;
    
    const response = await api.get(url);
    return response.data;
  },

  // Obter action items por status
  async getByStatus(status: string, projectId?: number): Promise<ActionItem[]> {
    const url = projectId 
      ? `/projects/${projectId}/action-items?status=${status}`
      : `/action-items?status=${status}`;
    
    const response = await api.get(url);
    return response.data;
  },

  // Obter action items por tipo
  async getByType(type: string, projectId?: number): Promise<ActionItem[]> {
    const url = projectId 
      ? `/projects/${projectId}/action-items?type=${type}`
      : `/action-items?type=${type}`;
    
    const response = await api.get(url);
    return response.data;
  },

  // Obter action items por prioridade
  async getByPriority(priority: string, projectId?: number): Promise<ActionItem[]> {
    const url = projectId 
      ? `/projects/${projectId}/action-items?priority=${priority}`
      : `/action-items?priority=${priority}`;
    
    const response = await api.get(url);
    return response.data;
  },

  // Obter action items pendentes
  async getPending(projectId?: number): Promise<ActionItem[]> {
    return this.getByStatus('pending', projectId);
  },

  // Obter action items em progresso
  async getInProgress(projectId?: number): Promise<ActionItem[]> {
    return this.getByStatus('in_progress', projectId);
  },

  // Obter action items concluídos
  async getCompleted(projectId?: number): Promise<ActionItem[]> {
    return this.getByStatus('completed', projectId);
  },

  // Obter action items vencidos
  async getOverdue(projectId?: number): Promise<ActionItem[]> {
    const url = projectId 
      ? `/projects/${projectId}/action-items/overdue`
      : '/action-items/overdue';
    
    const response = await api.get(url);
    return response.data;
  },

  // Marcar action item como concluído
  async markAsCompleted(id: number): Promise<ActionItem> {
    return this.update(id, { status: 'completed' });
  },

  // Marcar action item como em progresso
  async markAsInProgress(id: number): Promise<ActionItem> {
    return this.update(id, { status: 'in_progress' });
  },

  // Marcar action item como pendente
  async markAsPending(id: number): Promise<ActionItem> {
    return this.update(id, { status: 'pending' });
  },

  // Cancelar action item
  async cancel(id: number): Promise<ActionItem> {
    return this.update(id, { status: 'cancelled' });
  },

  // Colocar action item em espera
  async putOnHold(id: number): Promise<ActionItem> {
    return this.update(id, { status: 'on_hold' });
  }
};

// Hook personalizado para action items (para uso em componentes React)
export const useActionItems = (projectId?: number) => {
  const [actionItems, setActionItems] = useState<ActionItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchActionItems = async (filters?: ActionItemFilters) => {
    try {
      setLoading(true);
      setError(null);
      const data = projectId 
        ? await actionItemsApi.getByProject(projectId, filters)
        : await actionItemsApi.getAll({ ...filters, project_id: projectId });
      setActionItems(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar action items');
    } finally {
      setLoading(false);
    }
  };

  const createActionItem = async (data: ActionItemCreateRequest) => {
    try {
      setLoading(true);
      setError(null);
      const newActionItem = await actionItemsApi.create(data);
      setActionItems(prev => [...prev, newActionItem]);
      return newActionItem;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar action item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateActionItem = async (id: number, data: ActionItemUpdateRequest) => {
    try {
      setLoading(true);
      setError(null);
      const updatedActionItem = await actionItemsApi.update(id, data);
      setActionItems(prev => prev.map(item => item.id === id ? updatedActionItem : item));
      return updatedActionItem;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar action item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteActionItem = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await actionItemsApi.delete(id);
      setActionItems(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao deletar action item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const markAsCompleted = async (id: number) => {
    return updateActionItem(id, { status: 'completed' });
  };

  const markAsInProgress = async (id: number) => {
    return updateActionItem(id, { status: 'in_progress' });
  };

  const markAsPending = async (id: number) => {
    return updateActionItem(id, { status: 'pending' });
  };

  const cancel = async (id: number) => {
    return updateActionItem(id, { status: 'cancelled' });
  };

  const putOnHold = async (id: number) => {
    return updateActionItem(id, { status: 'on_hold' });
  };

  return {
    actionItems,
    loading,
    error,
    fetchActionItems,
    createActionItem,
    updateActionItem,
    deleteActionItem,
    markAsCompleted,
    markAsInProgress,
    markAsPending,
    cancel,
    putOnHold,
  };
};

// Import necessário para o hook
import { useState } from 'react';
