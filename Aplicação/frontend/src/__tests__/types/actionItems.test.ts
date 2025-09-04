import type {
  ActionItem,
  ActionItemType,
  ActionItemStatus,
  ActionItemPriority,
  ActionItemFilters,
  ActionItemCreateRequest,
  ActionItemUpdateRequest,
  ActionItemStats,
  ProjectActionItemSummary
} from '../../types/actionItems';

describe('Action Items Types', () => {
  describe('ActionItem', () => {
    it('deve ter todas as propriedades obrigatórias', () => {
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

      expect(actionItem.id).toBe(1);
      expect(actionItem.project_id).toBe(1);
      expect(actionItem.title).toBe('Ação Teste');
      expect(actionItem.type).toBe('technical');
      expect(actionItem.status).toBe('pending');
      expect(actionItem.priority).toBe('medium');
    });

    it('deve permitir propriedades opcionais', () => {
      const actionItem: ActionItem = {
        id: 1,
        project_id: 1,
        title: 'Ação Teste',
        description: 'Descrição da ação',
        type: 'technical',
        status: 'pending',
        priority: 'medium',
        assignee_id: 1,
        due_date: '2024-12-31',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      };

      expect(actionItem.description).toBe('Descrição da ação');
      expect(actionItem.assignee_id).toBe(1);
      expect(actionItem.due_date).toBe('2024-12-31');
    });
  });

  describe('ActionItemType', () => {
    it('deve aceitar todos os tipos válidos', () => {
      const types: ActionItemType[] = [
        'technical',
        'business',
        'communication',
        'documentation',
        'testing',
        'deployment',
        'training',
        'support'
      ];

      types.forEach(type => {
        const actionItem: ActionItem = {
          id: 1,
          project_id: 1,
          title: 'Ação Teste',
          type,
          status: 'pending',
          priority: 'medium',
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        };

        expect(actionItem.type).toBe(type);
      });
    });
  });

  describe('ActionItemStatus', () => {
    it('deve aceitar todos os status válidos', () => {
      const statuses: ActionItemStatus[] = [
        'pending',
        'in_progress',
        'completed',
        'cancelled',
        'on_hold'
      ];

      statuses.forEach(status => {
        const actionItem: ActionItem = {
          id: 1,
          project_id: 1,
          title: 'Ação Teste',
          type: 'technical',
          status,
          priority: 'medium',
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        };

        expect(actionItem.status).toBe(status);
      });
    });
  });

  describe('ActionItemPriority', () => {
    it('deve aceitar todas as prioridades válidas', () => {
      const priorities: ActionItemPriority[] = [
        'low',
        'medium',
        'high',
        'critical'
      ];

      priorities.forEach(priority => {
        const actionItem: ActionItem = {
          id: 1,
          project_id: 1,
          title: 'Ação Teste',
          type: 'technical',
          status: 'pending',
          priority,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        };

        expect(actionItem.priority).toBe(priority);
      });
    });
  });

  describe('ActionItemFilters', () => {
    it('deve permitir todos os filtros opcionais', () => {
      const filters: ActionItemFilters = {
        type: 'technical',
        status: 'pending',
        priority: 'high',
        project_id: 1
      };

      expect(filters.type).toBe('technical');
      expect(filters.status).toBe('pending');
      expect(filters.priority).toBe('high');
      expect(filters.project_id).toBe(1);
    });

    it('deve permitir filtros parciais', () => {
      const partialFilters: ActionItemFilters = {
        status: 'pending'
      };

      expect(partialFilters.status).toBe('pending');
      expect(partialFilters.type).toBeUndefined();
    });
  });

  describe('ActionItemCreateRequest', () => {
    it('deve ter propriedades obrigatórias para criação', () => {
      const createRequest: ActionItemCreateRequest = {
        project_id: 1,
        title: 'Nova Ação',
        type: 'technical',
        priority: 'medium'
      };

      expect(createRequest.project_id).toBe(1);
      expect(createRequest.title).toBe('Nova Ação');
      expect(createRequest.type).toBe('technical');
      expect(createRequest.priority).toBe('medium');
    });

    it('deve permitir propriedades opcionais', () => {
      const createRequest: ActionItemCreateRequest = {
        project_id: 1,
        title: 'Nova Ação',
        description: 'Descrição da ação',
        type: 'technical',
        priority: 'medium',
        assignee_id: 1,
        due_date: '2024-12-31'
      };

      expect(createRequest.description).toBe('Descrição da ação');
      expect(createRequest.assignee_id).toBe(1);
      expect(createRequest.due_date).toBe('2024-12-31');
    });
  });

  describe('ActionItemUpdateRequest', () => {
    it('deve permitir todas as propriedades opcionais para atualização', () => {
      const updateRequest: ActionItemUpdateRequest = {
        title: 'Ação Atualizada',
        description: 'Nova descrição',
        type: 'business',
        status: 'in_progress',
        priority: 'high',
        assignee_id: 2,
        due_date: '2024-11-30'
      };

      expect(updateRequest.title).toBe('Ação Atualizada');
      expect(updateRequest.description).toBe('Nova descrição');
      expect(updateRequest.type).toBe('business');
      expect(updateRequest.status).toBe('in_progress');
      expect(updateRequest.priority).toBe('high');
      expect(updateRequest.assignee_id).toBe(2);
      expect(updateRequest.due_date).toBe('2024-11-30');
    });

    it('deve permitir atualizações parciais', () => {
      const partialUpdate: ActionItemUpdateRequest = {
        status: 'completed'
      };

      expect(partialUpdate.status).toBe('completed');
      expect(partialUpdate.title).toBeUndefined();
    });
  });

  describe('ActionItemStats', () => {
    it('deve ter estrutura completa de estatísticas', () => {
      const stats: ActionItemStats = {
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

      expect(stats.total).toBe(50);
      expect(stats.pending).toBe(20);
      expect(stats.by_type.technical).toBe(25);
      expect(stats.by_priority.high).toBe(15);
    });
  });

  describe('ProjectActionItemSummary', () => {
    it('deve ter estrutura de resumo por projeto', () => {
      const summary: ProjectActionItemSummary = {
        project_id: 1,
        project_name: 'Projeto Teste',
        total_actions: 15,
        pending_actions: 5,
        completed_actions: 8,
        overdue_actions: 2
      };

      expect(summary.project_id).toBe(1);
      expect(summary.project_name).toBe('Projeto Teste');
      expect(summary.total_actions).toBe(15);
      expect(summary.pending_actions).toBe(5);
      expect(summary.completed_actions).toBe(8);
      expect(summary.overdue_actions).toBe(2);
    });
  });
});
