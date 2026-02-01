import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload as UploadIcon, ArrowLeft, FileSpreadsheet } from 'lucide-react'
import axios from 'axios'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [dataType, setDataType] = useState('profit_loss')
  const [uploading, setUploading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const dataTypes = [
    { value: 'profit_loss', label: 'Profit & Loss Statement' },
    { value: 'balance_sheet', label: 'Balance Sheet' },
    { value: 'cash_flow', label: 'Cash Flow Statement' }
  ]

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      const validTypes = [
        'text/csv',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/pdf'
      ]
      
      if (validTypes.includes(selectedFile.type) || 
          selectedFile.name.endsWith('.csv') || 
          selectedFile.name.endsWith('.xlsx') || 
          selectedFile.name.endsWith('.xls') ||
          selectedFile.name.endsWith('.pdf')) {
        setFile(selectedFile)
        setError('')
      } else {
        setError('Please upload a CSV, XLSX, or PDF file')
        setFile(null)
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }

    setUploading(true)
    setError('')

    try {
      // Get authentication token
      const token = localStorage.getItem('token')
      
      if (!token) {
        setError('Please login first')
        navigate('/login')
        return
      }

      // Upload file
      const formData = new FormData()
      formData.append('file', file)
      formData.append('data_type', dataType)

      const uploadResponse = await axios.post('/api/financial-data/upload', formData, {
        headers: { 
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      })

      const dataId = uploadResponse.data.data_id

      // Create analysis
      setUploading(false)
      setAnalyzing(true)

      const analysisResponse = await axios.post(`/api/analysis/create/${dataId}?language=en`, {}, {
        headers: { 
          'Authorization': `Bearer ${token}`
        }
      })
      const analysisId = analysisResponse.data.analysis_id

      // Navigate to analysis page
      navigate(`/analysis/${analysisId}`)

    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
      setUploading(false)
      setAnalyzing(false)
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
            Back to Dashboard
          </button>
          <h1 className="text-2xl font-bold text-white gradient-text-neon">Upload Financial Data</h1>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="metric-card p-8">
          {error && (
            <div className="bg-red-500/20 border border-red-500/50 text-red-300 px-4 py-3 rounded-2xl mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Data Type
              </label>
              <select
                value={dataType}
                onChange={(e) => setDataType(e.target.value)}
                className="input-glass w-full"
              >
                {dataTypes.map(type => (
                  <option key={type.value} value={type.value}>{type.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Upload File (CSV or XLSX)
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-white/20 border-dashed rounded-2xl hover:border-green-400/50 transition glass-card-dark">
                <div className="space-y-1 text-center">
                  <FileSpreadsheet className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="flex text-sm text-gray-400">
                    <label className="relative cursor-pointer rounded-md font-medium text-green-400 hover:text-green-300">
                      <span>Upload a file</span>
                      <input
                        type="file"
                        className="sr-only"
                        accept=".csv,.xlsx,.xls,.pdf"
                        onChange={handleFileChange}
                      />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">CSV, XLSX, or PDF up to 10MB</p>
                  {file && (
                    <p className="text-sm text-green-400 font-medium mt-2">
                      Selected: {file.name}
                    </p>
                  )}
                </div>
              </div>
            </div>

            <div className="glass-card-dark p-4 rounded-2xl border border-green-500/30">
              <h3 className="text-sm font-medium text-green-300 mb-2">File Requirements:</h3>
              <ul className="text-sm text-gray-400 space-y-1 list-disc list-inside">
                <li>File format: CSV, XLSX, or PDF</li>
                <li>Include column headers (for CSV/XLSX)</li>
                <li>Use standard financial terms (revenue, expenses, assets, etc.)</li>
                <li>Ensure numerical values are properly formatted</li>
                <li>PDF should contain clear financial statement tables</li>
              </ul>
            </div>

            <button
              type="submit"
              disabled={!file || uploading || analyzing}
              className="btn-neon w-full flex items-center justify-center gap-2"
            >
              {uploading ? (
                <>Uploading...</>
              ) : analyzing ? (
                <>Analyzing...</>
              ) : (
                <>
                  <UploadIcon size={20} />
                  Upload and Analyze
                </>
              )}
            </button>
          </form>
        </div>

        {/* Sample Data Info */}
        <div className="mt-8 metric-card">
          <h3 className="text-lg font-semibold text-white mb-4">Sample Data Format</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="glass-card-dark">
                <tr>
                  <th className="px-4 py-2 text-left text-gray-300">Column</th>
                  <th className="px-4 py-2 text-left text-gray-300">Example Value</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                <tr>
                  <td className="px-4 py-2 text-gray-400">Revenue</td>
                  <td className="px-4 py-2 text-white">5000000</td>
                </tr>
                <tr>
                  <td className="px-4 py-2 text-gray-400">Cost of Goods Sold</td>
                  <td className="px-4 py-2 text-white">3000000</td>
                </tr>
                <tr>
                  <td className="px-4 py-2 text-gray-400">Operating Expenses</td>
                  <td className="px-4 py-2 text-white">1200000</td>
                </tr>
                <tr>
                  <td className="px-4 py-2 text-gray-400">Net Profit</td>
                  <td className="px-4 py-2 text-white">500000</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  )
}
