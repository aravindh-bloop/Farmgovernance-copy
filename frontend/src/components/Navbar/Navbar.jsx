import React from 'react';
import { 
  Building2, MessageSquare, Scale, Award, ShieldAlert, 
  Layers, Landmark, FileText, Bell, Volume2
} from 'lucide-react';
import LanguageSelector from '../LanguageSelector/LanguageSelector';
import { TRANSLATIONS } from '../../utils/translations';

export default function Navbar({ activeTab, setActiveTab, currentLang, setCurrentLang, notificationsCount }) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const navItems = [
    { id: 'dashboard', label: t.navHome, icon: Building2 },
    { id: 'chat', label: t.navChat, icon: MessageSquare },
    { id: 'grievance', label: t.navGrievance, icon: ShieldAlert, highlight: true },
    { id: 'law', label: t.navLaw, icon: Scale },
    { id: 'schemes', label: t.navSchemes, icon: Award },
    { id: 'pmfby', label: t.navPMFBY, icon: Layers },
    { id: 'pacs', label: t.navPACS, icon: Landmark },
    { id: 'financial', label: t.navFinance, icon: FileText },
  ];

  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 50,
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid #e2e8f0',
      boxShadow: '0 2px 10px rgba(0,0,0,0.03)'
    }}>
      {/* Top Gov / SIH Banner */}
      <div style={{
        background: 'linear-gradient(90deg, #064e3b 0%, #047857 50%, #0f766e 100%)',
        color: '#ffffff',
        padding: '6px 24px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        fontSize: '12px',
        fontWeight: '500'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ 
            background: 'rgba(255,255,255,0.2)', 
            padding: '2px 8px', 
            borderRadius: '4px',
            letterSpacing: '0.5px'
          }}>
            🇮🇳 SIH 2026 • PS ID: SIH26088
          </span>
          <span>Ministry of Cooperation & Agriculture Assistance Platform</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ color: '#fef08a' }}>Team BRAVITS</span>
          <span style={{ opacity: 0.8 }}>|</span>
          <span>Toll-Free: 1800-180-COOP</span>
        </div>
      </div>

      {/* Main Navbar */}
      <div style={{
        maxWidth: '1440px',
        margin: '0 auto',
        padding: '12px 24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '20px'
      }}>
        {/* Brand Logo */}
        <div 
          onClick={() => setActiveTab('dashboard')}
          style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }}
        >
          <div style={{
            width: '44px',
            height: '44px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            boxShadow: '0 4px 12px rgba(4, 120, 87, 0.3)'
          }}>
            <Building2 size={24} />
          </div>
          <div>
            <h1 style={{ fontSize: '18px', fontWeight: '800', color: '#064e3b', lineHeight: 1.2 }}>
              {t.appName}
            </h1>
            <p style={{ fontSize: '11px', color: '#64748b', fontWeight: '500' }}>
              {t.tagline}
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '4px', overflowX: 'auto' }}>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '8px 14px',
                  borderRadius: '10px',
                  fontSize: '13px',
                  fontWeight: isActive ? '700' : '500',
                  border: 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  background: isActive 
                    ? (item.highlight ? '#fef2f2' : '#ecfdf5')
                    : 'transparent',
                  color: isActive 
                    ? (item.highlight ? '#b91c1c' : '#047857')
                    : '#475569',
                  borderBottom: isActive ? `2px solid ${item.highlight ? '#ef4444' : '#059669'}` : '2px solid transparent'
                }}
              >
                <Icon size={16} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Right Tools: Language Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <LanguageSelector currentLang={currentLang} onSelectLang={setCurrentLang} />
        </div>
      </div>
    </header>
  );
}
