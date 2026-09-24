import React, { useState, useEffect } from 'react';
import { TRANSLATIONS } from '../translations';
import { X, User, Phone, MapPin, Building, ShieldCheck, CheckCircle2, LogOut, Sparkles } from 'lucide-react';

const TN_DISTRICTS = [
  'Theni', 'Madurai', 'Pudukkottai', 'Coimbatore', 'Thanjavur', 'Dindigul',
  'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Erode', 'Vellore', 'Kanchipuram',
  'Cuddalore', 'Villupuram', 'Tiruppur', 'Ramanathapuram', 'Sivaganga',
  'Virudhunagar', 'Karur', 'Nagapattinam', 'Tiruvarur', 'Krishnagiri',
  'Dharmapuri', 'Namakkal', 'Nilgiris', 'Thoothukudi', 'Kanyakumari',
  'Tiruvallur', 'Tiruvannamalai', 'Ranipet', 'Tenkasi', 'Chengalpattu',
  'Kallakurichi', 'Mayiladuthurai', 'Ariyalur', 'Perambalur', 'Tirupathur', 'Chennai'
];

export default function AccountModal({ langCode, user, onSaveUser, onLogout, onClose }) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;

  const [formData, setFormData] = useState({
    name: user?.name || '',
    mobile: user?.mobile || '',
    district: user?.district || 'Theni',
    societyName: user?.societyName || '',
    memberType: user?.memberType || 'Farmer Member',
    preferredLang: user?.preferredLang || langCode || 'en',
  });

  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.name.trim()) return;

    const updatedUser = {
      ...formData,
      id: user?.id || `MEMBER-${Date.now().toString().slice(-6)}`,
      createdAt: user?.createdAt || new Date().toISOString(),
    };

    localStorage.setItem('coop_portal_user', JSON.stringify(updatedUser));
    onSaveUser(updatedUser);
    setIsSubmitted(true);
    setTimeout(() => {
      setIsSubmitted(false);
      onClose();
    }, 800);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '520px' }}>
        {/* Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--bg-card-border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #2563eb 0%, #10b981 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
            }}>
              <User size={20} />
            </div>
            <div>
              <h2 style={{ fontSize: '1.2rem', fontWeight: '700', color: 'var(--text-primary)', margin: 0 }}>
                {user ? 'Member Account Profile' : 'Create Cooperative Account'}
              </h2>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                Personalized PACS Advisory & Scheme Assistance
              </span>
            </div>
          </div>

          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '0.4rem',
              borderRadius: '0.5rem',
              display: 'flex',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
          {isSubmitted && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.6rem',
              padding: '0.85rem 1rem',
              background: 'rgba(16, 185, 129, 0.12)',
              border: '1px solid #10b981',
              borderRadius: '0.75rem',
              color: '#059669',
              fontWeight: '600',
              fontSize: '0.9rem',
            }}>
              <CheckCircle2 size={18} />
              <span>Account profile saved successfully!</span>
            </div>
          )}

          {/* Full Name */}
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
              Farmer / Member Name *
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                name="name"
                required
                value={formData.name}
                onChange={handleChange}
                placeholder="e.g. M. Ramasamy / எஸ். முருகன்"
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '0.75rem',
                  border: '1px solid var(--bg-card-border)',
                  background: 'var(--bg-main)',
                  color: 'var(--text-primary)',
                  fontSize: '0.95rem',
                  outline: 'none',
                }}
              />
            </div>
          </div>

          {/* Mobile Number & Member Type in 2 columns */}
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
                  padding: '0.65rem 0.85rem',
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
                  padding: '0.65rem 0.85rem',
                  borderRadius: '0.75rem',
                  border: '1px solid var(--bg-card-border)',
                  background: 'var(--bg-main)',
                  color: 'var(--text-primary)',
                  fontSize: '0.95rem',
                  outline: 'none',
                }}
              >
                <option value="Farmer Member">🌾 Farmer Member</option>
                <option value="PACS Secretary / Officer">🏛️ PACS Secretary / Staff</option>
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
                padding: '0.65rem 0.85rem',
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
              Local PACS Society / Village
            </label>
            <input
              type="text"
              name="societyName"
              value={formData.societyName}
              onChange={handleChange}
              placeholder="e.g. Vadipatti Primary Agricultural Credit Society"
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '0.75rem',
                border: '1px solid var(--bg-card-border)',
                background: 'var(--bg-main)',
                color: 'var(--text-primary)',
                fontSize: '0.95rem',
                outline: 'none',
              }}
            />
          </div>

          {/* Action Buttons */}
          <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.75rem' }}>
            <button
              type="submit"
              className="btn-primary"
              style={{
                flex: 1,
                padding: '0.75rem',
                borderRadius: '0.75rem',
                fontWeight: '700',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
              }}
            >
              <Sparkles size={16} />
              <span>{user ? 'Update Profile' : 'Save & Start Session'}</span>
            </button>

            {user && (
              <button
                type="button"
                onClick={() => {
                  localStorage.removeItem('coop_portal_user');
                  onLogout();
                  onClose();
                }}
                className="btn-secondary"
                style={{
                  padding: '0.75rem 1rem',
                  borderRadius: '0.75rem',
                  borderColor: '#ef4444',
                  color: '#ef4444',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                }}
              >
                <LogOut size={16} />
                <span>Sign Out</span>
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
