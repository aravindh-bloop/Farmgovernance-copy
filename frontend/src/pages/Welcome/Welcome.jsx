import React, { useState, useRef, useCallback } from 'react';
import {
  Globe,
  MapPin,
  ShieldCheck,
  Mic,
  Volume2,
  ChevronRight,
  Maximize2,
  X,
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { LANGUAGES } from '../../utils/languages';
import ChatBox from '../../components/ChatBox/ChatBox';
import EReportDock from '../../components/EReportDock/EReportDock';

/* ────────────────────── Mascot Speech Bubble Text ────────────────────── */
const SPEECH_BUBBLE_TEXT = {
  en: { line1: 'Hello!', line2: "I'm Arav AI.", line3: 'How can I help?' },
  ta: { line1: 'வணக்கம்!', line2: 'நான் Arav AI.', line3: 'என்ன உதவி வேண்டும்?' },
  hi: { line1: 'नमस्ते!', line2: 'मैं Arav AI हूँ।', line3: 'कैसे मदद करूँ?' },
  kn: { line1: 'ನಮಸ್ಕಾರ!', line2: 'ನಾನು Arav AI.', line3: 'ಏನು ಸಹಾಯ ಬೇಕು?' },
  te: { line1: 'నమస్కారం!', line2: 'నేను Arav AI.', line3: 'ఏం సహాయం కావాలి?' },
  mr: { line1: 'नमस्कार!', line2: 'मी Arav AI आहे.', line3: 'कशी मदत करू?' },
  gu: { line1: 'નમસ્તે!', line2: 'હું Arav AI છું.', line3: 'શું મદદ કરું?' },
  bn: { line1: 'নমস্কার!', line2: 'আমি Arav AI।', line3: 'কী সাহায্য চাই?' },
  ml: { line1: 'നമസ്കാരം!', line2: 'ഞാൻ Arav AI.', line3: 'എന്ത് സഹായം?' },
  pa: { line1: 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ!', line2: 'ਮੈਂ Arav AI ਹਾਂ।', line3: 'ਕੀ ਮਦਦ ਚਾਹੀਦੀ?' },
  or: { line1: 'ନମସ୍କାର!', line2: 'ମୁଁ Arav AI।', line3: 'କଣ ସାହାଯ୍ୟ?' },
};

/* ────────────────────── Dynamic Languages Array ────────────────────── */
const DYNAMIC_LANGUAGES = [
  'Your Language',
  'आपकी भाषा',
  'உங்கள் மொழியில்',
  'ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ',
  'మీ భాషలో',
  'तुमच्या भाषेत',
  'તમારી ભાષામાં',
  'আপনার ভাষায়',
  'നിങ്ങളുടെ ഭാഷയിൽ',
  'ਤੁਹਾਡੀ ਭਾਸ਼ਾ ਵਿੱਚ',
  'ଆପଣଙ୍କ ଭାଷାରେ'
];

/* ────────────────────── SVG Icons for Cards ────────────────────── */
const FarmerIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22c4-4 8-7.5 8-12a8 8 0 00-16 0c0 4.5 4 8 8 12z"/>
    <path d="M9 12l2 2 4-4"/>
  </svg>
);
const LawIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
    <polyline points="14 2 14 8 20 8"/>
    <line x1="16" y1="13" x2="8" y2="13"/>
    <line x1="16" y1="17" x2="8" y2="17"/>
  </svg>
);
const ShieldIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    <path d="M9 12l2 2 4-4"/>
  </svg>
);
const CoinsIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="9" cy="7" r="5"/>
    <path d="M14 12a5 5 0 015 5"/>
    <circle cx="9" cy="17" r="5" opacity="0.5"/>
  </svg>
);
const GrievanceIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
    <polyline points="14 2 14 8 20 8"/>
    <path d="M12 18v-6"/>
    <circle cx="12" cy="12" r="0.5"/>
  </svg>
);

