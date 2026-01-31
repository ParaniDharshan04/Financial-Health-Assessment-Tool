import React from 'react'
import { useTranslation } from 'react-i18next'
import { Globe } from 'lucide-react'

export default function LanguageSelector() {
  const { i18n } = useTranslation()

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
    { code: 'ta', name: 'தமிழ்', flag: '🇮🇳' },
  ]

  const handleLanguageChange = (e) => {
    const newLang = e.target.value
    i18n.changeLanguage(newLang)
    localStorage.setItem('language', newLang)
  }

  return (
    <div className="flex items-center gap-2">
      <Globe size={18} className="text-gray-600" />
      <select
        value={i18n.language}
        onChange={handleLanguageChange}
        className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.flag} {lang.name}
          </option>
        ))}
      </select>
    </div>
  )
}
