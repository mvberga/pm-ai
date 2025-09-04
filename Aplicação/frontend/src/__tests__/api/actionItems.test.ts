import { renderHook, act } from '@testing-library/react';
import { actionItemsApi, useActionItems } from '../../api/actionItems';
import api from '../../api/client';
import type { ActionItemFilters, ActionItemCreateRequest, ActionItemUpdateRequest } from '../../types/actionItems';

// Mock do cliente API
jest.mock('../../api/client', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
}));

const mockApi = api as jest.Mocked<typeof api>;

describe('actionItemsApi', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getAll', () => {
    it('deve buscar todos os action items sem filtros', async () => {
      const mockActionItems = [
        { id: 1, title: 'Ação 1', status: 'pending' },
        { id: 2, title: 'Ação 2', status: 'completed' }
      ];
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getAll();

      expect(mockApi.get).toHaveBeenCalledWith('/action-items?');
      expect(result).toEqual(mockActionItems);
    });

    it('deve buscar action items com filtros', async () => {
      const mockActionItems = [{ id: 1, title: 'Ação 1', status: 'pending' }];
      const filters: ActionItemFilters = {
        type: 'task',
        status: 'pending',
        priority: 'high',
        project_id: 1
      };
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getAll(filters);

      expect(mockApi.get).toHaveBeenCalledWith('/action-items?type=task&status=pending&priority=high&project_id=1');
      expect(result).toEqual(mockActionItems);
    });
  });

  describe('getById', () => {
    it('deve buscar action item por ID', async () => {
      const mockActionItem = { id: 1, title: 'Ação 1', status: 'pending' };
      
      mockApi.get.mockResolvedValue({ data: mockActionItem });

      const result = await actionItemsApi.getById(1);

      expect(mockApi.get).toHaveBeenCalledWith('/action-items/1');
      expect(result).toEqual(mockActionItem);
    });
  });

  describe('create', () => {
    it('deve criar novo action item', async () => {
      const mockActionItem = { id: 1, title: 'Nova Ação', status: 'pending' };
      const actionItemData: ActionItemCreateRequest = {
        title: 'Nova Ação',
        description: 'Descrição da ação',
        type: 'task',
        priority: 'medium',
        project_id: 1,
        assigned_to: 1,
        due_date: '2024-12-31'
      };
      
      mockApi.post.mockResolvedValue({ data: mockActionItem });

      const result = await actionItemsApi.create(actionItemData);

      expect(mockApi.post).toHaveBeenCalledWith('/action-items', actionItemData);
      expect(result).toEqual(mockActionItem);
    });
  });

  describe('update', () => {
    it('deve atualizar action item', async () => {
      const mockActionItem = { id: 1, title: 'Ação Atualizada', status: 'completed' };
      const updateData: ActionItemUpdateRequest = {
        title: 'Ação Atualizada',
        status: 'completed'
      };
      
      mockApi.put.mockResolvedValue({ data: mockActionItem });

      const result = await actionItemsApi.update(1, updateData);

      expect(mockApi.put).toHaveBeenCalledWith('/action-items/1', updateData);
      expect(result).toEqual(mockActionItem);
    });
  });

  describe('delete', () => {
    it('deve deletar action item', async () => {
      mockApi.delete.mockResolvedValue(undefined);

      await actionItemsApi.delete(1);

      expect(mockApi.delete).toHaveBeenCalledWith('/action-items/1');
    });
  });

  describe('getByProject', () => {
    it('deve buscar action items de um projeto', async () => {
      const mockActionItems = [
        { id: 1, title: 'Ação 1', project_id: 1 },
        { id: 2, title: 'Ação 2', project_id: 1 }
      ];
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getByProject(1);

      expect(mockApi.get).toHaveBeenCalledWith('/projects/1/action-items?');
      expect(result).toEqual(mockActionItems);
    });

    it('deve buscar action items de um projeto com filtros', async () => {
      const mockActionItems = [{ id: 1, title: 'Ação 1', project_id: 1, status: 'pending' }];
      const filters = { status: 'pending', priority: 'high' };
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getByProject(1, filters);

      expect(mockApi.get).toHaveBeenCalledWith('/projects/1/action-items?status=pending&priority=high');
      expect(result).toEqual(mockActionItems);
    });
  });

  describe('getStats', () => {
    it('deve obter estatísticas dos action items', async () => {
      const mockStats = {
        total: 20,
        pending: 10,
        in_progress: 5,
        completed: 5
      };
      
      mockApi.get.mockResolvedValue({ data: mockStats });

      const result = await actionItemsApi.getStats();

      expect(mockApi.get).toHaveBeenCalledWith('/action-items/stats');
      expect(result).toEqual(mockStats);
    });
  });

  describe('getPending', () => {
    it('deve buscar action items pendentes', async () => {
      const mockActionItems = [{ id: 1, title: 'Ação 1', status: 'pending' }];
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getPending();

      expect(mockApi.get).toHaveBeenCalledWith('/action-items?status=pending');
      expect(result).toEqual(mockActionItems);
    });
  });

  describe('search', () => {
    it('deve buscar action items por texto', async () => {
      const mockActionItems = [{ id: 1, title: 'Ação de Teste' }];
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.search('teste');

      expect(mockApi.get).toHaveBeenCalledWith('/action-items/search?q=teste');
      expect(result).toEqual(mockActionItems);
    });
  });

  describe('getByStatus', () => {
    it('deve buscar action items por status', async () => {
      const mockActionItems = [{ id: 1, title: 'Ação 1', status: 'pending' }];
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getByStatus('pending');

      expect(mockApi.get).toHaveBeenCalledWith('/action-items?status=pending');
      expect(result).toEqual(mockActionItems);
    });
  });

  describe('getByPriority', () => {
    it('deve buscar action items por prioridade', async () => {
      const mockActionItems = [{ id: 1, title: 'Ação 1', priority: 'high' }];
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getByPriority('high');

      expect(mockApi.get).toHaveBeenCalledWith('/action-items?priority=high');
      expect(result).toEqual(mockActionItems);
    });
  });

  describe('getByType', () => {
    it('deve buscar action items por tipo', async () => {
      const mockActionItems = [{ id: 1, title: 'Ação 1', type: 'task' }];
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getByType('task');

      expect(mockApi.get).toHaveBeenCalledWith('/action-items?type=task');
      expect(result).toEqual(mockActionItems);
    });
  });

  describe('getOverdue', () => {
    it('deve buscar action items em atraso', async () => {
      const mockActionItems = [{ id: 1, title: 'Ação Atrasada', due_date: '2024-01-01' }];
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getOverdue();

      expect(mockApi.get).toHaveBeenCalledWith('/action-items/overdue');
      expect(result).toEqual(mockActionItems);
    });
  });

  describe('getInProgress', () => {
    it('deve buscar action items em progresso', async () => {
      const mockActionItems = [{ id: 1, title: 'Ação em Progresso', status: 'in_progress' }];
      
      mockApi.get.mockResolvedValue({ data: mockActionItems });

      const result = await actionItemsApi.getInProgress();

      expect(mockApi.get).toHaveBeenCalledWith('/action-items?status=in_progress');
      expect(result).toEqual(mockActionItems);
    });
  });

  describe('markAsCompleted', () => {
    it('deve marcar action item como concluído', async () => {
      const mockActionItem = { id: 1, title: 'Ação 1', status: 'completed' };
      
      mockApi.put.mockResolvedValue({ data: mockActionItem });

      const result = await actionItemsApi.markAsCompleted(1);

      expect(mockApi.put).toHaveBeenCalledWith('/action-items/1', { status: 'completed' });
      expect(result).toEqual(mockActionItem);
    });
  });

  describe('markAsInProgress', () => {
    it('deve marcar action item como em progresso', async () => {
      const mockActionItem = { id: 1, title: 'Ação 1', status: 'in_progress' };
      
      mockApi.put.mockResolvedValue({ data: mockActionItem });

      const result = await actionItemsApi.markAsInProgress(1);

      expect(mockApi.put).toHaveBeenCalledWith('/action-items/1', { status: 'in_progress' });
      expect(result).toEqual(mockActionItem);
    });
  });
});

