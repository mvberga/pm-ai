import React, { useState, useEffect } from 'react';
import { useRisks, useRiskAnalysis } from '../api/risks';
import type { RiskCreate, RiskUpdate, RiskCategory, RiskStatus, RiskPriority } from '../types/portfolio';

interface RiskManagerProps {
  projectId: number;
}

export const RiskManager: React.FC<RiskManagerProps> = ({ projectId }) => {
  const { risks, loading, error, fetchRisks, createRisk, updateRisk, deleteRisk } = useRisks(projectId);
  const { analysis, loading: analysisLoading, fetchAnalysis } = useRiskAnalysis(projectId);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingRisk, setEditingRisk] = useState<number | null>(null);
  const [formData, setFormData] = useState<RiskCreate>({
    project_id: projectId,
    title: '',
    description: '',
    category: 'technical',
    priority: 'medium',
    probability: 0.5,
    impact: 0.5,
    mitigation_plan: ''
  });

  useEffect(() => {
    fetchRisks();
    fetchAnalysis();
  }, [fetchRisks, fetchAnalysis]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createRisk(formData);
      setFormData({
        project_id: projectId,
        title: '',
        description: '',
        category: 'technical',
        priority: 'medium',
        probability: 0.5,
        impact: 0.5,
        mitigation_plan: ''
      });
      setShowCreateForm(false);
    } catch (err) {
      console.error('Erro ao criar risco:', err);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingRisk) return;
    
    try {
      const updateData: RiskUpdate = {
        title: formData.title,
        description: formData.description,
        category: formData.category,
        priority: formData.priority,
        probability: formData.probability,
        impact: formData.impact,
        mitigation_plan: formData.mitigation_plan
      };
      await updateRisk(editingRisk, updateData);
      setEditingRisk(null);
      setFormData({
        project_id: projectId,
        title: '',
        description: '',
        category: 'technical',
        priority: 'medium',
        probability: 0.5,
        impact: 0.5,
        mitigation_plan: ''
      });
    } catch (err) {
      console.error('Erro ao atualizar risco:', err);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja deletar este risco?')) {
      try {
        await deleteRisk(id);
      } catch (err) {
        console.error('Erro ao deletar risco:', err);
      }
    }
  };

  const startEdit = (risk: any) => {
    setEditingRisk(risk.id);
    setFormData({
      project_id: projectId,
      title: risk.title,
      description: risk.description,
      category: risk.category,
      priority: risk.priority,
      probability: risk.probability,
      impact: risk.impact,
      mitigation_plan: risk.mitigation_plan || ''
    });
  };

  const cancelEdit = () => {
    setEditingRisk(null);
    setFormData({
      project_id: projectId,
      title: '',
      description: '',
      category: 'technical',
      priority: 'medium',
      probability: 0.5,
      impact: 0.5,
      mitigation_plan: ''
    });
  };

  const getRiskLevel = (probability: number, impact: number) => {
    const riskScore = probability * impact;
    if (riskScore >= 0.8) return { level: 'Crítico', color: 'bg-red-100 text-red-800' };
    if (riskScore >= 0.6) return { level: 'Alto', color: 'bg-orange-100 text-orange-800' };
    if (riskScore >= 0.4) return { level: 'Médio', color: 'bg-yellow-100 text-yellow-800' };
    return { level: 'Baixo', color: 'bg-green-100 text-green-800' };
  };

  const getPriorityColor = (priority: RiskPriority) => {
    switch (priority) {
      case 'critical': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
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
        <p className="text-red-800">Erro ao carregar riscos: {error}</p>
        <button 
          onClick={() => fetchRisks()}
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
        <h2 className="text-2xl font-bold text-gray-900">Gestão de Riscos</h2>
        <button
          onClick={() => setShowCreateForm(true)}
          className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
        >
          Novo Risco
        </button>
      </div>

      {/* Análise de Riscos */}
      {analysis && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Análise de Riscos</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-primary-50 p-4 rounded-lg">
              <h4 className="font-medium text-primary-900">Total de Riscos</h4>
              <p className="text-2xl font-bold text-primary-600">{analysis.total_risks}</p>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <h4 className="font-medium text-orange-900">Riscos de Alto Impacto</h4>
              <p className="text-2xl font-bold text-orange-600">{analysis.high_impact_risks.length}</p>
            </div>
            <div className="bg-red-50 p-4 rounded-lg">
              <h4 className="font-medium text-red-900">Riscos Atrasados</h4>
              <p className="text-2xl font-bold text-red-600">{analysis.overdue_risks.length}</p>
            </div>
          </div>
        </div>
      )}

      {/* Formulário de Criação/Edição */}
      {(showCreateForm || editingRisk) && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">
            {editingRisk ? 'Editar Risco' : 'Novo Risco'}
          </h3>
          <form onSubmit={editingRisk ? handleUpdate : handleCreate} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Título do Risco
                </label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Categoria
                </label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value as RiskCategory })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="technical">Técnico</option>
                  <option value="business">Negócio</option>
                  <option value="operational">Operacional</option>
                  <option value="financial">Financeiro</option>
                  <option value="legal">Legal</option>
                  <option value="environmental">Ambiental</option>
                </select>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Descrição
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                rows={3}
                required
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Prioridade
                </label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value as RiskPriority })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="low">Baixa</option>
                  <option value="medium">Média</option>
                  <option value="high">Alta</option>
                  <option value="critical">Crítica</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Probabilidade (0-1)
                </label>
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  value={formData.probability}
                  onChange={(e) => setFormData({ ...formData, probability: parseFloat(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Impacto (0-1)
                </label>
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  value={formData.impact}
                  onChange={(e) => setFormData({ ...formData, impact: parseFloat(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  required
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Plano de Mitigação
              </label>
              <textarea
                value={formData.mitigation_plan}
                onChange={(e) => setFormData({ ...formData, mitigation_plan: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                rows={3}
              />
            </div>
            
            <div className="flex space-x-2">
              <button
                type="submit"
                className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
              >
                {editingRisk ? 'Atualizar' : 'Criar'}
              </button>
              <button
                type="button"
                onClick={editingRisk ? cancelEdit : () => setShowCreateForm(false)}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Lista de Riscos */}
      <div className="bg-white rounded-lg shadow-md">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold">Riscos ({risks.length})</h3>
        </div>
        
        {risks.length === 0 ? (
          <div className="px-6 py-8 text-center text-gray-500">
            Nenhum risco identificado. Crie seu primeiro risco!
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {risks.map((risk) => {
              const riskLevel = getRiskLevel(risk.probability, risk.impact);
              return (
                <div key={risk.id} className="px-6 py-4 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <h4 className="text-lg font-medium text-gray-900">{risk.title}</h4>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(risk.priority)}`}>
                          {risk.priority.toUpperCase()}
                        </span>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${riskLevel.color}`}>
                          {riskLevel.level}
                        </span>
                      </div>
                      <p className="mt-1 text-sm text-gray-600">{risk.description}</p>
                      <div className="mt-2 text-sm text-gray-500">
                        <span>Categoria: {risk.category}</span>
                        <span className="mx-2">•</span>
                        <span>Probabilidade: {(risk.probability * 100).toFixed(0)}%</span>
                        <span className="mx-2">•</span>
                        <span>Impacto: {(risk.impact * 100).toFixed(0)}%</span>
                        <span className="mx-2">•</span>
                        <span>Criado em: {new Date(risk.created_at).toLocaleDateString('pt-BR')}</span>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => startEdit(risk)}
                        className="px-3 py-1 text-sm bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleDelete(risk.id)}
                        className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
                      >
                        Deletar
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
