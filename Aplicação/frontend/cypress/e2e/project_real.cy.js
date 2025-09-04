describe('Fluxo de projetos (mockado com fixtures)', () => {
  it('abre detalhe de projeto com dados mockados', () => {
    // Intercepta apenas as chamadas da API do detalhe
    cy.intercept('GET', '**/api/v1/projects/1', { fixture: 'project_1.json' }).as('getProject')
    cy.intercept('GET', '**/api/v1/projects/1/action-items*', { fixture: 'action_items_project_1.json' }).as('getActionItems')
    cy.intercept('GET', '**/api/v1/projects/1/checklist-groups*', { fixture: 'checklist_groups_project_1.json' }).as('getChecklist')

    // Vai direto para a rota de detalhes
    cy.visit('/projects/1')

    // Aguarda os dados mockados
    cy.wait('@getProject')

    // Confirma carregamento básico da página
    cy.get('h1, h2, h3', { timeout: 10000 }).should('exist')
  })
})


