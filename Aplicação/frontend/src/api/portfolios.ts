import { useState } from 'react';
import api from './client';
import type { 
  Portfolio, 
  PortfolioCreate, 
  PortfolioUpdate, 
  PortfolioSummary,
  PortfolioWithProjects
} from '../types/portfolio';

// Serviços de API para portfólios
export const portfoliosApi = {
  // Listar todos os portfólios do usuário
  async getAll(includeInactive: boolean = false): Promise<PortfolioSummary[]> {
    const params = new URLSearchParams();
    if (includeInactive) {
      params.append('include_inactive', 'true');
    }
    
    const response = await api.get(`/portfolios?${params.toString()}`);
    return response.data;
  },

  // Buscar portfólio por ID
  async getById(id: number): Promise<Portfolio> {
    const response = await api.get(`/portfolios/${id}`);
    return response.data;
  },

  // Criar novo portfólio
  async create(data: PortfolioCreate): Promise<Portfolio> {
    const response = await api.post('/portfolios', data);
    return response.data;
  },

  // Atualizar portfólio
  async update(id: number, data: PortfolioUpdate): Promise<Portfolio> {
    const response = await api.put(`/portfolios/${id}`, data);
    return response.data;
  },

  // Deletar portfólio
  async delete(id: number): Promise<void> {
    await api.delete(`/portfolios/${id}`);
  },

  // Obter estatísticas do portfólio
  async getStats(id: number): Promise<any> {
    const response = await api.get(`/portfolios/${id}/statistics`);
    return response.data;
  },

  // Ativar portfólio
  async activate(id: number): Promise<Portfolio> {
    const response = await api.patch(`/portfolios/${id}/activate`);
    return response.data;
  },

  // Desativar portfólio
  async deactivate(id: number): Promise<Portfolio> {
    const response = await api.patch(`/portfolios/${id}/deactivate`);
    return response.data;
  },

  // Obter portfólio com projetos
  async getWithProjects(id: number): Promise<PortfolioWithProjects> {
    const response = await api.get(`/portfolios/${id}/projects`);
    return response.data;
  }
};

// Hook personalizado para portfólios
export const usePortfolios = () => {
  const [portfolios, setPortfolios] = useState<PortfolioSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPortfolios = async (includeInactive: boolean = false) => {
    try {
      setLoading(true);
      setError(null);
      const data = await portfoliosApi.getAll(includeInactive);
      setPortfolios(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar portfólios');
    } finally {
      setLoading(false);
    }
  };

  const createPortfolio = async (data: PortfolioCreate) => {
    try {
      setLoading(true);
      setError(null);
      const newPortfolio = await portfoliosApi.create(data);
      setPortfolios(prev => [...prev, newPortfolio]);
      return newPortfolio;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar portfólio');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updatePortfolio = async (id: number, data: PortfolioUpdate) => {
    try {
      setLoading(true);
      setError(null);
      const updatedPortfolio = await portfoliosApi.update(id, data);
      setPortfolios(prev => prev.map(p => p.id === id ? updatedPortfolio : p));
      return updatedPortfolio;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar portfólio');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deletePortfolio = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await portfoliosApi.delete(id);
      setPortfolios(prev => prev.filter(p => p.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao deletar portfólio');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const activatePortfolio = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      const activatedPortfolio = await portfoliosApi.activate(id);
      setPortfolios(prev => prev.map(p => p.id === id ? activatedPortfolio : p));
      return activatedPortfolio;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao ativar portfólio');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deactivatePortfolio = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      const deactivatedPortfolio = await portfoliosApi.deactivate(id);
      setPortfolios(prev => prev.map(p => p.id === id ? deactivatedPortfolio : p));
      return deactivatedPortfolio;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao desativar portfólio');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    portfolios,
    loading,
    error,
    fetchPortfolios,
    createPortfolio,
    updatePortfolio,
    deletePortfolio,
    activatePortfolio,
    deactivatePortfolio,
  };
};

// Hook para um portfólio específico
export const usePortfolio = (id: number) => {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPortfolio = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await portfoliosApi.getById(id);
      setPortfolio(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar portfólio');
    } finally {
      setLoading(false);
    }
  };

  const updatePortfolio = async (data: PortfolioUpdate) => {
    try {
      setLoading(true);
      setError(null);
      const updatedPortfolio = await portfoliosApi.update(id, data);
      setPortfolio(updatedPortfolio);
      return updatedPortfolio;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar portfólio');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    portfolio,
    loading,
    error,
    fetchPortfolio,
    updatePortfolio,
  };
};
