import { useState } from 'react';
import api from './client';
import type { 
  Risk, 
  RiskCreate, 
  RiskUpdate, 
  RiskResponse,
  RiskSummary,
  RiskAnalysis,
  RiskBulkCreate,
  RiskBulkUpdate
} from '../types/portfolio';

// Serviços de API para riscos
export const risksApi = {
  // Listar riscos de um projeto
  async getByProject(
    projectId: number, 
    skip: number = 0, 
    limit: number = 100,
    statusFilter?: string,
    priorityFilter?: string,
    categoryFilter?: string
  ): Promise<RiskSummary[]> {
    const params = new URLSearchParams();
    params.append('project_id', projectId.toString());
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    if (statusFilter) {
      params.append('status_filter', statusFilter);
    }
    if (priorityFilter) {
      params.append('priority_filter', priorityFilter);
    }
    if (categoryFilter) {
      params.append('category_filter', categoryFilter);
    }
    
    const response = await api.get(`/risks?${params.toString()}`);
    return response.data;
  },

  // Buscar risco por ID
  async getById(id: number): Promise<Risk> {
    const response = await api.get(`/risks/${id}`);
    return response.data;
  },

  // Criar novo risco
  async create(data: RiskCreate): Promise<Risk> {
    const response = await api.post('/risks', data);
    return response.data;
  },

  // Atualizar risco
  async update(id: number, data: RiskUpdate): Promise<Risk> {
    const response = await api.put(`/risks/${id}`, data);
    return response.data;
  },

  // Deletar risco
  async delete(id: number): Promise<void> {
    await api.delete(`/risks/${id}`);
  },

  // Criar múltiplos riscos
  async bulkCreate(data: RiskBulkCreate): Promise<Risk[]> {
    const response = await api.post('/risks/bulk', data);
    return response.data;
  },

  // Atualizar múltiplos riscos
  async bulkUpdate(data: RiskBulkUpdate): Promise<Risk[]> {
    const response = await api.put('/risks/bulk', data);
    return response.data;
  },

  // Obter análise de riscos
  async getAnalysis(projectId: number): Promise<RiskAnalysis> {
    const response = await api.get(`/risks/analysis?project_id=${projectId}`);
    return response.data;
  },

  // Atualizar status do risco
  async updateStatus(id: number, status: string): Promise<Risk> {
    const response = await api.patch(`/risks/${id}/status`, { status });
    return response.data;
  },

  // Atualizar prioridade do risco
  async updatePriority(id: number, priority: string): Promise<Risk> {
    const response = await api.patch(`/risks/${id}/priority`, { priority });
    return response.data;
  }
};

// Hook personalizado para riscos
export const useRisks = (projectId: number) => {
  const [risks, setRisks] = useState<RiskSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRisks = async (
    skip: number = 0, 
    limit: number = 100, 
    statusFilter?: string,
    priorityFilter?: string,
    categoryFilter?: string
  ) => {
    try {
      setLoading(true);
      setError(null);
      const data = await risksApi.getByProject(projectId, skip, limit, statusFilter, priorityFilter, categoryFilter);
      setRisks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar riscos');
    } finally {
      setLoading(false);
    }
  };

  const createRisk = async (data: RiskCreate) => {
    try {
      setLoading(true);
      setError(null);
      const newRisk = await risksApi.create(data);
      setRisks(prev => [...prev, newRisk]);
      return newRisk;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar risco');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateRisk = async (id: number, data: RiskUpdate) => {
    try {
      setLoading(true);
      setError(null);
      const updatedRisk = await risksApi.update(id, data);
      setRisks(prev => prev.map(risk => risk.id === id ? updatedRisk : risk));
      return updatedRisk;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar risco');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteRisk = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await risksApi.delete(id);
      setRisks(prev => prev.filter(risk => risk.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao deletar risco');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const bulkCreateRisks = async (data: RiskBulkCreate) => {
    try {
      setLoading(true);
      setError(null);
      const newRisks = await risksApi.bulkCreate(data);
      setRisks(prev => [...prev, ...newRisks]);
      return newRisks;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar riscos');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateRiskStatus = async (id: number, status: string) => {
    try {
      setLoading(true);
      setError(null);
      const updatedRisk = await risksApi.updateStatus(id, status);
      setRisks(prev => prev.map(risk => risk.id === id ? updatedRisk : risk));
      return updatedRisk;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar status do risco');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateRiskPriority = async (id: number, priority: string) => {
    try {
      setLoading(true);
      setError(null);
      const updatedRisk = await risksApi.updatePriority(id, priority);
      setRisks(prev => prev.map(risk => risk.id === id ? updatedRisk : risk));
      return updatedRisk;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar prioridade do risco');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    risks,
    loading,
    error,
    fetchRisks,
    createRisk,
    updateRisk,
    deleteRisk,
    bulkCreateRisks,
    updateRiskStatus,
    updateRiskPriority,
  };
};

// Hook para um risco específico
export const useRisk = (id: number) => {
  const [risk, setRisk] = useState<Risk | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRisk = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await risksApi.getById(id);
      setRisk(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar risco');
    } finally {
      setLoading(false);
    }
  };

  const updateRisk = async (data: RiskUpdate) => {
    try {
      setLoading(true);
      setError(null);
      const updatedRisk = await risksApi.update(id, data);
      setRisk(updatedRisk);
      return updatedRisk;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar risco');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    risk,
    loading,
    error,
    fetchRisk,
    updateRisk,
  };
};

// Hook para análise de riscos
export const useRiskAnalysis = (projectId: number) => {
  const [analysis, setAnalysis] = useState<RiskAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await risksApi.getAnalysis(projectId);
      setAnalysis(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar análise de riscos');
    } finally {
      setLoading(false);
    }
  };

  return {
    analysis,
    loading,
    error,
    fetchAnalysis,
  };
};
