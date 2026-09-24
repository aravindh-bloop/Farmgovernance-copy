import React from 'react';
import { Globe, Sprout } from 'lucide-react';
import ChatBox from '../../components/ChatBox/ChatBox';
import { useLanguage } from '../../context/LanguageContext';

export default function Chat({ onChangeLanguage, initialQuery = '' }) {
  const { t } = useLanguage();

  return (
    <div className="kiosk-chat-portal">
      <div className="kiosk-chat-shell">
        <div className="kiosk-chat-topbar">
          <div className="kiosk-brand-lockup">
            <div className="kiosk-brand-mark"><Sprout size={20} /></div>
            <div><strong>CoopAssist</strong><span>Voice-first cooperative guidance</span></div>
          </div>
          <span className="kiosk-chat-title">{t('chatTitle')}</span>
          <button onClick={onChangeLanguage} className="change-lang-btn">
            <Globe size={16} />
            {t('changeLanguage')}
          </button>
        </div>
        <div className="kiosk-chat-body">
          <ChatBox initialQuery={initialQuery} />
        </div>
      </div>
    </div>
  );
}
