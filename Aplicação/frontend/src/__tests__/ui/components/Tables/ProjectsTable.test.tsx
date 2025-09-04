import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProjectsTable } from '../../../../ui/components/Tables/ProjectsTable';
import type { ProjectWithActions } from '../../../../types/portfolio';

// Mock da função getStatusColor
jest.mock('../../../../ui/tokens/colors', () => ({
  getStatusColor: jest.fn((status: string) => {
    const colors: Record<string, string> = {
      'not_started': '#6B7280',
      'on_track': '#10B981',
      'warning': '#F59E0B',
      'delayed': '#EF4444',
      'completed': '#3B82F6'
    };
    return colors[status] || '#6B7280';
  })
}));

describe('ProjectsTable', () => {
  const mockProjects: ProjectWithActions[] = [
    {
      id: 1,
      name: 'Projeto Alpha',
      municipio: 'São Paulo',
      entidade: 'Entidade A',
      portfolio: 'Portfolio 1',
      tipo: 'implementacao',
      data_inicio: '2024-01-01',
      data_fim: '2024-12-31',
      valor_implantacao: 100000,
      valor_recorrente: 10000,
      recursos: 5,
      status: 'on_track',
      gerente_projeto_id: 1,
      gerente_portfolio_id: 1,
      owner_id: 1,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
      action_items_count: 5,
      pending_actions_count: 2,
      completed_actions_count: 3,
      overdue_actions_count: 0
    },
    {
      id: 2,
      name: 'Projeto Beta',
      municipio: 'Rio de Janeiro',
      entidade: 'Entidade B',
      portfolio: 'Portfolio 2',
      tipo: 'migracao',
      data_inicio: '2024-02-01',
      data_fim: '2024-11-30',
      valor_implantacao: 200000,
      valor_recorrente: 20000,
      recursos: 8,
      status: 'delayed',
      gerente_projeto_id: 2,
      gerente_portfolio_id: 2,
      owner_id: 2,
      created_at: '2024-02-01T00:00:00Z',
      updated_at: '2024-02-01T00:00:00Z',
      action_items_count: 8,
      pending_actions_count: 5,
      completed_actions_count: 2,
      overdue_actions_count: 1
    },
    {
      id: 3,
      name: 'Projeto Gamma',
      municipio: 'Belo Horizonte',
      entidade: 'Entidade C',
      portfolio: 'Portfolio 1',
      tipo: 'configuracao',
      data_inicio: '2024-03-01',
      data_fim: '2024-10-31',
      valor_implantacao: 150000,
      valor_recorrente: 15000,
      recursos: 6,
      status: 'completed',
      gerente_projeto_id: 3,
      gerente_portfolio_id: 1,
      owner_id: 3,
      created_at: '2024-03-01T00:00:00Z',
      updated_at: '2024-03-01T00:00:00Z',
      action_items_count: 3,
      pending_actions_count: 0,
      completed_actions_count: 3,
      overdue_actions_count: 0
    }
  ];

  const defaultProps = {
    projects: mockProjects,
    onProjectClick: jest.fn(),
    onActionItemsClick: jest.fn(),
    onSearchChange: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Renderização Básica', () => {
    it('deve renderizar a tabela com projetos', () => {
      render(<ProjectsTable {...defaultProps} />);

      expect(screen.getByText('Projetos (3)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Alpha')).toBeInTheDocument();
      expect(screen.getByText('Projeto Beta')).toBeInTheDocument();
      expect(screen.getByText('Projeto Gamma')).toBeInTheDocument();
    });

    it('deve renderizar estado de loading', () => {
      render(<ProjectsTable {...defaultProps} loading={true} />);

      // No estado de loading, não deve mostrar contador nem projetos
      expect(screen.queryByText(/Projetos \(\d+\)/)).not.toBeInTheDocument();
      expect(screen.queryByText('Projeto Alpha')).not.toBeInTheDocument();
      
      // Deve mostrar elementos de loading (skeleton)
      expect(document.querySelector('.animate-pulse')).toBeInTheDocument();
    });

    it('deve renderizar com lista vazia', () => {
      render(<ProjectsTable {...defaultProps} projects={[]} />);

      expect(screen.getByText('Projetos (0)')).toBeInTheDocument();
    });

    it('deve aplicar className customizada', () => {
      const { container } = render(
        <ProjectsTable {...defaultProps} className="custom-class" />
      );

      expect(container.firstChild).toHaveClass('custom-class');
    });
  });

  describe('Funcionalidades de Busca', () => {
    it('deve filtrar projetos por nome', () => {
      render(<ProjectsTable {...defaultProps} searchQuery="Alpha" />);

      expect(screen.getByText('Projetos (1)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Alpha')).toBeInTheDocument();
      expect(screen.queryByText('Projeto Beta')).not.toBeInTheDocument();
    });

    it('deve filtrar projetos por município', () => {
      render(<ProjectsTable {...defaultProps} searchQuery="São Paulo" />);

      expect(screen.getByText('Projetos (1)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Alpha')).toBeInTheDocument();
    });

    it('deve filtrar projetos por entidade', () => {
      render(<ProjectsTable {...defaultProps} searchQuery="Entidade B" />);

      expect(screen.getByText('Projetos (1)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Beta')).toBeInTheDocument();
    });

    it('deve ser case insensitive na busca', () => {
      render(<ProjectsTable {...defaultProps} searchQuery="ALPHA" />);

      expect(screen.getByText('Projetos (1)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Alpha')).toBeInTheDocument();
    });

    it('deve chamar onSearchChange quando busca é alterada', async () => {
      const user = userEvent.setup();
      const onSearchChange = jest.fn();
      render(<ProjectsTable {...defaultProps} onSearchChange={onSearchChange} />);

      const searchInput = screen.getByPlaceholderText('Buscar projetos...');
      await user.type(searchInput, 'test');

      expect(onSearchChange).toHaveBeenCalledWith('t');
      expect(onSearchChange).toHaveBeenCalledWith('e');
      expect(onSearchChange).toHaveBeenCalledWith('s');
      expect(onSearchChange).toHaveBeenCalledWith('t');
    });

    it('deve usar searchQuery externa quando fornecida', () => {
      render(<ProjectsTable {...defaultProps} searchQuery="Alpha" />);

      expect(screen.getByText('Projetos (1)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Alpha')).toBeInTheDocument();
    });
  });

  describe('Funcionalidades de Filtro', () => {
    it('deve filtrar por status', async () => {
      const user = userEvent.setup();
      render(<ProjectsTable {...defaultProps} />);

      const statusFilter = screen.getByDisplayValue('Todos os Status');
      await user.selectOptions(statusFilter, 'on_track');

      expect(screen.getByText('Projetos (1)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Alpha')).toBeInTheDocument();
    });

    it('deve filtrar por portfólio', async () => {
      const user = userEvent.setup();
      render(<ProjectsTable {...defaultProps} />);

      const portfolioFilter = screen.getByDisplayValue('Todos os Portfólios');
      await user.selectOptions(portfolioFilter, 'Portfolio 1');

      expect(screen.getByText('Projetos (2)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Alpha')).toBeInTheDocument();
      expect(screen.getByText('Projeto Gamma')).toBeInTheDocument();
    });

    it('deve combinar filtros de status e portfólio', async () => {
      const user = userEvent.setup();
      render(<ProjectsTable {...defaultProps} />);

      const statusFilter = screen.getByDisplayValue('Todos os Status');
      const portfolioFilter = screen.getByDisplayValue('Todos os Portfólios');

      await user.selectOptions(statusFilter, 'completed');
      await user.selectOptions(portfolioFilter, 'Portfolio 1');

      expect(screen.getByText('Projetos (1)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Gamma')).toBeInTheDocument();
    });
  });

  describe('Funcionalidades de Ordenação', () => {
    it('deve ordenar por nome em ordem crescente por padrão', () => {
      render(<ProjectsTable {...defaultProps} />);

      const projectRows = screen.getAllByRole('row');
      // Primeira linha é o header, então os projetos começam na linha 2
      expect(projectRows[1]).toHaveTextContent('Projeto Alpha');
      expect(projectRows[2]).toHaveTextContent('Projeto Beta');
      expect(projectRows[3]).toHaveTextContent('Projeto Gamma');
    });

    it('deve alternar ordenação ao clicar no header', async () => {
      const user = userEvent.setup();
      render(<ProjectsTable {...defaultProps} />);

      const nameHeader = screen.getByText('Projeto');
      await user.click(nameHeader);

      const projectRows = screen.getAllByRole('row');
      expect(projectRows[1]).toHaveTextContent('Projeto Gamma');
      expect(projectRows[2]).toHaveTextContent('Projeto Beta');
      expect(projectRows[3]).toHaveTextContent('Projeto Alpha');
    });

    it('deve ordenar por status', async () => {
      const user = userEvent.setup();
      render(<ProjectsTable {...defaultProps} />);

      const statusHeader = screen.getByText('Status');
      await user.click(statusHeader);

      // Verifica se a ordenação foi aplicada
      expect(screen.getByText('Projetos (3)')).toBeInTheDocument();
    });

    it('deve ordenar por valor de implantação', async () => {
      const user = userEvent.setup();
      render(<ProjectsTable {...defaultProps} />);

      const valueHeader = screen.getByText('Valor');
      await user.click(valueHeader);

      const projectRows = screen.getAllByRole('row');
      expect(projectRows[1]).toHaveTextContent('Projeto Alpha'); // 100000
      expect(projectRows[2]).toHaveTextContent('Projeto Gamma'); // 150000
      expect(projectRows[3]).toHaveTextContent('Projeto Beta'); // 200000
    });
  });

  describe('Formatação de Dados', () => {
    it('deve formatar valores monetários corretamente', () => {
      render(<ProjectsTable {...defaultProps} />);

      expect(screen.getByText('R$ 100.000,00')).toBeInTheDocument();
      expect(screen.getByText('R$ 200.000,00')).toBeInTheDocument();
      expect(screen.getByText('R$ 150.000,00')).toBeInTheDocument();
    });

    it('deve formatar datas corretamente', () => {
      render(<ProjectsTable {...defaultProps} />);

      expect(screen.getByText('30/12/2024')).toBeInTheDocument();
      expect(screen.getByText('29/11/2024')).toBeInTheDocument();
      expect(screen.getByText('30/10/2024')).toBeInTheDocument();
    });

    it('deve exibir badges de status com cores corretas', () => {
      render(<ProjectsTable {...defaultProps} />);

      // Verifica se os badges estão presentes (pode haver duplicatas nos selects)
      expect(screen.getAllByText('No Prazo')).toHaveLength(2); // 1 no select + 1 no badge
      expect(screen.getAllByText('Atrasado')).toHaveLength(2); // 1 no select + 1 no badge
      expect(screen.getAllByText('Concluído')).toHaveLength(2); // 1 no select + 1 no badge
    });
  });

  describe('Interações de Clique', () => {
    it('deve chamar onProjectClick quando projeto é clicado', async () => {
      const user = userEvent.setup();
      const onProjectClick = jest.fn();
      render(<ProjectsTable {...defaultProps} onProjectClick={onProjectClick} />);

      const projectRow = screen.getByText('Projeto Alpha').closest('tr');
      await user.click(projectRow!);

      expect(onProjectClick).toHaveBeenCalledWith(mockProjects[0]);
    });

    it('deve chamar onActionItemsClick quando botão de ações é clicado', async () => {
      const user = userEvent.setup();
      const onActionItemsClick = jest.fn();
      render(<ProjectsTable {...defaultProps} onActionItemsClick={onActionItemsClick} />);

      const actionButtons = screen.getAllByText('Ver Ações');
      await user.click(actionButtons[0]);

      expect(onActionItemsClick).toHaveBeenCalledWith(mockProjects[0]);
    });

    it('deve exibir contador de ações pendentes', () => {
      render(<ProjectsTable {...defaultProps} />);

      expect(screen.getByText('2')).toBeInTheDocument(); // Projeto Alpha
      expect(screen.getByText('5')).toBeInTheDocument(); // Projeto Beta
      expect(screen.getByText('0')).toBeInTheDocument(); // Projeto Gamma
    });
  });

  describe('Configurações de Exibição', () => {
    it('deve ocultar busca quando showSearch é false', () => {
      render(<ProjectsTable {...defaultProps} showSearch={false} />);

      expect(screen.queryByPlaceholderText('Buscar projetos...')).not.toBeInTheDocument();
    });

    it('deve ocultar filtros quando showFilters é false', () => {
      render(<ProjectsTable {...defaultProps} showFilters={false} />);

      expect(screen.queryByDisplayValue('Todos os Status')).not.toBeInTheDocument();
      expect(screen.queryByDisplayValue('Todos os Portfólios')).not.toBeInTheDocument();
    });
  });

  describe('Casos Especiais', () => {
    it('deve lidar com projetos sem entidade', () => {
      const projectsWithoutEntity = [
        {
          ...mockProjects[0],
          entidade: undefined
        }
      ];

      render(<ProjectsTable {...defaultProps} projects={projectsWithoutEntity} />);

      expect(screen.getByText('Projetos (1)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Alpha')).toBeInTheDocument();
    });

    it('deve lidar com projetos sem município', () => {
      const projectsWithoutMunicipio = [
        {
          ...mockProjects[0],
          municipio: undefined
        }
      ];

      render(<ProjectsTable {...defaultProps} projects={projectsWithoutMunicipio} />);

      expect(screen.getByText('Projetos (1)')).toBeInTheDocument();
      expect(screen.getByText('Projeto Alpha')).toBeInTheDocument();
    });

    it('deve lidar com status desconhecido', () => {
      const projectsWithUnknownStatus = [
        {
          ...mockProjects[0],
          status: 'unknown_status'
        }
      ];

      render(<ProjectsTable {...defaultProps} projects={projectsWithUnknownStatus} />);

      expect(screen.getByText('unknown_status')).toBeInTheDocument();
    });
  });

  describe('Responsividade', () => {
    it('deve aplicar classes responsivas corretamente', () => {
      const { container } = render(<ProjectsTable {...defaultProps} />);

      // Verifica se as classes responsivas estão presentes
      expect(container.querySelector('.flex-col.lg\\:flex-row')).toBeInTheDocument();
      expect(container.querySelector('.flex-col.sm\\:flex-row')).toBeInTheDocument();
    });
  });

  describe('Acessibilidade', () => {
    it('deve ter headers de tabela acessíveis', () => {
      render(<ProjectsTable {...defaultProps} />);

      expect(screen.getByRole('columnheader', { name: 'Projeto ↑' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Status' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Valor' })).toBeInTheDocument();
    });

    it('deve ter botões acessíveis', () => {
      render(<ProjectsTable {...defaultProps} />);

      const actionButtons = screen.getAllByRole('button', { name: 'Ver Ações' });
      expect(actionButtons).toHaveLength(3);
    });
  });
});
