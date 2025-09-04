import React, { useState, useEffect } from 'react';
import { usePortfolios } from '../api/portfolios';
import type { PortfolioCreate, PortfolioUpdate } from '../types/portfolio';

interface PortfolioManagerProps {
  onPortfolioSelect?: (portfolioId: number) => void;
}

export const PortfolioManager: React.FC<PortfolioManagerProps> = ({ onPortfolioSelect }) => {
  const { portfolios, loading, error, fetchPortfolios, createPortfolio, updatePortfolio, deletePortfolio } = usePortfolios();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingPortfolio, setEditingPortfolio] = useState<number | null>(null);
  const [formData, setFormData] = useState<PortfolioCreate>({
    name: '',
    description: '',
    is_active: true
  });

  useEffect(() => {
    fetchPortfolios();
  }, [fetchPortfolios]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createPortfolio(formData);
      setFormData({ name: '', description: '', is_active: true });
      setShowCreateForm(false);
    } catch (err) {
      console.error('Erro ao criar portfólio:', err);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingPortfolio) return;
    
    try {
      const updateData: PortfolioUpdate = {
        name: formData.name,
        description: formData.description,
        is_active: formData.is_active
      };
      await updatePortfolio(editingPortfolio, updateData);
      setEditingPortfolio(null);
      setFormData({ name: '', description: '', is_active: true });
    } catch (err) {
      console.error('Erro ao atualizar portfólio:', err);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja deletar este portfólio?')) {
      try {
        await deletePortfolio(id);
      } catch (err) {
        console.error('Erro ao deletar portfólio:', err);
      }
    }
  };

  const startEdit = (portfolio: any) => {
    setEditingPortfolio(portfolio.id);
    setFormData({
      name: portfolio.name,
      description: portfolio.description || '',
      is_active: portfolio.is_active
    });
  };

  const cancelEdit = () => {
    setEditingPortfolio(null);
    setFormData({ name: '', description: '', is_active: true });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-800">Erro ao carregar portfólios: {error}</p>
        <button 
          onClick={() => fetchPortfolios()}
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
        <h2 className="text-2xl font-bold text-gray-900">Gestão de Portfólios</h2>
        <button
          onClick={() => setShowCreateForm(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Novo Portfólio
        </button>
      </div>

      {/* Formulário de Criação/Edição */}
      {(showCreateForm || editingPortfolio) && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">
            {editingPortfolio ? 'Editar Portfólio' : 'Novo Portfólio'}
          </h3>
          <form onSubmit={editingPortfolio ? handleUpdate : handleCreate} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nome do Portfólio
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Descrição
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
              />
            </div>
            
            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_active"
                checked={formData.is_active}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="is_active" className="ml-2 block text-sm text-gray-700">
                Portfólio ativo
              </label>
            </div>
            
            <div className="flex space-x-2">
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                {editingPortfolio ? 'Atualizar' : 'Criar'}
              </button>
              <button
                type="button"
                onClick={editingPortfolio ? cancelEdit : () => setShowCreateForm(false)}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Lista de Portfólios */}
      <div className="bg-white rounded-lg shadow-md">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold">Portfólios ({portfolios.length})</h3>
        </div>
        
        {portfolios.length === 0 ? (
          <div className="px-6 py-8 text-center text-gray-500">
            Nenhum portfólio encontrado. Crie seu primeiro portfólio!
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {portfolios.map((portfolio) => (
              <div key={portfolio.id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <h4 className="text-lg font-medium text-gray-900">{portfolio.name}</h4>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        portfolio.is_active 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {portfolio.is_active ? 'Ativo' : 'Inativo'}
                      </span>
                    </div>
                    {portfolio.description && (
                      <p className="mt-1 text-sm text-gray-600">{portfolio.description}</p>
                    )}
                    <div className="mt-2 text-sm text-gray-500">
                      <span>Projetos: {portfolio.projects_count}</span>
                      <span className="mx-2">•</span>
                      <span>Criado em: {new Date(portfolio.created_at).toLocaleDateString('pt-BR')}</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => onPortfolioSelect?.(portfolio.id)}
                      className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                    >
                      Selecionar
                    </button>
                    <button
                      onClick={() => startEdit(portfolio)}
                      className="px-3 py-1 text-sm bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDelete(portfolio.id)}
                      className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
                    >
                      Deletar
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
