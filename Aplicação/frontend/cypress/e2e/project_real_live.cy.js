// Teste E2E opcional contra backend real
// Execute com: npm run cypress:run:live  (ou: npx cypress run --env RUN_LIVE=1 --spec cypress/e2e/project_real_live.cy.js)

describe('Fluxo real contra backend (opcional)', () => {
  it('lista projetos reais e abre detalhe', function () {
    if (!Cypress.env('RUN_LIVE')) {
      // pular de forma programática quando não estiver habilitado
      this.skip()
    }

    cy.visit('/projects')

    // Aguarda renderização básica
    cy.contains('Projetos', { timeout: 15000 })

    // Aguarda término de spinners (se houver)
    cy.get('body').then($body => {
      const hasSpinner = $body.find('.animate-spin').length > 0
      if (hasSpinner) {
        cy.get('.animate-spin', { timeout: 15000 }).should('not.exist')
      }
    })

    // Verifica que há ao menos um projeto visível e navega
    cy.get('a[href*="/projects/"]').first().click()

    // Confirma que carregou detalhe
    cy.url().should('include', '/projects/')
  })
})


