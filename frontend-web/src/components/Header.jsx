import React from 'react';
import { TRANSLATIONS, LANGUAGES } from '../translations';
import { Bot, Sun, Moon, HelpCircle, MapPin, Globe, Type, RotateCcw, User, UserCheck, PanelLeft, Plus } from 'lucide-react';

/**
 * Modern Header & Navigation Bar
 * Features app branding, sidebar toggle, personal account profile button,
 * dark mode toggle, text-size toggle, language badge, FAQ & Locator shortcuts.
 */
export default function Header({
  langCode,
  theme,
  onToggleTheme,
  textSize,
  onToggleTextSize,
  onOpenLangModal,
  onOpenFaq,
  onOpenLocator,
  onOpenAccount,
  user,
  onResetChat,
  hasMessages,
  sidebarOpen,
  onToggleSidebar,
}) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const currentLang = LANGUAGES.find((l) => l.code === langCode) || LANGUAGES[0];

  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 80,
      background: 'var(--header-bg)',
      backdropFilter: 'blur(12px)',
      WebkitBackdropFilter: 'blur(12px)',
      borderBottom: '1px solid var(--bg-card-border)',
      padding: '0.75rem 1.25rem',
      boxShadow: 'var(--shadow-sm)',
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '0.75rem',
      }}>
        {/* Left: Sidebar Toggle & Branding */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {/* Sidebar Toggle Button */}
          <button
            onClick={onToggleSidebar}
            title={sidebarOpen ? 'Collapse Recent Chats' : 'Open Recent Chats'}
            style={{
              background: sidebarOpen ? 'rgba(37, 99, 235, 0.12)' : 'var(--bg-card)',
              border: '1px solid var(--bg-card-border)',
              color: sidebarOpen ? '#2563eb' : 'var(--text-primary)',
              padding: '0.45rem',
              borderRadius: '0.6rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.2s ease',
            }}
          >
            <PanelLeft size={19} />
          </button>

          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '0.75rem',
            background: 'var(--primary-gradient)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#ffffff',
            boxShadow: 'var(--shadow-glow)',
          }}>
            <Bot size={22} />
          </div>

          <div>
            <h1 style={{
              fontSize: '1.15rem',
              fontWeight: '700',
              lineHeight: '1.2',
              color: 'var(--text-primary)',
              letterSpacing: '-0.01em',
              margin: 0,
            }}>
              {t.appName}
            </h1>
            <span style={{
              fontSize: '0.72rem',
              color: 'var(--text-muted)',
              fontWeight: '500',
              display: 'block',
            }}>
              {t.tagline}
            </span>
          </div>
        </div>

        {/* Right Controls Area */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          flexWrap: 'wrap',
        }}>
          {/* New Chat Reset Button */}
          <button
            onClick={onResetChat}
            className="btn-secondary"
            title={t.newChat}
            style={{ padding: '0.45rem 0.8rem', fontSize: '0.82rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}
          >
            <Plus size={15} color="#2563eb" />
            <span className="hide-mobile">New Chat</span>
          </button>

          {/* User Account / Profile Button */}
          <button
            onClick={onOpenAccount}
            className="btn-secondary"
            title={user ? 'View Member Account Profile' : 'Create Member Account'}
            style={{
              padding: '0.45rem 0.8rem',
              fontSize: '0.82rem',
              borderColor: user ? 'rgba(16, 185, 129, 0.4)' : 'rgba(37, 99, 235, 0.4)',
              background: user ? 'rgba(16, 185, 129, 0.08)' : 'rgba(37, 99, 235, 0.08)',
              color: user ? '#059669' : '#2563eb',
              fontWeight: '600',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
            }}
          >
            {user ? <UserCheck size={15} color="#10b981" /> : <User size={15} color="#2563eb" />}
            <span>{user ? `${user.name.split(' ')[0]} (${user.district || 'Member'})` : 'Account'}</span>
          </button>

          {/* FAQ Modal Trigger */}
          <button
            onClick={onOpenFaq}
            className="btn-secondary"
            title={t.faq}
            style={{ padding: '0.45rem 0.75rem', fontSize: '0.82rem' }}
          >
            <HelpCircle size={16} color="#3b82f6" />
            <span className="hide-mobile">{t.faq}</span>
          </button>

          {/* Office Locator Trigger */}
          <button
            onClick={onOpenLocator}
            className="btn-secondary"
            title={t.locator}
            style={{ padding: '0.45rem 0.75rem', fontSize: '0.82rem' }}
          >
            <MapPin size={16} color="#10b981" />
            <span className="hide-mobile">{t.locator}</span>
          </button>

          {/* Language Selector Modal Button */}
          <button
            onClick={onOpenLangModal}
            className="btn-secondary"
            title={t.changeLang}
            style={{
              padding: '0.45rem 0.75rem',
              fontSize: '0.82rem',
              borderColor: 'rgba(59, 130, 246, 0.4)',
              background: 'rgba(59, 130, 246, 0.08)',
            }}
          >
            <Globe size={15} color="#3b82f6" />
            <span style={{ fontWeight: '600' }}>{currentLang.native}</span>
          </button>

          {/* Text-Size Toggle (Normal / Large) */}
          <button
            onClick={onToggleTextSize}
            className="btn-secondary"
            title={textSize === 'large' ? t.textSizeNormal : t.textSizeLarge}
            style={{ padding: '0.45rem 0.65rem' }}
          >
            <Type size={15} />
            <span style={{ fontSize: '0.72rem', fontWeight: '700' }}>
              {textSize === 'large' ? 'A+' : 'A'}
            </span>
          </button>

          {/* Dark / Light Theme Toggle */}
          <button
            onClick={onToggleTheme}
            className="btn-secondary"
            title={theme === 'dark' ? t.themeLight : t.themeDark}
            style={{ padding: '0.45rem 0.65rem' }}
          >
            {theme === 'dark' ? (
              <Sun size={16} color="#fbbf24" />
            ) : (
              <Moon size={16} color="#6366f1" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
