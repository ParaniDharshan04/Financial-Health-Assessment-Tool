import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Home, TrendingUp, FileText, Receipt, Building2 } from 'lucide-react'

export default function BottomNav() {
  const navigate = useNavigate()
  const location = useLocation()

  const handleNavigation = (path, label) => {
    // For Analysis, scroll to the analyses section on dashboard
    if (label === 'Analysis') {
      navigate('/')
      setTimeout(() => {
        const analysesSection = document.querySelector('[data-section="analyses"]')
        if (analysesSection) {
          analysesSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      }, 100)
    } else {
      navigate(path)
    }
  }

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/', icon: TrendingUp, label: 'Analysis' },
    { path: '/tax-compliance', icon: FileText, label: 'Tax' },
    { path: '/gst', icon: Receipt, label: 'GST' },
    { path: '/banking', icon: Building2, label: 'Banking' }
  ]

  return (
    <nav className="bottom-nav">
      {navItems.map((item) => {
        const Icon = item.icon
        const isActive = (item.label === 'Home' && location.pathname === '/') ||
                        (item.label === 'Analysis' && (location.pathname === '/' || location.pathname.startsWith('/analysis/'))) ||
                        (item.label !== 'Home' && item.label !== 'Analysis' && location.pathname === item.path)
        
        return (
          <button
            key={item.label}
            onClick={() => handleNavigation(item.path, item.label)}
            className={`bottom-nav-item ${isActive ? 'active' : ''}`}
          >
            <Icon size={20} />
            <span className="text-xs mt-1">{item.label}</span>
          </button>
        )
      })}
    </nav>
  )
}
