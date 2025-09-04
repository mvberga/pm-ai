import { useState } from 'react';
import api from './client';
import type { 
  TeamMember, 
  TeamMemberCreate, 
  TeamMemberUpdate, 
  TeamMemberSummary,
  TeamMemberBulkCreate,
  TeamMemberBulkUpdate
} from '../types/portfolio';

// Serviços de API para membros da equipe
export const teamMembersApi = {
  // Listar membros da equipe de um projeto
  async getByProject(
    projectId: number, 
    skip: number = 0, 
    limit: number = 100,
    roleFilter?: string
  ): Promise<TeamMemberSummary[]> {
    const params = new URLSearchParams();
    params.append('project_id', projectId.toString());
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    if (roleFilter) {
      params.append('role_filter', roleFilter);
    }
    
    const response = await api.get(`/team-members?${params.toString()}`);
    return response.data;
  },

  // Buscar membro da equipe por ID
  async getById(id: number): Promise<TeamMember> {
    const response = await api.get(`/team-members/${id}`);
    return response.data;
  },

  // Criar novo membro da equipe
  async create(data: TeamMemberCreate): Promise<TeamMember> {
    const response = await api.post('/team-members', data);
    return response.data;
  },

  // Atualizar membro da equipe
  async update(id: number, data: TeamMemberUpdate): Promise<TeamMember> {
    const response = await api.put(`/team-members/${id}`, data);
    return response.data;
  },

  // Deletar membro da equipe
  async delete(id: number): Promise<void> {
    await api.delete(`/team-members/${id}`);
  },

  // Criar múltiplos membros da equipe
  async bulkCreate(data: TeamMemberBulkCreate): Promise<TeamMember[]> {
    const response = await api.post('/team-members/bulk', data);
    return response.data;
  },

  // Atualizar múltiplos membros da equipe
  async bulkUpdate(data: TeamMemberBulkUpdate): Promise<TeamMember[]> {
    const response = await api.put('/team-members/bulk', data);
    return response.data;
  },

  // Ativar/desativar membro da equipe
  async toggleStatus(id: number, isActive: boolean): Promise<TeamMember> {
    const response = await api.patch(`/team-members/${id}/status`, { is_active: isActive });
    return response.data;
  }
};

// Hook personalizado para membros da equipe
export const useTeamMembers = (projectId: number) => {
  const [teamMembers, setTeamMembers] = useState<TeamMemberSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTeamMembers = async (skip: number = 0, limit: number = 100, roleFilter?: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await teamMembersApi.getByProject(projectId, skip, limit, roleFilter);
      setTeamMembers(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar membros da equipe');
    } finally {
      setLoading(false);
    }
  };

  const createTeamMember = async (data: TeamMemberCreate) => {
    try {
      setLoading(true);
      setError(null);
      const newTeamMember = await teamMembersApi.create(data);
      setTeamMembers(prev => [...prev, newTeamMember]);
      return newTeamMember;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar membro da equipe');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateTeamMember = async (id: number, data: TeamMemberUpdate) => {
    try {
      setLoading(true);
      setError(null);
      const updatedTeamMember = await teamMembersApi.update(id, data);
      setTeamMembers(prev => prev.map(member => member.id === id ? updatedTeamMember : member));
      return updatedTeamMember;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar membro da equipe');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteTeamMember = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await teamMembersApi.delete(id);
      setTeamMembers(prev => prev.filter(member => member.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao deletar membro da equipe');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const bulkCreateTeamMembers = async (data: TeamMemberBulkCreate) => {
    try {
      setLoading(true);
      setError(null);
      const newTeamMembers = await teamMembersApi.bulkCreate(data);
      setTeamMembers(prev => [...prev, ...newTeamMembers]);
      return newTeamMembers;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar membros da equipe');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const toggleTeamMemberStatus = async (id: number, isActive: boolean) => {
    try {
      setLoading(true);
      setError(null);
      const updatedTeamMember = await teamMembersApi.toggleStatus(id, isActive);
      setTeamMembers(prev => prev.map(member => member.id === id ? updatedTeamMember : member));
      return updatedTeamMember;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao alterar status do membro da equipe');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    teamMembers,
    loading,
    error,
    fetchTeamMembers,
    createTeamMember,
    updateTeamMember,
    deleteTeamMember,
    bulkCreateTeamMembers,
    toggleTeamMemberStatus,
  };
};

// Hook para um membro da equipe específico
export const useTeamMember = (id: number) => {
  const [teamMember, setTeamMember] = useState<TeamMember | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTeamMember = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await teamMembersApi.getById(id);
      setTeamMember(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar membro da equipe');
    } finally {
      setLoading(false);
    }
  };

  const updateTeamMember = async (data: TeamMemberUpdate) => {
    try {
      setLoading(true);
      setError(null);
      const updatedTeamMember = await teamMembersApi.update(id, data);
      setTeamMember(updatedTeamMember);
      return updatedTeamMember;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar membro da equipe');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    teamMember,
    loading,
    error,
    fetchTeamMember,
    updateTeamMember,
  };
};
