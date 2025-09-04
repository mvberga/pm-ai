import React, { useEffect } from 'react';
import { useProjects, useProjectsMetrics } from '../../api/projects';
import type { Project, PortfolioMetrics } from '../../types/portfolio';

export const PortfolioOverview: React.FC = () => {
  const { 
    projects, 
    loading: projectsLoading, 
    error: projectsError, 
    fetchProjects 
  } = useProjects();
  
  const { 
    metrics, 
    loading: metricsLoading, 
    error: metricsError, 
    fetchMetrics 
  } = useProjectsMetrics();

  const loading = projectsLoading || metricsLoading;
  const error = projectsError || metricsError;

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    // Buscar métricas e projetos em paralelo usando os hooks
    await Promise.all([
      fetchMetrics(),
      fetchProjects()
    ]);
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
        <h1 className="text-4xl font-bold text-secondary-900 dark:text-secondary-100 mb-2">
          Portfólio Clientes Premium SC/MG
        </h1>
        <div className="flex flex-wrap justify-center gap-8 text-secondary-600 dark:text-secondary-400">
          <span><strong>Gerente:</strong> Leandro de Faveri</span>
          <span><strong>Coordenador:</strong> Maxwell Santos</span>
          <span><strong>Gerentes de Projetos:</strong> Vitor Vargas, Marcos Bergamaschi</span>
        </div>
      </div>

      {/* KPIs Principais */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div className="card p-6 text-center">
          <h3 className="text-secondary-500 dark:text-secondary-400 font-semibold text-sm">Total Projetos</h3>
          <p className="text-3xl font-bold text-secondary-800 dark:text-secondary-200 mt-2">{metrics?.total_projects}</p>
        </div>
        <div className="card p-6 text-center">
          <h3 className="text-secondary-500 dark:text-secondary-400 font-semibold text-sm">Implantação</h3>
          <p className="text-3xl font-bold text-green-600 dark:text-green-400 mt-2">
            R$ {metrics?.total_implantation.toLocaleString('pt-BR')}
          </p>
        </div>
        <div className="card p-6 text-center">
          <h3 className="text-secondary-500 dark:text-secondary-400 font-semibold text-sm">Recorrente</h3>
          <p className="text-3xl font-bold text-primary-600 dark:text-primary-400 mt-2">
            R$ {metrics?.total_recurring.toLocaleString('pt-BR')}
          </p>
        </div>
        <div className="card p-6 text-center">
          <h3 className="text-secondary-500 dark:text-secondary-400 font-semibold text-sm">Recursos</h3>
          <p className="text-3xl font-bold text-purple-600 dark:text-purple-400 mt-2">
            {metrics?.total_resources}
          </p>
        </div>
      </div>

      {/* Status dos Projetos */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {Object.entries(metrics?.projects_by_status || {}).map(([status, count]) => (
          <div key={status} className="card p-4 text-center">
            <div className={`w-4 h-4 rounded-full ${getStatusColor(status)} mx-auto mb-2`}></div>
            <h3 className="text-secondary-500 dark:text-secondary-400 font-semibold text-sm">{getStatusText(status)}</h3>
            <p className="text-2xl font-bold text-secondary-800 dark:text-secondary-200 mt-1">{count}</p>
          </div>
        ))}
      </div>

      {/* Lista de Cidades */}
      <div className="card p-6">
        <h2 className="text-xl font-bold mb-4 text-center text-secondary-800 dark:text-secondary-200">
          Projetos por Cidade
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(metrics?.projects_by_municipio || {}).map(([municipio, count]) => {
            const municipioProjects = projects.filter(p => p.municipio === municipio);
            const totalImplantation = municipioProjects.reduce((sum, p) => sum + p.valor_implantacao, 0);
            const totalRecurring = municipioProjects.reduce((sum, p) => sum + p.valor_recorrente, 0);
            
            return (
              <div key={municipio} className="p-4 rounded-lg border border-secondary-200 dark:border-secondary-700 hover:border-primary-300 dark:hover:border-primary-600 transition-colors cursor-pointer bg-secondary-50 dark:bg-secondary-800">
                <div className="flex justify-between items-start">
                  <span className="font-semibold text-secondary-800 dark:text-secondary-200 text-lg">{municipio}</span>
                </div>
                <div className="mt-2 text-sm text-secondary-600 dark:text-secondary-400 space-y-1">
                  <div><strong>Projetos:</strong> {count}</div>
                  <div><strong>Implantação:</strong> R$ {totalImplantation.toLocaleString('pt-BR')}</div>
                  <div><strong>Recorrente:</strong> R$ {totalRecurring.toLocaleString('pt-BR')}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Lista de Projetos */}
      <div className="card p-6">
        <h2 className="text-xl font-bold mb-4 text-secondary-800 dark:text-secondary-200">Todos os Projetos</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-secondary-200 dark:divide-secondary-700">
            <thead className="bg-secondary-50 dark:bg-secondary-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wider">
                  Projeto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wider">
                  Município
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wider">
                  Etapa Atual
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wider">
                  Implantação
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wider">
                  Recorrente
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wider">
                  Recursos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wider">
                  Portfólio
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wider">
                  Vertical
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-secondary-800 divide-y divide-secondary-200 dark:divide-secondary-700">
              {projects.map((project) => (
                <tr key={project.id} className="hover:bg-secondary-50 dark:hover:bg-secondary-700 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-secondary-900 dark:text-secondary-100">
                    {project.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-500 dark:text-secondary-400">
                    {project.municipio}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(project.status)} mr-2`}></div>
                      <span className="text-sm text-secondary-900 dark:text-secondary-100">{getStatusText(project.status)}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-500 dark:text-secondary-400">
                    {project.etapa_atual || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-500 dark:text-secondary-400">
                    R$ {project.valor_implantacao.toLocaleString('pt-BR')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-500 dark:text-secondary-400">
                    {project.valor_recorrente > 0 ? `R$ ${project.valor_recorrente.toLocaleString('pt-BR')}` : 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-500 dark:text-secondary-400">
                    {project.recursos}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-500 dark:text-secondary-400">
                    {project.portfolio || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-500 dark:text-secondary-400">
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
