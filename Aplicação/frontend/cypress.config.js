import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: process.env.CYPRESS_BASE_URL || 'http://localhost:5174',
    video: false,
    screenshotOnRunFailure: true,
    supportFile: 'cypress/support/e2e.js'
  },
  env: {
    // Disponibiliza ambas as chaves para compatibilidade nos specs
    api: process.env.CYPRESS_API || process.env.API || 'http://localhost:8000/api/v1',
    API: process.env.CYPRESS_API || process.env.API || 'http://localhost:8000/api/v1',
    RUN_LIVE: process.env.RUN_LIVE || false
  }
})
