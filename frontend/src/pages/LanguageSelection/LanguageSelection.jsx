import React from 'react';
import { Globe, ShieldCheck, Sprout } from 'lucide-react';
import { LANGUAGES } from '../../utils/languages';
import { useLanguage } from '../../context/LanguageContext';

export default function LanguageSelection({ onComplete }) {
  const { setLanguage, t } = useLanguage();

  const handleSelect = (code) => {
    setLanguage(code);
    onComplete();
  };

  return (
    <div className="kiosk-portal kiosk-language-portal">
      <div className="kiosk-stage">
        <header className="kiosk-topbar">
          <div className="kiosk-brand-lockup">
            <div className="kiosk-brand-mark"><Sprout size={20} /></div>
            <div><strong>CoopAssist</strong><span>Trusted cooperative guidance</span></div>
          </div>
          <span className="kiosk-live-status"><i /> Offline-ready</span>
        </header>

        <main className="language-welcome-content">
          <p className="kiosk-eyebrow"><ShieldCheck size={13} /> VOICE-FIRST COOPERATIVE ASSISTANCE</p>
          <div className="language-globe"><Globe size={30} /></div>
          <h1>{t('selectLanguageTitle')}</h1>
          <p>{t('selectLanguageHint')}</p>
          <div className="language-grid">
            {LANGUAGES.map((lang) => (
              <button key={lang.code} onClick={() => handleSelect(lang.code)} className="language-kiosk-option">
                <strong>{lang.native}</strong>
                <span>{lang.code.toUpperCase()}</span>
              </button>
            ))}
          </div>
        </main>

        <footer className="kiosk-footer-strip">
          <span><Globe size={13} /> Choose the language you are most comfortable with</span>
          <span>11 Indian languages <span className="footer-dot">•</span> Tap to continue</span>
        </footer>
      </div>
    </div>
  );
}
