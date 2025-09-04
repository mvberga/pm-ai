import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { SideNav, NavIcons } from '../../../../ui/components/Layout/SideNav';

describe('SideNav', () => {
  const mockItems = [
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
      isActive: true,
      badge: 5
    },
    {
      id: 'actions',
      label: 'Ações',
      icon: NavIcons.Actions,
      href: '/actions',
      isActive: false,
      badge: 99
    }
  ];

  const defaultProps = {
    items: mockItems,
    onItemClick: jest.fn(),
    onToggleCollapse: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Renderização básica', () => {
    it('deve renderizar o componente corretamente', () => {
      render(<SideNav {...defaultProps} />);
      
      expect(screen.getByRole('complementary')).toBeInTheDocument();
      expect(screen.getByAltText('Betha Logo')).toBeInTheDocument();
      expect(screen.getByText('Betha Sistemas')).toBeInTheDocument();
      expect(screen.getByText('Gerenciamento')).toBeInTheDocument();
    });

    it('deve renderizar todos os itens de navegação', () => {
      render(<SideNav {...defaultProps} />);
      
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Projetos')).toBeInTheDocument();
      expect(screen.getByText('Ações')).toBeInTheDocument();
    });

    it('deve aplicar className customizada', () => {
      const customClass = 'custom-sidebar';
      render(<SideNav {...defaultProps} className={customClass} />);
      
      const sidebar = screen.getByRole('complementary');
      expect(sidebar).toHaveClass(customClass);
    });
  });

  describe('Estados de colapso', () => {
    it('deve renderizar expandido por padrão', () => {
      render(<SideNav {...defaultProps} />);
      
      expect(screen.getByText('Betha Sistemas')).toBeInTheDocument();
      expect(screen.getByText('Gerenciamento')).toBeInTheDocument();
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Projetos')).toBeInTheDocument();
    });

    it('deve renderizar colapsado quando isCollapsed é true', () => {
      render(<SideNav {...defaultProps} isCollapsed={true} />);
      
      // Logo deve estar visível
      expect(screen.getByAltText('Betha Logo')).toBeInTheDocument();
      
      // Textos devem estar ocultos
      expect(screen.queryByText('Betha Sistemas')).not.toBeInTheDocument();
      expect(screen.queryByText('Gerenciamento')).not.toBeInTheDocument();
      expect(screen.queryByText('Dashboard')).not.toBeInTheDocument();
      expect(screen.queryByText('Projetos')).not.toBeInTheDocument();
    });

    it('deve mostrar tooltip quando colapsado', () => {
      render(<SideNav {...defaultProps} isCollapsed={true} />);
      
      const projectLink = screen.getByTitle('Projetos');
      expect(projectLink).toBeInTheDocument();
    });
  });

  describe('Botão de toggle', () => {
    it('deve renderizar botão de toggle quando onToggleCollapse é fornecido', () => {
      render(<SideNav {...defaultProps} />);
      
      const toggleButton = screen.getByLabelText('Colapsar menu');
      expect(toggleButton).toBeInTheDocument();
    });

    it('deve não renderizar botão de toggle quando onToggleCollapse não é fornecido', () => {
      const { onToggleCollapse, ...propsWithoutToggle } = defaultProps;
      render(<SideNav {...propsWithoutToggle} />);
      
      expect(screen.queryByLabelText('Colapsar menu')).not.toBeInTheDocument();
      expect(screen.queryByLabelText('Expandir menu')).not.toBeInTheDocument();
    });

    it('deve chamar onToggleCollapse quando botão é clicado', () => {
      render(<SideNav {...defaultProps} />);
      
      const toggleButton = screen.getByLabelText('Colapsar menu');
      fireEvent.click(toggleButton);
      
      expect(defaultProps.onToggleCollapse).toHaveBeenCalledTimes(1);
    });

    it('deve mostrar ícone correto baseado no estado de colapso', () => {
      const { rerender } = render(<SideNav {...defaultProps} isCollapsed={false} />);
      
      let toggleButton = screen.getByLabelText('Colapsar menu');
      expect(toggleButton).toBeInTheDocument();
      
      rerender(<SideNav {...defaultProps} isCollapsed={true} />);
      
      toggleButton = screen.getByLabelText('Expandir menu');
      expect(toggleButton).toBeInTheDocument();
    });
  });

  describe('Itens de navegação', () => {
    it('deve renderizar links com hrefs corretos', () => {
      render(<SideNav {...defaultProps} />);
      
      const dashboardLink = screen.getByText('Dashboard').closest('a');
      const projectsLink = screen.getByText('Projetos').closest('a');
      
      expect(dashboardLink).toHaveAttribute('href', '/dashboard');
      expect(projectsLink).toHaveAttribute('href', '/projects');
    });

    it('deve aplicar estilo ativo para item ativo', () => {
      render(<SideNav {...defaultProps} />);
      
      const activeLink = screen.getByText('Projetos').closest('a');
      expect(activeLink).toHaveClass('bg-primary-600', 'font-semibold');
    });

    it('deve aplicar estilo hover para itens não ativos', () => {
      render(<SideNav {...defaultProps} />);
      
      const inactiveLink = screen.getByText('Dashboard').closest('a');
      expect(inactiveLink).toHaveClass('hover:bg-primary-600/50');
    });

    it('deve chamar onItemClick quando item é clicado', () => {
      render(<SideNav {...defaultProps} />);
      
      const dashboardLink = screen.getByText('Dashboard').closest('a');
      fireEvent.click(dashboardLink!);
      
      expect(defaultProps.onItemClick).toHaveBeenCalledWith(mockItems[0]);
    });

    it('deve prevenir comportamento padrão do link', () => {
      render(<SideNav {...defaultProps} />);
      
      const dashboardLink = screen.getByText('Dashboard').closest('a');
      const clickEvent = new MouseEvent('click', { bubbles: true });
      const preventDefaultSpy = jest.spyOn(clickEvent, 'preventDefault');
      
      fireEvent(dashboardLink!, clickEvent);
      
      expect(preventDefaultSpy).toHaveBeenCalled();
    });
  });

  describe('Badges', () => {
    it('deve renderizar badge quando fornecido', () => {
      render(<SideNav {...defaultProps} />);
      
      expect(screen.getByText('5')).toBeInTheDocument();
    });

    it('deve mostrar "99+" para badges maiores que 99', () => {
      const itemsWithHighBadge = [
        {
          id: 'actions',
          label: 'Ações',
          icon: NavIcons.Actions,
          href: '/actions',
          isActive: false,
          badge: 150
        }
      ];
      
      render(<SideNav {...defaultProps} items={itemsWithHighBadge} />);
      
      expect(screen.getByText('99+')).toBeInTheDocument();
    });

    it('deve não renderizar badge quando valor é 0', () => {
      const itemsWithZeroBadge = [
        {
          id: 'test',
          label: 'Teste',
          icon: NavIcons.Settings,
          href: '/test',
          badge: 0
        }
      ];
      
      render(<SideNav {...defaultProps} items={itemsWithZeroBadge} />);
      
      // Verifica se o badge não está presente no elemento do link
      const testLink = screen.getByText('Teste').closest('a');
      expect(testLink).toBeInTheDocument();
      expect(testLink).not.toHaveTextContent('0');
      
      // Verifica se não há span com classe de badge
      const badgeSpan = testLink?.querySelector('.bg-red-500');
      expect(badgeSpan).not.toBeInTheDocument();
    });

    it('deve não renderizar badge quando não fornecido', () => {
      const itemsWithoutBadge = [
        {
          id: 'test',
          label: 'Teste',
          icon: NavIcons.Settings,
          href: '/test'
        }
      ];
      
      render(<SideNav {...defaultProps} items={itemsWithoutBadge} />);
      
      expect(screen.queryByText('Teste')).toBeInTheDocument();
      expect(screen.queryByText('0')).not.toBeInTheDocument();
    });

    it('deve ocultar badges quando colapsado', () => {
      render(<SideNav {...defaultProps} isCollapsed={true} />);
      
      expect(screen.queryByText('5')).not.toBeInTheDocument();
      expect(screen.queryByText('99+')).not.toBeInTheDocument();
    });
  });

  describe('Footer', () => {
    it('deve renderizar botão de voltar ao menu', () => {
      render(<SideNav {...defaultProps} />);
      
      expect(screen.getByText('Voltar ao Menu')).toBeInTheDocument();
    });

    it('deve ocultar texto do botão quando colapsado', () => {
      render(<SideNav {...defaultProps} isCollapsed={true} />);
      
      expect(screen.queryByText('Voltar ao Menu')).not.toBeInTheDocument();
      expect(screen.getByText('↩️')).toBeInTheDocument();
    });
  });

  describe('Acessibilidade', () => {
    it('deve ter role complementar', () => {
      render(<SideNav {...defaultProps} />);
      
      expect(screen.getByRole('complementary')).toBeInTheDocument();
    });

    it('deve ter aria-label correto no botão de toggle', () => {
      const { rerender } = render(<SideNav {...defaultProps} isCollapsed={false} />);
      
      expect(screen.getByLabelText('Colapsar menu')).toBeInTheDocument();
      
      rerender(<SideNav {...defaultProps} isCollapsed={true} />);
      
      expect(screen.getByLabelText('Expandir menu')).toBeInTheDocument();
    });

    it('deve ter alt text no logo', () => {
      render(<SideNav {...defaultProps} />);
      
      expect(screen.getByAltText('Betha Logo')).toBeInTheDocument();
    });
  });

  describe('Casos extremos', () => {
    it('deve lidar com lista vazia de itens', () => {
      render(<SideNav {...defaultProps} items={[]} />);
      
      expect(screen.getByAltText('Betha Logo')).toBeInTheDocument();
      expect(screen.getByText('Betha Sistemas')).toBeInTheDocument();
      expect(screen.queryByText('Dashboard')).not.toBeInTheDocument();
    });

    it('deve lidar com onItemClick undefined', () => {
      const { onItemClick, ...propsWithoutClick } = defaultProps;
      render(<SideNav {...propsWithoutClick} />);
      
      const dashboardLink = screen.getByText('Dashboard').closest('a');
      expect(() => fireEvent.click(dashboardLink!)).not.toThrow();
    });

    it('deve lidar com itens sem ícone', () => {
      const itemsWithoutIcon = [
        {
          id: 'test',
          label: 'Teste',
          icon: null as any,
          href: '/test'
        }
      ];
      
      render(<SideNav {...defaultProps} items={itemsWithoutIcon} />);
      
      expect(screen.getByText('Teste')).toBeInTheDocument();
    });
  });
});

describe('NavIcons', () => {
  it('deve exportar todos os ícones necessários', () => {
    expect(NavIcons.Dashboard).toBeDefined();
    expect(NavIcons.Projects).toBeDefined();
    expect(NavIcons.Actions).toBeDefined();
    expect(NavIcons.Checklists).toBeDefined();
    expect(NavIcons.Reports).toBeDefined();
    expect(NavIcons.Settings).toBeDefined();
  });

  it('deve renderizar ícones como elementos SVG', () => {
    const { container } = render(<div>{NavIcons.Dashboard}</div>);
    
    expect(container.querySelector('svg')).toBeInTheDocument();
  });
});
