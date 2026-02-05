// API Configuration
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Export axios instance with base URL
import axios from 'axios'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
