import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { KPICard, KPIIcons } from '../../../../ui/components/Cards/KPICard'

describe('KPICard Component', () => {
  describe('Renderização Básica', () => {
    it('renderiza título e valor corretamente', () => {
      render(
        <KPICard
          title="Total de Projetos"
          value={42}
        />
      )

      expect(screen.getByText('Total de Projetos')).toBeInTheDocument()
      expect(screen.getByText('42')).toBeInTheDocument()
    })

    it('renderiza valor como string', () => {
      render(
        <KPICard
          title="Status"
          value="Ativo"
        />
      )

      expect(screen.getByText('Status')).toBeInTheDocument()
      expect(screen.getByText('Ativo')).toBeInTheDocument()
    })

    it('renderiza subtítulo quando fornecido', () => {
      render(
        <KPICard
          title="Projetos"
          value={10}
          subtitle="Últimos 30 dias"
        />
      )

      expect(screen.getByText('Projetos')).toBeInTheDocument()
      expect(screen.getByText('10')).toBeInTheDocument()
      expect(screen.getByText('Últimos 30 dias')).toBeInTheDocument()
    })

    it('renderiza ícone quando fornecido', () => {
      const customIcon = <span data-testid="custom-icon">📊</span>

      render(
        <KPICard
          title="Projetos"
          value={5}
          icon={customIcon}
        />
      )

      expect(screen.getByTestId('custom-icon')).toBeInTheDocument()
    })
  })

  describe('Estados de Status', () => {
    it('aplica estilos de sucesso', () => {
      const { container } = render(
        <KPICard
          title="Projetos Concluídos"
          value={8}
          status="success"
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('bg-green-900/20', 'border-green-500/20')
    })

    it('aplica estilos de warning', () => {
      const { container } = render(
        <KPICard
          title="Projetos em Atraso"
          value={3}
          status="warning"
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('bg-yellow-900/20', 'border-yellow-500/20')
    })

    it('aplica estilos de erro', () => {
      const { container } = render(
        <KPICard
          title="Projetos Bloqueados"
          value={1}
          status="error"
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('bg-red-900/20', 'border-red-500/20')
    })

    it('aplica estilos de info', () => {
      const { container } = render(
        <KPICard
          title="Projetos em Andamento"
          value={12}
          status="info"
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('bg-blue-900/20', 'border-blue-500/20')
    })

    it('aplica estilos neutros por padrão', () => {
      const { container } = render(
        <KPICard
          title="Total"
          value={24}
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('bg-slate-800', 'border-slate-700')
    })
  })

  describe('Tamanhos', () => {
    it('aplica estilos de tamanho pequeno', () => {
      const { container } = render(
        <KPICard
          title="Pequeno"
          value={1}
          size="sm"
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('p-4')
    })

    it('aplica estilos de tamanho médio por padrão', () => {
      const { container } = render(
        <KPICard
          title="Médio"
          value={2}
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('p-6')
    })

    it('aplica estilos de tamanho grande', () => {
      const { container } = render(
        <KPICard
          title="Grande"
          value={3}
          size="lg"
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('p-8')
    })
  })

  describe('Estado de Loading', () => {
    it('renderiza skeleton quando loading é true', () => {
      render(
        <KPICard
          title="Carregando"
          value={0}
          loading={true}
        />
      )

      // Verifica se há elementos de skeleton
      const skeletonElements = document.querySelectorAll('.animate-pulse')
      expect(skeletonElements).toHaveLength(1)

      // Verifica se não renderiza o conteúdo normal
      expect(screen.queryByText('Carregando')).not.toBeInTheDocument()
      expect(screen.queryByText('0')).not.toBeInTheDocument()
    })

    it('não renderiza skeleton quando loading é false', () => {
      render(
        <KPICard
          title="Carregado"
          value={5}
          loading={false}
        />
      )

      expect(screen.getByText('Carregado')).toBeInTheDocument()
      expect(screen.getByText('5')).toBeInTheDocument()
    })
  })

  describe('Tendências', () => {
    it('renderiza tendência positiva', () => {
      render(
        <KPICard
          title="Crescimento"
          value={100}
          trend={{
            value: 15,
            isPositive: true,
            label: 'vs mês anterior'
          }}
        />
      )

      expect(screen.getByText('↗ 15%')).toBeInTheDocument()
      expect(screen.getByText('vs mês anterior')).toBeInTheDocument()
    })

    it('renderiza tendência negativa', () => {
      render(
        <KPICard
          title="Declínio"
          value={50}
          trend={{
            value: 8,
            isPositive: false
          }}
        />
      )

      expect(screen.getByText('↘ 8%')).toBeInTheDocument()
    })

    it('renderiza tendência sem label', () => {
      render(
        <KPICard
          title="Sem Label"
          value={25}
          trend={{
            value: 5,
            isPositive: true
          }}
        />
      )

      expect(screen.getByText('↗ 5%')).toBeInTheDocument()
      expect(screen.queryByText('vs mês anterior')).not.toBeInTheDocument()
    })
  })

  describe('Interações', () => {
    it('chama onClick quando clicado', () => {
      const mockOnClick = jest.fn()

      render(
        <KPICard
          title="Clicável"
          value={10}
          onClick={mockOnClick}
        />
      )

      const card = screen.getByText('Clicável').closest('div')
      fireEvent.click(card!)

      expect(mockOnClick).toHaveBeenCalledTimes(1)
    })

    it('não chama onClick quando não fornecido', () => {
      const mockOnClick = jest.fn()

      render(
        <KPICard
          title="Não Clicável"
          value={10}
        />
      )

      const card = screen.getByText('Não Clicável').closest('div')
      fireEvent.click(card!)

      expect(mockOnClick).not.toHaveBeenCalled()
    })

    it('aplica cursor pointer quando onClick é fornecido', () => {
      const { container } = render(
        <KPICard
          title="Clicável"
          value={10}
          onClick={() => {}}
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('cursor-pointer')
    })
  })

  describe('Formatação de Números', () => {
    it('formata números grandes corretamente', () => {
      render(
        <KPICard
          title="Valor Grande"
          value={1234567}
        />
      )

      expect(screen.getByText('1.234.567')).toBeInTheDocument()
    })

    it('formata números decimais corretamente', () => {
      render(
        <KPICard
          title="Valor Decimal"
          value={1234.56}
        />
      )

      expect(screen.getByText('1.234,56')).toBeInTheDocument()
    })
  })

  describe('Classes CSS Customizadas', () => {
    it('aplica className customizada', () => {
      const { container } = render(
        <KPICard
          title="Customizado"
          value={5}
          className="custom-class"
        />
      )

      const card = container.firstChild as HTMLElement
      expect(card).toHaveClass('custom-class')
    })
  })
})

describe('KPIIcons', () => {
  it('renderiza ícone de projetos', () => {
    render(
      <KPICard
        title="Projetos"
        value={10}
        icon={KPIIcons.Projects}
      />
    )

    // Verifica se o SVG está presente
    const svg = document.querySelector('svg')
    expect(svg).toBeInTheDocument()
  })

  it('renderiza ícone de ações', () => {
    render(
      <KPICard
        title="Ações"
        value={5}
        icon={KPIIcons.Actions}
      />
    )

    const svg = document.querySelector('svg')
    expect(svg).toBeInTheDocument()
  })

  it('renderiza ícone de dinheiro', () => {
    render(
      <KPICard
        title="Valor"
        value="R$ 100.000"
        icon={KPIIcons.Money}
      />
    )

    const svg = document.querySelector('svg')
    expect(svg).toBeInTheDocument()
  })

  it('renderiza ícone de usuários', () => {
    render(
      <KPICard
        title="Usuários"
        value={25}
        icon={KPIIcons.Users}
      />
    )

    const svg = document.querySelector('svg')
    expect(svg).toBeInTheDocument()
  })

  it('renderiza ícone de relógio', () => {
    render(
      <KPICard
        title="Tempo"
        value="2h"
        icon={KPIIcons.Clock}
      />
    )

    const svg = document.querySelector('svg')
    expect(svg).toBeInTheDocument()
  })

  it('renderiza ícone de check', () => {
    render(
      <KPICard
        title="Concluído"
        value={8}
        icon={KPIIcons.CheckCircle}
      />
    )

    const svg = document.querySelector('svg')
    expect(svg).toBeInTheDocument()
  })

  it('renderiza ícone de alerta', () => {
    render(
      <KPICard
        title="Alerta"
        value={3}
        icon={KPIIcons.Alert}
      />
    )

    const svg = document.querySelector('svg')
    expect(svg).toBeInTheDocument()
  })
})
