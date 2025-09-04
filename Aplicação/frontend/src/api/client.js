import axios from 'axios'

// Configuração compatível com Jest e Vite (sem usar import.meta)
const getBaseURL = () => {
  // Ambiente de teste (Jest)
  if (typeof process !== 'undefined' && process.env && process.env.NODE_ENV === 'test') {
    return 'http://localhost:8000/api/v1'
  }

  // Preferir variável de ambiente se disponível (útil para Jest e ambientes configurados)
  if (typeof process !== 'undefined' && process.env && process.env.VITE_API_URL) {
    return process.env.VITE_API_URL
  }

  // Para Cypress E2E - usa backend interno
  if (typeof window !== 'undefined' && window.location && window.location.hostname === 'frontend') {
    return 'http://backend:8000/api/v1'
  }

  // Fallback para localhost
  return 'http://localhost:8000/api/v1'
}

const api = axios.create({
  baseURL: getBaseURL()
})

export default api
