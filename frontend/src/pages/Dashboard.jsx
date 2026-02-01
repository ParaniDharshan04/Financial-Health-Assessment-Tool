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
        {/* Metric Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6 animate-fadeInUp">
          <div className="metric-card">
            <div className="flex justify-between items-start mb-3">
              <div>
                <p className="text-sm text-gray-400 mb-2">{t('totalAnalyses')}</p>
                <p className="text-3xl font-bold text-white">{analyses.length}</p>
              </div>
              <TrendingUp size={28} className="text-purple-400" />
            </div>
            <div className="sparkline-container">
              <div className="h-8 flex items-end gap-1">
                {[40, 60, 45, 70, 55, 80, 65].map((height, i) => (
                  <div key={i} className="flex-1 bg-green-400/30 rounded-t" style={{height: `${height}%`}}></div>
                ))}
              </div>
            </div>
          </div>

          <div className="metric-card">
            <div className="flex justify-between items-start mb-3">
              <div>
                <p className="text-sm text-gray-400 mb-2">{t('taxComplianceStatus')}</p>
                <p className="text-3xl font-bold text-blue-400">{t('active')}</p>
              </div>
              <FileCheck size={28} className="text-blue-400" />
            </div>
            <div className="sparkline-container">
              <div className="h-8 flex items-end gap-1">
                {[70, 75, 80, 78, 85, 88, 90].map((height, i) => (
                  <div key={i} className="flex-1 bg-green-400/30 rounded-t" style={{height: `${height}%`}}></div>
                ))}
              </div>
            </div>
          </div>

          <div className="metric-card">
            <div className="flex justify-between items-start mb-3">
              <div>
                <p className="text-sm text-gray-400 mb-2">{t('bankingStatus')}</p>
                <p className="text-3xl font-bold text-cyan-400">{t('ready')}</p>
              </div>
              <Building2 size={28} className="text-cyan-400" />
            </div>
            <div className="sparkline-container">
              <div className="h-8 flex items-end gap-1">
                {[50, 55, 60, 58, 65, 70, 75].map((height, i) => (
                  <div key={i} className="flex-1 bg-green-400/30 rounded-t" style={{height: `${height}%`}}></div>
                ))}
              </div>
            </div>
          </div>

          <div className="metric-card">
            <div className="flex justify-between items-start mb-3">
              <div>
                <p className="text-sm text-gray-400 mb-2">{t('gstReturns')}</p>
                <p className="text-3xl font-bold text-white">3</p>
              </div>
              <Receipt size={28} className="text-indigo-400" />
            </div>
            <div className="sparkline-container">
              <div className="h-8 flex items-end gap-1">
                {[60, 65, 70, 68, 75, 80, 85].map((height, i) => (
                  <div key={i} className="flex-1 bg-green-400/30 rounded-t" style={{height: `${height}%`}}></div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <button
            onClick={() => navigate('/upload')}
            className="metric-card hover:scale-105 transition-transform text-left"
          >
            <Upload size={32} className="text-purple-400 mb-3" />
            <h3 className="text-base font-semibold text-white">{t('uploadData')}</h3>
            <p className="text-sm text-gray-400 mt-2">{t('uploadDataDesc')}</p>
          </button>

          <button
            onClick={() => navigate('/tax-compliance')}
            className="metric-card hover:scale-105 transition-transform text-left"
          >
            <FileCheck size={32} className="text-blue-400 mb-3" />
            <h3 className="text-base font-semibold text-white">{t('taxCompliance')}</h3>
            <p className="text-sm text-gray-400 mt-2">{t('taxComplianceDesc')}</p>
          </button>

          <button
            onClick={() => navigate('/gst')}
            className="metric-card hover:scale-105 transition-transform text-left"
          >
            <Receipt size={32} className="text-indigo-400 mb-3" />
            <h3 className="text-base font-semibold text-white">{t('gstReturns')}</h3>
            <p className="text-sm text-gray-400 mt-2">{t('gstReturnsDesc')}</p>
          </button>

          <button
            onClick={() => navigate('/banking')}
            className="metric-card hover:scale-105 transition-transform text-left"
          >
            <Building2 size={32} className="text-cyan-400 mb-3" />
            <h3 className="text-base font-semibold text-white">{t('banking')}</h3>
            <p className="text-sm text-gray-400 mt-2">{t('bankingDesc')}</p>
          </button>
        </div>

        {/* Recent Analyses */}
        <div className="metric-card" data-section="analyses">
          <div className="mb-4">
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
            <div className="space-y-3">
              {analyses.map((analysis) => (
                <div
                  key={analysis.id}
                  onClick={() => navigate(`/analysis/${analysis.id}`)}
                  className="p-5 bg-white/5 rounded-xl hover:bg-white/10 cursor-pointer transition border border-white/10"
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`text-3xl font-bold ${getScoreColor(analysis.health_score)}`}>
                          {analysis.health_score}
                        </span>
                        <span className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                          analysis.risk_band === 'Safe' ? 'bg-green-500/20 text-green-400' :
                          analysis.risk_band === 'Watch' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-red-500/20 text-red-400'
                        }`}>
                          {translateRiskBand(analysis.risk_band)}
                        </span>
                      </div>
                      <p className="text-sm text-gray-400">
                        {new Date(analysis.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric'
                        })}
                      </p>
                    </div>
                    <button className="text-purple-400 hover:text-purple-300 text-base font-medium">
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
