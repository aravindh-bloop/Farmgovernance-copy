import React, { useState } from 'react';
import {
  Plus,
  MessageSquare,
  Trash2,
  Search,
  User,
  LogOut,
  Settings,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  Bot,
  Sparkles,
  ShieldAlert,
  FileText,
  Building2,
  CreditCard,
  Flame,
} from 'lucide-react';
import { TRANSLATIONS } from '../translations';

/**
 * ChatGPT / Gemini Style Sidebar
 * Features:
 * - New Chat creation
 * - Search chat sessions
 * - Quick Topics / Popular Shortcuts in the side tab
 * - Grouped Recent Queries history (Today, Yesterday, Previous 7 Days, Older)
 * - Load past conversation on click
 * - Delete past conversation
 * - User Personal Profile Card with avatar and account settings at bottom
 */
export default function Sidebar({
  isOpen,
  onToggle,
  sessions,
  currentSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
  onSelectTopic,
  user,
  onOpenAccount,
  langCode,
}) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const [searchQuery, setSearchQuery] = useState('');

  const quickTopics = [
    {
      id: 'grievance',
      icon: <ShieldAlert size={14} color="#ef4444" />,
      label: t.grievanceTitle || 'File Grievance',
      query: {
        en: 'I want to file a grievance regarding PACS membership rejection',
        ta: 'PACS உறுப்பினர் நிராகரிப்பு குறித்து புகார் அளிக்க விரும்புகிறேன்',
        hi: 'मैं PACS सदस्यता अस्वीकृति के संबंध में शिकायत दर्ज करना चाहता हूँ',
      },
    },
    {
      id: 'pmfby',
      icon: <FileText size={14} color="#3b82f6" />,
      label: t.schemeTitle || 'PMFBY Crop Insurance',
      query: {
        en: 'What is the procedure for PMFBY crop insurance claim and 72-hour loss reporting?',
        ta: 'PMFBY பயிர் காப்பீட்டு உரிமை கோரல் மற்றும் 72 மணிநேர அறிக்கை செயல்முறை என்ன?',
        hi: 'PMFBY फसल बीमा दावे और 72 घंटे में फसल क्षति की सूचना की प्रक्रिया क्या है?',
      },
    },
    {
      id: 'pacs_reg',
      icon: <Building2 size={14} color="#10b981" />,
      label: t.registrationTitle || 'PACS Registration',
      query: {
        en: 'What documents are required to register for PACS membership?',
        ta: 'PACS உறுப்பினர் பதிவுக்கு என்ன ஆவணங்கள் தேவை?',
        hi: 'PACS सदस्यता के लिए पंजीकरण करने हेतु कौन से दस्तावेज आवश्यक हैं?',
      },
    },
    {
      id: 'kcc',
      icon: <CreditCard size={14} color="#8b5cf6" />,
      label: t.kccTitle || 'Kisan Credit Card (KCC)',
      query: {
        en: 'How to apply for Kisan Credit Card (KCC) loan with 4% interest subvention?',
        ta: '4% வட்டி மானியத்துடன் கிசான் கிரெடிட் கார்டு (KCC) கடனுக்கு எவ்வாறு விண்ணப்பிப்பது?',
        hi: '4% ब्याज छूट के साथ किसान क्रेडिट कार्ड (KCC) ऋण के लिए कैसे आवेदन करें?',
      },
    },
  ];

  const filteredSessions = sessions.filter((s) =>
    (s.title || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
    (s.preview || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Group sessions by date
  const groupSessionsByDate = (list) => {
    const today = new Date().toDateString();
    const yesterday = new Date(Date.now() - 86400000).toDateString();

    const groups = {
      today: [],
      yesterday: [],
      earlier: [],
    };

    list.forEach((session) => {
      const sessionDate = new Date(session.updatedAt || session.createdAt || Date.now()).toDateString();
      if (sessionDate === today) {
        groups.today.push(session);
      } else if (sessionDate === yesterday) {
        groups.yesterday.push(session);
      } else {
        groups.earlier.push(session);
      }
    });

    return groups;
  };

  const grouped = groupSessionsByDate(filteredSessions);

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="sidebar-backdrop-mobile"
          onClick={onToggle}
          style={{
            display: 'none',
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.4)',
            zIndex: 90,
            backdropFilter: 'blur(4px)',
          }}
        />
      )}

      <aside
        className={`sidebar-container ${isOpen ? 'sidebar-open' : 'sidebar-collapsed'}`}
        style={{
          width: isOpen ? '280px' : '0px',
          minWidth: isOpen ? '280px' : '0px',
          height: '100vh',
          background: 'var(--bg-card)',
          borderRight: isOpen ? '1px solid var(--bg-card-border)' : 'none',
          display: 'flex',
          flexDirection: 'column',
          transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
          overflow: 'hidden',
          position: 'sticky',
          top: 0,
          zIndex: 95,
          boxShadow: isOpen ? 'var(--shadow-md)' : 'none',
        }}
      >
        {/* Top: Branding & New Chat */}
        <div style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem', borderBottom: '1px solid var(--bg-card-border)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                background: 'var(--primary-gradient)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#ffffff',
              }}>
                <Bot size={18} />
              </div>
              <span style={{ fontWeight: '700', fontSize: '0.95rem', color: 'var(--text-primary)', whiteSpace: 'nowrap' }}>
                Cooperative AI
              </span>
            </div>

            <button
              onClick={onToggle}
              title="Close Sidebar"
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-muted)',
                cursor: 'pointer',
                padding: '4px',
                borderRadius: '6px',
                display: 'flex',
              }}
            >
              <ChevronLeft size={18} />
            </button>
          </div>

          {/* ➕ New Chat Button */}
          <button
            onClick={onNewChat}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              width: '100%',
              padding: '0.65rem 1rem',
              borderRadius: '0.75rem',
              border: '1px solid rgba(37, 99, 235, 0.3)',
              background: 'linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%)',
              color: '#2563eb',
              fontWeight: '700',
              fontSize: '0.9rem',
              cursor: 'pointer',
              boxShadow: 'var(--shadow-sm)',
              transition: 'all 0.2s ease',
            }}
          >
            <Plus size={16} />
            <span>New Chat</span>
          </button>

          {/* 🔍 Search Sessions */}
          <div style={{ position: 'relative' }}>
            <Search size={14} color="var(--text-muted)" style={{ position: 'absolute', left: '0.65rem', top: '50%', transform: 'translateY(-50%)' }} />
            <input
              type="text"
              placeholder="Search chats..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '0.45rem 0.65rem 0.45rem 2rem',
                borderRadius: '0.6rem',
                border: '1px solid var(--bg-card-border)',
                background: 'var(--bg-main)',
                color: 'var(--text-primary)',
                fontSize: '0.82rem',
                outline: 'none',
              }}
            />
          </div>
        </div>

        {/* Quick Topics in Side Tab */}
        <div style={{ padding: '0.75rem 0.85rem 0.5rem 0.85rem', borderBottom: '1px solid var(--bg-card-border)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            <Flame size={13} color="#f97316" />
            <span>Popular Topics</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.3rem' }}>
            {quickTopics.map((topic) => (
              <button
                key={topic.id}
                type="button"
                onClick={() => {
                  const queryText = topic.query[langCode] || topic.query.en;
                  onSelectTopic(queryText);
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.4rem 0.6rem',
                  borderRadius: '0.5rem',
                  background: 'var(--bg-main)',
                  border: '1px solid var(--bg-card-border)',
                  color: 'var(--text-primary)',
                  fontSize: '0.8rem',
                  fontWeight: '500',
                  textAlign: 'left',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  overflow: 'hidden',
                  whiteSpace: 'nowrap',
                  textOverflow: 'ellipsis',
                }}
                onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#3b82f6'; e.currentTarget.style.color = '#2563eb'; }}
                onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--bg-card-border)'; e.currentTarget.style.color = 'var(--text-primary)'; }}
              >
                {topic.icon}
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{topic.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Middle: Recent Queries List */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '0.75rem 0.5rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.85rem',
        }}>
          {filteredSessions.length === 0 ? (
            <div style={{
              textAlign: 'center',
              padding: '2rem 1rem',
              color: 'var(--text-muted)',
              fontSize: '0.82rem',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '0.5rem',
            }}>
              <MessageSquare size={24} style={{ opacity: 0.4 }} />
              <span>No chat history yet</span>
              <span style={{ fontSize: '0.75rem', opacity: 0.8 }}>Your queries and verified solutions will appear here</span>
            </div>
          ) : (
            <>
              {grouped.today.length > 0 && (
                <div>
                  <div style={{ fontSize: '0.72rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)', padding: '0 0.5rem 0.35rem 0.5rem', letterSpacing: '0.05em' }}>
                    Today
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                    {grouped.today.map((s) => renderSessionItem(s))}
                  </div>
                </div>
              )}

              {grouped.yesterday.length > 0 && (
                <div>
                  <div style={{ fontSize: '0.72rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)', padding: '0 0.5rem 0.35rem 0.5rem', letterSpacing: '0.05em' }}>
                    Yesterday
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                    {grouped.yesterday.map((s) => renderSessionItem(s))}
                  </div>
                </div>
              )}

              {grouped.earlier.length > 0 && (
                <div>
                  <div style={{ fontSize: '0.72rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)', padding: '0 0.5rem 0.35rem 0.5rem', letterSpacing: '0.05em' }}>
                    Previous 7 Days
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                    {grouped.earlier.map((s) => renderSessionItem(s))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Bottom: User Personal Account Profile Card */}
        <div style={{
          padding: '0.85rem',
          borderTop: '1px solid var(--bg-card-border)',
          background: 'var(--bg-main)',
        }}>
          <div
            onClick={onOpenAccount}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '0.5rem 0.65rem',
              borderRadius: '0.75rem',
              background: 'var(--bg-card)',
              border: '1px solid var(--bg-card-border)',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', overflow: 'hidden' }}>
              <div style={{
                width: '34px',
                height: '34px',
                borderRadius: '50%',
                background: user ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : 'var(--primary-gradient)',
                color: '#fff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: '700',
                fontSize: '0.88rem',
                flexShrink: 0,
              }}>
                {user ? user.name.charAt(0).toUpperCase() : <User size={16} />}
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden', textAlign: 'left' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {user ? user.name : 'Personal Account'}
                </span>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {user ? `${user.district || 'Tamil Nadu'} • ${user.memberType || 'Member'}` : 'Sign in / Create profile'}
                </span>
              </div>
            </div>

            <Settings size={15} color="var(--text-muted)" />
          </div>
        </div>
      </aside>
    </>
  );

  function renderSessionItem(session) {
    const isSelected = session.id === currentSessionId;
    return (
      <div
        key={session.id}
        onClick={() => onSelectSession(session.id)}
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0.55rem 0.75rem',
          borderRadius: '0.6rem',
          background: isSelected ? 'rgba(37, 99, 235, 0.12)' : 'transparent',
          border: isSelected ? '1px solid rgba(37, 99, 235, 0.3)' : '1px solid transparent',
          color: isSelected ? '#2563eb' : 'var(--text-primary)',
          cursor: 'pointer',
          transition: 'all 0.15s ease',
          fontSize: '0.85rem',
          fontWeight: isSelected ? '600' : '400',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.55rem', overflow: 'hidden', flex: 1 }}>
          <MessageSquare size={14} style={{ flexShrink: 0, opacity: isSelected ? 1 : 0.6 }} />
          <span style={{
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
          }}>
            {session.title || 'Cooperative Inquiry'}
          </span>
        </div>

        <button
          onClick={(e) => {
            e.stopPropagation();
            onDeleteSession(session.id);
          }}
          title="Delete Chat"
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '2px 4px',
            borderRadius: '4px',
            opacity: 0.5,
            display: 'flex',
          }}
          onMouseEnter={(e) => { e.currentTarget.style.opacity = '1'; e.currentTarget.style.color = '#ef4444'; }}
          onMouseLeave={(e) => { e.currentTarget.style.opacity = '0.5'; e.currentTarget.style.color = 'var(--text-muted)'; }}
        >
          <Trash2 size={13} />
        </button>
      </div>
    );
  }
}
