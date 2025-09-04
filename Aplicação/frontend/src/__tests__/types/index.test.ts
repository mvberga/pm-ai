import type {
  // Portfolio types
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
  ProjectType,
  // Action Items types
  ActionItem,
  ActionItemType,
  ActionItemStatus,
  ActionItemPriority,
  ActionItemFilters,
  ActionItemCreateRequest,
  ActionItemUpdateRequest,
  ActionItemStats,
  ProjectActionItemSummary
} from '../../types/index';

describe('Types Index', () => {
  describe('Portfolio Types Export', () => {
    it('deve exportar tipos de portfolio corretamente', () => {
      // Testa se os tipos estão disponíveis
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

      const projectWithActions: ProjectWithActions = {
        ...project,
        action_items_count: 10,
        pending_actions_count: 3
      };

      const filters: ProjectFilters = {
        status: 'active',
        portfolio: 'portfolio1'
      };

      const stats: ProjectStats = {
        total_projects: 10,
        projects_by_status: { active: 5 },
        projects_by_portfolio: { portfolio1: 5 },
        projects_by_vertical: {},
        projects_by_municipio: {},
        total_implantation_value: 1000000,
        total_recurring_value: 100000,
        total_resources: 50,
        projects_with_pending_actions: 7,
        projects_with_overdue_actions: 2
      };

      const metrics: PortfolioMetrics = {
        total_projects: 15,
        total_implantation: 1500000,
        total_recurring: 150000,
        total_resources: 75,
        projects_by_status: { active: 8 },
        projects_by_municipio: { 'São Paulo': 10 },
        projects_by_portfolio: { portfolio1: 8 }
      };

      const task: ProjectTask = {
        id: 1,
        project_id: 1,
        name: 'Tarefa Teste',
        start_date: '2024-01-01',
        end_date: '2024-01-31',
        status: 'pending',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      };

      const implantador: ProjectImplantador = {
        id: 1,
        project_id: 1,
        user_id: 1,
        created_at: '2024-01-01T00:00:00Z'
      };

      const migrador: ProjectMigrador = {
        id: 1,
        project_id: 1,
        user_id: 1,
        created_at: '2024-01-01T00:00:00Z'
      };

      const user: User = {
        id: 1,
        email: 'user@test.com',
        name: 'Usuário Teste',
        created_at: '2024-01-01T00:00:00Z'
      };

      const projectStatus: ProjectStatus = 'active';
      const projectType: ProjectType = 'implementacao';

      // Verifica se os objetos foram criados corretamente
      expect(project.id).toBe(1);
      expect(projectWithActions.action_items_count).toBe(10);
      expect(filters.status).toBe('active');
      expect(stats.total_projects).toBe(10);
      expect(metrics.total_projects).toBe(15);
      expect(task.name).toBe('Tarefa Teste');
      expect(implantador.user_id).toBe(1);
      expect(migrador.user_id).toBe(1);
      expect(user.email).toBe('user@test.com');
      expect(projectStatus).toBe('active');
      expect(projectType).toBe('implementacao');
    });
  });

  describe('Action Items Types Export', () => {
    it('deve exportar tipos de action items corretamente', () => {
      // Testa se os tipos estão disponíveis
      const actionItem: ActionItem = {
        id: 1,
        project_id: 1,
        title: 'Ação Teste',
        type: 'technical',
        status: 'pending',
        priority: 'medium',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      };

      const actionItemType: ActionItemType = 'technical';
      const actionItemStatus: ActionItemStatus = 'pending';
      const actionItemPriority: ActionItemPriority = 'medium';

      const actionItemFilters: ActionItemFilters = {
        type: 'technical',
        status: 'pending'
      };

      const createRequest: ActionItemCreateRequest = {
        project_id: 1,
        title: 'Nova Ação',
        type: 'technical',
        priority: 'medium'
      };

      const updateRequest: ActionItemUpdateRequest = {
        status: 'completed'
      };

      const actionItemStats: ActionItemStats = {
        total: 50,
        pending: 20,
        in_progress: 15,
        completed: 10,
        cancelled: 3,
        on_hold: 2,
        by_type: {
          technical: 25,
          business: 10,
          communication: 5,
          documentation: 5,
          testing: 3,
          deployment: 1,
          training: 1,
          support: 0
        },
        by_priority: {
          low: 10,
          medium: 20,
          high: 15,
          critical: 5
        }
      };

      const summary: ProjectActionItemSummary = {
        project_id: 1,
        project_name: 'Projeto Teste',
        total_actions: 15,
        pending_actions: 5,
        completed_actions: 8,
        overdue_actions: 2
      };

      // Verifica se os objetos foram criados corretamente
      expect(actionItem.id).toBe(1);
      expect(actionItemType).toBe('technical');
      expect(actionItemStatus).toBe('pending');
      expect(actionItemPriority).toBe('medium');
      expect(actionItemFilters.type).toBe('technical');
      expect(createRequest.title).toBe('Nova Ação');
      expect(updateRequest.status).toBe('completed');
      expect(actionItemStats.total).toBe(50);
      expect(summary.project_name).toBe('Projeto Teste');
    });
  });

  describe('Type Compatibility', () => {
    it('deve manter compatibilidade entre tipos relacionados', () => {
      // Testa compatibilidade entre Project e ProjectWithActions
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

      const projectWithActions: ProjectWithActions = {
        ...project,
        action_items_count: 10
      };

      // Verifica se a extensão funciona corretamente
      expect(projectWithActions.id).toBe(project.id);
      expect(projectWithActions.name).toBe(project.name);
      expect(projectWithActions.action_items_count).toBe(10);

      // Testa compatibilidade entre ActionItem e ActionItemCreateRequest
      const createRequest: ActionItemCreateRequest = {
        project_id: 1,
        title: 'Nova Ação',
        type: 'technical',
        priority: 'medium'
      };

      const actionItem: ActionItem = {
        id: 1,
        project_id: createRequest.project_id,
        title: createRequest.title,
        type: createRequest.type,
        status: 'pending',
        priority: createRequest.priority,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      };

      expect(actionItem.project_id).toBe(createRequest.project_id);
      expect(actionItem.title).toBe(createRequest.title);
      expect(actionItem.type).toBe(createRequest.type);
      expect(actionItem.priority).toBe(createRequest.priority);
    });
  });
});
