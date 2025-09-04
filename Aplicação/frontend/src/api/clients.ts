import { useState } from 'react';
import api from './client';
import type { 
  Client, 
  ClientCreate, 
  ClientUpdate, 
  ClientResponse,
  ClientSummary,
  ClientBulkCreate,
  ClientBulkUpdate
} from '../types/portfolio';

// Serviços de API para clientes
export const clientsApi = {
  // Listar clientes de um projeto
  async getByProject(
    projectId: number, 
    skip: number = 0, 
    limit: number = 100,
    typeFilter?: string,
    communicationLevelFilter?: string
  ): Promise<ClientSummary[]> {
    const params = new URLSearchParams();
    params.append('project_id', projectId.toString());
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    if (typeFilter) {
      params.append('type_filter', typeFilter);
    }
    if (communicationLevelFilter) {
      params.append('communication_level_filter', communicationLevelFilter);
    }
    
    const response = await api.get(`/clients?${params.toString()}`);
    return response.data;
  },

  // Buscar cliente por ID
  async getById(id: number): Promise<Client> {
    const response = await api.get(`/clients/${id}`);
    return response.data;
  },

  // Criar novo cliente
  async create(data: ClientCreate): Promise<Client> {
    const response = await api.post('/clients', data);
    return response.data;
  },

  // Atualizar cliente
  async update(id: number, data: ClientUpdate): Promise<Client> {
    const response = await api.put(`/clients/${id}`, data);
    return response.data;
  },

  // Deletar cliente
  async delete(id: number): Promise<void> {
    await api.delete(`/clients/${id}`);
  },

  // Criar múltiplos clientes
  async bulkCreate(data: ClientBulkCreate): Promise<Client[]> {
    const response = await api.post('/clients/bulk', data);
    return response.data;
  },

  // Atualizar múltiplos clientes
  async bulkUpdate(data: ClientBulkUpdate): Promise<Client[]> {
    const response = await api.put('/clients/bulk', data);
    return response.data;
  },

  // Obter estatísticas de clientes por projeto
  async getStats(projectId: number): Promise<any> {
    const response = await api.get(`/clients/stats?project_id=${projectId}`);
    return response.data;
  }
};

// Hook personalizado para clientes
export const useClients = (projectId: number) => {
  const [clients, setClients] = useState<ClientSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchClients = async (
    skip: number = 0, 
    limit: number = 100, 
    typeFilter?: string,
    communicationLevelFilter?: string
  ) => {
    try {
      setLoading(true);
      setError(null);
      const data = await clientsApi.getByProject(projectId, skip, limit, typeFilter, communicationLevelFilter);
      setClients(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar clientes');
    } finally {
      setLoading(false);
    }
  };

  const createClient = async (data: ClientCreate) => {
    try {
      setLoading(true);
      setError(null);
      const newClient = await clientsApi.create(data);
      setClients(prev => [...prev, newClient]);
      return newClient;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar cliente');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateClient = async (id: number, data: ClientUpdate) => {
    try {
      setLoading(true);
      setError(null);
      const updatedClient = await clientsApi.update(id, data);
      setClients(prev => prev.map(client => client.id === id ? updatedClient : client));
      return updatedClient;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar cliente');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteClient = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await clientsApi.delete(id);
      setClients(prev => prev.filter(client => client.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao deletar cliente');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const bulkCreateClients = async (data: ClientBulkCreate) => {
    try {
      setLoading(true);
      setError(null);
      const newClients = await clientsApi.bulkCreate(data);
      setClients(prev => [...prev, ...newClients]);
      return newClients;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar clientes');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    clients,
    loading,
    error,
    fetchClients,
    createClient,
    updateClient,
    deleteClient,
    bulkCreateClients,
  };
};

// Hook para um cliente específico
export const useClient = (id: number) => {
  const [client, setClient] = useState<Client | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchClient = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await clientsApi.getById(id);
      setClient(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar cliente');
    } finally {
      setLoading(false);
    }
  };

  const updateClient = async (data: ClientUpdate) => {
    try {
      setLoading(true);
      setError(null);
      const updatedClient = await clientsApi.update(id, data);
      setClient(updatedClient);
      return updatedClient;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar cliente');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    client,
    loading,
    error,
    fetchClient,
    updateClient,
  };
};
