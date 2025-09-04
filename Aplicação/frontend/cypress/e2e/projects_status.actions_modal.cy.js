/// <reference types="cypress" />

describe('Report Executivo - Modal de Ações', () => {
  beforeEach(() => {
    cy.intercept('GET', '**/api/v1/projects*', (req) => {
      req.reply({
        statusCode: 200,
        body: [
          {
            id: 1,
            name: 'Projeto Teste',
            municipio: 'Cidade X',
            valor_implantacao: 1000,
            valor_recorrente: 100,
            recursos: 1,
            status: 'on_track',
            tipo: 'implantacao',
            data_inicio: '2025-01-01',
            data_fim: '2025-12-31',
            gerente_projeto_id: 1,
            gerente_portfolio_id: 1,
            owner_id: 1,
            created_at: '2025-01-01',
            updated_at: '2025-01-02',
            pending_actions_count: 2
          }
        ]
      });
    }).as('getProjects');

    // Hook useActionItems() sem projectId chama /action-items?project_id=1
    cy.intercept('GET', '**/api/v1/action-items*', (req) => {
      if (req.query && String(req.query.project_id) === '1') {
        req.reply({
          statusCode: 200,
          body: [
            { id: 101, title: 'Ação 1', status: 'pending', priority: 'high', type: 'action' },
            { id: 102, title: 'Ação 2', status: 'in_progress', priority: 'medium', type: 'task' }
          ]
        });
      } else {
        req.reply({ statusCode: 200, body: [] });
      }
    }).as('getActionItems');

    cy.visit('/projects/status');
    cy.wait('@getProjects');
    cy.get('[data-testid="projects-table"]', { timeout: 15000 }).should('exist');
  });

  it('abre e fecha o modal de ações ao clicar no botão', () => {
    cy.contains('Projeto Teste', { timeout: 15000 }).should('exist');

    cy.get('[data-testid="open-actions-1"]').click({ force: true });
    cy.wait('@getActionItems');
    cy.get('[data-testid="actions-modal"]').should('be.visible');

    cy.get('[data-testid="actions-modal-close"]').click();
    cy.get('[data-testid="actions-modal"]').should('not.exist');
  });
});


