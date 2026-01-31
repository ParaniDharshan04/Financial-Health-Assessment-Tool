import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Analysis from './pages/Analysis'
import TaxCompliance from './pages/TaxCompliance'
import GSTManagement from './pages/GSTManagement'
import Banking from './pages/Banking'
import { AuthProvider, useAuth } from './context/AuthContext'

function PrivateRoute({ children }) {
  const { user } = useAuth()
  return user ? children : <Navigate to="/login" />
}

function App() {
  return (
    <AuthProvider>
      <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/upload" element={<PrivateRoute><Upload /></PrivateRoute>} />
          <Route path="/analysis/:id" element={<PrivateRoute><Analysis /></PrivateRoute>} />
          <Route path="/tax-compliance" element={<PrivateRoute><TaxCompliance /></PrivateRoute>} />
          <Route path="/gst" element={<PrivateRoute><GSTManagement /></PrivateRoute>} />
          <Route path="/banking" element={<PrivateRoute><Banking /></PrivateRoute>} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
