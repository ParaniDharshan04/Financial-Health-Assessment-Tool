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
      <Globe size={18} className="text-gray-300" />
      <select
        value={i18n.language}
        onChange={handleLanguageChange}
        className="input-glass px-3 py-2 text-sm cursor-pointer"
        style={{ colorScheme: 'dark' }}
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code} style={{backgroundColor: '#1e293b', color: '#fff'}}>
            {lang.flag} {lang.name}
          </option>
        ))}
      </select>
    </div>
  )
}
