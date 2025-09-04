import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { TopBar } from '../ui/components/Layout/TopBar';
import { SideNav, NavIcons } from '../ui/components/Layout/SideNav';
import { Breadcrumbs } from '../ui/components/Layout/Breadcrumbs';
import { KPICard, KPIIcons } from '../ui/components/Cards/KPICard';
import { ProjectsTable } from '../ui/components/Tables/ProjectsTable';
import { useProjects } from '../api/projects';
import { useActionItems } from '../api/actionItems';
import { ProjectWithActions } from '../types/portfolio';
import { ActionItem } from '../types/actionItems';

export default function ProjectsStatusPage() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedProject, setSelectedProject] = useState(null as ProjectWithActions | null);
  const [showActionItems, setShowActionItems] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  // Hooks para dados
  const { 
    projects, 
    loading: projectsLoading, 
    error: projectsError, 
    fetchProjects 
  } = useProjects();

  const { 
    actionItems, 
    loading: actionItemsLoading, 
    fetchActionItems 
  } = useActionItems();

  // Carregar dados iniciais
  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  // Carregar action items quando um projeto é selecionado
  useEffect(() => {
    if (selectedProject) {
      fetchActionItems({ project_id: selectedProject.id });
    }
  }, [selectedProject, fetchActionItems]);

  // Calcular KPIs
  const kpis = React.useMemo(() => {
    const totalProjects = projects.length;
    const projectsWithPendingActions = projects.filter(p => (p.pending_actions_count || 0) > 0).length;
    const totalPendingActions = projects.reduce((sum, p) => sum + (p.pending_actions_count || 0), 0);
    const totalValue = projects.reduce((sum, p) => sum + p.valor_implantacao, 0);
    const completedProjects = projects.filter(p => p.status === 'completed').length;
    const completionRate = totalProjects > 0 ? (completedProjects / totalProjects) * 100 : 0;

    return {
      totalProjects,
      projectsWithPendingActions,
      totalPendingActions,
      totalValue,
      completionRate
    };
  }, [projects]);

  // Navegação da sidebar
  const navItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: NavIcons.Dashboard,
      href: '/dashboard',
      isActive: false
    },
    {
      id: 'projects',
      label: 'Projetos',
      icon: NavIcons.Projects,
      href: '/projects',
      isActive: true
    },
    {
      id: 'actions',
      label: 'Ações',
      icon: NavIcons.Actions,
      href: '/actions',
      isActive: false,
      badge: kpis.totalPendingActions
    },
    {
      id: 'checklists',
      label: 'Checklists',
      icon: NavIcons.Checklists,
      href: '/checklists',
      isActive: false
    },
    {
      id: 'reports',
      label: 'Relatórios',
      icon: NavIcons.Reports,
      href: '/reports',
      isActive: false
    }
  ];

  // Breadcrumbs
  const breadcrumbItems = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Projetos', href: '/projects' },
    { label: 'Status Executivo', isActive: true }
  ];

  // Handlers
  const handleProjectClick = (project: ProjectWithActions) => {
    navigate(`/projects/${project.id}`);
  };

  const handleActionItemsClick = (project: ProjectWithActions) => {
    setSelectedProject(project);
    setShowActionItems(true);
  };

  const handleBackToProjects = () => {
    setShowActionItems(false);
    setSelectedProject(null);
  };

  const handleNavItemClick = (item: any) => {
    navigate(item.href);
  };

  const handleBreadcrumbClick = (item: any) => {
    if (item.href) {
      navigate(item.href);
    }
  };

  // Utilitário simples para calcular progresso baseado em datas (cronograma)
  const getProgressByDates = (p: ProjectWithActions) => {
    const start = new Date(p.data_inicio);
    const end = new Date(p.data_fim);
    if (isNaN(start.getTime()) || isNaN(end.getTime()) || start >= end) {
      return p.status === 'completed' ? 100 : 0;
    }
    const now = new Date();
    const total = end.getTime() - start.getTime();
    const elapsed = Math.min(Math.max(now.getTime() - start.getTime(), 0), total);
    return Math.round((elapsed / total) * 100);
  };

  // Renderizar painel de action items
  const renderActionItemsPanel = () => {
    if (!showActionItems || !selectedProject) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4" data-testid="actions-modal">
        <div className="bg-slate-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[80vh] overflow-hidden">
          <div className="p-6 border-b border-slate-700">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-white">
                Ações - {selectedProject.name}
              </h2>
              <button
                onClick={handleBackToProjects}
                className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700 transition-colors"
                data-testid="actions-modal-close"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <div className="p-6 overflow-y-auto max-h-[60vh]">
            {actionItemsLoading ? (
              <div className="animate-pulse space-y-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-16 bg-slate-700 rounded"></div>
                ))}
              </div>
            ) : actionItems.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-slate-400">Nenhuma ação pendente para este projeto.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {actionItems.map((item: ActionItem) => (
                  <div key={item.id} className="bg-slate-700 p-4 rounded-lg">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="text-white font-medium">{item.title}</h3>
                        {item.description && (
                          <p className="text-slate-400 text-sm mt-1">{item.description}</p>
                        )}
                        <div className="flex items-center space-x-4 mt-2">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            item.status === 'pending' ? 'bg-yellow-900/20 text-yellow-400' :
                            item.status === 'in_progress' ? 'bg-primary-900/20 text-primary-400' :
                            item.status === 'completed' ? 'bg-green-900/20 text-green-400' :
                            'bg-gray-900/20 text-gray-400'
                          }`}>
                            {item.status}
                          </span>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            item.priority === 'critical' ? 'bg-red-900/20 text-red-400' :
                            item.priority === 'high' ? 'bg-orange-900/20 text-orange-400' :
                            item.priority === 'medium' ? 'bg-yellow-900/20 text-yellow-400' :
                            'bg-green-900/20 text-green-400'
                          }`}>
                            {item.priority}
                          </span>
                          <span className="text-slate-500 text-xs">
                            {item.type}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-900">
      {/* TopBar */}
      <TopBar 
        title="Status Executivo de Projetos"
        user={{
          name: "Usuário Demo",
          email: "usuario@betha.com.br"
        }}
      />

      <div className="flex">
        {/* Sidebar */}
        <SideNav 
          items={navItems}
          onItemClick={handleNavItemClick}
          className="w-64"
        />

        {/* Main Content */}
        <main className="flex-1 p-6">
          {/* Breadcrumbs */}
          <Breadcrumbs 
            items={breadcrumbItems}
            onItemClick={handleBreadcrumbClick}
            className="mb-6"
          />

          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold text-white">Status Executivo</h1>
              <p className="text-slate-400 mt-2">
                Visão geral dos projetos e ações pendentes
              </p>
            </div>
          </div>

          {/* Abas */}
          <div className="mb-8 border-b border-slate-700">
            <nav role="tablist" aria-label="Seções do Status" className="-mb-px flex gap-6">
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === 'overview'}
                data-testid="tab-overview"
                onClick={() => setActiveTab('overview')}
                className={`px-2 pb-3 border-b-2 text-sm ${
                  activeTab === 'overview'
                    ? 'border-primary-500 text-white font-semibold'
                    : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-500'
                }`}
              >
                Visão Geral
              </button>
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === 'timeline'}
                data-testid="tab-timeline"
                onClick={() => setActiveTab('timeline')}
                className={`px-2 pb-3 border-b-2 text-sm ${
                  activeTab === 'timeline'
                    ? 'border-primary-500 text-white font-semibold'
                    : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-500'
                }`}
              >
                Cronograma
              </button>
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === 'financial'}
                data-testid="tab-financial"
                onClick={() => setActiveTab('financial')}
                className={`px-2 pb-3 border-b-2 text-sm ${
                  activeTab === 'financial'
                    ? 'border-primary-500 text-white font-semibold'
                    : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-500'
                }`}
              >
                Financeiro
              </button>
            </nav>
          </div>

          {/* Visão Geral (padrão) */}
          {activeTab === 'overview' && (
            <section role="tabpanel" aria-labelledby="tab-overview" data-testid="panel-overview">
              {/* KPIs */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <KPICard
                  title="Total de Projetos"
                  value={kpis.totalProjects}
                  icon={KPIIcons.Projects}
                  status="info"
                />
                <KPICard
                  title="Projetos com Ações Pendentes"
                  value={kpis.projectsWithPendingActions}
                  subtitle={`${kpis.totalProjects > 0 ? ((kpis.projectsWithPendingActions / kpis.totalProjects) * 100).toFixed(1) : 0}% do total`}
                  icon={KPIIcons.Actions}
                  status={kpis.projectsWithPendingActions > 0 ? "warning" : "success"}
                />
                <KPICard
                  title="Total de Ações Pendentes"
                  value={kpis.totalPendingActions}
                  icon={KPIIcons.Alert}
                  status={kpis.totalPendingActions > 0 ? "warning" : "success"}
                />
                <KPICard
                  title="Valor Total dos Projetos"
                  value={new Intl.NumberFormat('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                  }).format(kpis.totalValue)}
                  icon={KPIIcons.Money}
                  status="info"
                />
              </div>

              {/* Tabela de Projetos */}
              <ProjectsTable
                projects={projects}
                loading={projectsLoading}
                onProjectClick={handleProjectClick}
                onActionItemsClick={handleActionItemsClick}
                searchQuery={searchQuery}
                onSearchChange={setSearchQuery}
                showSearch={true}
                showFilters={true}
              />
            </section>
          )}

          {/* Cronograma */}
          {activeTab === 'timeline' && (
            <section role="tabpanel" aria-labelledby="tab-timeline" data-testid="panel-timeline" className="space-y-4">
              {projects.map((p) => {
                const progress = getProgressByDates(p);
                return (
                  <div key={p.id} className="bg-slate-800 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <div>
                        <div className="text-white font-medium">{p.name}</div>
                        <div className="text-slate-400 text-sm">{p.municipio}</div>
                      </div>
                      <div className="text-slate-300 text-sm min-w-[56px] text-right">{progress}%</div>
                    </div>
                    <div className="h-2 w-full bg-slate-700 rounded">
                      <div
                        className="h-2 bg-primary-600 rounded"
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-xs text-slate-400 mt-2">
                      <span>Início: {new Date(p.data_inicio).toLocaleDateString('pt-BR')}</span>
                      <span>Fim: {new Date(p.data_fim).toLocaleDateString('pt-BR')}</span>
                    </div>
                  </div>
                );
              })}
              {projects.length === 0 && (
                <div className="text-slate-400">Nenhum projeto para exibir.</div>
              )}
            </section>
          )}

          {/* Financeiro */}
          {activeTab === 'financial' && (
            <section role="tabpanel" aria-labelledby="tab-financial" data-testid="panel-financial" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-800 rounded-lg p-4">
                  <div className="text-slate-400 text-sm">Valor Total (Implantação)</div>
                  <div className="text-white text-2xl font-semibold mt-1">
                    {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(kpis.totalValue)}
                  </div>
                </div>
                <div className="bg-slate-800 rounded-lg p-4">
                  <div className="text-slate-400 text-sm">% Projetos Concluídos</div>
                  <div className="text-white text-2xl font-semibold mt-1">
                    {kpis.completionRate.toFixed(1)}%
                  </div>
                </div>
                <div className="bg-slate-800 rounded-lg p-4">
                  <div className="text-slate-400 text-sm">Ações Pendentes</div>
                  <div className="text-white text-2xl font-semibold mt-1">
                    {kpis.totalPendingActions}
                  </div>
                </div>
              </div>

              <div className="bg-slate-800 rounded-lg p-4">
                <div className="text-white font-medium mb-4">Projetos e Valores</div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-slate-700">
                    <thead className="bg-slate-900/50">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Projeto</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Município</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Valor de Implantação</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Ações Pendentes</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700">
                      {projects.map((p) => (
                        <tr key={p.id} className="hover:bg-slate-700/40">
                          <td className="px-4 py-2 text-white">{p.name}</td>
                          <td className="px-4 py-2 text-slate-300">{p.municipio}</td>
                          <td className="px-4 py-2 text-slate-300">
                            {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(p.valor_implantacao)}
                          </td>
                          <td className="px-4 py-2 text-slate-300">{p.pending_actions_count || 0}</td>
                        </tr>
                      ))}
                      {projects.length === 0 && (
                        <tr>
                          <td colSpan={4} className="px-4 py-6 text-slate-400 text-center">Nenhum dado financeiro disponível.</td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
          )}

          {/* Error State */}
          {projectsError && (
            <div className="mt-6 p-4 bg-red-900/20 border border-red-500/20 rounded-lg">
              <div className="flex items-center">
                <svg className="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-red-400">
                  Erro ao carregar projetos: {projectsError}
                </p>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Modal de Action Items */}
      {renderActionItemsPanel()}
    </div>
  );
}
