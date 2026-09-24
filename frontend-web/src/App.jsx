import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import LanguageSelectionScreen from './components/LanguageSelectionScreen';
import ChatInterface from './components/ChatInterface';
import FaqModal from './components/FaqModal';
import OfficeLocatorModal from './components/OfficeLocatorModal';
import AccountModal from './components/AccountModal';
import { sendTextQuery, sendVoiceQuery } from './services/api';
import { downloadConversationPDF } from './utils/pdfExport';
import { TRANSLATIONS } from './translations';

const SESSIONS_STORAGE_KEY = 'coop_chat_sessions';
const USER_STORAGE_KEY = 'coop_portal_user';

/**
 * Multilingual Cooperative Assistant — Web Frontend Root App
 * 
 * Layout Architecture:
 * - Left: ChatGPT / Gemini Collapsible Sidebar with New Chat, Search, Popular Topics, and Chat History
 * - Center: ONLY the Chat Interface taking full vertical screen cleanly
 * - First Time: Onboarding asks for Language Selection + Personal Account Registration
 */
export default function App() {
  // User Personal Account State
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem(USER_STORAGE_KEY);
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  // Session & Preferences State
  const [langCode, setLangCode] = useState(() => user?.preferredLang || 'en');
  const [showOnboarding, setShowOnboarding] = useState(() => !user);
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('coop_theme') || 'light';
    } catch {
      return 'light';
    }
  });
  const [textSize, setTextSize] = useState('normal');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Modal Visibility State
  const [activeModal, setActiveModal] = useState(null); // 'lang', 'faq', 'locator', 'account' or null

  // Chat History / Sessions State
  const [sessions, setSessions] = useState(() => {
    try {
      const saved = localStorage.getItem(SESSIONS_STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [currentSessionId, setCurrentSessionId] = useState(() => `session-${Date.now()}`);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Sync theme & text-size attributes to document root and localStorage
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('coop_theme', theme);
    } catch (e) {
      console.error(e);
    }
  }, [theme]);

  useEffect(() => {
    document.documentElement.setAttribute('data-text-size', textSize);
  }, [textSize]);

  // Persist chat sessions to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(SESSIONS_STORAGE_KEY, JSON.stringify(sessions));
    } catch (e) {
      console.error('Error saving sessions:', e);
    }
  }, [sessions]);

  // Handlers
  const handleSelectLanguage = (code) => {
    setLangCode(code);
  };

  const handleCompleteOnboarding = (newUser) => {
    setUser(newUser);
    if (newUser.preferredLang) {
      setLangCode(newUser.preferredLang);
    }
    setShowOnboarding(false);
  };

  const handleToggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const handleToggleTextSize = () => {
    setTextSize((prev) => (prev === 'normal' ? 'large' : 'normal'));
  };

  const handleToggleSidebar = () => {
    setSidebarOpen((prev) => !prev);
  };

  const handleSaveUser = (updatedUser) => {
    setUser(updatedUser);
    if (updatedUser.preferredLang) {
      setLangCode(updatedUser.preferredLang);
    }
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem(USER_STORAGE_KEY);
    setShowOnboarding(true);
  };

  // Helper to save / update current session
  const saveCurrentSession = (newMessages) => {
    if (!newMessages || newMessages.length === 0) return;

    const firstUserMsg = newMessages.find((m) => m.sender === 'user');
    const title = firstUserMsg ? firstUserMsg.text.slice(0, 36) + (firstUserMsg.text.length > 36 ? '...' : '') : 'Cooperative Inquiry';
    const preview = newMessages[newMessages.length - 1]?.text?.slice(0, 60) || '';

    setSessions((prev) => {
      const existingIdx = prev.findIndex((s) => s.id === currentSessionId);
      const sessionObj = {
        id: currentSessionId,
        title,
        preview,
        messages: newMessages,
        updatedAt: Date.now(),
        createdAt: existingIdx >= 0 ? prev[existingIdx].createdAt : Date.now(),
      };

      if (existingIdx >= 0) {
        const updated = [...prev];
        updated[existingIdx] = sessionObj;
        return updated;
      }
      return [sessionObj, ...prev];
    });
  };

  const handleNewChat = () => {
    const newId = `session-${Date.now()}`;
    setCurrentSessionId(newId);
    setMessages([]);
    setInputText('');
  };

  const handleSelectSession = (sessionId) => {
    const session = sessions.find((s) => s.id === sessionId);
    if (session) {
      setCurrentSessionId(session.id);
      setMessages(session.messages || []);
      setInputText('');
    }
  };

  const handleDeleteSession = (sessionId) => {
    setSessions((prev) => prev.filter((s) => s.id !== sessionId));
    if (currentSessionId === sessionId) {
      handleNewChat();
    }
  };

  const handleSendMessage = async (text) => {
    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text,
      isVoice: false,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setIsLoading(true);

    try {
      const res = await sendTextQuery(text, langCode);
      const assistantMsg = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: res.answer,
        responseType: res.responseType,
        officerRecommendation: res.officerRecommendation,
        citations: res.citations || [],
        verifiedFacts: res.verifiedFacts || [],
        trustScore: res.trustScore || 0.98,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      const finalMessages = [...updatedMessages, assistantMsg];
      setMessages(finalMessages);
      saveCurrentSession(finalMessages);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMsg = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: 'An error occurred while connecting to the assistant. Please try again.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      const finalMessages = [...updatedMessages, errorMsg];
      setMessages(finalMessages);
      saveCurrentSession(finalMessages);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendVoice = async (audioBlob, transcript) => {
    const spokenText = transcript ? transcript.trim() : '';

    if (spokenText) {
      const userMsg = {
        id: Date.now(),
        sender: 'user',
        text: spokenText,
        isVoice: true,
        transcription: spokenText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      const updatedMessages = [...messages, userMsg];
      setMessages(updatedMessages);
      setIsLoading(true);

      try {
        const res = await sendTextQuery(spokenText, langCode);
        const assistantMsg = {
          id: Date.now() + 1,
          sender: 'assistant',
          text: res.answer,
          responseType: res.responseType,
          officerRecommendation: res.officerRecommendation,
          citations: res.citations || [],
          verifiedFacts: res.verifiedFacts || [],
          trustScore: res.trustScore || 0.98,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        const finalMessages = [...updatedMessages, assistantMsg];
        setMessages(finalMessages);
        saveCurrentSession(finalMessages);
      } catch (err) {
        console.error('Voice query error:', err);
      } finally {
        setIsLoading(false);
      }
      return;
    }

    setIsLoading(true);
    try {
      const res = await sendVoiceQuery(audioBlob, langCode);
      
      let updatedMessages = messages;
      if (res.transcription) {
        const userMsg = {
          id: Date.now(),
          sender: 'user',
          text: res.transcription,
          isVoice: true,
          transcription: res.transcription,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        updatedMessages = [...messages, userMsg];
        setMessages(updatedMessages);
      }

      const assistantMsg = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: res.answer,
        responseType: res.responseType,
        officerRecommendation: res.officerRecommendation,
        citations: res.citations || [],
        verifiedFacts: res.verifiedFacts || [],
        trustScore: res.trustScore || 0.98,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      const finalMessages = [...updatedMessages, assistantMsg];
      setMessages(finalMessages);
      saveCurrentSession(finalMessages);
    } catch (err) {
      console.error('Voice chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadPdf = () => {
    const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
    downloadConversationPDF(messages, langCode, t.appName);
  };

  // If first visit / not registered, present onboarding language + account setup
  if (showOnboarding) {
    return (
      <LanguageSelectionScreen
        selectedLang={langCode}
        onSelectLanguage={handleSelectLanguage}
        onCompleteOnboarding={handleCompleteOnboarding}
        theme={theme}
        onToggleTheme={handleToggleTheme}
      />
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', background: 'var(--bg-main)' }}>
      {/* 📜 ChatGPT / Gemini Collapsible Recent Queries Sidebar with Popular Topics */}
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={handleToggleSidebar}
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={handleSelectSession}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
        onSelectTopic={handleSendMessage}
        user={user}
        onOpenAccount={() => setActiveModal('account')}
        langCode={langCode}
      />

      {/* Main Content Area: Header on top, ONLY ChatInterface centered */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0, height: '100vh', overflow: 'hidden' }}>
        {/* Header Bar */}
        <Header
          langCode={langCode}
          theme={theme}
          onToggleTheme={handleToggleTheme}
          textSize={textSize}
          onToggleTextSize={handleToggleTextSize}
          onOpenLangModal={() => setActiveModal('lang')}
          onOpenFaq={() => setActiveModal('faq')}
          onOpenLocator={() => setActiveModal('locator')}
          onOpenAccount={() => setActiveModal('account')}
          user={user}
          onResetChat={handleNewChat}
          hasMessages={messages.length > 0}
          sidebarOpen={sidebarOpen}
          onToggleSidebar={handleToggleSidebar}
        />

        {/* Center: ONLY the Chat Interface */}
        <main style={{
          flex: 1,
          maxWidth: '1080px',
          width: '100%',
          margin: '0 auto',
          padding: '1rem',
          display: 'flex',
          flexDirection: 'column',
          height: 'calc(100vh - 65px)',
          overflow: 'hidden',
        }}>
          <div className="glass-panel" style={{
            flex: 1,
            padding: '1.25rem',
            display: 'flex',
            flexDirection: 'column',
            height: '100%',
            overflow: 'hidden',
          }}>
            <ChatInterface
              messages={messages}
              langCode={langCode}
              onSelectLanguage={handleSelectLanguage}
              onSendMessage={handleSendMessage}
              onSendVoice={handleSendVoice}
              isLoading={isLoading}
              onDownloadPdf={handleDownloadPdf}
              inputText={inputText}
              setInputText={setInputText}
            />
          </div>
        </main>
      </div>

      {/* Modals */}
      {activeModal === 'account' && (
        <AccountModal
          langCode={langCode}
          user={user}
          onSaveUser={handleSaveUser}
          onLogout={handleLogout}
          onClose={() => setActiveModal(null)}
        />
      )}

      {activeModal === 'lang' && (
        <div className="modal-overlay" onClick={() => setActiveModal(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '750px' }}>
            <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--bg-card-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h2 style={{ fontSize: '1.15rem', fontWeight: '700' }}>Select Session Language</h2>
              <button onClick={() => setActiveModal(null)} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '1.2rem' }}>✕</button>
            </div>
            <div style={{ padding: '1.5rem' }}>
              <LanguageSelectionScreen
                selectedLang={langCode}
                onSelectLanguage={(code) => {
                  handleSelectLanguage(code);
                  setActiveModal(null);
                }}
                onCompleteOnboarding={(newUser) => {
                  handleCompleteOnboarding(newUser);
                  setActiveModal(null);
                }}
              />
            </div>
          </div>
        </div>
      )}

      {activeModal === 'faq' && (
        <FaqModal
          langCode={langCode}
          onClose={() => setActiveModal(null)}
        />
      )}

      {activeModal === 'locator' && (
        <OfficeLocatorModal
          langCode={langCode}
          onClose={() => setActiveModal(null)}
        />
      )}
    </div>
  );
}
