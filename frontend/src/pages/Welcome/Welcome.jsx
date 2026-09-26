import React, { useState, useCallback } from 'react';
import {
  Building2,
  FileText,
  Globe,
  Award,
  ShieldCheck,
  Sprout,
  Volume2,
  Maximize2,
  X,
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import ChatBox from '../../components/ChatBox/ChatBox';
import EReportDock from '../../components/EReportDock/EReportDock';

const SERVICE_CARDS = [
  { label: 'Farmer Schemes', icon: Sprout, query: 'Tell me about farmer welfare schemes available to me' },
  { label: 'Cooperative Law', icon: Building2, query: 'Help me understand cooperative law and PACS by-laws' },
  { label: 'PMFBY Insurance', icon: ShieldCheck, query: 'What is the PMFBY crop insurance claim process?' },
  { label: 'Financial Literacy', icon: Award, query: 'Explain KCC loans and interest subvention' },
  { label: 'File Grievance', icon: FileText, query: 'I want to file a grievance about a cooperative service' },
];

/** Stable per-kiosk identity so a farmer can be recognised across sessions. */
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

export default function Welcome({ onStart }) {
  const { language } = useLanguage();
  const userTag = useUserTag();

  // The voice conversation lives on this page. Opening it never navigates away,
  // so the kiosk keeps its voice-first identity for the whole session.
  const [chatOpen, setChatOpen] = useState(false);
  const [seed, setSeed] = useState('');
  const [turns, setTurns] = useState([]);
  const [chatBusy, setChatBusy] = useState(false);

  // Stable callback identity, otherwise the reporter effect re-fires forever.
  const handleConversationState = useCallback((next) => {
    setTurns(next.turns);
    setChatBusy(next.isLoading);
  }, []);

  const openChat = (initialQuery = '') => {
    setSeed(initialQuery);
    setChatOpen(true);
  };

  return (
    <div className="kiosk-portal">
      <div className={`kiosk-stage ${chatOpen ? 'is-conversing' : ''}`}>
        <header className="kiosk-topbar">
          <div className="kiosk-brand-lockup">
            <div className="kiosk-brand-mark"><Sprout size={20} /></div>
            <div>
              <strong>CoopAssist</strong>
              <span>Trusted cooperative guidance</span>
            </div>
          </div>
          <div className="kiosk-status-row">
            <span className="kiosk-live-status"><i /> Offline-ready</span>
            <span className="kiosk-user-tag" title="This kiosk's user reference">
              <span className="kiosk-user-tag-dot" />
              {userTag}
            </span>
            <button className="kiosk-language-pill" aria-label="Current language"><Globe size={14} /> {language.toUpperCase()}</button>
          </div>
        </header>

        <main className="kiosk-welcome-content">
          {/* Greeting sits at the top of the content area, not centred. */}
          <div className="kiosk-greeting">
            <p className="kiosk-eyebrow"><ShieldCheck size={13} /> VERIFIED COOPERATIVE ASSISTANCE</p>
            <h1>Hello!</h1>
            <h2>Welcome to <strong>CoopAssist.</strong></h2>
            <p className="kiosk-instruction">
              Ask about schemes, laws, insurance, credit or grievances.<br />
              Tap the microphone and speak — I will listen and reply by voice.
            </p>
          </div>

          {/* One large, centred microphone is the primary way in. */}
          <div className="kiosk-mic-stage">
            <button
              className="kiosk-orb-button"
              onClick={() => openChat()}
              aria-label="Start a voice conversation"
            >
              <span className="orb-halo halo-one" />
              <span className="orb-halo halo-two" />
              <span className="kiosk-orb"><span className="kiosk-orb-mic" /></span>
            </button>
            <span className="kiosk-orb-caption">Tap to speak</span>
          </div>
        </main>

        <section className="kiosk-services">
          <div className="kiosk-services-heading">
            <span>Explore assistance</span>
            <small>Choose a topic to get started</small>
          </div>
          <div className="kiosk-service-dock">
            {SERVICE_CARDS.map(({ label, icon: Icon, query }) => (
              <button key={label} className="kiosk-service-card" onClick={() => openChat(query)}>
                <span className="service-icon"><Icon size={22} /></span>
                <span>{label}</span>
              </button>
            ))}
          </div>
        </section>

        <footer className="kiosk-footer-strip">
          <span><Volume2 size={13} /> Voice-first assistance for every citizen</span>
          <span>11 Indian languages <span className="footer-dot">•</span> Official knowledge sources</span>
        </footer>

        {/* Voice conversation opens over the welcome page — no new screen. */}
        {chatOpen && (
          <div className="kiosk-chat-overlay" role="dialog" aria-modal="true" aria-label="Voice conversation">
            <div className="kiosk-chat-overlay-topbar">
              <div className="kiosk-brand-lockup">
                <div className="kiosk-brand-mark"><Sprout size={20} /></div>
                <div>
                  <strong>CoopAssist</strong>
                  <span>Voice conversation</span>
                </div>
              </div>
              <div className="kiosk-chat-overlay-actions">
                <button
                  className="kiosk-overlay-btn"
                  onClick={() => onStart(seed)}
                  title="Open full screen"
                >
                  <Maximize2 size={16} />
                  <span>Full screen</span>
                </button>
                <button
                  className="kiosk-overlay-btn"
                  onClick={() => { setChatOpen(false); setSeed(''); }}
                  title="Close conversation"
                >
                  <X size={16} />
                  <span>Close</span>
                </button>
              </div>
            </div>
            <div className="kiosk-chat-overlay-body">
              <ChatBox initialQuery={seed} onConversationState={handleConversationState} />
            </div>
            <EReportDock turns={turns} isLoading={chatBusy} userTag={userTag} />
          </div>
        )}
      </div>
    </div>
  );
}
