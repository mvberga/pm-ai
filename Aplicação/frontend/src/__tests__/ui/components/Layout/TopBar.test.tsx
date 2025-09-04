import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { TopBar } from '../../../../ui/components/Layout/TopBar';

describe('TopBar', () => {
  const mockUser = {
    name: 'João Silva',
    email: 'joao.silva@betha.com.br',
    avatar: 'https://example.com/avatar.jpg'
  };

  const defaultProps = {
    onThemeToggle: jest.fn(),
    onUserMenuClick: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Renderização básica', () => {
    it('deve renderizar o componente corretamente', () => {
      render(<TopBar {...defaultProps} />);
      
      expect(screen.getByRole('banner')).toBeInTheDocument();
      expect(screen.getByAltText('Betha Logo')).toBeInTheDocument();
      expect(screen.getByText('Dashboard Central')).toBeInTheDocument();
      expect(screen.getByText('Betha Sistemas')).toBeInTheDocument();
    });

    it('deve aplicar className customizada', () => {
      const customClass = 'custom-topbar';
      render(<TopBar {...defaultProps} className={customClass} />);
      
      const topbar = screen.getByRole('banner');
      expect(topbar).toHaveClass(customClass);
    });

    it('deve usar título padrão quando não fornecido', () => {
      render(<TopBar {...defaultProps} />);
      
      expect(screen.getByText('Dashboard Central')).toBeInTheDocument();
    });

    it('deve usar título customizado quando fornecido', () => {
      const customTitle = 'Meu Dashboard';
      render(<TopBar {...defaultProps} title={customTitle} />);
      
      expect(screen.getByText(customTitle)).toBeInTheDocument();
      expect(screen.queryByText('Dashboard Central')).not.toBeInTheDocument();
    });
  });

  describe('Botão de toggle de tema', () => {
    it('deve renderizar botão de toggle por padrão', () => {
      render(<TopBar {...defaultProps} />);
      
      const themeButton = screen.getByLabelText('Alternar tema');
      expect(themeButton).toBeInTheDocument();
    });

    it('deve chamar onThemeToggle quando clicado', () => {
      render(<TopBar {...defaultProps} />);
      
      const themeButton = screen.getByLabelText('Alternar tema');
      fireEvent.click(themeButton);
      
      expect(defaultProps.onThemeToggle).toHaveBeenCalledTimes(1);
    });

    it('deve ocultar botão quando showThemeToggle é false', () => {
      render(<TopBar {...defaultProps} showThemeToggle={false} />);
      
      expect(screen.queryByLabelText('Alternar tema')).not.toBeInTheDocument();
    });

    it('deve não chamar onThemeToggle quando não fornecido', () => {
      const { onThemeToggle, ...propsWithoutToggle } = defaultProps;
      render(<TopBar {...propsWithoutToggle} />);
      
      const themeButton = screen.getByLabelText('Alternar tema');
      expect(() => fireEvent.click(themeButton)).not.toThrow();
    });
  });

  describe('Link de documentação', () => {
    it('deve renderizar link de documentação', () => {
      render(<TopBar {...defaultProps} />);
      
      const docsLink = screen.getByLabelText('Documentação');
      expect(docsLink).toBeInTheDocument();
      expect(docsLink).toHaveAttribute('href', '/docs');
    });

    it('deve ter ícone de documentação', () => {
      render(<TopBar {...defaultProps} />);
      
      const docsLink = screen.getByLabelText('Documentação');
      const svgIcon = docsLink.querySelector('svg');
      expect(svgIcon).toBeInTheDocument();
    });
  });

  describe('Menu do usuário', () => {
    it('deve renderizar menu do usuário quando user é fornecido', () => {
      render(<TopBar {...defaultProps} user={mockUser} />);
      
      expect(screen.getByLabelText('Menu do usuário')).toBeInTheDocument();
      expect(screen.getByText('João Silva')).toBeInTheDocument();
      expect(screen.getByText('joao.silva@betha.com.br')).toBeInTheDocument();
    });

    it('deve renderizar avatar quando fornecido', () => {
      render(<TopBar {...defaultProps} user={mockUser} />);
      
      const avatar = screen.getByAltText('João Silva');
      expect(avatar).toBeInTheDocument();
      expect(avatar).toHaveAttribute('src', 'https://example.com/avatar.jpg');
    });

    it('deve renderizar inicial do nome quando avatar não é fornecido', () => {
      const userWithoutAvatar = {
        name: 'João Silva',
        email: 'joao.silva@betha.com.br'
      };
      
      render(<TopBar {...defaultProps} user={userWithoutAvatar} />);
      
      expect(screen.getByText('J')).toBeInTheDocument();
      expect(screen.queryByAltText('João Silva')).not.toBeInTheDocument();
    });

    it('deve chamar onUserMenuClick quando clicado', () => {
      render(<TopBar {...defaultProps} user={mockUser} />);
      
      const userButton = screen.getByLabelText('Menu do usuário');
      fireEvent.click(userButton);
      
      expect(defaultProps.onUserMenuClick).toHaveBeenCalledTimes(1);
    });

    it('deve ocultar menu quando showUserMenu é false', () => {
      render(<TopBar {...defaultProps} user={mockUser} showUserMenu={false} />);
      
      expect(screen.queryByLabelText('Menu do usuário')).not.toBeInTheDocument();
    });

    it('deve ocultar menu quando user não é fornecido', () => {
      render(<TopBar {...defaultProps} />);
      
      expect(screen.queryByLabelText('Menu do usuário')).not.toBeInTheDocument();
    });

    it('deve não chamar onUserMenuClick quando não fornecido', () => {
      const { onUserMenuClick, ...propsWithoutClick } = defaultProps;
      render(<TopBar {...propsWithoutClick} user={mockUser} />);
      
      const userButton = screen.getByLabelText('Menu do usuário');
      expect(() => fireEvent.click(userButton)).not.toThrow();
    });
  });

  describe('Responsividade', () => {
    it('deve ocultar informações do usuário em telas pequenas', () => {
      render(<TopBar {...defaultProps} user={mockUser} />);
      
      const userInfo = screen.getByText('João Silva').closest('div');
      expect(userInfo).toHaveClass('hidden', 'md:block');
    });

    it('deve manter avatar visível em todas as telas', () => {
      render(<TopBar {...defaultProps} user={mockUser} />);
      
      const avatar = screen.getByAltText('João Silva');
      expect(avatar).not.toHaveClass('hidden');
    });
  });

  describe('Acessibilidade', () => {
    it('deve ter role banner', () => {
      render(<TopBar {...defaultProps} />);
      
      expect(screen.getByRole('banner')).toBeInTheDocument();
    });

    it('deve ter alt text no logo', () => {
      render(<TopBar {...defaultProps} />);
      
      expect(screen.getByAltText('Betha Logo')).toBeInTheDocument();
    });

    it('deve ter aria-label nos botões', () => {
      render(<TopBar {...defaultProps} user={mockUser} />);
      
      expect(screen.getByLabelText('Alternar tema')).toBeInTheDocument();
      expect(screen.getByLabelText('Documentação')).toBeInTheDocument();
      expect(screen.getByLabelText('Menu do usuário')).toBeInTheDocument();
    });

    it('deve ter alt text no avatar do usuário', () => {
      render(<TopBar {...defaultProps} user={mockUser} />);
      
      expect(screen.getByAltText('João Silva')).toBeInTheDocument();
    });
  });

  describe('Casos extremos', () => {
    it('deve lidar com nome de usuário vazio', () => {
      const userWithEmptyName = {
        name: '',
        email: 'test@example.com'
      };
      
      render(<TopBar {...defaultProps} user={userWithEmptyName} />);
      
      expect(screen.getByText('test@example.com')).toBeInTheDocument();
    });

    it('deve lidar com email vazio', () => {
      const userWithEmptyEmail = {
        name: 'João Silva',
        email: ''
      };
      
      render(<TopBar {...defaultProps} user={userWithEmptyEmail} />);
      
      expect(screen.getByText('João Silva')).toBeInTheDocument();
    });

    it('deve lidar com nome com caracteres especiais', () => {
      const userWithSpecialChars = {
        name: 'João-Silva & Cia.',
        email: 'joao@example.com'
      };
      
      render(<TopBar {...defaultProps} user={userWithSpecialChars} />);
      
      expect(screen.getByText('João-Silva & Cia.')).toBeInTheDocument();
      expect(screen.getByText('J')).toBeInTheDocument(); // Inicial
    });

    it('deve lidar com avatar com URL inválida', () => {
      const userWithInvalidAvatar = {
        name: 'João Silva',
        email: 'joao@example.com',
        avatar: 'invalid-url'
      };
      
      render(<TopBar {...defaultProps} user={userWithInvalidAvatar} />);
      
      const avatar = screen.getByAltText('João Silva');
      expect(avatar).toHaveAttribute('src', 'invalid-url');
    });

    it('deve lidar com título muito longo', () => {
      const longTitle = 'Este é um título muito longo que pode causar problemas de layout em telas pequenas';
      render(<TopBar {...defaultProps} title={longTitle} />);
      
      expect(screen.getByText(longTitle)).toBeInTheDocument();
    });

    it('deve lidar com todas as props opcionais undefined', () => {
      render(<TopBar />);
      
      expect(screen.getByText('Dashboard Central')).toBeInTheDocument();
      expect(screen.getByText('Betha Sistemas')).toBeInTheDocument();
      expect(screen.getByLabelText('Alternar tema')).toBeInTheDocument();
      expect(screen.getByLabelText('Documentação')).toBeInTheDocument();
    });
  });

  describe('Estrutura do layout', () => {
    it('deve ter estrutura correta do header', () => {
      render(<TopBar {...defaultProps} user={mockUser} />);
      
      const header = screen.getByRole('banner');
      expect(header).toHaveClass('bg-slate-900', 'border-b', 'border-slate-700');
    });

    it('deve ter logo e título no lado esquerdo', () => {
      render(<TopBar {...defaultProps} />);
      
      const logo = screen.getByAltText('Betha Logo');
      const title = screen.getByText('Dashboard Central');
      
      expect(logo).toBeInTheDocument();
      expect(title).toBeInTheDocument();
    });

    it('deve ter ações do usuário no lado direito', () => {
      render(<TopBar {...defaultProps} user={mockUser} />);
      
      const themeButton = screen.getByLabelText('Alternar tema');
      const docsLink = screen.getByLabelText('Documentação');
      const userButton = screen.getByLabelText('Menu do usuário');
      
      expect(themeButton).toBeInTheDocument();
      expect(docsLink).toBeInTheDocument();
      expect(userButton).toBeInTheDocument();
    });
  });
});
