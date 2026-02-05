import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Download, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react'
import axios from 'axios'
import { useTranslation } from 'react-i18next'
import LanguageSelector from '../components/LanguageSelector'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar, Line, Doughnut } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

export default function Analysis() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {
    fetchAnalysis()
  }, [id])

  const fetchAnalysis = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`/api/analysis/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      setAnalysis(response.data)
    } catch (error) {
      console.error('Error fetching analysis:', error)
    } finally {
      setLoading(false)
    }
  }

  const downloadReport = async () => {
    setDownloading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`/api/reports/${id}/pdf`, {
        headers: { 'Authorization': `Bearer ${token}` },
        responseType: 'blob'
      })
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `financial_report_${id}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Error downloading report:', error)
    } finally {
      setDownloading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="spinner-dark mx-auto"></div>
          <p className="mt-4 text-gray-300">{t('loadingAnalysis')}</p>
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-300">{t('analysisNotFound')}</p>
          <button onClick={() => navigate('/')} className="mt-4 text-blue-400 hover:text-blue-300">
            {t('backToDashboard')}
          </button>
        </div>
      </div>
    )
  }

  const getRiskBadgeColor = (riskBand) => {
    switch (riskBand) {
      case 'Safe': return 'bg-green-100 text-green-800 border-green-300'
      case 'Watch': return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'Critical': return 'bg-red-100 text-red-800 border-red-300'
      default: return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-600'
    if (score >= 40) return 'text-yellow-600'
    return 'text-red-600'
  }

  // Chart data
  const componentScoresData = {
    labels: ['Liquidity', 'Profitability', 'Cash Flow', 'Debt Health'],
    datasets: [{
      label: 'Score',
      data: [
        analysis.liquidity_score,
        analysis.profitability_score,
        analysis.cash_flow_score,
        analysis.debt_health_score
      ],
      backgroundColor: [
        'rgba(59, 130, 246, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(139, 92, 246, 0.8)'
      ]
    }]
  }

  const healthScoreData = {
    labels: ['Health Score', 'Remaining'],
    datasets: [{
      data: [analysis.health_score, 100 - analysis.health_score],
      backgroundColor: [
        analysis.health_score >= 70 ? 'rgba(16, 185, 129, 0.8)' :
        analysis.health_score >= 40 ? 'rgba(245, 158, 11, 0.8)' :
        'rgba(239, 68, 68, 0.8)',
        'rgba(229, 231, 235, 0.3)'
      ],
      borderWidth: 0
    }]
  }

  const cashFlowForecastData = analysis.cash_flow_forecast?.forecast ? {
    labels: analysis.cash_flow_forecast.forecast.map(f => f.month),
    datasets: [{
      label: 'Projected Cash Flow',
      data: analysis.cash_flow_forecast.forecast.map(f => f.projected_cash_flow),
      borderColor: 'rgb(59, 130, 246)',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4
    }]
  } : null

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="header-glass sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-gray-300 hover:text-white mb-2 transition-colors"
          >
            <ArrowLeft size={20} />
            {t('backToDashboard')}
          </button>
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-white gradient-text-neon">{t('financialAnalysisReport')}</h1>
            <div className="flex items-center gap-4">
              <LanguageSelector />
              <button
                onClick={downloadReport}
                disabled={downloading}
                className="btn-neon flex items-center gap-2"
              >
                <Download size={20} />
                {downloading ? t('generating') : t('downloadPDF')}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Health Score Overview */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6 animate-fadeInUp">
          <div className="lg:col-span-2 metric-card">
            <h2 className="text-lg font-semibold text-white mb-4">{t('financialHealthScore')}</h2>
            <div className="flex items-center gap-6">
              <div className="text-center">
                <div className={`text-5xl font-bold ${getScoreColor(analysis.health_score)} text-glow`}>
                  {analysis.health_score}
                </div>
                <div className="text-gray-400 mt-2 text-sm">{t('outOf100')}</div>
              </div>
              <div className="flex-1">
                <div className={`inline-block px-3 py-1 rounded-lg text-sm font-semibold mb-3 ${
                  analysis.risk_band === 'Safe' ? 'bg-green-500/20 text-green-400' :
                  analysis.risk_band === 'Watch' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-red-500/20 text-red-400'
                }`}>
                  {t(analysis.risk_band.toLowerCase())}
                </div>
                <p className="text-gray-300 text-sm">
                  {analysis.ai_insights?.summary || 'Analysis complete'}
                </p>
              </div>
            </div>
          </div>

          <div className="metric-card">
            <h3 className="text-sm font-semibold text-white mb-4">{t('scoreDistribution')}</h3>
            <Doughnut data={healthScoreData} options={{ maintainAspectRatio: true }} />
          </div>
        </div>

        {/* Component Scores */}
        <div className="metric-card mb-6">
          <h2 className="text-lg font-semibold text-white mb-4">{t('componentScores')}</h2>
          <Bar
            data={componentScoresData}
            options={{
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true,
                  max: 100,
                  ticks: { color: '#9ca3af' },
                  grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: {
                  ticks: { color: '#9ca3af' },
                  grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
              },
              plugins: {
                legend: { labels: { color: '#fff' } }
              }
            }}
          />
        </div>

        {/* Key Metrics */}
        <div className="metric-card mb-6">
          <h2 className="text-lg font-semibold text-white mb-4">{t('keyFinancialMetrics')}</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {Object.entries(analysis.metrics).slice(0, 8).map(([key, value]) => (
              <div key={key} className="p-3 bg-white/5 rounded-xl hover:scale-105 transition-transform border border-white/10">
                <div className="text-xs text-gray-400 mb-1">
                  {key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                </div>
                <div className="text-xl font-bold text-white">
                  {typeof value === 'number' ? value.toFixed(2) : value}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recommendations */}
        <div className="metric-card mb-6">
          <h2 className="text-lg font-semibold text-white mb-4">{t('recommendations')}</h2>
          <div className="space-y-3">
            {analysis.recommendations?.map((rec, index) => (
              <div key={index} className="p-4 bg-white/5 rounded-xl border-l-4 border-green-500">
                <div className="flex items-start gap-3">
                  <div className={`mt-1 ${rec.priority === 'High' ? 'text-red-400' : 'text-yellow-400'}`}>
                    <AlertCircle size={18} />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="font-semibold text-white text-sm">{rec.title}</h3>
                      <span className={`text-xs px-2 py-1 rounded ${
                        rec.priority === 'High' ? 'bg-red-500/20 text-red-300' : 'bg-yellow-500/20 text-yellow-300'
                      }`}>
                        {t(rec.priority.toLowerCase())} {t('priority')}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm mb-2">{rec.description}</p>
                    {rec.actions && (
                      <ul className="space-y-1">
                        {rec.actions.map((action, i) => (
                          <li key={i} className="flex items-start gap-2 text-xs text-gray-400">
                            <CheckCircle size={14} className="mt-0.5 text-green-400" />
                            {action}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Cash Flow Forecast */}
        {cashFlowForecastData && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {t('cashFlowForecast')}
            </h2>
            <div className="mb-4">
              <span className="text-sm text-gray-600">{t('trend')}: </span>
              <span className={`font-semibold ${
                analysis.cash_flow_forecast.trend === 'Improving' ? 'text-green-600' :
                analysis.cash_flow_forecast.trend === 'Declining' ? 'text-red-600' :
                'text-gray-600'
              }`}>
                {analysis.cash_flow_forecast.trend}
              </span>
            </div>
            <Line data={cashFlowForecastData} options={{ responsive: true }} />
          </div>
        )}

        {/* Industry Comparison */}
        {analysis.industry_comparison && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">{t('industryBenchmarking')}</h2>
            <div className="mb-4">
              <span className="text-sm text-gray-600">{t('industry')}: </span>
              <span className="font-semibold text-gray-900">{analysis.industry_comparison.industry}</span>
              <span className="ml-4 text-sm text-gray-600">{t('performance')}: </span>
              <span className={`font-semibold ${
                analysis.industry_comparison.overall_performance === 'Strong' ? 'text-green-600' :
                analysis.industry_comparison.overall_performance === 'Weak' ? 'text-red-600' :
                'text-yellow-600'
              }`}>
                {analysis.industry_comparison.overall_performance}
              </span>
            </div>
          </div>
        )}

        {/* Credit Readiness */}
        {analysis.credit_readiness?.credit_readiness && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">{t('creditReadiness')}</h2>
            <div className="mb-4">
              <div className="flex items-center gap-4 mb-2">
                <span className="text-3xl font-bold text-blue-600">
                  {analysis.credit_readiness.credit_readiness.credit_readiness_score.toFixed(1)}
                </span>
                <span className="text-lg font-semibold text-gray-700">
                  {analysis.credit_readiness.credit_readiness.readiness_level}
                </span>
              </div>
              <p className="text-gray-700">{analysis.credit_readiness.credit_readiness.description}</p>
            </div>
            
            {analysis.credit_readiness.recommended_financing?.length > 0 && (
              <div className="mt-6">
                <h3 className="font-semibold text-gray-900 mb-3">{t('recommendedFinancing')}</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {analysis.credit_readiness.recommended_financing.slice(0, 4).map((option, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900">{option.product}</h4>
                      <p className="text-sm text-gray-600">{option.provider}</p>
                      <div className="mt-2 text-sm">
                        <div className="text-gray-700">Rate: {option.interest_rate}</div>
                        <div className="text-gray-700">Tenure: {option.tenure}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
