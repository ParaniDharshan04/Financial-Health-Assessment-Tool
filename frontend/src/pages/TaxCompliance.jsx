import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, CheckCircle, AlertTriangle, XCircle, FileText, Upload } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import axios from 'axios'

export default function TaxCompliance() {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [complianceData, setComplianceData] = useState(null)
  const [deductions, setDeductions] = useState([])
  const [filingReadiness, setFilingReadiness] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')
  const [showAddDeduction, setShowAddDeduction] = useState(false)
  const [newDeduction, setNewDeduction] = useState({
    section: '80C',
    description: '',
    amount: '',
    is_eligible: true
  })

  useEffect(() => {
    fetchComplianceData()
  }, [])

  const fetchComplianceData = async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      
      // Fetch deductions
      const deductionsRes = await axios.get('/api/tax/deductions/summary?financial_year=2024-25', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      if (deductionsRes.data.deductions) {
        setDeductions(deductionsRes.data.deductions)
      }

      // Set mock compliance data for demo
      setComplianceData({
        overall_status: 'Mostly Compliant',
        compliance_score: 78,
        checks_passed: 6,
        checks_failed: 2,
        checks: [
          { check_name: 'GST Returns Filed', status: 'Compliant', message: 'All GST returns filed on time' },
          { check_name: 'TDS Payments', status: 'Compliant', message: 'TDS payments up to date' },
          { check_name: 'Advance Tax', status: 'Compliant', message: 'Advance tax paid' },
          { check_name: 'Income Tax Return', status: 'Pending', message: 'ITR not filed yet' },
          { check_name: 'Professional Tax', status: 'Compliant', message: 'Professional tax paid' },
          { check_name: 'ESI/PF Compliance', status: 'Compliant', message: 'ESI and PF compliant' },
          { check_name: 'Books of Accounts', status: 'Compliant', message: 'Books maintained properly' },
          { check_name: 'Audit Requirement', status: 'Pending', message: 'Audit required (Revenue > ₹1 Cr)' }
        ],
        issues: [
          { 
            type: 'Income Tax Return Pending', 
            description: 'Income tax return for FY 2024-25 not filed yet',
            recommendation: 'File ITR before July 31, 2025 to avoid penalties'
          },
          {
            type: 'Unclaimed Deductions',
            description: 'Some eligible deductions may not be claimed',
            recommendation: 'Review all deductions in the Deductions tab'
          }
        ]
      })

      // Set mock filing readiness
      setFilingReadiness({
        readiness_score: 75,
        status: 'Ready with minor items pending',
        missing_items: [
          'Form 16 from employer',
          'Interest certificate from bank',
          'Donation receipts for 80G'
        ],
        recommendations: [
          'Collect all Form 16 documents',
          'Download interest certificates from bank',
          'Ensure all donation receipts are available',
          'Review and claim all eligible deductions'
        ]
      })
    } catch (error) {
      console.error('Error fetching tax data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddDeduction = async () => {
    if (!newDeduction.description || !newDeduction.amount) {
      // Show error toast
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">Please fill in all fields</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
      return
    }

    try {
      const token = localStorage.getItem('token')
      await axios.post('/api/tax/deductions/add', {
        financial_year: '2024-25',
        section: newDeduction.section,
        description: newDeduction.description,
        amount: parseFloat(newDeduction.amount),
        is_eligible: newDeduction.is_eligible
      }, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      // Refresh deductions list
      const deductionsRes = await axios.get('/api/tax/deductions/summary?financial_year=2024-25', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      if (deductionsRes.data.deductions) {
        setDeductions(deductionsRes.data.deductions)
      }
      
      // Reset form and close modal
      setNewDeduction({
        section: '80C',
        description: '',
        amount: '',
        is_eligible: true
      })
      setShowAddDeduction(false)
      
      // Show success toast
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">Deduction added successfully!</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
    } catch (error) {
      console.error('Error adding deduction:', error)
      
      // Show error toast
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">Error adding deduction: ${error.response?.data?.detail || error.message}</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Compliant':
        return <CheckCircle className="text-green-600" size={24} />
      case 'Non-compliant':
        return <XCircle className="text-red-600" size={24} />
      default:
        return <AlertTriangle className="text-yellow-600" size={24} />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'Compliant':
        return 'bg-green-100 text-green-800 border-green-300'
      case 'Non-compliant':
        return 'bg-red-100 text-red-800 border-red-300'
      default:
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="spinner-dark mx-auto"></div>
          <p className="mt-4 text-gray-300">{t('loading')}</p>
        </div>
      </div>
    )
  }

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
          <h1 className="text-2xl font-bold text-white gradient-text-neon">{t('taxComplianceDashboard')}</h1>
          <p className="text-sm text-gray-400">{t('financialYear')} 2024-25</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tabs */}
        <div className="metric-card mb-6">
          <div className="border-b border-white/10">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('overview')}
                className={`px-4 py-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === 'overview'
                    ? 'border-green-500 text-green-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-600'
                }`}
              >
                {t('complianceOverview')}
              </button>
              <button
                onClick={() => setActiveTab('deductions')}
                className={`px-4 py-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === 'deductions'
                    ? 'border-green-500 text-green-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-600'
                }`}
              >
                {t('taxDeductions')}
              </button>
              <button
                onClick={() => setActiveTab('filing')}
                className={`px-4 py-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === 'filing'
                    ? 'border-green-500 text-green-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-600'
                }`}
              >
                {t('filingReadiness')}
              </button>
            </nav>
          </div>
        </div>

        {/* Compliance Overview Tab */}
        {activeTab === 'overview' && complianceData && (
          <div className="space-y-6">
            {/* Overall Status */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">{t('overallComplianceStatus')}</h2>
                <span className={`px-4 py-2 rounded-full border-2 ${getStatusColor(complianceData.overall_status)}`}>
                  {complianceData.overall_status}
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-3xl font-bold text-blue-600">{complianceData.compliance_score}</div>
                  <div className="text-sm text-gray-600 mt-1">{t('complianceScore')}</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-3xl font-bold text-green-600">{complianceData.checks_passed}</div>
                  <div className="text-sm text-gray-600 mt-1">{t('checksPassed')}</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-3xl font-bold text-red-600">{complianceData.checks_failed}</div>
                  <div className="text-sm text-gray-600 mt-1">{t('issuesFound')}</div>
                </div>
              </div>
            </div>

            {/* Compliance Checks */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">{t('complianceChecks')}</h2>
              <div className="space-y-3">
                {complianceData.checks?.map((check, index) => (
                  <div key={index} className="flex items-start gap-3 p-4 border border-gray-200 rounded-lg">
                    {getStatusIcon(check.status)}
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{check.check_name}</h3>
                      <p className="text-sm text-gray-600 mt-1">{check.message}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Issues */}
            {complianceData.issues?.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">{t('issuesToAddress')}</h2>
                <div className="space-y-3">
                  {complianceData.issues.map((issue, index) => (
                    <div key={index} className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                      <AlertTriangle className="text-red-600 mt-1" size={20} />
                      <div className="flex-1">
                        <h3 className="font-semibold text-red-900">{issue.type}</h3>
                        <p className="text-sm text-red-700 mt-1">{issue.description}</p>
                        {issue.recommendation && (
                          <p className="text-sm text-red-600 mt-2">
                            <strong>Recommendation:</strong> {issue.recommendation}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tax Deductions Tab */}
        {activeTab === 'deductions' && (
          <div className="space-y-6">
            <div className="metric-card">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-semibold text-white">{t('taxDeductions')}</h2>
                <button 
                  onClick={() => setShowAddDeduction(true)}
                  className="btn-neon flex items-center gap-2"
                >
                  <Upload size={18} />
                  {t('addDeduction')}
                </button>
              </div>

              {deductions.length === 0 ? (
                <div className="text-center py-12">
                  <FileText size={48} className="mx-auto text-gray-400 mb-4" />
                  <p className="text-gray-400">No deductions recorded yet</p>
                  <p className="text-sm text-gray-500 mt-2">Click "Add Deduction" to start tracking your tax deductions</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {deductions.map((deduction, index) => (
                    <div key={index} className="border border-white/10 rounded-lg p-4 bg-white/5">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold text-white text-sm">{deduction.section}</h3>
                          <p className="text-xs text-gray-400 mt-1">{deduction.description}</p>
                        </div>
                        <div className="text-right">
                          <div className="text-base font-bold text-white">
                            ₹{deduction.amount.toLocaleString()}
                          </div>
                          <span className={`text-xs px-2 py-1 rounded ${
                            deduction.is_eligible ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                          }`}>
                            {deduction.is_eligible ? 'Eligible' : 'Not Eligible'}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Deduction Summary */}
            <div className="metric-card">
              <h2 className="text-lg font-semibold text-white mb-4">Deduction Summary</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="p-3 bg-green-500/20 rounded-lg border border-green-400/30">
                  <div className="text-xl font-bold text-green-400">
                    ₹{deductions.reduce((sum, d) => sum + d.amount, 0).toLocaleString()}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">Total Deductions</div>
                </div>
                <div className="p-3 bg-green-500/20 rounded-lg border border-green-400/30">
                  <div className="text-xl font-bold text-green-400">
                    {deductions.filter(d => d.is_eligible).length}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">Eligible Deductions</div>
                </div>
                <div className="p-3 bg-green-500/20 rounded-lg border border-green-400/30">
                  <div className="text-xl font-bold text-green-400">
                    ₹{(deductions.reduce((sum, d) => sum + d.amount, 0) * 0.3).toLocaleString()}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">Estimated Tax Savings</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Filing Readiness Tab */}
        {activeTab === 'filing' && filingReadiness && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">{t('filingReadinessAssessment')}</h2>
              
              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">{t('readinessScore')}</span>
                  <span className="text-sm font-medium text-gray-900">{filingReadiness.readiness_score}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full ${
                      filingReadiness.readiness_score >= 80 ? 'bg-green-600' :
                      filingReadiness.readiness_score >= 50 ? 'bg-yellow-600' : 'bg-red-600'
                    }`}
                    style={{ width: `${filingReadiness.readiness_score}%` }}
                  ></div>
                </div>
                <p className="text-sm text-gray-600 mt-2">{filingReadiness.status}</p>
              </div>

              {/* Missing Items */}
              {filingReadiness.missing_items?.length > 0 && (
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 mb-3">{t('missingItems')}</h3>
                  <div className="space-y-2">
                    {filingReadiness.missing_items.map((item, index) => (
                      <div key={index} className="flex items-center gap-2 text-sm text-gray-700">
                        <XCircle size={16} className="text-red-600" />
                        {item}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Recommendations */}
              {filingReadiness.recommendations?.length > 0 && (
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">{t('recommendations')}</h3>
                  <div className="space-y-2">
                    {filingReadiness.recommendations.map((rec, index) => (
                      <div key={index} className="flex items-start gap-2 p-3 bg-blue-50 rounded-lg">
                        <CheckCircle size={16} className="text-blue-600 mt-0.5" />
                        <span className="text-sm text-gray-700">{rec}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Add Deduction Modal */}
      {showAddDeduction && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="glass-card p-8 max-w-md w-full mx-4 animate-fadeInUp">
            <h3 className="text-2xl font-bold text-white mb-6">Add Tax Deduction</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Section</label>
                <select
                  value={newDeduction.section}
                  onChange={(e) => setNewDeduction({...newDeduction, section: e.target.value})}
                  className="input-glass w-full"
                  style={{
                    colorScheme: 'dark'
                  }}
                >
                  <option value="80C" style={{backgroundColor: '#1f2937', color: '#fff'}}>80C - Investments (EPF, PPF, LIC)</option>
                  <option value="80D" style={{backgroundColor: '#1f2937', color: '#fff'}}>80D - Health Insurance</option>
                  <option value="80E" style={{backgroundColor: '#1f2937', color: '#fff'}}>80E - Education Loan Interest</option>
                  <option value="80G" style={{backgroundColor: '#1f2937', color: '#fff'}}>80G - Charitable Donations</option>
                  <option value="80TTA" style={{backgroundColor: '#1f2937', color: '#fff'}}>80TTA - Savings Account Interest</option>
                  <option value="24B" style={{backgroundColor: '#1f2937', color: '#fff'}}>24B - Home Loan Interest</option>
                  <option value="Other" style={{backgroundColor: '#1f2937', color: '#fff'}}>Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Description</label>
                <input
                  type="text"
                  value={newDeduction.description}
                  onChange={(e) => setNewDeduction({...newDeduction, description: e.target.value})}
                  placeholder="e.g., Employee Provident Fund"
                  className="input-glass w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Amount (₹)</label>
                <input
                  type="number"
                  value={newDeduction.amount}
                  onChange={(e) => setNewDeduction({...newDeduction, amount: e.target.value})}
                  placeholder="150000"
                  className="input-glass w-full"
                />
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="eligible"
                  checked={newDeduction.is_eligible}
                  onChange={(e) => setNewDeduction({...newDeduction, is_eligible: e.target.checked})}
                  className="w-4 h-4"
                />
                <label htmlFor="eligible" className="text-sm text-gray-300">Eligible for deduction</label>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={handleAddDeduction}
                className="btn-neon flex-1"
              >
                Add Deduction
              </button>
              <button
                onClick={() => setShowAddDeduction(false)}
                className="btn-glass flex-1"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
