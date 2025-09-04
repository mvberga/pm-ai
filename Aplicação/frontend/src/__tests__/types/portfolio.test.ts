import type {
  Project,
  ProjectWithActions,
  ProjectFilters,
  ProjectStats,
  PortfolioMetrics,
  ProjectTask,
  ProjectImplantador,
  ProjectMigrador,
  User,
  ProjectStatus,
  ProjectType
} from '../../types/portfolio';

describe('Portfolio Types', () => {
  describe('Project', () => {
    it('deve ter todas as propriedades obrigatórias', () => {
      const project: Project = {
        id: 1,
        name: 'Projeto Teste',
        municipio: 'São Paulo',
        tipo: 'implementacao',
        data_inicio: '2024-01-01',
        data_fim: '2024-12-31',
        valor_implantacao: 100000,
        valor_recorrente: 10000,
        recursos: 5,
        status: 'active',
        gerente_projeto_id: 1,
        gerente_portfolio_id: 1,
        owner_id: 1,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      };

      expect(project.id).toBe(1);
      expect(project.name).toBe('Projeto Teste');
      expect(project.municipio).toBe('São Paulo');
      expect(project.tipo).toBe('implementacao');
      expect(project.status).toBe('active');
    });

    it('deve permitir propriedades opcionais', () => {
      const project: Project = {
        id: 1,
        name: 'Projeto Teste',
        municipio: 'São Paulo',
        entidade: 'Entidade Teste',
        chamado_jira: 'JIRA-123',
        portfolio: 'Portfolio Teste',
        vertical: 'Vertical Teste',
        product: 'Product Teste',
        tipo: 'implementacao',
        data_inicio: '2024-01-01',
        data_fim: '2024-12-31',
        etapa_atual: 'Planejamento',
        valor_implantacao: 100000,
        valor_recorrente: 10000,
        recursos: 5,
        status: 'active',
        gerente_projeto_id: 1,
        gerente_portfolio_id: 1,
        owner_id: 1,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      };

      expect(project.entidade).toBe('Entidade Teste');
      expect(project.chamado_jira).toBe('JIRA-123');
      expect(project.portfolio).toBe('Portfolio Teste');
      expect(project.vertical).toBe('Vertical Teste');
      expect(project.product).toBe('Product Teste');
      expect(project.etapa_atual).toBe('Planejamento');
    });
  });

  describe('ProjectWithActions', () => {
    it('deve estender Project com propriedades de action items', () => {
      const projectWithActions: ProjectWithActions = {
        id: 1,
        name: 'Projeto Teste',
        municipio: 'São Paulo',
        tipo: 'implementacao',
        data_inicio: '2024-01-01',
        data_fim: '2024-12-31',
        valor_implantacao: 100000,
        valor_recorrente: 10000,
        recursos: 5,
        status: 'active',
        gerente_projeto_id: 1,
        gerente_portfolio_id: 1,
        owner_id: 1,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
        action_items_count: 10,
        pending_actions_count: 3,
        completed_actions_count: 7,
        overdue_actions_count: 1
      };

      expect(projectWithActions.action_items_count).toBe(10);
      expect(projectWithActions.pending_actions_count).toBe(3);
      expect(projectWithActions.completed_actions_count).toBe(7);
      expect(projectWithActions.overdue_actions_count).toBe(1);
    });
  });

  describe('ProjectFilters', () => {
    it('deve permitir todos os filtros opcionais', () => {
      const filters: ProjectFilters = {
        status: 'active',
        portfolio: 'portfolio1',
        vertical: 'vertical1',
        municipio: 'São Paulo',
        search: 'teste'
      };

      expect(filters.status).toBe('active');
      expect(filters.portfolio).toBe('portfolio1');
      expect(filters.vertical).toBe('vertical1');
      expect(filters.municipio).toBe('São Paulo');
      expect(filters.search).toBe('teste');
    });

    it('deve permitir filtros parciais', () => {
      const partialFilters: ProjectFilters = {
        status: 'active'
      };

      expect(partialFilters.status).toBe('active');
      expect(partialFilters.portfolio).toBeUndefined();
    });
  });

  describe('ProjectStats', () => {
    it('deve ter estrutura completa de estatísticas', () => {
      const stats: ProjectStats = {
        total_projects: 10,
        projects_by_status: {
          active: 5,
          completed: 3,
          delayed: 2
        },
        projects_by_portfolio: {
          portfolio1: 4,
          portfolio2: 6
        },
        projects_by_vertical: {
          vertical1: 3,
          vertical2: 7
        },
        projects_by_municipio: {
          'São Paulo': 6,
          'Rio de Janeiro': 4
        },
        total_implantation_value: 1000000,
        total_recurring_value: 100000,
        total_resources: 50,
        projects_with_pending_actions: 7,
        projects_with_overdue_actions: 2
      };

      expect(stats.total_projects).toBe(10);
      expect(stats.projects_by_status.active).toBe(5);
      expect(stats.total_implantation_value).toBe(1000000);
    });
  });

  describe('PortfolioMetrics', () => {
    it('deve ter estrutura de métricas do portfólio', () => {
      const metrics: PortfolioMetrics = {
        total_projects: 15,
        total_implantation: 1500000,
        total_recurring: 150000,
        total_resources: 75,
        projects_by_status: {
          active: 8,
          completed: 5,
          delayed: 2
        },
        projects_by_municipio: {
          'São Paulo': 10,
          'Rio de Janeiro': 5
        },
        projects_by_portfolio: {
          portfolio1: 8,
          portfolio2: 7
        }
      };

      expect(metrics.total_projects).toBe(15);
      expect(metrics.total_implantation).toBe(1500000);
      expect(metrics.projects_by_status.active).toBe(8);
    });
  });

  describe('ProjectTask', () => {
    it('deve ter estrutura de tarefa de projeto', () => {
      const task: ProjectTask = {
        id: 1,
        project_id: 1,
        name: 'Tarefa Teste',
        description: 'Descrição da tarefa',
        start_date: '2024-01-01',
        end_date: '2024-01-31',
        status: 'pending',
        assignee_id: 1,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      };

      expect(task.id).toBe(1);
      expect(task.project_id).toBe(1);
      expect(task.name).toBe('Tarefa Teste');
      expect(task.status).toBe('pending');
    });
  });

  describe('ProjectImplantador', () => {
    it('deve ter estrutura de implantador de projeto', () => {
      const implantador: ProjectImplantador = {
        id: 1,
        project_id: 1,
        user_id: 1,
        role: 'Lead',
        created_at: '2024-01-01T00:00:00Z'
      };

      expect(implantador.id).toBe(1);
      expect(implantador.project_id).toBe(1);
      expect(implantador.user_id).toBe(1);
      expect(implantador.role).toBe('Lead');
    });
  });

  describe('ProjectMigrador', () => {
    it('deve ter estrutura de migrador de projeto', () => {
      const migrador: ProjectMigrador = {
        id: 1,
        project_id: 1,
        user_id: 1,
        role: 'Specialist',
        created_at: '2024-01-01T00:00:00Z'
      };

      expect(migrador.id).toBe(1);
      expect(migrador.project_id).toBe(1);
      expect(migrador.user_id).toBe(1);
      expect(migrador.role).toBe('Specialist');
    });
  });

  describe('User', () => {
    it('deve ter estrutura de usuário', () => {
      const user: User = {
        id: 1,
        email: 'user@test.com',
        name: 'Usuário Teste',
        created_at: '2024-01-01T00:00:00Z'
      };

      expect(user.id).toBe(1);
      expect(user.email).toBe('user@test.com');
      expect(user.name).toBe('Usuário Teste');
    });
  });

  describe('ProjectStatus', () => {
    it('deve aceitar todos os status válidos', () => {
      const statuses: ProjectStatus[] = [
        'not_started',
        'on_track',
        'warning',
        'delayed',
        'completed'
      ];

      statuses.forEach(status => {
        const project: Project = {
          id: 1,
          name: 'Projeto Teste',
          municipio: 'São Paulo',
          tipo: 'implementacao',
          data_inicio: '2024-01-01',
          data_fim: '2024-12-31',
          valor_implantacao: 100000,
          valor_recorrente: 10000,
          recursos: 5,
          status,
          gerente_projeto_id: 1,
          gerente_portfolio_id: 1,
          owner_id: 1,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        };

        expect(project.status).toBe(status);
      });
    });
  });

  describe('ProjectType', () => {
    it('deve aceitar todos os tipos válidos', () => {
      const types: ProjectType[] = [
        'implantacao',
        'migracao',
        'configuracao',
        'treinamento',
        'suporte'
      ];

      types.forEach(tipo => {
        const project: Project = {
          id: 1,
          name: 'Projeto Teste',
          municipio: 'São Paulo',
          tipo,
          data_inicio: '2024-01-01',
          data_fim: '2024-12-31',
          valor_implantacao: 100000,
          valor_recorrente: 10000,
          recursos: 5,
          status: 'active',
          gerente_projeto_id: 1,
          gerente_portfolio_id: 1,
          owner_id: 1,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        };

        expect(project.tipo).toBe(tipo);
      });
    });
  });
});
