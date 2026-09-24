import React, { useState } from 'react';
import { LANGUAGES, TRANSLATIONS } from '../translations';
import { Globe, Check, ArrowRight, Bot, User, Phone, MapPin, Building, Sparkles, ShieldCheck, Sun, Moon } from 'lucide-react';

const TN_DISTRICTS = [
  'Theni', 'Madurai', 'Pudukkottai', 'Coimbatore', 'Thanjavur', 'Dindigul',
  'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Erode', 'Vellore', 'Kanchipuram',
  'Cuddalore', 'Villupuram', 'Tiruppur', 'Ramanathapuram', 'Sivaganga',
  'Virudhunagar', 'Karur', 'Nagapattinam', 'Tiruvarur', 'Krishnagiri',
  'Dharmapuri', 'Namakkal', 'Nilgiris', 'Thoothukudi', 'Kanyakumari',
  'Tiruvallur', 'Tiruvannamalai', 'Ranipet', 'Tenkasi', 'Chengalpattu',
  'Kallakurichi', 'Mayiladuthurai', 'Ariyalur', 'Perambalur', 'Tirupathur', 'Chennai'
];

/**
 * Onboarding Screen with Language Selection + Personal Account Creation
 * First-time visitors establish their language and register their personal account
 * before entering the main chat interface.
 */
