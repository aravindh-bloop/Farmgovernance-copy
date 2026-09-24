import React from 'react';
import { 
  Building2, Sparkles, ShieldCheck, Award, MessageSquare, 
  ArrowRight, PhoneCall, ExternalLink, Activity
} from 'lucide-react';
import DomainCards from '../../components/DomainCards/DomainCards';
import NotificationPanel from '../../components/NotificationPanel/NotificationPanel';
import VoiceInput from '../../components/VoiceInput/VoiceInput';
import { TRANSLATIONS } from '../../utils/translations';

export default function Dashboard({ currentLang, setActiveTab, setChatQuery }) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const quickQuestions = [
    { text: "What is the 72-hour crop loss intimation rule under PMFBY?", domain: "pmfby" },
    { text: "How to appeal against illegal PACS membership rejection under Section 19?", domain: "law" },
    { text: "What is the effective 4% interest subvention formula on KCC loans?", domain: "financial" },
    { text: "How can PACS become a Multi-Purpose Center and Jan Aushadhi Kendra?", domain: "pacs" }
  ];

  return (
    <div style={{ paddingBottom: '60px' }}>
      {/* Hero Banner with Modern Gradient */}
      <div style={{
        background: 'linear-gradient(135deg, #064e3b 0%, #047857 50%, #065f46 100%)',
        borderRadius: '24px',
        padding: '40px 36px',
        color: '#ffffff',
        position: 'relative',
        overflow: 'hidden',
        boxShadow: '0 20px 40px -15px rgba(6, 78, 59, 0.35)'
      }}>
        <div style={{ position: 'relative', zIndex: 10, maxWidth: '820px' }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            background: 'rgba(255, 255, 255, 0.15)',
            backdropFilter: 'blur(8px)',
            padding: '6px 14px',
            borderRadius: '999px',
            fontSize: '13px',
            fontWeight: '600',
            marginBottom: '16px'
          }}>
            <Sparkles size={16} color="#fef08a" />
            <span>AI-Powered Multilingual Governance & Kiosk Assistance</span>
          </div>

          <h1 style={{ fontSize: '34px', fontWeight: '800', lineHeight: 1.25, marginBottom: '14px' }}>
            Empowering 63,000+ PACS & 10 Crore+ Indian Farmers with Verified Legal AI
          </h1>

          <p style={{ fontSize: '16px', color: '#a7f3d0', lineHeight: 1.6, marginBottom: '28px' }}>
            Instant statutory guidance on Cooperative Laws (MSCS Act 2023), PMFBY Crop Insurance claim workflows, PACS modernization bylaws, and automated Grievance Resolution Navigation.
          </p>

          {/* Quick Voice / Chat Trigger Bar */}
          <div style={{
            background: '#ffffff',
            borderRadius: '16px',
            padding: '8px 12px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            boxShadow: '0 10px 30px rgba(0,0,0,0.15)'
          }}>
            <VoiceInput
              currentLang={currentLang}
              onTranscript={(text) => {
                setChatQuery(text);
                setActiveTab('chat');
              }}
            />

            <input
              type="text"
              placeholder={t.askAnything}
              style={{
                flex: 1,
                border: 'none',
                outline: 'none',
                padding: '10px 12px',
                fontSize: '15px',
                color: '#0f172a'
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && e.target.value) {
                  setChatQuery(e.target.value);
                  setActiveTab('chat');
                }
              }}
            />

            <button
              onClick={() => setActiveTab('chat')}
              className="kiosk-btn kiosk-btn-primary"
              style={{ padding: '12px 24px', borderRadius: '10px' }}
            >
              <span>Ask AI</span>
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* Quick Prompts */}
      <div style={{
        marginTop: '20px',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        overflowX: 'auto',
        paddingBottom: '6px'
      }}>
        <span style={{ fontSize: '13px', fontWeight: '700', color: '#64748b', flexShrink: 0 }}>
          💡 Quick Topics:
        </span>
        {quickQuestions.map((q, i) => (
          <button
            key={i}
            onClick={() => {
              setChatQuery(q.text);
              setActiveTab('chat');
            }}
            style={{
              padding: '6px 14px',
              borderRadius: '999px',
              background: '#ffffff',
              border: '1px solid #cbd5e1',
              fontSize: '12px',
              fontWeight: '500',
              color: '#334155',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              transition: 'all 0.15s'
            }}
            onMouseEnter={(e) => (e.target.style.borderColor = '#059669')}
            onMouseLeave={(e) => (e.target.style.borderColor = '#cbd5e1')}
          >
            {q.text}
          </button>
        ))}
      </div>

      {/* Main Grid: Domain Modules & Live Notification Panel */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '2.4fr 1fr',
        gap: '24px',
        marginTop: '32px'
      }}>
        {/* Left: Domain Modules */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <h2 style={{ fontSize: '20px', fontWeight: '800', color: '#0f172a' }}>
                Key Functional Domains & Knowledge Portals
              </h2>
              <p style={{ fontSize: '13px', color: '#64748b' }}>
                Select a domain to view verified laws, guidelines, bylaws, or resolve specific queries.
              </p>
            </div>
          </div>

          <DomainCards onSelectDomain={(id) => setActiveTab(id)} currentLang={currentLang} />
        </div>

        {/* Right: Live Notifications & Stats */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <NotificationPanel />

          {/* Kiosk & Edge Device Status Box */}
          <div style={{
            background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
            borderRadius: '16px',
            padding: '20px',
            color: '#ffffff'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#34d399', marginBottom: '8px' }}>
              <Activity size={18} />
              <strong style={{ fontSize: '14px' }}>Edge Kiosk Diagnostics</strong>
            </div>
            <p style={{ fontSize: '12px', color: '#94a3b8', lineHeight: 1.5, marginBottom: '12px' }}>
              Optimized for Raspberry Pi 4/5 & Mini PCs with zero-bandwidth offline fallback.
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#cbd5e1' }}>Offline Engine:</span>
                <span style={{ color: '#34d399', fontWeight: '700' }}>Active & Synced</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#cbd5e1' }}>Speech Recognition:</span>
                <span style={{ color: '#34d399', fontWeight: '700' }}>Bhashini / Web Speech</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#cbd5e1' }}>Verified Acts:</span>
                <span style={{ color: '#ffffff', fontWeight: '700' }}>MSCS 2023 / PMFBY 2023</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
