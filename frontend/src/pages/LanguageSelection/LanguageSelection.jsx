import React, { useState, useEffect } from 'react';
import { Globe, MapPin, ShieldCheck, ChevronRight } from 'lucide-react';
import { LANGUAGES } from '../../utils/languages';
import { useLanguage } from '../../context/LanguageContext';

export default function LanguageSelection({ onComplete }) {
  const { setLanguage } = useLanguage();

  const [userLocation, setUserLocation] = useState('Locating...');
  useEffect(() => {
    fetch('https://ipapi.co/json/')
      .then(res => res.json())
      .then(data => {
        if (data.city) setUserLocation(data.city);
        else setUserLocation('New Delhi');
      })
      .catch(() => setUserLocation('New Delhi'));
  }, []);

  const handleSelect = (code) => {
    setLanguage(code);
    onComplete();
  };

  return (
    <div className="arav-home">
      <div className="arav-home__bg" />
      <div className="arav-home__overlay" />

      {/* ── HEADER ── */}
      <header className="arav-header" role="banner">
        <div className="arav-header__inner">
          <div className="arav-header__brand">
            <img src="/images/logo.png" alt="Arav AI" className="arav-header__logo" width="56" height="56" />
            <div className="arav-header__brand-text">
              <span className="arav-header__name">Arav <span className="arav-ai-text">AI</span></span>
              <span className="arav-header__tagline-text">Your Cooperative Guide, in Your Language.</span>
            </div>
          </div>
          <div className="arav-header__controls">
            <span className="arav-pill arav-pill--status"><i className="arav-status-dot" /> <span className="arav-pill__label">Offline-ready</span></span>
            <span className="arav-pill"><MapPin size={16} /> <span className="arav-pill__label">{userLocation}</span></span>
            <div className="arav-lang-wrap">
              <button className="arav-pill arav-pill--lang" aria-label="Language" type="button">
                <Globe size={16} />
                <span>EN</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* ── MAIN HERO ── */}
      <main className="arav-main">
        <section className="arav-hero">
          <div className="arav-hero__layout">
            
            {/* Mascot */}
            <div className="arav-hero__mascot-area">
              <div className="arav-mascot">
                <img src="/images/aravai-mascot.png" alt="Arav AI Mascot" className="arav-mascot__img" />
              </div>
            </div>

            {/* Language Selection Area */}
            <div className="arav-hero__text-area" style={{ maxWidth: '900px', zIndex: 10 }}>
              <div className="arav-badge"><ShieldCheck size={13} /> VERIFIED COOPERATIVE ASSISTANCE</div>
              <h1 className="arav-hero__title" style={{ fontSize: '4rem', marginBottom: '0' }}>
                Choose your <span className="arav-ai-text">language</span>
              </h1>
              <p className="arav-hero__desc" style={{ fontSize: '1.2rem', marginBottom: '2.5rem', fontWeight: '600' }}>
                Select the language you are most comfortable with
              </p>
              
              <div className="arav-lang-selection-grid">
                {LANGUAGES.map((lang) => (
                  <button 
                    key={lang.code} 
                    onClick={() => handleSelect(lang.code)} 
                    className="arav-lang-selection-btn"
                  >
                    <div className="arav-lang-selection-content">
                      <strong className="arav-lang-selection-native">{lang.native}</strong>
                      <span className="arav-lang-selection-code">{lang.code.toUpperCase()}</span>
                    </div>
                    <ChevronRight size={18} className="arav-lang-selection-arrow" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* ── FOOTER ── */}
      <footer className="arav-footer" style={{ padding: '0 2rem 1.5rem', position: 'absolute', bottom: 0, width: '100%', borderTop: 'none' }}>
        <div className="arav-footer__left">
          <Globe size={16} /> Choose the language you are most comfortable with
        </div>
        <div className="arav-footer__right">
          <span>11 Indian languages</span>
          <span className="arav-footer__dot">•</span>
          <span>Official knowledge sources</span>
        </div>
      </footer>
    </div>
  );
}
