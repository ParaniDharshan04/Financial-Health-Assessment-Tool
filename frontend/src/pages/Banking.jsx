import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Link as LinkIcon, RefreshCw, DollarSign, TrendingUp, XCircle } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import axios from 'axios'
import { usePlaidLink } from 'react-plaid-link'

export default function Banking() {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [accounts, setAccounts] = useState([])
  const [transactions, setTransactions] = useState([])
  const [linkToken, setLinkToken] = useState(null)
  const [bankStatus, setBankStatus] = useState(null)
  const [notification, setNotification] = useState(null)

  // Show notification helper
  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 5000)
  }

  useEffect(() => {
    fetchBankingStatus()
  }, [])

  const fetchBankingStatus = async () => {
    try {
      const response = await axios.get('/api/banking/status')
      setBankStatus(response.data)
      
      // If already connected, fetch accounts
      if (response.data.is_connected) {
        fetchAccounts()
      }
    } catch (error) {
      console.error('Error fetching banking status:', error)
    }
  }

  const createLinkToken = async () => {
    setLoading(true)
    showNotification('Opening Plaid Link...', 'success')
    
    try {
      const response = await axios.post('/api/banking/create-link-token')
      
      if (response.data.link_token) {
        setLinkToken(response.data.link_token)
        showNotification('Select your bank to connect', 'success')
      } else if (response.data.is_demo) {
        // Only show notification if there's an actual error
        if (response.data.error) {
          console.warn('Plaid configuration issue:', response.data.error)
          showNotification('Using demo mode - Plaid not fully configured', 'error')
        } else {
          showNotification('Showing demo data', 'success')
        }
        // Fetch demo accounts
        fetchAccounts()
      }
    } catch (error) {
      console.error('Error creating link token:', error)
      showNotification('Error connecting. Showing demo data.', 'error')
      // Show demo data
      fetchAccounts()
    } finally {
      setLoading(false)
    }
  }

  const onSuccess = async (public_token, metadata) => {
    setLoading(true)
    try {
      const response = await axios.post('/api/banking/link-bank', {
        public_token,
        institution_id: metadata.institution?.institution_id,
        institution_name: metadata.institution?.name,
        accounts: metadata.accounts
      })
      
      showNotification(`✓ ${metadata.institution?.name || 'Bank'} connected successfully!`, 'success')
      
      // Refresh status and fetch accounts
      await fetchBankingStatus()
      await fetchAccounts()
    } catch (error) {
      console.error('Error linking bank:', error)
      showNotification('Error linking bank account. Please try again.', 'error')
    } finally {
      setLoading(false)
    }
  }

  const config = {
    token: linkToken,
    onSuccess,
  }

  const { open, ready } = usePlaidLink(config)

  // Trigger Plaid Link when token is ready
  useEffect(() => {
    if (linkToken && ready) {
      open()
    }
  }, [linkToken, ready, open])

  const fetchAccounts = async () => {
    setLoading(true)
    try {
      const response = await axios.get('/api/banking/accounts')
      setAccounts(response.data.accounts || [])
    } catch (error) {
      console.error('Error fetching accounts:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTransactions = async () => {
    setLoading(true)
    try {
      const response = await axios.get('/api/banking/transactions')
      setTransactions(response.data.transactions || [])
    } catch (error) {
      console.error('Error fetching transactions:', error)
    } finally {
      setLoading(false)
    }
  }

  const disconnectBank = async () => {
    if (!confirm('Are you sure you want to disconnect your bank account?')) return
    
    setLoading(true)
    try {
      await axios.post('/api/banking/disconnect')
      showNotification('Bank disconnected successfully', 'success')
      setBankStatus({ is_connected: false, is_demo_mode: true })
      setAccounts([])
      setTransactions([])
    } catch (error) {
      console.error('Error disconnecting bank:', error)
      showNotification('Error disconnecting bank', 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen">
      {/* Notification Toast */}
      {notification && (
        <div className={`fixed top-4 right-4 z-[9999] glass-card p-4 rounded-2xl animate-fadeInUp shadow-2xl ${
          notification.type === 'success' ? 'border-l-4 border-green-500' : 'border-l-4 border-red-500'
        }`}>
          <p className={`text-sm font-medium ${
            notification.type === 'success' ? 'text-green-300' : 'text-red-300'
          }`}>
            {notification.message}
          </p>
        </div>
      )}

      <header className="header-glass sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-gray-300 hover:text-white mb-2 transition-colors"
          >
            <ArrowLeft size={20} />
            {t('backToDashboard')}
          </button>
          <h1 className="text-2xl font-bold text-white gradient-text-neon">{t('bankingIntegration')}</h1>
          <p className="text-sm text-gray-400">{t('connectManageBanks')}</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Connect Bank Section */}
        <div className="glass-card p-6 mb-6">
          <h2 className="text-xl font-semibold text-white mb-4">{t('connectBankAccount')}</h2>
          
          {bankStatus?.is_connected ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 glass-card-dark rounded-2xl">
                <div>
                  <p className="text-green-400 font-semibold">✓ Connected</p>
                  <p className="text-gray-300 text-sm">{bankStatus.institution_name}</p>
                  {bankStatus.last_sync && (
                    <p className="text-gray-400 text-xs mt-1">
                      Last synced: {new Date(bankStatus.last_sync).toLocaleString()}
                    </p>
                  )}
                </div>
                <button
                  onClick={disconnectBank}
                  disabled={loading}
                  className="flex items-center gap-2 px-4 py-2 bg-red-500/20 text-red-300 rounded-lg hover:bg-red-500/30 transition-colors"
                >
                  <XCircle size={20} />
                  Disconnect
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <p className="text-gray-300 mb-4">
                {t('connectBankDesc')}
              </p>
              <button
                onClick={createLinkToken}
                disabled={loading}
                className="btn-neon flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <div className="spinner-dark w-5 h-5"></div>
                    <span>Connecting...</span>
                  </>
                ) : (
                  <>
                    <LinkIcon size={20} />
                    {t('connectBankAccount')}
                  </>
                )}
              </button>
              <p className="text-sm text-gray-400 mt-3">
                {t('poweredByPlaid')}
              </p>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <button
            onClick={fetchAccounts}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition text-left"
          >
            <DollarSign className="text-green-600 mb-3" size={32} />
            <h3 className="text-lg font-semibold text-gray-900">{t('viewAccounts')}</h3>
            <p className="text-sm text-gray-600 mt-1">{t('checkAccountBalances')}</p>
          </button>

          <button
            onClick={fetchTransactions}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition text-left"
          >
            <TrendingUp className="text-blue-600 mb-3" size={32} />
            <h3 className="text-lg font-semibold text-gray-900">{t('transactions')}</h3>
            <p className="text-sm text-gray-600 mt-1">{t('viewRecentTransactions')}</p>
          </button>

          <div className="bg-white p-6 rounded-lg shadow">
            <RefreshCw className="text-purple-600 mb-3" size={32} />
            <h3 className="text-lg font-semibold text-gray-900">{t('autoSync')}</h3>
            <p className="text-sm text-gray-600 mt-1">{t('automaticDailyUpdates')}</p>
          </div>
        </div>

        {/* Connected Accounts */}
        {accounts.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">{t('connectedAccounts')}</h2>
            <div className="space-y-3">
              {accounts.map((account, index) => (
                <div key={index} className="flex justify-between items-center p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h3 className="font-semibold text-gray-900">{account.name}</h3>
                    <p className="text-sm text-gray-600">{account.type}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-gray-900">
                      ${typeof account.balance === 'object' 
                        ? (account.balance?.current || account.balance?.available || 0).toLocaleString()
                        : (account.balance || 0).toLocaleString()}
                    </div>
                    <p className="text-xs text-gray-500">{account.currency || 'USD'}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recent Transactions */}
        {transactions.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">{t('recentTransactions')}</h2>
            <div className="space-y-2">
              {transactions.slice(0, 10).map((transaction, index) => (
                <div key={index} className="flex justify-between items-center p-3 border-b border-gray-100">
                  <div>
                    <p className="font-medium text-gray-900">{transaction.name}</p>
                    <p className="text-sm text-gray-600">{transaction.date}</p>
                  </div>
                  <div className={`font-semibold ${transaction.amount < 0 ? 'text-red-600' : 'text-green-600'}`}>
                    ${Math.abs(transaction.amount).toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Demo Notice */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-6">
          <h3 className="font-semibold text-blue-900 mb-2">{t('demoModeActive')}</h3>
          <p className="text-sm text-blue-700">
            {t('demoModeBankingDesc')}
          </p>
        </div>
      </main>
    </div>
  )
}
