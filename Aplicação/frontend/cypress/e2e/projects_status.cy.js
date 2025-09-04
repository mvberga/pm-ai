/// <reference types="cypress" />

describe('Report Executivo - /projects/status', () => {
  it('abre a página e exibe elementos básicos', () => {
    cy.visit('/projects/status')
    // Deve mostrar título ou algum marcador
    cy.contains('Status Executivo').should('exist')
  })
})


