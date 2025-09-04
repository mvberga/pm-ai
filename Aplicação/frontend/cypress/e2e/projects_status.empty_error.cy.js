/// <reference types="cypress" />

describe('Report Executivo - Estados vazio e erro', () => {
  it('exibe estado vazio quando não há projetos', () => {
    cy.intercept('GET', '**/api/v1/projects*', { statusCode: 200, body: [] }).as('getProjectsEmpty');
    cy.visit('/projects/status');
    cy.wait('@getProjectsEmpty');

    // Deve existir a tabela (container) e mensagem de vazio
    cy.get('[data-testid="projects-table"]').should('exist');
    cy.contains('Nenhum projeto encontrado').should('exist');
  });

  it('exibe estado de erro quando a API falha', () => {
    cy.intercept('GET', '**/api/v1/projects*', { statusCode: 500, body: { detail: 'Erro' } }).as('getProjectsError');
    cy.visit('/projects/status');
    cy.wait('@getProjectsError');

    cy.contains('Erro ao carregar projetos').should('exist');
  });
});


