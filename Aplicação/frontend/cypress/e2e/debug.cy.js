describe('Debug - Conectividade', () => {
  it('verifica se frontend carrega e faz requisições', () => {
    // Intercepta todas as requisições
    cy.intercept('GET', '**/api/v1/**').as('apiRequests')
    cy.intercept('GET', '**/api/v1/projects').as('projects')
    
    // Visita a página
    cy.visit('/projects')
    
    // Aguarda um pouco para a página carregar
    cy.wait(3000)
    
    // Verifica se a página carregou
    cy.get('body').should('be.visible')
    
    // Verifica se há algum texto na página
    cy.get('body').should('contain.text', 'Projetos')
    
    // Verifica se houve requisições para a API
    cy.get('@apiRequests.all').then((requests) => {
      cy.log(`Número de requisições API: ${requests.length}`)
      if (requests.length > 0) {
        requests.forEach((req, index) => {
          cy.log(`Requisição ${index + 1}:`, req.request.url)
        })
      }
    })
    
    // Verifica especificamente a requisição de projetos
    cy.get('@projects.all').then((requests) => {
      cy.log(`Número de requisições de projetos: ${requests.length}`)
    })
  })
})
