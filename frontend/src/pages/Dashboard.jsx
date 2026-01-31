import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTranslation } from 'react-i18next'
import axios from 'axios'
import { TrendingUp, Upload, FileText, LogOut, FileCheck, Building2, Receipt } from 'lucide-react'
import LanguageSelector from '../components/LanguageSelector'

export default function Dashboard() {
  const [analyses, setAnalyses] = useState([])
  const [loading, setLoading] = useState(true)
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const { t } = useTranslation()

  useEffect(() => {
    fetchAnalyses()
  }, [])

  const fetchAnalyses = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('/api/analysis/list/all', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      setAnalyses(response.data.analyses)
    } catch (error) {
      console.error('Error fetching analyses:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRiskBadgeColor = (riskBand) => {
    switch (riskBand) {
      case 'Safe': return 'bg-green-100 text-green-800'
      case 'Watch': return 'bg-yellow-100 text-yellow-800'
      case 'Critical': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const translateRiskBand = (riskBand) => {
    const mapping = {
      'Safe': 'safe',
      'Watch': 'watch',
      'Critical': 'critical'
    }
    return t(mapping[riskBand] || riskBand.toLowerCase())
  }

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-600'
    if (score >= 40) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="header-glass sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-white gradient-text-neon">{t('dashboard')}</h1>
              <p className="text-sm text-gray-300">{user?.company_name}</p>
            </div>
            <div className="flex items-center gap-4">
              <LanguageSelector />
              <button
                onClick={logout}
                className="flex items-center gap-2 px-4 py-2 text-gray-300 hover:text-white transition-colors"
              >
                <LogOut size={20} />
                {t('logout')}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 animate-fadeInUp">
          <button
            onClick={() => navigate('/upload')}
            className="feature-card text-white p-6 flex items-center gap-4 neon-blue"
          >
            <Upload size={32} className="text-blue-400" />
            <div className="text-left">
              <h3 className="text-lg font-semibold">{t('uploadData')}</h3>
              <p className="text-sm text-gray-300">{t('uploadDataDesc')}</p>
            </div>
          </button>

          <button
            onClick={() => navigate('/tax-compliance')}
            className="feature-card text-white p-6 flex items-center gap-4 neon-purple"
          >
            <FileCheck size={32} className="text-green-400" />
            <div className="text-left">
              <h3 className="text-lg font-semibold">{t('taxCompliance')}</h3>
              <p className="text-sm text-gray-300">{t('taxComplianceDesc')}</p>
            </div>
          </button>

          <button
            onClick={() => navigate('/gst')}
            className="feature-card text-white p-6 flex items-center gap-4 neon-pink"
          >
            <Receipt size={32} className="text-purple-400" />
            <div className="text-left">
              <h3 className="text-lg font-semibold">{t('gstReturns')}</h3>
              <p className="text-sm text-gray-300">{t('gstReturnsDesc')}</p>
            </div>
          </button>

          <button
            onClick={() => navigate('/banking')}
            className="feature-card text-white p-6 flex items-center gap-4 neon-blue"
          >
            <Building2 size={32} className="text-indigo-400" />
            <div className="text-left">
              <h3 className="text-lg font-semibold">{t('banking')}</h3>
              <p className="text-sm text-gray-300">{t('bankingDesc')}</p>
            </div>
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="stat-card-glow">
            <div className="flex items-center gap-4">
              <TrendingUp size={32} className="text-blue-400" />
              <div>
                <h3 className="text-sm text-gray-400">{t('totalAnalyses')}</h3>
                <p className="text-3xl font-bold text-white">{analyses.length}</p>
              </div>
            </div>
          </div>

          <div className="stat-card-glow">
            <div className="flex items-center gap-4">
              <FileCheck size={32} className="text-green-400" />
              <div>
                <h3 className="text-sm text-gray-400">{t('taxComplianceStatus')}</h3>
                <p className="text-2xl font-bold text-green-400">{t('active')}</p>
              </div>
            </div>
          </div>

          <div className="stat-card-glow">
            <div className="flex items-center gap-4">
              <Building2 size={32} className="text-purple-400" />
              <div>
                <h3 className="text-sm text-gray-400">{t('bankingStatus')}</h3>
                <p className="text-2xl font-bold text-purple-400">{t('ready')}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Analyses */}
        <div className="glass-card">
          <div className="px-6 py-4 border-b border-white/10">
            <h2 className="text-xl font-semibold text-white">{t('recentAnalyses')}</h2>
          </div>

          {loading ? (
            <div className="p-8 text-center">
              <div className="spinner-dark mx-auto"></div>
              <p className="mt-4 text-gray-300">{t('loading')}</p>
            </div>
          ) : analyses.length === 0 ? (
            <div className="p-8 text-center text-gray-400">
              <FileText size={48} className="mx-auto mb-4 text-gray-500" />
              <p>{t('noAnalyses')}</p>
            </div>
          ) : (
            <div className="divide-y divide-white/10">
              {analyses.map((analysis) => (
                <div
                  key={analysis.id}
                  onClick={() => navigate(`/analysis/${analysis.id}`)}
                  className="p-6 hover:bg-white/5 cursor-pointer transition"
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`text-3xl font-bold ${getScoreColor(analysis.health_score)}`}>
                          {analysis.health_score}
                        </span>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          analysis.risk_band === 'Safe' ? 'score-badge-safe' :
                          analysis.risk_band === 'Watch' ? 'score-badge-watch' :
                          'score-badge-critical'
                        }`}>
                          {translateRiskBand(analysis.risk_band)}
                        </span>
                      </div>
                      <p className="text-sm text-gray-400">
                        {new Date(analysis.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </p>
                    </div>
                    <button className="text-blue-400 hover:text-blue-300 font-medium">
                      {t('viewDetails')} →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
