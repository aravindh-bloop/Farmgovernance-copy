import React, { useState, useEffect } from 'react';
import { LanguageProvider, useLanguage } from './context/LanguageContext';
import LanguageSelection from './pages/LanguageSelection/LanguageSelection';
import Welcome from './pages/Welcome/Welcome';
import Chat from './pages/Chat/Chat';
import { Sun, Moon } from 'lucide-react';

const SCREENS = {
  LANGUAGE: 'language',
  WELCOME: 'welcome',
  CHAT: 'chat',
};

function AppContent() {
  const { hasSelectedLanguage, clearLanguage } = useLanguage();
  const [screen, setScreen] = useState(() =>
    hasSelectedLanguage ? SCREENS.WELCOME : SCREENS.LANGUAGE
  );

  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('coop_kiosk_theme') || 'light';
    } catch {
      return 'light';
    }
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('coop_kiosk_theme', theme);
    } catch (e) {
      console.error(e);
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const handleLanguageComplete = () => setScreen(SCREENS.WELCOME);
  const handleStartChat = (initialQuery = '') => setScreen({ screen: SCREENS.CHAT, initialQuery });
  const handleChangeLanguage = () => {
    clearLanguage();
    setScreen(SCREENS.LANGUAGE);
  };

  return (
    <div className="app-root" style={{ position: 'relative' }}>
      {/* 🌙 Floating Corner Dark Mode Switch from the very start of the website */}
      <div className="theme-toggle" style={{
        position: 'fixed',
        top: '1rem',
        right: '1rem',
        zIndex: 9999,
      }}>
        <button
          onClick={toggleTheme}
          title={theme === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme'}
          style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--border-light)',
            color: 'var(--text-main)',
            padding: '0.45rem 0.9rem',
            borderRadius: '999px',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.45rem',
            fontWeight: '600',
            fontSize: '0.82rem',
            boxShadow: 'var(--card-shadow)',
            backdropFilter: 'blur(10px)',
            transition: 'all 0.2s ease',
          }}
        >
          {theme === 'dark' ? <Sun size={15} color="#fbbf24" /> : <Moon size={15} color="#059669" />}
          <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
        </button>
      </div>

      {screen === SCREENS.LANGUAGE && (
        <LanguageSelection onComplete={handleLanguageComplete} />
      )}
      {screen === SCREENS.WELCOME && (
        <Welcome onStart={handleStartChat} />
      )}
      {screen.screen === SCREENS.CHAT && (
        <Chat initialQuery={screen.initialQuery} onChangeLanguage={handleChangeLanguage} />
      )}

      <footer className="app-footer">
        Smart India Hackathon 2026 • Team BRAVITS (PS ID: SIH26088)
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  );
}
