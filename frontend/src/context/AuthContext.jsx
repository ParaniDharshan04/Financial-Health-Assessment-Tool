import React, { createContext, useState, useContext, useEffect } from 'react'
import axios from 'axios'
import '../config' // Import to configure axios defaults

const AuthContext = createContext()

export function useAuth() {
  return useContext(AuthContext)
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      const userData = JSON.parse(localStorage.getItem('user') || '{}')
      setUser(userData)
    }
    setLoading(false)
  }, [token])

  const login = async (email, password) => {
    const response = await axios.post('/api/auth/login', { email, password })
    const { access_token, user: userData } = response.data
    
    localStorage.setItem('token', access_token)
    localStorage.setItem('user', JSON.stringify(userData))
    setToken(access_token)
    setUser(userData)
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    
    return userData
  }

  const register = async (email, password, company_name, industry) => {
    const response = await axios.post('/api/auth/register', {
      email,
      password,
      company_name,
      industry
    })
    const { access_token, user: userData } = response.data
    
    localStorage.setItem('token', access_token)
    localStorage.setItem('user', JSON.stringify(userData))
    setToken(access_token)
    setUser(userData)
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    
    return userData
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken(null)
    setUser(null)
    delete axios.defaults.headers.common['Authorization']
  }

  const updateUser = (userData) => {
    const updatedUser = { ...user, ...userData }
    setUser(updatedUser)
    localStorage.setItem('user', JSON.stringify(updatedUser))
  }

  const value = {
    user,
    token,
    login,
    register,
    logout,
    updateUser,
    loading
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
