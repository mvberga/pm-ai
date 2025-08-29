import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: process.env.CYPRESS_BASE_URL || 'http://localhost:5173',
    video: false,
    screenshotOnRunFailure: true,
    supportFile: 'cypress/support/e2e.js'
  }
})
