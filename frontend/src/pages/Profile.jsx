import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTranslation } from 'react-i18next'
import axios from 'axios'
import { User, Building2, Mail, Briefcase, Phone, MapPin, Calendar, Save, ArrowLeft, LogOut } from 'lucide-react'
import LanguageSelector from '../components/LanguageSelector'

export default function Profile() {
  const { user, logout, updateUser } = useAuth()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  const [profileData, setProfileData] = useState({
    email: user?.email || '',
    company_name: user?.company_name || '',
    industry: user?.industry || 'services',
    phone: user?.phone || '',
    address: user?.address || '',
    city: user?.city || '',
    state: user?.state || '',
    pincode: user?.pincode || '',
    gstin: user?.gstin || '',
    pan: user?.pan || '',
    registration_date: user?.registration_date || '',
    company_size: user?.company_size || '',
    annual_revenue: user?.annual_revenue || ''
  })

  // Sync profile data when user object changes
  useEffect(() => {
    if (user) {
      setProfileData({
        email: user.email || '',
        company_name: user.company_name || '',
        industry: user.industry || 'services',
        phone: user.phone || '',
        address: user.address || '',
        city: user.city || '',
        state: user.state || '',
        pincode: user.pincode || '',
        gstin: user.gstin || '',
        pan: user.pan || '',
        registration_date: user.registration_date || '',
        company_size: user.company_size || '',
        annual_revenue: user.annual_revenue || ''
      })
    }
  }, [user])

  const industries = [
    { value: 'retail', label: 'Retail' },
    { value: 'manufacturing', label: 'Manufacturing' },
    { value: 'services', label: 'Services' },
    { value: 'technology', label: 'Technology' },
    { value: 'hospitality', label: 'Hospitality' },
    { value: 'healthcare', label: 'Healthcare' },
    { value: 'education', label: 'Education' },
    { value: 'construction', label: 'Construction' },
    { value: 'agriculture', label: 'Agriculture' },
    { value: 'other', label: 'Other' }
  ]

  const companySizes = [
    { value: 'micro', label: 'Micro (1-10 employees)' },
    { value: 'small', label: 'Small (11-50 employees)' },
    { value: 'medium', label: 'Medium (51-250 employees)' },
    { value: 'large', label: 'Large (250+ employees)' }
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess(false)
    setLoading(true)

    try {
      const token = localStorage.getItem('token')
      
      // Remove email from the data being sent (it's read-only)
      const { email, ...dataToUpdate } = profileData
      
      console.log('Submitting profile data:', dataToUpdate)
      
      const response = await axios.put('/api/auth/profile', dataToUpdate, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      console.log('Profile update response:', response.data)
      
      // Update user in AuthContext and local storage
      updateUser(response.data)
      
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      console.error('Profile update error:', err)
      setError(err.response?.data?.detail || 'Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (field, value) => {
    setProfileData(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="header-glass sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/')}
                className="text-gray-300 hover:text-white transition-colors"
              >
                <ArrowLeft size={24} />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-white gradient-text-neon">{t('profile')}</h1>
                <p className="text-sm text-gray-300">{t('manageYourProfile')}</p>
              </div>
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

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Success Message */}
        {success && (
          <div className="mb-6 bg-green-500/20 border border-green-500/50 text-green-300 px-4 py-3 rounded-2xl animate-fadeInUp">
            Profile updated successfully!
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-500/20 border border-red-500/50 text-red-300 px-4 py-3 rounded-2xl animate-fadeInUp">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Information */}
          <div className="metric-card">
            <div className="flex items-center gap-3 mb-6">
              <User className="text-purple-400" size={24} />
              <h2 className="text-xl font-semibold text-white">Basic Information</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Mail size={16} className="inline mr-2" />
                  Email
                </label>
                <input
                  type="email"
                  value={profileData.email}
                  className="input-glass w-full bg-white/5 cursor-not-allowed"
                  disabled
                />
                <p className="text-xs text-gray-500 mt-1">Email cannot be changed</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Phone size={16} className="inline mr-2" />
                  Phone Number
                </label>
                <input
                  type="tel"
                  value={profileData.phone}
                  onChange={(e) => handleChange('phone', e.target.value)}
                  className="input-glass w-full"
                  placeholder="+91 98765 43210"
                />
              </div>
            </div>
          </div>

          {/* Company Information */}
          <div className="metric-card">
            <div className="flex items-center gap-3 mb-6">
              <Building2 className="text-cyan-400" size={24} />
              <h2 className="text-xl font-semibold text-white">Company Information</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Company Name
                </label>
                <input
                  type="text"
                  value={profileData.company_name}
                  onChange={(e) => handleChange('company_name', e.target.value)}
                  className="input-glass w-full"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Briefcase size={16} className="inline mr-2" />
                  Industry
                </label>
                <select
                  value={profileData.industry}
                  onChange={(e) => handleChange('industry', e.target.value)}
                  className="input-glass w-full"
                >
                  {industries.map(ind => (
                    <option key={ind.value} value={ind.value}>{ind.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Company Size
                </label>
                <select
                  value={profileData.company_size}
                  onChange={(e) => handleChange('company_size', e.target.value)}
                  className="input-glass w-full"
                >
                  <option value="">Select company size</option>
                  {companySizes.map(size => (
                    <option key={size.value} value={size.value}>{size.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Calendar size={16} className="inline mr-2" />
                  Registration Date
                </label>
                <input
                  type="date"
                  value={profileData.registration_date}
                  onChange={(e) => handleChange('registration_date', e.target.value)}
                  className="input-glass w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  GSTIN
                </label>
                <input
                  type="text"
                  value={profileData.gstin}
                  onChange={(e) => handleChange('gstin', e.target.value)}
                  className="input-glass w-full"
                  placeholder="22AAAAA0000A1Z5"
                  maxLength={15}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  PAN
                </label>
                <input
                  type="text"
                  value={profileData.pan}
                  onChange={(e) => handleChange('pan', e.target.value.toUpperCase())}
                  className="input-glass w-full"
                  placeholder="ABCDE1234F"
                  maxLength={10}
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Annual Revenue (₹)
                </label>
                <input
                  type="text"
                  value={profileData.annual_revenue}
                  onChange={(e) => handleChange('annual_revenue', e.target.value)}
                  className="input-glass w-full"
                  placeholder="e.g., 50,00,000"
                />
              </div>
            </div>
          </div>

          {/* Address Information */}
          <div className="metric-card">
            <div className="flex items-center gap-3 mb-6">
              <MapPin className="text-green-400" size={24} />
              <h2 className="text-xl font-semibold text-white">Address Information</h2>
            </div>
            
            <div className="grid grid-cols-1 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Address
                </label>
                <textarea
                  value={profileData.address}
                  onChange={(e) => handleChange('address', e.target.value)}
                  className="input-glass w-full"
                  rows="3"
                  placeholder="Street address, building name, etc."
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    City
                  </label>
                  <input
                    type="text"
                    value={profileData.city}
                    onChange={(e) => handleChange('city', e.target.value)}
                    className="input-glass w-full"
                    placeholder="Mumbai"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    State
                  </label>
                  <input
                    type="text"
                    value={profileData.state}
                    onChange={(e) => handleChange('state', e.target.value)}
                    className="input-glass w-full"
                    placeholder="Maharashtra"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Pincode
                  </label>
                  <input
                    type="text"
                    value={profileData.pincode}
                    onChange={(e) => handleChange('pincode', e.target.value)}
                    className="input-glass w-full"
                    placeholder="400001"
                    maxLength={6}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end gap-4">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="px-6 py-3 bg-white/5 text-gray-300 rounded-2xl hover:bg-white/10 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="btn-neon flex items-center gap-2"
            >
              <Save size={20} />
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </main>
    </div>
  )
}
