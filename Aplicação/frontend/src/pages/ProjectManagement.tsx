import React, { useState } from 'react';
import { PortfolioManager } from '../components/PortfolioManager';
import { TeamManager } from '../components/TeamManager';
import { RiskManager } from '../components/RiskManager';

export const ProjectManagement: React.FC = () => {
  const [selectedPortfolio, setSelectedPortfolio] = useState<number | null>(null);
  const [selectedProject, setSelectedProject] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<'portfolios' | 'team' | 'risks'>('portfolios');

  const handlePortfolioSelect = (portfolioId: number) => {
    setSelectedPortfolio(portfolioId);
    // Aqui você poderia carregar os projetos do portfólio selecionado
    console.log('Portfólio selecionado:', portfolioId);
  };

  const handleProjectSelect = (projectId: number) => {
    setSelectedProject(projectId);
    console.log('Projeto selecionado:', projectId);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Gestão de Projetos</h1>
          <p className="mt-2 text-gray-600">
            Sistema completo de gestão de portfólios, equipes e riscos
          </p>
        </div>

        {/* Navegação por Abas */}
        <div className="mb-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('portfolios')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'portfolios'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Portfólios
            </button>
            <button
              onClick={() => setActiveTab('team')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'team'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Equipe
            </button>
            <button
              onClick={() => setActiveTab('risks')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'risks'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Riscos
            </button>
          </nav>
        </div>

        {/* Status da Seleção */}
        {(selectedPortfolio || selectedProject) && (
          <div className="mb-6 bg-primary-50 border border-primary-200 rounded-md p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-primary-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-primary-800">
                  Contexto Atual
                </h3>
                <div className="mt-2 text-sm text-primary-700">
                  {selectedPortfolio && (
                    <p>Portfólio selecionado: ID {selectedPortfolio}</p>
                  )}
                  {selectedProject && (
                    <p>Projeto selecionado: ID {selectedProject}</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Conteúdo das Abas */}
        <div className="bg-white rounded-lg shadow-md">
          {activeTab === 'portfolios' && (
            <div className="p-6">
              <PortfolioManager onPortfolioSelect={handlePortfolioSelect} />
            </div>
          )}

          {activeTab === 'team' && (
            <div className="p-6">
              {selectedProject ? (
                <TeamManager projectId={selectedProject} />
              ) : (
                <div className="text-center py-12">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <h3 className="mt-2 text-sm font-medium text-gray-900">Selecione um Projeto</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Para gerenciar a equipe, primeiro selecione um projeto.
                  </p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'risks' && (
            <div className="p-6">
              {selectedProject ? (
                <RiskManager projectId={selectedProject} />
              ) : (
                <div className="text-center py-12">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  <h3 className="mt-2 text-sm font-medium text-gray-900">Selecione um Projeto</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Para gerenciar riscos, primeiro selecione um projeto.
                  </p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Informações de Integração */}
        <div className="mt-8 bg-green-50 border border-green-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800">
                Integração com Backend Expandido
              </h3>
              <div className="mt-2 text-sm text-green-700">
                <p>Esta página demonstra a integração completa com os novos endpoints:</p>
                <ul className="mt-2 list-disc list-inside space-y-1">
                  <li>✅ Portfólios - CRUD completo com estatísticas</li>
                  <li>✅ Membros da Equipe - Gestão por projeto</li>
                  <li>✅ Riscos - Análise e gestão avançada</li>
                  <li>✅ Hooks personalizados para cada domínio</li>
                  <li>✅ Tratamento de erros e estados de loading</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
