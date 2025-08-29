import React, { useState, useEffect } from 'react';
import api from '../../api/client';

interface Project {
  id: number;
  name: string;
  municipio: string;
  status: string;
  valor_implantacao: number;
  valor_recorrente: number;
  recursos: number;
  data_inicio: string;
  data_fim: string;
  gerente_projeto: string;
  portfolio: string;
  vertical: string;
  etapa_atual: string;
}

interface PortfolioMetrics {
  total_projects: number;
  total_implantation: number;
  total_recurring: number;
  total_resources: number;
  projects_by_status: Record<string, number>;
  projects_by_municipio: Record<string, number>;
  projects_by_portfolio: Record<string, number>;
}

export const PortfolioOverview: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [metrics, setMetrics] = useState<PortfolioMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Buscar métricas e projetos em paralelo
      const [metricsResponse, projectsResponse] = await Promise.all([
        api.get('/projects/metrics'),
        api.get('/projects')
      ]);
      
      setMetrics(metricsResponse.data);
      setProjects(projectsResponse.data);
    } catch (error) {
      console.error('Erro ao carregar dados do portfólio:', error);
      setError('Erro ao carregar dados. Tente novamente.');
    } finally {
      setLoading(false);
    }
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
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Erro ao carregar dados</h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{error}</p>
            </div>
            <button 
              onClick={fetchPortfolioData}
              className="mt-2 bg-red-100 text-red-800 px-3 py-1 rounded text-sm hover:bg-red-200"
            >
              Tentar novamente
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          Portfólio Clientes Premium SC/MG
        </h1>
        <div className="flex flex-wrap justify-center gap-8 text-gray-600">
          <span><strong>Gerente:</strong> Leandro de Faveri</span>
          <span><strong>Coordenador:</strong> Maxwell Santos</span>
          <span><strong>Gerentes de Projetos:</strong> Vitor Vargas, Marcos Bergamaschi</span>
        </div>
      </div>

      {/* KPIs Principais */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm text-center">
          <h3 className="text-gray-500 font-semibold text-sm">Total Projetos</h3>
          <p className="text-3xl font-bold text-gray-800 mt-2">{metrics?.total_projects}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm text-center">
          <h3 className="text-gray-500 font-semibold text-sm">Implantação</h3>
          <p className="text-3xl font-bold text-green-600 mt-2">
            R$ {metrics?.total_implantation.toLocaleString('pt-BR')}
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm text-center">
          <h3 className="text-gray-500 font-semibold text-sm">Recorrente</h3>
          <p className="text-3xl font-bold text-blue-600 mt-2">
            R$ {metrics?.total_recurring.toLocaleString('pt-BR')}
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm text-center">
          <h3 className="text-gray-500 font-semibold text-sm">Recursos</h3>
          <p className="text-3xl font-bold text-purple-600 mt-2">
            {metrics?.total_resources}
          </p>
        </div>
      </div>

      {/* Status dos Projetos */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {Object.entries(metrics?.projects_by_status || {}).map(([status, count]) => (
          <div key={status} className="bg-white p-4 rounded-lg shadow-sm text-center">
            <div className={`w-4 h-4 rounded-full ${getStatusColor(status)} mx-auto mb-2`}></div>
            <h3 className="text-gray-500 font-semibold text-sm">{getStatusText(status)}</h3>
            <p className="text-2xl font-bold text-gray-800 mt-1">{count}</p>
          </div>
        ))}
      </div>

      {/* Lista de Cidades */}
      <div className="bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-xl font-bold mb-4 text-center text-gray-800">
          Projetos por Cidade
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(metrics?.projects_by_municipio || {}).map(([municipio, count]) => {
            const municipioProjects = projects.filter(p => p.municipio === municipio);
            const totalImplantation = municipioProjects.reduce((sum, p) => sum + p.valor_implantacao, 0);
            const totalRecurring = municipioProjects.reduce((sum, p) => sum + p.valor_recorrente, 0);
            
            return (
              <div key={municipio} className="p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors cursor-pointer">
                <div className="flex justify-between items-start">
                  <span className="font-semibold text-gray-800 text-lg">{municipio}</span>
                </div>
                <div className="mt-2 text-sm text-gray-600 space-y-1">
                  <div><strong>Projetos:</strong> {count}</div>
                  <div><strong>Impostação:</strong> R$ {totalImplantation.toLocaleString('pt-BR')}</div>
                  <div><strong>Recorrente:</strong> R$ {totalRecurring.toLocaleString('pt-BR')}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Lista de Projetos */}
      <div className="bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-xl font-bold mb-4 text-gray-800">Todos os Projetos</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Projeto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Município
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Etapa Atual
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Implantação
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Recorrente
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Recursos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Portfólio
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Vertical
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {projects.map((project) => (
                <tr key={project.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {project.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {project.municipio}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(project.status)} mr-2`}></div>
                      <span className="text-sm text-gray-900">{getStatusText(project.status)}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {project.etapa_atual || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    R$ {project.valor_implantacao.toLocaleString('pt-BR')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {project.valor_recorrente > 0 ? `R$ ${project.valor_recorrente.toLocaleString('pt-BR')}` : 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {project.recursos}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {project.portfolio || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {project.vertical || 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-emerald-500';
    case 'on_track': return 'bg-green-500';
    case 'warning': return 'bg-yellow-500';
    case 'delayed': return 'bg-red-500';
    case 'not_started': return 'bg-gray-400';
    default: return 'bg-gray-400';
  }
};

const getStatusText = (status: string) => {
  switch (status) {
    case 'completed': return 'Concluído';
    case 'on_track': return 'Em Dia';
    case 'warning': return 'Atenção';
    case 'delayed': return 'Atrasado';
    case 'not_started': return 'Não Iniciado';
    default: return 'Desconhecido';
  }
};
