import React, { useState, useEffect, useRef } from 'react';
import { LanguageProvider, useLanguage } from './context/LanguageContext';
import LanguageSelection from './pages/LanguageSelection/LanguageSelection';
import Welcome from './pages/Welcome/Welcome';
import Chat from './pages/Chat/Chat';
import { Sun, Moon } from 'lucide-react';
import IdleScreen from './components/IdleScreen/IdleScreen';

const SCREENS = {
  LANGUAGE: 'language',
  WELCOME: 'welcome',
  CHAT: 'chat',
};

// 3 minutes in milliseconds
const IDLE_TIMEOUT = 3 * 60 * 1000; 

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

  const [isIdle, setIsIdle] = useState(false);
  const idleTimerRef = useRef(null);

  const resetIdleTimer = () => {
    if (isIdle) {
      setIsIdle(false);
    }
    if (idleTimerRef.current) {
      clearTimeout(idleTimerRef.current);
    }
    idleTimerRef.current = setTimeout(() => {
      setIsIdle(true);
    }, IDLE_TIMEOUT);
  };

  useEffect(() => {
    // Initial timer start
    resetIdleTimer();

    // Event listeners for user activity
    const events = ['mousemove', 'mousedown', 'keydown', 'touchstart', 'scroll'];
    const handleUserActivity = () => resetIdleTimer();

    events.forEach(event => document.addEventListener(event, handleUserActivity));

    return () => {
      if (idleTimerRef.current) {
        clearTimeout(idleTimerRef.current);
      }
      events.forEach(event => document.removeEventListener(event, handleUserActivity));
    };
  }, [isIdle]);

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

  const handleWakeUp = () => {
    setIsIdle(false);
    resetIdleTimer();
    // Return to home page (Language Selection or Welcome depending on state)
    // "take us to the home page of the kiosk UI" - typically this means reset completely
    clearLanguage();
    setScreen(SCREENS.LANGUAGE);
  };

  const handleLanguageComplete = () => setScreen(SCREENS.WELCOME);
  const handleStartChat = (initialQuery = '') => setScreen({ screen: SCREENS.CHAT, initialQuery });
  const handleChangeLanguage = () => {
    clearLanguage();
    setScreen(SCREENS.LANGUAGE);
  };

  return (
    <div className="app-root" style={{ position: 'relative' }}>
      {isIdle && <IdleScreen onWakeUp={handleWakeUp} />}
      
      {/* 🌙 Floating Corner Dark Mode Switch from the very start of the website */}
      <div className="theme-toggle" style={{
        position: 'fixed',
        top: '1rem',
        right: '1rem',
        zIndex: 9999,
        display: isIdle ? 'none' : 'block'
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