const SERVICE_CARDS = [
  { id: 'schemes', label: 'Farmer Schemes', desc: 'PMFBY, Subsidies, Support Programs', icon: FarmerIcon, color: '#0B8F4D', bg: '#E8F7EF', query: 'Tell me about farmer welfare schemes available to me' },
  { id: 'law', label: 'Cooperative Law', desc: 'Laws, By-laws, Registration', icon: LawIcon, color: '#2F80ED', bg: '#EAF4FF', query: 'Help me understand cooperative law and PACS by-laws' },
  { id: 'insurance', label: 'Insurance Guidance', desc: 'PMFBY, Claim Process, Document Help', icon: ShieldIcon, color: '#E6A817', bg: '#FFF7DF', query: 'What is the PMFBY crop insurance claim process?' },
  { id: 'financial', label: 'Financial Literacy', desc: 'Loans, Credit, Savings, Best Practices', icon: CoinsIcon, color: '#7C3AED', bg: '#F4EEFF', query: 'Explain KCC loans and interest subvention' },
  { id: 'grievance', label: 'File Grievance', desc: 'Raise Complaints, Track Status', icon: GrievanceIcon, color: '#DC2626', bg: '#FFF0F0', query: 'I want to file a grievance about a cooperative service' },
];

/* ────────────────────── User Tag Hook (Kiosk) ────────────────────── */
function useUserTag() {
  const [tag] = useState(() => {
    try {
      const saved = localStorage.getItem('coop_user_tag');
      if (saved) return saved;
      const id = 'K' + Math.random().toString(36).slice(2, 6).toUpperCase();
      localStorage.setItem('coop_user_tag', id);
      return id;
    } catch {
      return 'K-GUEST';
    }
  });
  return tag;
}

/* ════════════════════════════════════════════════════════════════════
   Welcome / Home Page Component
   ════════════════════════════════════════════════════════════════════ */
