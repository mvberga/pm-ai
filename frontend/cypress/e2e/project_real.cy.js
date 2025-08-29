describe('Fluxo real contra backend', () => {
  it('lista projetos seed e abre detalhe', () => {
    cy.visit('/projects')
    cy.contains('Projetos')
    // nomes inseridos via seed em db/init/01_init.sql
    cy.contains('Lagoa Santa - Notas e Livro').click()
    cy.contains('Lagoa Santa - Notas e Livro')
    cy.contains('Checklist')
    cy.contains('Central de Ações')
  })
})