describe('useActionItems', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('deve inicializar com estado vazio', () => {
    const { result } = renderHook(() => useActionItems());

    expect(result.current.actionItems).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve buscar action items com sucesso', async () => {
    const mockActionItems = [
      { id: 1, title: 'Ação 1', status: 'pending' }
    ];
    
    mockApi.get.mockResolvedValue({ data: mockActionItems });

    const { result } = renderHook(() => useActionItems());

    await act(async () => {
      await result.current.fetchActionItems();
    });

    expect(result.current.actionItems).toEqual(mockActionItems);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve tratar erro ao buscar action items', async () => {
    const errorMessage = 'Erro de rede';
    mockApi.get.mockRejectedValue(new Error(errorMessage));

    const { result } = renderHook(() => useActionItems());

    await act(async () => {
      await result.current.fetchActionItems();
    });

    expect(result.current.actionItems).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(errorMessage);
  });

  it('deve criar action item com sucesso', async () => {
    const mockActionItem = { id: 1, title: 'Nova Ação' };
    const actionItemData: ActionItemCreateRequest = {
      title: 'Nova Ação',
      description: 'Descrição',
      type: 'task',
      priority: 'medium',
      project_id: 1,
      assigned_to: 1,
      due_date: '2024-12-31'
    };
    
    mockApi.post.mockResolvedValue({ data: mockActionItem });

    const { result } = renderHook(() => useActionItems());

    let createdActionItem;
    await act(async () => {
      createdActionItem = await result.current.createActionItem(actionItemData);
    });

    expect(createdActionItem).toEqual(mockActionItem);
    expect(result.current.actionItems).toContain(mockActionItem);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve atualizar action item com sucesso', async () => {
    const existingActionItem = { id: 1, title: 'Ação Original' };
    const updatedActionItem = { id: 1, title: 'Ação Atualizada' };
    const updateData: ActionItemUpdateRequest = { title: 'Ação Atualizada' };
    
    mockApi.put.mockResolvedValue({ data: updatedActionItem });

    const { result } = renderHook(() => useActionItems());

    // Primeiro adiciona um action item
    await act(async () => {
      result.current.actionItems.push(existingActionItem);
    });

    let updated;
    await act(async () => {
      updated = await result.current.updateActionItem(1, updateData);
    });

    expect(updated).toEqual(updatedActionItem);
    expect(result.current.actionItems).toContain(updatedActionItem);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('deve deletar action item com sucesso', async () => {
    const actionItemToDelete = { id: 1, title: 'Ação para Deletar' };
    
    mockApi.delete.mockResolvedValue(undefined);

    const { result } = renderHook(() => useActionItems());

    // Primeiro adiciona um action item
    await act(async () => {
      result.current.actionItems.push(actionItemToDelete);
    });

    await act(async () => {
      await result.current.deleteActionItem(1);
    });

    expect(result.current.actionItems).not.toContain(actionItemToDelete);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });
});
