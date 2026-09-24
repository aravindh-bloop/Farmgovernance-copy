import React, { useState } from 'react';
import {
  Award,
  Building2,
  FileText,
  Globe,
  MessageSquare,
  Mic,
  ShieldCheck,
  Sprout,
  Volume2,
  ChevronUp,
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import VoiceInput from '../../components/VoiceInput/VoiceInput';

const SERVICE_CARDS = [
  { label: 'Farmer Schemes', icon: Sprout, query: 'Tell me about farmer welfare schemes available to me' },
  { label: 'Cooperative Law', icon: Building2, query: 'Help me understand cooperative law and PACS by-laws' },
  { label: 'PMFBY Insurance', icon: ShieldCheck, query: 'What is the PMFBY crop insurance claim process?' },
  { label: 'Financial Literacy', icon: Award, query: 'Explain KCC loans and interest subvention' },
  { label: 'File Grievance', icon: FileText, query: 'I want to file a grievance about a cooperative service' },
];

export default function Welcome({ onStart }) {
  const { language } = useLanguage();
  const [query, setQuery] = useState('');

  const submitQuery = (value = query) => onStart(value.trim());

  return (
    <div className="kiosk-portal">
      <div className="kiosk-stage">
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
            <button className="kiosk-language-pill" aria-label="Current language"><Globe size={14} /> {language.toUpperCase()}</button>
          </div>
        </header>

        <main className="kiosk-welcome-content">
          <p className="kiosk-eyebrow"><ShieldCheck size={13} /> VERIFIED COOPERATIVE ASSISTANCE</p>
          <h1>Hello!</h1>
          <h2>Welcome to <strong>CoopAssist.</strong></h2>
          <p className="kiosk-instruction">Tap the assistant and speak, or ask a question below<br />about schemes, laws, insurance, or grievances.</p>

          <button className="kiosk-orb-button" onClick={() => submitQuery()} aria-label="Start a conversation">
            <span className="orb-halo halo-one" />
            <span className="orb-halo halo-two" />
            <span className="kiosk-orb"><Mic size={27} /></span>
          </button>
          <span className="kiosk-orb-caption">Tap to speak</span>

          <div className="kiosk-prompt-bar">
            <MessageSquare size={17} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              onKeyDown={(event) => event.key === 'Enter' && submitQuery()}
              placeholder="Ask anything about cooperatives..."
              aria-label="Ask the cooperative assistant"
            />
            <VoiceInput onVoiceResult={(audioBlob, transcript) => submitQuery(transcript || '')} disabled={false} />
            <button onClick={() => submitQuery()} className="kiosk-prompt-send" aria-label="Send question"><ChevronUp size={17} /></button>
          </div>
        </main>

        <section className="kiosk-services">
          <div className="kiosk-services-heading">
            <span>Explore assistance</span>
            <small>Choose a topic to get started</small>
          </div>
          <div className="kiosk-service-dock">
            {SERVICE_CARDS.map(({ label, icon: Icon, query: serviceQuery }) => (
              <button key={label} className="kiosk-service-card" onClick={() => submitQuery(serviceQuery)}>
                <span className="service-icon"><Icon size={24} /></span>
                <span>{label}</span>
              </button>
            ))}
          </div>
        </section>

        <footer className="kiosk-footer-strip">
          <span><Volume2 size={13} /> Voice-first assistance for every citizen</span>
          <span>11 Indian languages <span className="footer-dot">•</span> Official knowledge sources</span>
        </footer>
      </div>
    </div>
  );
}
