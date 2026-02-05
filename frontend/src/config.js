// API Configuration
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Configure axios defaults globally
import axios from 'axios'

axios.defaults.baseURL = API_URL

export default axios
