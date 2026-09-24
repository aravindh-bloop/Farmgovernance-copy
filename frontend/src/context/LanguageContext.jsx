import React, { createContext, useContext, useState, useCallback } from 'react';
import { TRANSLATIONS } from '../utils/translations';

const LanguageContext = createContext(null);

const SESSION_KEY = 'coop_ui_lang';

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    return sessionStorage.getItem(SESSION_KEY) || null;
  });

  const setLanguage = useCallback((code) => {
    sessionStorage.setItem(SESSION_KEY, code);
    setLanguageState(code);
  }, []);

  const clearLanguage = useCallback(() => {
    sessionStorage.removeItem(SESSION_KEY);
    setLanguageState(null);
  }, []);

  const t = useCallback(
    (key) => {
      const dict = TRANSLATIONS[language] || TRANSLATIONS.en;
      return dict[key] ?? TRANSLATIONS.en[key] ?? key;
    },
    [language]
  );

  return (
    <LanguageContext.Provider value={{ language, setLanguage, clearLanguage, t, hasSelectedLanguage: !!language }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error('useLanguage must be used within LanguageProvider');
  return ctx;
}
