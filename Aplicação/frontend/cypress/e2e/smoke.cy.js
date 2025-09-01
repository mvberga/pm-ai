describe('Smoke', () => {
  it('abre dashboard e navega para projetos', () => {
    cy.visit('/')
    cy.contains('PM AI MVP')
    cy.contains('Projetos').click()
    cy.url().should('include', '/projects')
    cy.contains('Projetos')
  })
})
