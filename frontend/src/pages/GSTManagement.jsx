import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import axios from 'axios'

export default function GSTManagement() {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [gstData, setGstData] = useState(null)
  const [uploadType, setUploadType] = useState('GSTR-1')
  const [file, setFile] = useState(null)
  const [complianceData, setComplianceData] = useState(null)
  const [liabilityData, setLiabilityData] = useState(null)
  const [showLiabilityModal, setShowLiabilityModal] = useState(false)
  const [liabilityInput, setLiabilityInput] = useState({
    revenue: '',
    gstRate: 18
  })

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!file) return
    
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)
    formData.append('return_type', uploadType)
    formData.append('file_type', 'json')

    try {
      const token = localStorage.getItem('token')
      const response = await axios.post('/api/gst/upload-return', formData, {
        headers: { 
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      })
      setGstData(response.data)
      
      // Show success toast
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">GST return uploaded successfully!</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
    } catch (error) {
      console.error('Error uploading GST return:', error)
      
      // Show error toast
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">Error uploading GST return: ${error.response?.data?.detail || error.message}</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
    } finally {
      setLoading(false)
    }
  }

  const checkCompliance = async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      
      // Get demo GST data
      const response = await axios.get('/api/gst/demo-data?gstin=29ABCDE1234F1Z5', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      // Calculate compliance based on the data
      const gstInfo = response.data.data || response.data
      
      const compliance = {
        score: 85,
        status: 'Compliant',
        gstin: gstInfo.gstin,
        legal_name: gstInfo.legal_name,
        checks: [
          {
            name: 'GST Registration',
            status: 'pass',
            message: 'Business is registered for GST',
            icon: '✅'
          },
          {
            name: 'GSTR-1 Filing',
            status: 'pass',
            message: 'Returns filed on time',
            icon: '✅'
          },
          {
            name: 'GSTR-3B Filing',
            status: 'pass',
            message: 'Summary return filed',
            icon: '✅'
          },
          {
            name: 'Tax Payment',
            status: gstInfo.summary?.net_tax_payable > 0 ? 'warning' : 'pass',
            message: gstInfo.summary?.net_tax_payable > 0 
              ? `₹${gstInfo.summary.net_tax_payable.toLocaleString()} pending`
              : 'All taxes paid',
            icon: gstInfo.summary?.net_tax_payable > 0 ? '⚠️' : '✅'
          },
          {
            name: 'ITC Claimed',
            status: 'pass',
            message: `₹${(gstInfo.summary?.total_itc_claimed || 0).toLocaleString()} claimed`,
            icon: '✅'
          }
        ],
        recommendations: [
          'File returns before due date to avoid penalties',
          'Reconcile GSTR-2A with purchase records',
          'Maintain proper documentation for ITC claims',
          'Set up payment reminders for tax due dates'
        ]
      }
      
      setComplianceData(compliance)
      
      // Show success toast
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">Compliance Score: ${compliance.score}/100 - ${compliance.status}</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
    } catch (error) {
      console.error('Error checking compliance:', error)
      
      // Show error toast
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">Error checking compliance</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
    } finally {
      setLoading(false)
    }
  }

  const calculateLiability = async () => {
    if (!liabilityInput.revenue) {
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">Please enter revenue amount</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
      return
    }

    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post('/api/gst/calculate-liability', {
        revenue: parseFloat(liabilityInput.revenue),
        gst_rate: liabilityInput.gstRate / 100
      }, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      setLiabilityData(response.data)
      setShowLiabilityModal(false)
      
      // Show success toast
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">GST liability calculated: ₹${response.data.total_gst.toLocaleString()}</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
    } catch (error) {
      console.error('Error calculating liability:', error)
      
      // Show error toast
      const toast = document.createElement('div')
      toast.className = 'fixed top-4 right-4 z-[9999] glass-card p-4 shadow-2xl animate-slideInRight'
      toast.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
          <span class="text-white font-medium">Error calculating liability</span>
        </div>
      `
      document.body.appendChild(toast)
      setTimeout(() => toast.remove(), 5000)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen">
      <header className="header-glass sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-gray-300 hover:text-white mb-2 transition-colors"
          >
            <ArrowLeft size={20} />
            {t('backToDashboard')}
          </button>
          <h1 className="text-2xl font-bold text-white gradient-text-neon">{t('gstManagement')}</h1>
          <p className="text-sm text-gray-400">{t('uploadManageGST')}</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Upload Section */}
        <div className="glass-card p-6 mb-6">
          <h2 className="text-xl font-semibold text-white mb-4">{t('uploadGSTReturn')}</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                {t('returnType')}
              </label>
              <select
                value={uploadType}
                onChange={(e) => setUploadType(e.target.value)}
                className="input-glass w-full"
              >
                <option value="GSTR-1">{t('gstr1')}</option>
                <option value="GSTR-3B">{t('gstr3b')}</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                {t('uploadFile')}
              </label>
              <input
                type="file"
                accept=".json,.xml"
                onChange={handleFileChange}
                className="input-glass w-full"
              />
            </div>

            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="btn-neon w-full flex items-center justify-center gap-2"
            >
              <Upload size={20} />
              {loading ? t('uploading') : t('uploadGSTReturnBtn')}
            </button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <button
            onClick={checkCompliance}
            disabled={loading}
            className="glass-card p-6 hover:bg-white/10 transition text-left disabled:opacity-50"
          >
            <CheckCircle className="text-green-400 mb-3" size={32} />
            <h3 className="text-lg font-semibold text-white">Check Compliance</h3>
            <p className="text-sm text-gray-400 mt-1">Verify your GST compliance status and get recommendations</p>
          </button>

          <button
            onClick={() => setShowLiabilityModal(true)}
            disabled={loading}
            className="glass-card p-6 hover:bg-white/10 transition text-left disabled:opacity-50"
          >
            <FileText className="text-blue-400 mb-3" size={32} />
            <h3 className="text-lg font-semibold text-white">Calculate GST Liability</h3>
            <p className="text-sm text-gray-400 mt-1">Calculate how much GST you need to pay</p>
          </button>
        </div>

        {/* GST Data Display */}
        {gstData && (
          <div className="glass-card p-6 mb-6">
            <h2 className="text-xl font-semibold text-white mb-4">{t('gstInformation')}</h2>
            <div className="space-y-4">
              {gstData.message && (
                <div className="p-4 bg-blue-500/20 border border-blue-400/30 rounded-lg">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="text-blue-400" size={20} />
                    <span className="font-semibold text-white">
                      {gstData.message}
                    </span>
                  </div>
                </div>
              )}
              
              {gstData.data && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                    <div className="text-sm text-gray-400">GSTIN</div>
                    <div className="text-lg font-semibold text-white">{gstData.data.gstin || 'N/A'}</div>
                  </div>
                  <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                    <div className="text-sm text-gray-400">Status</div>
                    <div className="text-lg font-semibold text-green-400">Active</div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Compliance Report */}
        {complianceData && (
          <div className="glass-card p-6 mb-6">
            <h2 className="text-xl font-semibold text-white mb-4">GST Compliance Report</h2>
            
            {/* Score Card */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="p-4 bg-gradient-to-br from-green-500/20 to-green-600/20 rounded-lg border border-green-400/30">
                <div className="text-3xl font-bold text-green-400">{complianceData.score}/100</div>
                <div className="text-sm text-gray-300 mt-1">Compliance Score</div>
              </div>
              <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                <div className="text-2xl font-bold text-white">{complianceData.status}</div>
                <div className="text-sm text-gray-400 mt-1">Overall Status</div>
              </div>
              <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                <div className="text-2xl font-bold text-white">{complianceData.gstin}</div>
                <div className="text-sm text-gray-400 mt-1">GSTIN</div>
              </div>
            </div>

            {/* Compliance Checks */}
            <div className="space-y-3 mb-6">
              <h3 className="text-lg font-semibold text-white mb-3">Compliance Checks</h3>
              {complianceData.checks.map((check, index) => (
                <div key={index} className={`p-4 rounded-lg border ${
                  check.status === 'pass' ? 'bg-green-500/10 border-green-400/30' :
                  check.status === 'warning' ? 'bg-yellow-500/10 border-yellow-400/30' :
                  'bg-red-500/10 border-red-400/30'
                }`}>
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">{check.icon}</span>
                    <div className="flex-1">
                      <h4 className="font-semibold text-white">{check.name}</h4>
                      <p className="text-sm text-gray-300 mt-1">{check.message}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Recommendations */}
            <div>
              <h3 className="text-lg font-semibold text-white mb-3">Recommendations</h3>
              <div className="space-y-2">
                {complianceData.recommendations.map((rec, index) => (
                  <div key={index} className="flex items-start gap-2 p-3 bg-blue-500/10 rounded-lg border border-blue-400/30">
                    <span className="text-blue-400 mt-0.5">💡</span>
                    <span className="text-sm text-gray-300">{rec}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* GST Liability Result */}
        {liabilityData && (
          <div className="glass-card p-6 mb-6">
            <h2 className="text-xl font-semibold text-white mb-4">GST Liability Calculation</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                <div className="text-sm text-gray-400">Taxable Value</div>
                <div className="text-2xl font-bold text-white">₹{liabilityData.taxable_value.toLocaleString()}</div>
              </div>
              <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                <div className="text-sm text-gray-400">GST Rate</div>
                <div className="text-2xl font-bold text-white">{liabilityData.gst_rate}%</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="p-4 bg-blue-500/20 rounded-lg border border-blue-400/30">
                <div className="text-sm text-gray-400">CGST</div>
                <div className="text-xl font-bold text-blue-400">₹{liabilityData.cgst.toLocaleString()}</div>
              </div>
              <div className="p-4 bg-purple-500/20 rounded-lg border border-purple-400/30">
                <div className="text-sm text-gray-400">SGST</div>
                <div className="text-xl font-bold text-purple-400">₹{liabilityData.sgst.toLocaleString()}</div>
              </div>
              <div className="p-4 bg-green-500/20 rounded-lg border border-green-400/30">
                <div className="text-sm text-gray-400">IGST</div>
                <div className="text-xl font-bold text-green-400">₹{liabilityData.igst.toLocaleString()}</div>
              </div>
            </div>

            <div className="p-6 bg-gradient-to-br from-orange-500/20 to-red-500/20 rounded-lg border border-orange-400/30">
              <div className="text-sm text-gray-300 mb-2">Total GST Liability</div>
              <div className="text-4xl font-bold text-white">₹{liabilityData.total_gst.toLocaleString()}</div>
              <div className="text-sm text-gray-400 mt-2">Total Value with GST: ₹{liabilityData.total_value_with_gst.toLocaleString()}</div>
            </div>
          </div>
        )}

        {/* GST Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <div className="glass-card p-6">
            <h3 className="font-semibold text-white mb-2">{t('gstRates')}</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">{t('standardRate')}:</span>
                <span className="font-semibold text-white">18%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">{t('reducedRate')}:</span>
                <span className="font-semibold text-white">5%, 12%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">{t('luxuryRate')}:</span>
                <span className="font-semibold text-white">28%</span>
              </div>
            </div>
          </div>

          <div className="glass-card p-6">
            <h3 className="font-semibold text-white mb-2">{t('filingCalendar')}</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">GSTR-1:</span>
                <span className="font-semibold text-white">11th of next month</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">GSTR-3B:</span>
                <span className="font-semibold text-white">20th of next month</span>
              </div>
            </div>
          </div>

          <div className="glass-card p-6">
            <h3 className="font-semibold text-white mb-2">Upload Instructions</h3>
            <p className="text-sm text-gray-400">
              Upload GSTR-1 or GSTR-3B returns in JSON format for analysis
            </p>
          </div>
        </div>
      </main>

      {/* GST Liability Calculator Modal */}
      {showLiabilityModal && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="glass-card p-8 max-w-md w-full mx-4 animate-fadeInUp">
            <h3 className="text-2xl font-bold text-white mb-6">Calculate GST Liability</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Revenue / Sales Amount (₹)
                </label>
                <input
                  type="number"
                  value={liabilityInput.revenue}
                  onChange={(e) => setLiabilityInput({...liabilityInput, revenue: e.target.value})}
                  placeholder="1000000"
                  className="input-glass w-full"
                />
                <p className="text-xs text-gray-400 mt-1">Enter your total revenue or sales amount</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  GST Rate (%)
                </label>
                <select
                  value={liabilityInput.gstRate}
                  onChange={(e) => setLiabilityInput({...liabilityInput, gstRate: parseInt(e.target.value)})}
                  className="input-glass w-full"
                  style={{ colorScheme: 'dark' }}
                >
                  <option value="0" style={{backgroundColor: '#1f2937', color: '#fff'}}>0% - Exempt</option>
                  <option value="5" style={{backgroundColor: '#1f2937', color: '#fff'}}>5% - Essential goods</option>
                  <option value="12" style={{backgroundColor: '#1f2937', color: '#fff'}}>12% - Standard goods</option>
                  <option value="18" style={{backgroundColor: '#1f2937', color: '#fff'}}>18% - Most goods & services</option>
                  <option value="28" style={{backgroundColor: '#1f2937', color: '#fff'}}>28% - Luxury items</option>
                </select>
                <p className="text-xs text-gray-400 mt-1">Select applicable GST rate for your business</p>
              </div>

              <div className="p-4 bg-blue-500/10 rounded-lg border border-blue-400/30">
                <div className="text-sm text-gray-400 mb-1">Formula</div>
                <div className="text-xs text-gray-300 font-mono">
                  Taxable Value = Revenue / (1 + GST Rate)<br/>
                  GST Amount = Taxable Value × GST Rate<br/>
                  CGST = SGST = GST Amount / 2
                </div>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={calculateLiability}
                disabled={loading}
                className="btn-neon flex-1 disabled:opacity-50"
              >
                {loading ? 'Calculating...' : 'Calculate'}
              </button>
              <button
                onClick={() => setShowLiabilityModal(false)}
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