export default function LanguageSelectionScreen({
  selectedLang,
  onSelectLanguage,
  onCompleteOnboarding,
  theme,
  onToggleTheme,
}) {
  const [step, setStep] = useState(1); // Step 1: Language, Step 2: Account Creation
  const t = TRANSLATIONS[selectedLang] || TRANSLATIONS.en;

  const [formData, setFormData] = useState({
    name: '',
    mobile: '',
    district: 'Theni',
    societyName: '',
    memberType: 'Farmer Member',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFinish = (e) => {
    e?.preventDefault();
    const newUser = {
      ...formData,
      name: formData.name.trim() || 'Cooperative Member',
      preferredLang: selectedLang,
      id: `MEMBER-${Date.now().toString().slice(-6)}`,
      createdAt: new Date().toISOString(),
    };

    localStorage.setItem('coop_portal_user', JSON.stringify(newUser));
    onCompleteOnboarding(newUser);
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'radial-gradient(circle at 50% 20%, rgba(59, 130, 246, 0.15), transparent 70%), var(--bg-main)',
      padding: '2rem 1rem',
      position: 'relative',
    }}>
      {/* 🌙 Floating Corner Dark Mode Switch (Available from the starting screen) */}
      <div style={{
        position: 'fixed',
        top: '1.25rem',
        right: '1.25rem',
        zIndex: 999,
      }}>
        <button
          onClick={onToggleTheme}
          title={theme === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme'}
          style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--bg-card-border)',
            color: 'var(--text-primary)',
            padding: '0.55rem 1rem',
            borderRadius: '999px',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontWeight: '600',
            fontSize: '0.85rem',
            boxShadow: 'var(--shadow-md)',
            backdropFilter: 'blur(10px)',
            transition: 'all 0.25s ease',
          }}
        >
          {theme === 'dark' ? <Sun size={17} color="#fbbf24" /> : <Moon size={17} color="#3b82f6" />}
          <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
        </button>
      </div>
      <div className="glass-panel" style={{
        maxWidth: step === 1 ? '840px' : '580px',
        width: '100%',
        padding: '2.5rem',
        borderRadius: '1.5rem',
        boxShadow: 'var(--shadow-lg)',
        transition: 'all 0.3s ease',
      }}>
        {/* Header / Logo */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: '60px',
            height: '60px',
            borderRadius: '1rem',
            background: 'var(--primary-gradient)',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            marginBottom: '1rem',
            boxShadow: 'var(--shadow-glow)',
          }}>
            <Bot size={32} />
          </div>

          <h1 style={{
            fontSize: '1.85rem',
            fontWeight: '800',
            background: 'var(--primary-gradient)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            marginBottom: '0.4rem',
          }}>
            {t.appName || 'Multilingual Cooperative Assistant'}
          </h1>

          <p style={{ color: 'var(--text-secondary)', fontSize: '0.96rem', maxWidth: '520px', margin: '0 auto' }}>
            {step === 1
              ? (t.selectLanguageSubtitle || 'Choose a language to continue accessing cooperative services in your native tongue')
              : 'Create your personalized farmer / member profile to receive tailored PACS and crop scheme advisory'}
          </p>

          {/* Stepper Pill */}
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            marginTop: '1rem',
            padding: '0.3rem 0.85rem',
            borderRadius: '999px',
            background: 'rgba(37, 99, 235, 0.1)',
            color: '#2563eb',
            fontSize: '0.8rem',
            fontWeight: '700',
          }}>
            <span>Step {step} of 2</span>
            <span>•</span>
            <span>{step === 1 ? 'Select Language' : 'Personal Account Profile'}</span>
          </div>
        </div>

        {/* STEP 1: Language Selection */}
        {step === 1 && (
          <div>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))',
              gap: '1rem',
              marginBottom: '2rem',
            }}>
              {LANGUAGES.map((lang) => {
                const isSelected = selectedLang === lang.code;
                return (
                  <button
                    key={lang.code}
                    type="button"
                    onClick={() => onSelectLanguage(lang.code)}
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      padding: '1.1rem 0.85rem',
                      borderRadius: '1rem',
                      background: isSelected ? 'var(--primary-gradient)' : 'var(--bg-card)',
                      border: isSelected ? '2px solid transparent' : '1px solid var(--bg-card-border)',
                      color: isSelected ? '#ffffff' : 'var(--text-primary)',
                      boxShadow: isSelected ? 'var(--shadow-glow)' : 'var(--shadow-sm)',
                      cursor: 'pointer',
                      transform: isSelected ? 'scale(1.03)' : 'scale(1)',
                      transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                      position: 'relative',
                    }}
                  >
                    {isSelected && (
                      <div style={{
                        position: 'absolute',
                        top: '8px',
                        right: '8px',
                        background: 'rgba(255, 255, 255, 0.25)',
                        borderRadius: '50%',
                        padding: '2px',
                        display: 'flex',
                      }}>
                        <Check size={14} color="#fff" />
                      </div>
                    )}
                    <span style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.2rem' }}>
                      {lang.native}
                    </span>
                    <span style={{ fontSize: '0.8rem', opacity: isSelected ? 0.9 : 0.65 }}>
                      {lang.name}
                    </span>
                  </button>
                );
              })}
            </div>

            <div style={{ display: 'flex', justifyContent: 'center' }}>
              <button
                type="button"
                onClick={() => setStep(2)}
                className="btn-primary"
                style={{
                  padding: '0.85rem 2.5rem',
                  fontSize: '1rem',
                  borderRadius: '999px',
                  boxShadow: 'var(--shadow-glow)',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.65rem',
                  fontWeight: '700',
                }}
              >
                <span>Next: Setup Account</span>
                <ArrowRight size={18} />
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: Personal Account Creation */}
        {step === 2 && (
          <form onSubmit={handleFinish} style={{ display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
                Farmer / Member Full Name *
              </label>
              <input
                type="text"
                name="name"
                required
                value={formData.name}
                onChange={handleChange}
                placeholder="e.g. M. Ramasamy / எஸ். முருகன்"
                style={{
                  width: '100%',
                  padding: '0.7rem 0.85rem',
                  borderRadius: '0.75rem',
                  border: '1px solid var(--bg-card-border)',
                  background: 'var(--bg-main)',
                  color: 'var(--text-primary)',
                  fontSize: '0.95rem',
                  outline: 'none',
                }}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
                  Mobile Number
                </label>
                <input
                  type="tel"
                  name="mobile"
                  value={formData.mobile}
                  onChange={handleChange}
                  placeholder="e.g. 9876543210"
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.85rem',
                    borderRadius: '0.75rem',
                    border: '1px solid var(--bg-card-border)',
                    background: 'var(--bg-main)',
                    color: 'var(--text-primary)',
                    fontSize: '0.95rem',
                    outline: 'none',
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
                  Member Category
                </label>
                <select
                  name="memberType"
                  value={formData.memberType}
                  onChange={handleChange}
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.85rem',
                    borderRadius: '0.75rem',
                    border: '1px solid var(--bg-card-border)',
                    background: 'var(--bg-main)',
                    color: 'var(--text-primary)',
                    fontSize: '0.95rem',
                    outline: 'none',
                  }}
                >
                  <option value="Farmer Member">🌾 Farmer Member</option>
                  <option value="PACS Secretary / Staff">🏛️ PACS Secretary / Staff</option>
                  <option value="Cooperative Society Member">🤝 Society Member</option>
                  <option value="General Citizen">👤 General Citizen</option>
                </select>
              </div>
            </div>

            {/* District Selection (Priority: Theni, Madurai, Pudukkottai on Top) */}
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
                Jurisdictional District (Top Priority Districts First)
              </label>
              <select
                name="district"
                value={formData.district}
                onChange={handleChange}
                style={{
                  width: '100%',
                  padding: '0.7rem 0.85rem',
                  borderRadius: '0.75rem',
                  border: '1px solid var(--bg-card-border)',
                  background: 'var(--bg-main)',
                  color: 'var(--text-primary)',
                  fontSize: '0.95rem',
                  outline: 'none',
                  fontWeight: '600',
                }}
              >
                <optgroup label="🌟 Priority Core Districts">
                  <option value="Theni">📍 Theni (தேனி)</option>
                  <option value="Madurai">📍 Madurai (மதுரை)</option>
                  <option value="Pudukkottai">📍 Pudukkottai (புதுக்கோட்டை)</option>
                </optgroup>
                <optgroup label="All Tamil Nadu Districts">
                  {TN_DISTRICTS.filter((d) => !['Theni', 'Madurai', 'Pudukkottai'].includes(d)).map((dist) => (
                    <option key={dist} value={dist}>
                      {dist}
                    </option>
                  ))}
                </optgroup>
              </select>
            </div>

            {/* PACS / Society Name */}
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
                Local PACS Society / Village Name
              </label>
              <input
                type="text"
                name="societyName"
                value={formData.societyName}
                onChange={handleChange}
                placeholder="e.g. Vadipatti Primary Agricultural Credit Society"
                style={{
                  width: '100%',
                  padding: '0.7rem 0.85rem',
                  borderRadius: '0.75rem',
                  border: '1px solid var(--bg-card-border)',
                  background: 'var(--bg-main)',
                  color: 'var(--text-primary)',
                  fontSize: '0.95rem',
                  outline: 'none',
                }}
              />
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.75rem' }}>
              <button
                type="button"
                onClick={() => setStep(1)}
                className="btn-secondary"
                style={{ padding: '0.8rem 1.25rem', borderRadius: '0.75rem' }}
              >
                Back
              </button>

              <button
                type="submit"
                className="btn-primary"
                style={{
                  flex: 1,
                  padding: '0.8rem',
                  borderRadius: '0.75rem',
                  fontWeight: '700',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem',
                }}
              >
                <Sparkles size={16} />
                <span>Create Account & Enter Portal</span>
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
