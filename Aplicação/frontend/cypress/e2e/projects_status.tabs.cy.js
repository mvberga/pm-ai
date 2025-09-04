// Cypress E2E: Alternância de abas no Report Executivo (/projects/status)
/// <reference types="cypress" />

describe('Report Executivo - Abas', () => {
  beforeEach(() => {
    cy.visit('/projects/status')
  })

  it('exibe Visão Geral por padrão', () => {
    cy.get('[data-testid="tab-overview"]').should('have.attr', 'aria-selected', 'true')
    cy.get('[data-testid="panel-overview"]').should('be.visible')
    cy.get('[data-testid="panel-timeline"]').should('not.exist')
    cy.get('[data-testid="panel-financial"]').should('not.exist')
  })

  it('alterna para Cronograma e depois Financeiro', () => {
    cy.get('[data-testid="tab-timeline"]').click()
    cy.get('[data-testid="tab-timeline"]').should('have.attr', 'aria-selected', 'true')
    cy.get('[data-testid="panel-timeline"]').should('be.visible')
    cy.get('[data-testid="panel-overview"]').should('not.exist')

    cy.get('[data-testid="tab-financial"]').click()
    cy.get('[data-testid="tab-financial"]').should('have.attr', 'aria-selected', 'true')
    cy.get('[data-testid="panel-financial"]').should('be.visible')
    cy.get('[data-testid="panel-timeline"]').should('not.exist')
  })
})
