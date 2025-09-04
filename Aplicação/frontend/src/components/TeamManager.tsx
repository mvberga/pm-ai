import React, { useState, useEffect } from 'react';
import { useTeamMembers } from '../api/teamMembers';
import type { TeamMemberCreate, TeamMemberUpdate, TeamRole } from '../types/portfolio';

interface TeamManagerProps {
  projectId: number;
}

export const TeamManager: React.FC<TeamManagerProps> = ({ projectId }) => {
  const { teamMembers, loading, error, fetchTeamMembers, createTeamMember, updateTeamMember, deleteTeamMember, toggleTeamMemberStatus } = useTeamMembers(projectId);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingMember, setEditingMember] = useState<number | null>(null);
  const [formData, setFormData] = useState<TeamMemberCreate>({
    project_id: projectId,
    name: '',
    email: '',
    role: 'developer',
    is_active: true
  });

  useEffect(() => {
    fetchTeamMembers();
  }, [fetchTeamMembers]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createTeamMember(formData);
      setFormData({
        project_id: projectId,
        name: '',
        email: '',
        role: 'developer',
        is_active: true
      });
      setShowCreateForm(false);
    } catch (err) {
      console.error('Erro ao criar membro da equipe:', err);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingMember) return;
    
    try {
      const updateData: TeamMemberUpdate = {
        name: formData.name,
        email: formData.email,
        role: formData.role,
        is_active: formData.is_active
      };
      await updateTeamMember(editingMember, updateData);
      setEditingMember(null);
      setFormData({
        project_id: projectId,
        name: '',
        email: '',
        role: 'developer',
        is_active: true
      });
    } catch (err) {
      console.error('Erro ao atualizar membro da equipe:', err);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja remover este membro da equipe?')) {
      try {
        await deleteTeamMember(id);
      } catch (err) {
        console.error('Erro ao remover membro da equipe:', err);
      }
    }
  };

  const handleToggleStatus = async (id: number, currentStatus: boolean) => {
    try {
      await toggleTeamMemberStatus(id, !currentStatus);
    } catch (err) {
      console.error('Erro ao alterar status do membro:', err);
    }
  };

  const startEdit = (member: any) => {
    setEditingMember(member.id);
    setFormData({
      project_id: projectId,
      name: member.name,
      email: member.email,
      role: member.role,
      is_active: member.is_active
    });
  };

  const cancelEdit = () => {
    setEditingMember(null);
    setFormData({
      project_id: projectId,
      name: '',
      email: '',
      role: 'developer',
      is_active: true
    });
  };

  const getRoleColor = (role: TeamRole) => {
    switch (role) {
      case 'project_manager': return 'bg-purple-100 text-purple-800';
      case 'developer': return 'bg-primary-100 text-primary-800';
      case 'designer': return 'bg-pink-100 text-pink-800';
      case 'analyst': return 'bg-green-100 text-green-800';
      case 'tester': return 'bg-yellow-100 text-yellow-800';
      case 'consultant': return 'bg-indigo-100 text-indigo-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getRoleLabel = (role: TeamRole) => {
    switch (role) {
      case 'project_manager': return 'Gerente de Projeto';
      case 'developer': return 'Desenvolvedor';
      case 'designer': return 'Designer';
      case 'analyst': return 'Analista';
      case 'tester': return 'Testador';
      case 'consultant': return 'Consultor';
      default: return role;
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-800">Erro ao carregar membros da equipe: {error}</p>
        <button 
          onClick={() => fetchTeamMembers()}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Tentar novamente
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Gestão da Equipe</h2>
        <button
          onClick={() => setShowCreateForm(true)}
          className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
        >
          Adicionar Membro
        </button>
      </div>

      {/* Formulário de Criação/Edição */}
      {(showCreateForm || editingMember) && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">
            {editingMember ? 'Editar Membro da Equipe' : 'Novo Membro da Equipe'}
          </h3>
          <form onSubmit={editingMember ? handleUpdate : handleCreate} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  required
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Função
              </label>
              <select
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value as TeamRole })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="project_manager">Gerente de Projeto</option>
                <option value="developer">Desenvolvedor</option>
                <option value="designer">Designer</option>
                <option value="analyst">Analista</option>
                <option value="tester">Testador</option>
                <option value="consultant">Consultor</option>
              </select>
            </div>
            
            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_active"
                checked={formData.is_active}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="is_active" className="ml-2 block text-sm text-gray-700">
                Membro ativo
              </label>
            </div>
            
            <div className="flex space-x-2">
              <button
                type="submit"
                className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
              >
                {editingMember ? 'Atualizar' : 'Adicionar'}
              </button>
              <button
                type="button"
                onClick={editingMember ? cancelEdit : () => setShowCreateForm(false)}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Lista de Membros da Equipe */}
      <div className="bg-white rounded-lg shadow-md">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold">Membros da Equipe ({teamMembers.length})</h3>
        </div>
        
        {teamMembers.length === 0 ? (
          <div className="px-6 py-8 text-center text-gray-500">
            Nenhum membro da equipe encontrado. Adicione o primeiro membro!
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {teamMembers.map((member) => (
              <div key={member.id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <h4 className="text-lg font-medium text-gray-900">{member.name}</h4>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getRoleColor(member.role)}`}>
                        {getRoleLabel(member.role)}
                      </span>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        member.is_active 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {member.is_active ? 'Ativo' : 'Inativo'}
                      </span>
                    </div>
                    <p className="mt-1 text-sm text-gray-600">{member.email}</p>
                    <div className="mt-2 text-sm text-gray-500">
                      <span>Adicionado em: {new Date(member.created_at).toLocaleDateString('pt-BR')}</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleToggleStatus(member.id, member.is_active)}
                      className={`px-3 py-1 text-sm rounded ${
                        member.is_active
                          ? 'bg-red-100 text-red-700 hover:bg-red-200'
                          : 'bg-green-100 text-green-700 hover:bg-green-200'
                      }`}
                    >
                      {member.is_active ? 'Desativar' : 'Ativar'}
                    </button>
                    <button
                      onClick={() => startEdit(member)}
                      className="px-3 py-1 text-sm bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDelete(member.id)}
                      className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
                    >
                      Remover
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