export default function Welcome({ onStart }) {
  const { language, setLanguage } = useLanguage();
  const userTag = useUserTag();
  const bubble = SPEECH_BUBBLE_TEXT[language] || SPEECH_BUBBLE_TEXT.en;

  // Actual Location Fetcher
  const [userLocation, setUserLocation] = useState('Locating...');
  React.useEffect(() => {
    fetch('https://ipapi.co/json/')
      .then(res => res.json())
      .then(data => {
        if (data.city) setUserLocation(data.city);
        else setUserLocation('New Delhi');
      })
      .catch(() => setUserLocation('New Delhi'));
  }, []);

  // Dynamic Language Looper
  const [dynamicLangIndex, setDynamicLangIndex] = useState(0);
  React.useEffect(() => {
    const interval = setInterval(() => {
      setDynamicLangIndex((prev) => (prev + 1) % DYNAMIC_LANGUAGES.length);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  // Language dropdown
  const [langOpen, setLangOpen] = useState(false);

  // Chat overlay state (existing functionality preserved)
  const [chatOpen, setChatOpen] = useState(false);
  const [seed, setSeed] = useState('');
  const [autoListen, setAutoListen] = useState(false);
  const [turns, setTurns] = useState([]);
  const [chatBusy, setChatBusy] = useState(false);

  const handleConversationState = useCallback((next) => {
    setTurns(next.turns);
    setChatBusy(next.isLoading);
  }, []);

  const openChat = (initialQuery = '', listen = false) => {
    setSeed(initialQuery);
    setAutoListen(listen);
    setChatOpen(true);
  };

  const closeChat = () => {
    setChatOpen(false);
    setSeed('');
    setAutoListen(false);
  };

  return (
    <div className="arav-home">
      {/* ── Background ── */}
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
              <button className="arav-pill arav-pill--lang" onClick={() => setLangOpen(!langOpen)} aria-label="Language" type="button">
                <Globe size={16} />
                <span>{(language || 'en').toUpperCase()}</span>
                <svg width="9" height="5" viewBox="0 0 10 6" fill="none"><path d="M1 1L5 5L9 1" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
              </button>
              {langOpen && (
                <>
                  <div className="arav-lang-backdrop" onClick={() => setLangOpen(false)} />
                  <div className="arav-lang-dropdown">
                    {LANGUAGES.map((l) => (
                      <button 
                        key={l.code} 
                        className={`arav-lang-opt ${l.code === language ? 'arav-lang-opt--active' : ''}`} 
                        onClick={() => {
                          setLanguage(l.code);
                          setLangOpen(false);
                        }} 
                        type="button"
                      >
                        <span className="arav-lang-opt__native">{l.native}</span>
                        <span className="arav-lang-opt__code">{l.code.toUpperCase()}</span>
                      </button>
                    ))}
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* ── HERO ── */}
      <main className="arav-main">
        <section className="arav-hero">
          <div className="arav-hero__layout">
            {/* Left: Mascot */}
            <div className="arav-hero__mascot-area">
              <div className="arav-mascot">
                <div className="arav-speech-bubble">
                  <p className="arav-speech-bubble__greeting">{bubble.line1}</p>
                  <p className="arav-speech-bubble__line">{bubble.line2}</p>
                  <p className="arav-speech-bubble__line">{bubble.line3}</p>
                  <div className="arav-speech-bubble__tail" />
                </div>
                <img src="/images/aravai-mascot.png" alt="Arav AI Mascot" className="arav-mascot__img" draggable="false" />
              </div>
            </div>

            {/* Right: Content + Mic */}
            <div className="arav-hero__text-area">
              <div className="arav-badge"><ShieldCheck size={13} /> VERIFIED COOPERATIVE ASSISTANCE</div>
              <h1 className="arav-hero__title">Arav <span className="arav-ai-text">AI</span></h1>
              <p className="arav-hero__subtitle">
                Your Cooperative Guide,<br/>in <span key={dynamicLangIndex} className="arav-dynamic-lang-text">{DYNAMIC_LANGUAGES[dynamicLangIndex]}</span>.
              </p>
              <p className="arav-hero__desc">Ask about schemes, laws, insurance, credit or grievances.</p>
              <p className="arav-hero__hint">Tap the microphone and speak — I will listen and reply by voice.</p>

              {/* Mic Button */}
              <div className="arav-mic-cta">
                <div className="arav-mic-rings">
                  <span className="arav-mic-ring arav-mic-ring--1" />
                  <span className="arav-mic-ring arav-mic-ring--2" />
                  <span className="arav-mic-ring arav-mic-ring--3" />
                </div>
                <button className="arav-mic-btn" onClick={() => openChat('', true)} aria-label="Press to Speak" type="button">
                  <Mic size={38} strokeWidth={2} />
                </button>
                <div className="arav-mic-label-wrapper">
                  <span className="arav-mic-label">Press to Speak</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── BOTTOM SHEET AREA ── */}
        <div className="arav-bottom-sheet">
          {/* ── ASSISTANCE CARDS ── */}
          <section className="arav-assist" aria-labelledby="arav-assist-heading">
            <div className="arav-assist__header">
              <h2 id="arav-assist-heading" className="arav-assist__title">Explore Assistance</h2>
              <span className="arav-assist__hint">Choose a topic to get started</span>
            </div>
            <div className="arav-assist__grid">
              {SERVICE_CARDS.map(({ id, label, desc, icon: Icon, color, bg, query }) => (
                <button key={id} className="arav-card" onClick={() => openChat(query)} type="button" style={{ '--card-color': color, '--card-bg': bg }}>
                  <div className="arav-card__icon"><Icon /></div>
                  <div className="arav-card__body">
                    <strong className="arav-card__title">{label}</strong>
                    <span className="arav-card__desc">{desc}</span>
                  </div>
                  <ChevronRight size={16} className="arav-card__arrow" />
                </button>
              ))}
            </div>
          </section>

          {/* ── FOOTER ── */}
          <footer className="arav-footer">
            <span className="arav-footer__left"><Volume2 size={14} /> Voice-first assistance for every citizen</span>
            <span className="arav-footer__right">{LANGUAGES.length} Indian languages <span className="arav-footer__dot">•</span> Official knowledge sources</span>
          </footer>
        </div>
      </main>

      {/* ── CHAT OVERLAY (existing functionality preserved) ── */}
      {chatOpen && (
        <div className="kiosk-chat-overlay" role="dialog" aria-modal="false" aria-label="Voice conversation">
          <div className="kiosk-chat-overlay-topbar">
            <div className="arav-header__brand" style={{ gap: '8px' }}>
              <img src="/images/logo.png" alt="Arav AI" style={{ width: 28, height: 28, borderRadius: 6, objectFit: 'contain' }} />
              <div>
                <strong style={{ display: 'block', fontSize: 14, color: '#102A56' }}>Arav AI</strong>
                <span style={{ display: 'block', fontSize: 9, color: '#64748b', marginTop: 2 }}>Voice conversation</span>
              </div>
            </div>
            <div className="kiosk-chat-overlay-actions">
              <button className="kiosk-overlay-btn" onClick={() => onStart(seed)} title="Open full screen">
                <Maximize2 size={16} /><span>Full screen</span>
              </button>
              <button className="kiosk-overlay-btn" onClick={closeChat} title="Close conversation">
                <X size={16} /><span>Close</span>
              </button>
            </div>
          </div>
          <div className="kiosk-chat-overlay-body">
            <ChatBox
            initialQuery={seed}
            onConversationState={handleConversationState}
            autoListen={autoListen}
          />
          </div>
          <EReportDock turns={turns} isLoading={chatBusy} userTag={userTag} />
        </div>
      )}
    </div>
  );
}
