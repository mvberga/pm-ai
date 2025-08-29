const API = 'http://localhost:8000/api/v1'

describe('Fluxo de Projeto (mockado)', () => {
  it('lista projetos, abre detalhe, cria ação e grupo', () => {
    // Listagem de projetos
    cy.intercept('GET', `${API}/projects`, {
      statusCode: 200,
      body: [{ id: 1, name: 'Projeto Cypress' }]
    }).as('getProjects')

    // Detalhe do projeto
    cy.intercept('GET', `${API}/projects/1`, {
      statusCode: 200,
      body: { id: 1, name: 'Projeto Cypress', description: 'Desc' }
    }).as('getProjectDetail')

    // Checklist groups vazio inicialmente
    cy.intercept('GET', `${API}/projects/1/checklist-groups`, {
      statusCode: 200,
      body: []
    }).as('getGroupsEmpty')

    // Action items vazio inicialmente
    cy.intercept('GET', `${API}/projects/1/action-items*`, {
      statusCode: 200,
      body: []
    }).as('getActionsEmpty')

    // Visita lista de projetos
    cy.visit('/projects')
    cy.wait('@getProjects')
    cy.contains('Projeto Cypress').click()

    // Página de detalhes
    cy.wait('@getProjectDetail')
    cy.wait('@getGroupsEmpty')
    cy.contains('Projeto Cypress')

    // Central de Ações: criar nova ação
    cy.intercept('POST', `${API}/projects/1/action-items`, {
      statusCode: 201,
      body: { id: 99 }
    }).as('createAction')
    cy.intercept('GET', `${API}/projects/1/action-items*`, {
      statusCode: 200,
      body: [{ id: 99, title: 'Ação Teste', type: 'Ação Pontual' }]
    }).as('getActionsAfter')

    cy.contains('Central de Ações').click()
    cy.window().then((win) => {
      const promptStub = cy.stub(win, 'prompt')
      promptStub.onCall(0).returns('Ação Teste') // título ação
      promptStub.onCall(1).returns('Ação Pontual') // tipo ação
      promptStub.onCall(2).returns('Item 1') // título do item checklist
      cy.stub(win, 'confirm').returns(true)
    })
    cy.contains('+ Nova Ação').click()
    cy.wait('@createAction')
    cy.wait('@getActionsAfter')
    cy.contains('Ação Teste')

    // Checklist: criar novo grupo e adicionar item
    cy.contains('Checklist').click()
    cy.intercept('POST', `${API}/projects/1/checklist-groups`, {
      statusCode: 201,
      body: { id: 10, name: 'Grupo E2E' }
    }).as('createGroup')
    cy.intercept('GET', `${API}/projects/1/checklist-groups`, {
      statusCode: 200,
      body: [{ id: 10, name: 'Grupo E2E' }]
    }).as('getGroupsAfter')

    cy.get('input[placeholder="Novo grupo"]').type('Grupo E2E')
    cy.contains('Adicionar Grupo').click()
    cy.wait('@createGroup')
    cy.wait('@getGroupsAfter')
    cy.contains('Grupo E2E')

    cy.intercept('POST', `${API}/checklist-groups/10/items`, {
      statusCode: 201,
      body: { id: 100 }
    }).as('createItem')
    cy.contains('+ Item').click()
    cy.wait('@createItem')
  })
})


