import React, { useState, useMemo } from 'react';
import { ProjectWithActions } from '../../../types/portfolio';
import { getStatusColor } from '../../tokens/colors';

interface ProjectsTableProps {
  projects: ProjectWithActions[];
  loading?: boolean;
  onProjectClick?: (project: ProjectWithActions) => void;
  onActionItemsClick?: (project: ProjectWithActions) => void;
  searchQuery?: string;
  onSearchChange?: (query: string) => void;
  className?: string;
  showSearch?: boolean;
  showFilters?: boolean;
}

interface SortConfig {
  key: keyof ProjectWithActions;
  direction: 'asc' | 'desc';
}

export const ProjectsTable: React.FC<ProjectsTableProps> = ({
  projects,
  loading = false,
  onProjectClick,
  onActionItemsClick,
  searchQuery = '',
  onSearchChange,
  className = "",
  showSearch = true,
  showFilters = true
}) => {
  const [sortConfig, setSortConfig] = useState<SortConfig>({
    key: 'name',
    direction: 'asc'
  });

  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [portfolioFilter, setPortfolioFilter] = useState<string>('all');

  // Filtrar e ordenar projetos
  const filteredAndSortedProjects = useMemo(() => {
    let filtered = projects;

    // Aplicar filtro de busca
    if (searchQuery) {
      filtered = filtered.filter(project =>
        project.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (project.municipio && project.municipio.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (project.entidade && project.entidade.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    // Aplicar filtro de status
    if (statusFilter !== 'all') {
      filtered = filtered.filter(project => project.status === statusFilter);
    }

    // Aplicar filtro de portfólio
    if (portfolioFilter !== 'all') {
      filtered = filtered.filter(project => project.portfolio === portfolioFilter);
    }

    // Aplicar ordenação
    filtered.sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      if (aValue < bValue) {
        return sortConfig.direction === 'asc' ? -1 : 1;
      }
      if (aValue > bValue) {
        return sortConfig.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });

    return filtered;
  }, [projects, searchQuery, statusFilter, portfolioFilter, sortConfig]);

  const handleSort = (key: keyof ProjectWithActions) => {
    setSortConfig(prev => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  const getStatusBadge = (status: string) => {
    const color = getStatusColor(status);
    const statusLabels: Record<string, string> = {
      'not_started': 'Não Iniciado',
      'on_track': 'No Prazo',
      'warning': 'Atenção',
      'delayed': 'Atrasado',
      'completed': 'Concluído'
    };

    return (
      <span 
        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
        style={{ 
          backgroundColor: `${color}20`,
          color: color,
          border: `1px solid ${color}40`
        }}
      >
        {statusLabels[status] || status}
      </span>
    );
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  if (loading) {
    return (
      <div className={`bg-slate-800 rounded-lg shadow-sm border border-slate-700 ${className}`} data-testid="projects-table">
        <div className="p-6">
          <div className="animate-pulse">
            <div className="h-4 bg-slate-700 rounded w-1/4 mb-4"></div>
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-12 bg-slate-700 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-slate-800 rounded-lg shadow-sm border border-slate-700 ${className}`} data-testid="projects-table">
      {/* Header com busca e filtros */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <h3 className="text-xl font-bold text-slate-50">
            Projetos ({filteredAndSortedProjects.length})
          </h3>
          
          <div className="flex flex-col sm:flex-row gap-4">
            {/* Busca */}
            {showSearch && (
              <div className="relative">
                <input
                  type="text"
                  placeholder="Buscar projetos..."
                  value={searchQuery}
                  onChange={(e) => onSearchChange?.(e.target.value)}
                  className="w-full sm:w-64 px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
                <svg className="absolute right-3 top-2.5 w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            )}

            {/* Filtros */}
            {showFilters && (
              <div className="flex gap-2">
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="all">Todos os Status</option>
                  <option value="not_started">Não Iniciado</option>
                  <option value="on_track">No Prazo</option>
                  <option value="warning">Atenção</option>
                  <option value="delayed">Atrasado</option>
                  <option value="completed">Concluído</option>
                </select>

                <select
                  value={portfolioFilter}
                  onChange={(e) => setPortfolioFilter(e.target.value)}
                  className="px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="all">Todos os Portfólios</option>
                  {Array.from(new Set(projects.map(p => p.portfolio).filter(Boolean))).map(portfolio => (
                    <option key={portfolio} value={portfolio}>{portfolio}</option>
                  ))}
                </select>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Tabela */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-700">
          <thead className="bg-slate-700">
            <tr>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider cursor-pointer hover:bg-slate-600"
                onClick={() => handleSort('name')}
              >
                <div className="flex items-center space-x-1">
                  <span>Projeto</span>
                  {sortConfig.key === 'name' && (
                    <span>{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider cursor-pointer hover:bg-slate-600"
                onClick={() => handleSort('municipio')}
              >
                <div className="flex items-center space-x-1">
                  <span>Município</span>
                  {sortConfig.key === 'municipio' && (
                    <span>{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider cursor-pointer hover:bg-slate-600"
                onClick={() => handleSort('status')}
              >
                <div className="flex items-center space-x-1">
                  <span>Status</span>
                  {sortConfig.key === 'status' && (
                    <span>{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider cursor-pointer hover:bg-slate-600"
                onClick={() => handleSort('data_fim')}
              >
                <div className="flex items-center space-x-1">
                  <span>Prazo</span>
                  {sortConfig.key === 'data_fim' && (
                    <span>{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider cursor-pointer hover:bg-slate-600"
                onClick={() => handleSort('valor_implantacao')}
              >
                <div className="flex items-center space-x-1">
                  <span>Valor</span>
                  {sortConfig.key === 'valor_implantacao' && (
                    <span>{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                Ações Pendentes
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                Ações
              </th>
            </tr>
          </thead>
          <tbody className="bg-slate-800 divide-y divide-slate-700">
            {filteredAndSortedProjects.map((project) => (
              <tr 
                key={project.id} 
                className="hover:bg-slate-700 transition-colors cursor-pointer"
                onClick={() => onProjectClick?.(project)}
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div className="text-sm font-medium text-white">
                      {project.name}
                    </div>
                    <div className="text-sm text-slate-400">
                      {project.entidade || project.portfolio}
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                  {project.municipio}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {getStatusBadge(project.status)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                  {formatDate(project.data_fim)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                  {formatCurrency(project.valor_implantacao)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    (project.pending_actions_count || 0) > 0 
                      ? 'bg-red-900/20 text-red-400 border border-red-500/20' 
                      : 'bg-green-900/20 text-green-400 border border-green-500/20'
                  }`}>
                    {project.pending_actions_count || 0}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onActionItemsClick?.(project);
                    }}
                    className="text-primary-400 hover:text-primary-300 transition-colors"
                    data-testid={`open-actions-${project.id}`}
                  >
                    Ver Ações
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Estado vazio */}
      {filteredAndSortedProjects.length === 0 && !loading && (
        <div className="p-12 text-center">
          <svg className="mx-auto h-12 w-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-slate-300">Nenhum projeto encontrado</h3>
          <p className="mt-1 text-sm text-slate-500">
            {searchQuery || statusFilter !== 'all' || portfolioFilter !== 'all'
              ? 'Tente ajustar os filtros de busca.'
              : 'Não há projetos cadastrados no momento.'
            }
          </p>
        </div>
      )}
    </div>
  );
};

export default ProjectsTable;
