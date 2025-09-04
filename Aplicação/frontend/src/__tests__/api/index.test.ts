import { 
  api, 
  projectsApi, 
  useProjects, 
  useProjectsMetrics,
  actionItemsApi,
  useActionItems,
  type ProjectCreateRequest,
  type ProjectUpdateRequest
} from '../../api/index';

// Mock dos módulos
jest.mock('../../api/client');
jest.mock('../../api/projects');
jest.mock('../../api/actionItems');

describe('API Index', () => {
  it('deve exportar api client', () => {
    expect(api).toBeDefined();
  });

  it('deve exportar projectsApi', () => {
    expect(projectsApi).toBeDefined();
  });

  it('deve exportar useProjects hook', () => {
    expect(useProjects).toBeDefined();
  });

  it('deve exportar useProjectsMetrics hook', () => {
    expect(useProjectsMetrics).toBeDefined();
  });

  it('deve exportar actionItemsApi', () => {
    expect(actionItemsApi).toBeDefined();
  });

  it('deve exportar useActionItems hook', () => {
    expect(useActionItems).toBeDefined();
  });

  it('deve exportar tipos TypeScript', () => {
    // Testa se os tipos estão disponíveis (mesmo que sejam apenas tipos)
    const projectCreateRequest: ProjectCreateRequest = {
      name: 'Teste',
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
      owner_id: 1
    };

    const projectUpdateRequest: ProjectUpdateRequest = {
      name: 'Teste Atualizado'
    };

    expect(projectCreateRequest).toBeDefined();
    expect(projectUpdateRequest).toBeDefined();
  });
});
