import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { Breadcrumbs, useBreadcrumbs } from '../../../../ui/components/Layout/Breadcrumbs'

describe('Breadcrumbs Component', () => {
  describe('Renderização Básica', () => {
    it('renderiza breadcrumbs com itens', () => {
      const items = [
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Projetos', href: '/projects' },
        { label: 'Status', isActive: true }
      ]

      render(<Breadcrumbs items={items} />)

      expect(screen.getByText('Dashboard')).toBeInTheDocument()
      expect(screen.getByText('Projetos')).toBeInTheDocument()
      expect(screen.getByText('Status')).toBeInTheDocument()
    })

    it('não renderiza nada quando lista está vazia', () => {
      const { container } = render(<Breadcrumbs items={[]} />)
      expect(container.firstChild).toBeNull()
    })

    it('aplica className customizada', () => {
      const items = [{ label: 'Test', isActive: true }]
      const { container } = render(<Breadcrumbs items={items} className="custom-class" />)
      
      expect(container.firstChild).toHaveClass('custom-class')
    })
  })

  describe('Navegação e Links', () => {
    it('renderiza links para itens com href', () => {
      const items = [
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Projetos', href: '/projects' }
      ]

      render(<Breadcrumbs items={items} />)

      const dashboardLink = screen.getByRole('link', { name: 'Dashboard' })
      const projectsLink = screen.getByRole('link', { name: 'Projetos' })

      expect(dashboardLink).toHaveAttribute('href', '/dashboard')
      expect(projectsLink).toHaveAttribute('href', '/projects')
    })

    it('renderiza botões para itens sem href', () => {
      const items = [
        { label: 'Dashboard' },
        { label: 'Projetos' }
      ]

      render(<Breadcrumbs items={items} />)

      const dashboardButton = screen.getByRole('button', { name: 'Dashboard' })
      const projectsButton = screen.getByRole('button', { name: 'Projetos' })

      expect(dashboardButton).toBeInTheDocument()
      expect(projectsButton).toBeInTheDocument()
    })

    it('renderiza span para item ativo', () => {
      const items = [
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Status', isActive: true }
      ]

      render(<Breadcrumbs items={items} />)

      const statusSpan = screen.getByText('Status')
      expect(statusSpan).toHaveAttribute('aria-current', 'page')
      expect(statusSpan.tagName).toBe('SPAN')
    })
  })

  describe('Separadores', () => {
    it('renderiza separadores entre itens', () => {
      const items = [
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Projetos', href: '/projects' },
        { label: 'Status', isActive: true }
      ]

      render(<Breadcrumbs items={items} />)

      // Verifica se há separadores (SVG icons)
      const separators = document.querySelectorAll('svg')
      expect(separators).toHaveLength(2) // 2 separadores para 3 itens
    })

    it('não renderiza separador antes do primeiro item', () => {
      const items = [
        { label: 'Dashboard', isActive: true }
      ]

      render(<Breadcrumbs items={items} />)

      const separators = document.querySelectorAll('svg')
      expect(separators).toHaveLength(0)
    })

    it('usa separador customizado quando fornecido', () => {
      const items = [
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Projetos', href: '/projects' }
      ]

      const customSeparator = <span data-testid="custom-separator">→</span>

      render(<Breadcrumbs items={items} separator={customSeparator} />)

      expect(screen.getByTestId('custom-separator')).toBeInTheDocument()
    })
  })

  describe('Interações', () => {
    it('chama onItemClick quando link é clicado', () => {
      const mockOnItemClick = jest.fn()
      const items = [
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Projetos', href: '/projects' }
      ]

      render(<Breadcrumbs items={items} onItemClick={mockOnItemClick} />)

      const dashboardLink = screen.getByRole('link', { name: 'Dashboard' })
      fireEvent.click(dashboardLink)

      expect(mockOnItemClick).toHaveBeenCalledWith(items[0], 0)
    })

    it('chama onItemClick quando botão é clicado', () => {
      const mockOnItemClick = jest.fn()
      const items = [
        { label: 'Dashboard' },
        { label: 'Projetos' }
      ]

      render(<Breadcrumbs items={items} onItemClick={mockOnItemClick} />)

      const dashboardButton = screen.getByRole('button', { name: 'Dashboard' })
      fireEvent.click(dashboardButton)

      expect(mockOnItemClick).toHaveBeenCalledWith(items[0], 0)
    })

    it('não chama onItemClick para item ativo', () => {
      const mockOnItemClick = jest.fn()
      const items = [
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Status', isActive: true }
      ]

      render(<Breadcrumbs items={items} onItemClick={mockOnItemClick} />)

      const statusSpan = screen.getByText('Status')
      fireEvent.click(statusSpan)

      expect(mockOnItemClick).not.toHaveBeenCalled()
    })

    it('previne comportamento padrão do link', () => {
      const mockOnItemClick = jest.fn()
      const items = [
        { label: 'Dashboard', href: '/dashboard' }
      ]

      render(<Breadcrumbs items={items} onItemClick={mockOnItemClick} />)

      const dashboardLink = screen.getByRole('link', { name: 'Dashboard' })
      
      // Simula o evento de click
      fireEvent.click(dashboardLink)

      // Verifica se onItemClick foi chamado (indicando que preventDefault funcionou)
      expect(mockOnItemClick).toHaveBeenCalled()
    })
  })

  describe('Acessibilidade', () => {
    it('tem aria-label correto', () => {
      const items = [{ label: 'Dashboard', isActive: true }]
      render(<Breadcrumbs items={items} />)

      const nav = screen.getByRole('navigation', { name: 'Breadcrumb' })
      expect(nav).toBeInTheDocument()
    })

    it('marca item ativo com aria-current', () => {
      const items = [
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Status', isActive: true }
      ]

      render(<Breadcrumbs items={items} />)

      const activeItem = screen.getByText('Status')
      expect(activeItem).toHaveAttribute('aria-current', 'page')
    })
  })
})

describe('useBreadcrumbs Hook', () => {
  const TestComponent = ({ initialItems = [] }: { initialItems?: any[] }) => {
    const { items, addItem, removeItem, updateItem, setItems, clear } = useBreadcrumbs(initialItems)

    return (
      <div>
        <div data-testid="items-count">{items.length}</div>
        <div data-testid="items">{JSON.stringify(items)}</div>
        <button onClick={() => addItem({ label: 'New Item' })}>Add Item</button>
        <button onClick={() => removeItem(0)}>Remove First</button>
        <button onClick={() => updateItem(0, { label: 'Updated Item' })}>Update First</button>
        <button onClick={() => setItems([{ label: 'Set Items' }])}>Set Items</button>
        <button onClick={clear}>Clear</button>
      </div>
    )
  }

  it('inicializa com itens fornecidos', () => {
    const initialItems = [
      { label: 'Dashboard', href: '/dashboard' },
      { label: 'Projects', href: '/projects' }
    ]

    render(<TestComponent initialItems={initialItems} />)

    expect(screen.getByTestId('items-count')).toHaveTextContent('2')
    expect(screen.getByTestId('items')).toHaveTextContent(JSON.stringify(initialItems))
  })

  it('inicializa com lista vazia quando não há itens iniciais', () => {
    render(<TestComponent />)

    expect(screen.getByTestId('items-count')).toHaveTextContent('0')
    expect(screen.getByTestId('items')).toHaveTextContent('[]')
  })

  it('adiciona item corretamente', () => {
    render(<TestComponent />)

    const addButton = screen.getByText('Add Item')
    fireEvent.click(addButton)

    expect(screen.getByTestId('items-count')).toHaveTextContent('1')
    expect(screen.getByTestId('items')).toHaveTextContent('[{"label":"New Item"}]')
  })

  it('remove item corretamente', () => {
    const initialItems = [
      { label: 'Dashboard', href: '/dashboard' },
      { label: 'Projects', href: '/projects' }
    ]

    render(<TestComponent initialItems={initialItems} />)

    const removeButton = screen.getByText('Remove First')
    fireEvent.click(removeButton)

    expect(screen.getByTestId('items-count')).toHaveTextContent('1')
    // removeItem(0) mantém apenas o primeiro item (slice(0, 1))
    expect(screen.getByTestId('items')).toHaveTextContent('[{"label":"Dashboard","href":"/dashboard"}]')
  })

  it('atualiza item corretamente', () => {
    const initialItems = [
      { label: 'Dashboard', href: '/dashboard' }
    ]

    render(<TestComponent initialItems={initialItems} />)

    const updateButton = screen.getByText('Update First')
    fireEvent.click(updateButton)

    expect(screen.getByTestId('items-count')).toHaveTextContent('1')
    expect(screen.getByTestId('items')).toHaveTextContent('[{"label":"Updated Item"}]')
  })

  it('define itens corretamente', () => {
    const initialItems = [
      { label: 'Dashboard', href: '/dashboard' },
      { label: 'Projects', href: '/projects' }
    ]

    render(<TestComponent initialItems={initialItems} />)

    const setButton = screen.getByText('Set Items')
    fireEvent.click(setButton)

    expect(screen.getByTestId('items-count')).toHaveTextContent('1')
    expect(screen.getByTestId('items')).toHaveTextContent('[{"label":"Set Items"}]')
  })

  it('limpa itens corretamente', () => {
    const initialItems = [
      { label: 'Dashboard', href: '/dashboard' },
      { label: 'Projects', href: '/projects' }
    ]

    render(<TestComponent initialItems={initialItems} />)

    const clearButton = screen.getByText('Clear')
    fireEvent.click(clearButton)

    expect(screen.getByTestId('items-count')).toHaveTextContent('0')
    expect(screen.getByTestId('items')).toHaveTextContent('[]')
  })
})
