import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Volume2, Pause, Play, Loader2, Globe, ChevronLeft, ChevronRight } from 'lucide-react';
import { sendTextQuery, sendVoiceQuery, fetchTTSAudio } from '../../services/api';
import { useLanguage } from '../../context/LanguageContext';
import VoiceInput from '../VoiceInput/VoiceInput';
import OfficerRecommendationCard from '../OfficerRecommendationCard/OfficerRecommendationCard';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { formatStepsLineByLine } from '../../utils/formatSteps';

const SLIDING_LANGUAGES = [
  { code: 'en', name: 'English', native: 'English' },
  { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
  { code: 'hi', name: 'Hindi', native: 'हिन्दी' },
  { code: 'te', name: 'Telugu', native: 'తెలుగు' },
  { code: 'mr', name: 'Marathi', native: 'मराठी' },
  { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
  { code: 'bn', name: 'Bengali', native: 'বাংলা' },
  { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
  { code: 'ml', name: 'Malayalam', native: 'മലയാളം' },
  { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
  { code: 'or', name: 'Odia', native: 'ଓଡ଼ିଆ' },
];

export default function ChatBox({ initialQuery = '' }) {
  const { language, setLanguage, t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [audioState, setAudioState] = useState({ messageId: null, status: 'idle' });
  const currentAudioRef = useRef(null);
  const messagesEndRef = useRef(null);
  const sliderRef = useRef(null);

  const scrollSlider = (direction) => {
    if (sliderRef.current) {
      const amount = direction === 'left' ? -180 : 180;
      sliderRef.current.scrollBy({ left: amount, behavior: 'smooth' });
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Clean up audio on unmount
  useEffect(() => {
    return () => {
      if (currentAudioRef.current) {
        currentAudioRef.current.pause();
        currentAudioRef.current = null;
      }
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const stopCurrentAudio = () => {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      currentAudioRef.current = null;
    }
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setAudioState({ messageId: null, status: 'idle' });
  };

  const detectScriptLanguage = (str) => {
    if (!str) return language || 'en';
    if (/[\u0B80-\u0BFF]/.test(str)) return 'ta'; // Tamil
    if (/[\u0900-\u097F]/.test(str)) return 'hi'; // Hindi
    if (/[\u0C00-\u0C7F]/.test(str)) return 'te'; // Telugu
    if (/[\u0C80-\u0CFF]/.test(str)) return 'kn'; // Kannada
    if (/[\u0D00-\u0D7F]/.test(str)) return 'ml'; // Malayalam
    if (/[\u0980-\u09FF]/.test(str)) return 'bn'; // Bengali
    if (/[\u0A80-\u0AFF]/.test(str)) return 'gu'; // Gujarati
    if (/[\u0A00-\u0A7F]/.test(str)) return 'pa'; // Punjabi
    return language || 'en';
  };

  const playAssistantSpeech = async (messageId, text, langCode) => {
    stopCurrentAudio();
    if (!text) return;

    // Prefer the user's chosen language for neural TTS; only sniff the script
    // when the choice is English (e.g. auto-detected answers). This stops
    // Devanagari answers (hi/mr) always being read as Hindi.
    const effectiveLang =
      langCode && langCode !== 'en' ? langCode : detectScriptLanguage(text) || language || 'en';
    setAudioState({ messageId, status: 'loading' });

    // Safety guard: never allow the "Generating Voice..." spinner to hang forever.
    setTimeout(() => {
      setAudioState((prev) =>
        prev.messageId === messageId && prev.status === 'loading'
          ? { messageId: null, status: 'idle' }
          : prev
      );
    }, 18000);

    // Strip markdown/emoji and cap length so the neural TTS is fast & natural.
    const speakText = text
      .replace(/[#*`📌⚠️🏛️🌾⚖️💳🛡️💊🚜📲🏗️💻🧮📊🔒•]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 230);

    try {
      // 1. Try Backend TTS Engine (/chat/tts) with clean spoken text
      const audioUrl = await fetchTTSAudio(speakText, effectiveLang);
      if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.playbackRate = 1.0;
        currentAudioRef.current = audio;

        audio.onplay = () => setAudioState({ messageId, status: 'playing' });
        audio.onpause = () => {
          if (audio.currentTime < audio.duration) {
            setAudioState({ messageId, status: 'paused' });
          }
        };
        audio.onended = () => {
          setAudioState({ messageId: null, status: 'idle' });
          currentAudioRef.current = null;
        };
        audio.onerror = () => {
          fallbackSpeechSynthesis(messageId, speakText, effectiveLang);
        };

        try {
          await audio.play();
          return;
        } catch (playErr) {
          console.warn('Audio play failed, falling back to Web Speech:', playErr);
          fallbackSpeechSynthesis(messageId, speakText, effectiveLang);
          return;
        }
      }
    } catch (err) {
      console.warn('Backend audio play error, falling back to Web Speech:', err);
    }

    // Fallback: Web Speech API
    fallbackSpeechSynthesis(messageId, speakText, effectiveLang);
  };

  const getVoiceForLanguage = (code) => {
    if (!window.speechSynthesis) return null;
    const voices = window.speechSynthesis.getVoices();
    if (!voices || voices.length === 0) return null;

    const prefix = (code || 'en').toLowerCase().split('-')[0];

    // 1. Direct language code match (e.g. 'ta-IN', 'ta_IN', 'ta')
    let match = voices.find(
      (v) => v.lang.toLowerCase().startsWith(prefix) || v.lang.toLowerCase().includes(prefix)
    );

    // 2. Keyword match by voice name
    if (!match) {
      const nameKeywords = {
        ta: ['tamil', 'தமிழ்', 'valluvar', 'pallavi'],
        hi: ['hindi', 'हिन्दी', 'swara', 'madhur', 'kalpana', 'hemant'],
        te: ['telugu', 'తెలుగు', 'mohan', 'shruti'],
        kn: ['kannada', 'ಕನ್ನಡ', 'gagan', 'sapna'],
        ml: ['malayalam', 'മലയാളം', 'midhun', 'sobhana'],
        mr: ['marathi', 'मராठी', 'aarohi', 'manohar'],
        bn: ['bengali', 'বাংলা', 'bashkar', 'tanishaa'],
        gu: ['gujarati', 'ગુજરાતી', 'niranjan', 'dhwani'],
        pa: ['punjabi', 'ਪੰਜਾਬੀ', 'rajan'],
        en: ['english', 'india', 'en-in', 'natural'],
      };
      const kws = nameKeywords[prefix] || [];
      match = voices.find((v) => kws.some((kw) => v.name.toLowerCase().includes(kw)));
    }

    // 3. For Indic text, do not fall back to British/American voice if no native voice found
    return match || null;
  };

  const fallbackSpeechSynthesis = (messageId, text, langCode) => {
    if (!('speechSynthesis' in window)) {
      setAudioState({ messageId: null, status: 'idle' });
      return;
    }
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[#*`📌⚠️🏛️🌾⚖️💳🛡️💊🚜📲🏗️💻🧮📊🔒•]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(cleanText);

    const langLocales = {
      en: 'en-IN',
      hi: 'hi-IN',
      ta: 'ta-IN',
      te: 'te-IN',
      mr: 'mr-IN',
      kn: 'kn-IN',
      bn: 'bn-IN',
      gu: 'gu-IN',
      ml: 'ml-IN',
      pa: 'pa-IN',
    };

    const targetLang = langCode || language;
    const targetLocale = langLocales[targetLang] || 'en-IN';
    const chosenVoice = getVoiceForLanguage(targetLang);

    if (chosenVoice) {
      utterance.voice = chosenVoice;
      utterance.lang = chosenVoice.lang;
    } else {
      if (targetLang !== 'en') {
        // Skip British fallback if no native Indic voice installed
        setAudioState({ messageId: null, status: 'idle' });
        return;
      }
      utterance.lang = targetLocale;
    }

    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    utterance.onstart = () => setAudioState({ messageId, status: 'playing' });
    utterance.onend = () => setAudioState({ messageId: null, status: 'idle' });
    utterance.onerror = () => setAudioState({ messageId: null, status: 'idle' });

    window.speechSynthesis.speak(utterance);
  };

  const toggleSpeech = (messageId, text) => {
    if (audioState.messageId === messageId && audioState.status === 'playing') {
      if (currentAudioRef.current) {
        currentAudioRef.current.pause();
      } else if (window.speechSynthesis) {
        window.speechSynthesis.pause();
      }
      setAudioState({ messageId, status: 'paused' });
    } else if (audioState.messageId === messageId && audioState.status === 'paused') {
      if (currentAudioRef.current) {
        currentAudioRef.current.play();
      } else if (window.speechSynthesis) {
        window.speechSynthesis.resume();
      }
      setAudioState({ messageId, status: 'playing' });
    } else {
      playAssistantSpeech(messageId, text, language);
    }
  };

  const addAssistantMessage = (response) => {
    const newMsgId = Date.now() + 1;
    setMessages((prev) => [
      ...prev,
      {
        id: newMsgId,
        sender: 'ai',
        text: response.answer,
        responseType: response.responseType || response.domain,
        officerRecommendation: response.recommended_officer || response.officerRecommendation,
        citations: response.citations || [],
        verificationStatus: response.verificationStatus,
        trustScore: response.trustScore || 0.98,
        activeDomains: response.activeDomains || [response.domain || 'general'],
        verifiedFacts: response.verifiedFacts || [],
        sourceAuthority: response.sourceAuthority,
      },
    ]);

    // Auto-start with voice speech on output
    if (response.answer) {
      setTimeout(() => {
        playAssistantSpeech(newMsgId, response.answer, language);
      }, 100);
    }
  };

  const handleTextSend = async (text) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    stopCurrentAudio();
    setMessages((prev) => [
      ...prev,
      { id: Date.now(), sender: 'user', text: trimmed, isVoice: false },
    ]);
    setInputQuery('');
    setIsLoading(true);

    try {
      const response = await sendTextQuery(trimmed, language);
      addAssistantMessage(response);
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'ai', text: t('errorMessage') },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (initialQuery) {
      handleTextSend(initialQuery);
    }
  }, [initialQuery]);

  const handleVoiceInput = async (audioBlob, transcriptText) => {
    if (isLoading) return;

    stopCurrentAudio();
    setIsLoading(true);

    const spokenText = transcriptText ? transcriptText.trim() : '';

    try {
      if (spokenText) {
        // User spoke and Web Speech API captured text -> send directly to unified pipeline
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            sender: 'user',
            text: `🎙️ "${spokenText}"`,
            isVoice: true,
            showTranscriptLabel: true,
          },
        ]);

        const response = await sendTextQuery(spokenText, language);
        addAssistantMessage(response);
      } else if (audioBlob) {
        // Fallback for audio blob without browser transcript
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            sender: 'user',
            text: '🎙️ Audio query recording...',
            isVoice: true,
            showTranscriptLabel: true,
          },
        ]);

        const response = await sendVoiceQuery(audioBlob, language, spokenText);
        if (response.transcription) {
          setMessages((prev) =>
            prev.map((m) =>
              m.isVoice && m.text === '🎙️ Audio query recording...'
                ? { ...m, text: `🎙️ "${response.transcription}"` }
                : m
            )
          );
        }
        addAssistantMessage(response);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            sender: 'ai',
            text: language === 'hi' 
              ? 'कोई आवाज़ रिकॉर्ड नहीं हुई। कृपया माइक बटन दबाकर बोलें या नीचे प्रश्न लिखें।'
              : language === 'ta'
              ? 'குரல் பதிவு எதுவும் கிடைக்கவில்லை. தயவுசெய்து மைக்கை அழுத்திப் பேசவும் அல்லது தட்டச்சு செய்யவும்.'
              : 'No audio was recorded. Please press the microphone button to speak or type your question in the text box.',
          },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'ai', text: t('errorMessage') },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-header-icon">
          <Bot size={22} />
        </div>
        <h2>{t('chatTitle')}</h2>
      </div>

      {/* Horizontal Sliding Language Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        background: '#f1f5f9',
        padding: '6px 10px',
        borderRadius: '10px',
        margin: '0 16px 12px 16px',
        border: '1px solid #e2e8f0',
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          fontSize: '12px',
          fontWeight: '700',
          color: '#64748b',
          paddingRight: '6px',
          borderRight: '1px solid #cbd5e1',
          whiteSpace: 'nowrap',
        }}>
          <Globe size={13} color="#2563eb" />
          <span>Lang:</span>
        </div>

        <button
          type="button"
          onClick={() => scrollSlider('left')}
          style={{ background: 'transparent', border: 'none', cursor: 'pointer', padding: '2px', display: 'flex', color: '#64748b' }}
        >
          <ChevronLeft size={16} />
        </button>

        <div
          ref={sliderRef}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            overflowX: 'auto',
            scrollBehavior: 'smooth',
            scrollbarWidth: 'none',
            msOverflowStyle: 'none',
            flex: 1,
            padding: '2px 0',
          }}
        >
          {SLIDING_LANGUAGES.map((lang) => {
            const isActive = lang.code === (language || 'en');
            return (
              <button
                key={lang.code}
                type="button"
                onClick={() => setLanguage(lang.code)}
                style={{
                  padding: '3px 10px',
                  borderRadius: '999px',
                  fontSize: '12px',
                  fontWeight: isActive ? '700' : '500',
                  border: isActive ? '1.5px solid #2563eb' : '1px solid #cbd5e1',
                  background: isActive ? '#2563eb' : '#ffffff',
                  color: isActive ? '#ffffff' : '#1e293b',
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                  boxShadow: isActive ? '0 2px 6px rgba(37, 99, 235, 0.25)' : 'none',
                  transition: 'all 0.15s ease',
                  flexShrink: 0,
                }}
              >
                {lang.native} ({lang.code.toUpperCase()})
              </button>
            );
          })}
        </div>

        <button
          type="button"
          onClick={() => scrollSlider('right')}
          style={{ background: 'transparent', border: 'none', cursor: 'pointer', padding: '2px', display: 'flex', color: '#64748b' }}
        >
          <ChevronRight size={16} />
        </button>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <p className="chat-empty-hint">{t('welcomeMessage')}</p>
        )}

        {messages.map((msg) => {
          const isUser = msg.sender === 'user';
          const isCurrentAudio = audioState.messageId === msg.id;
          const isPlaying = isCurrentAudio && audioState.status === 'playing';
          const isPaused = isCurrentAudio && audioState.status === 'paused';
          const isAudioLoading = isCurrentAudio && audioState.status === 'loading';

          return (
            <div key={msg.id} className={`chat-row ${isUser ? 'chat-row-user' : 'chat-row-ai'}`}>
              <div className={`chat-avatar ${isUser ? 'chat-avatar-user' : 'chat-avatar-ai'}`}>
                {isUser ? <User size={16} /> : <Bot size={16} />}
              </div>
              <div className="chat-bubble-wrap">
                {isUser && msg.showTranscriptLabel && (
                  <span className="transcript-label">{t('youSaid')}</span>
                )}
                <div
                  className={`chat-bubble ${isUser ? 'chat-bubble-user' : 'chat-bubble-ai'}`}
                  style={msg.isVoice ? { fontStyle: 'italic', opacity: 0.9 } : undefined}
                >
                  {/* Meta Bar for AI: Active Subdomains & Database Verification Status */}
                  {!isUser && (
                    <div className="chat-meta-bar">
                      {msg.activeDomains && msg.activeDomains.map((dom, idx) => (
                        <span
                          key={idx}
                          className={`chat-domain-pill ${dom.includes('pmfby') ? 'pmfby' : dom.includes('grievance') ? 'grievance' : 'scheme'}`}
                        >
                          {dom === 'pacs_pmfby' ? '🌾 PACS + PMFBY' : dom === 'grievance' ? '⚖️ Grievance' : dom === 'cooperative_law' ? '🏛️ MSCS Law' : dom === 'financial_literacy' ? '💳 KCC 4%' : '📜 Farmer Scheme'}
                        </span>
                      ))}
                      {msg.verificationStatus && (
                        <span className="chat-trust-badge">
                          🛡️ {Math.round((msg.trustScore || 0.98) * 100)}% Verified Accuracy
                        </span>
                      )}
                    </div>
                  )}

                  {isUser ? msg.text : <ReactMarkdown remarkPlugins={[remarkGfm]}>{formatStepsLineByLine(msg.text)}</ReactMarkdown>}

                  {/* Verified Statutory Citations */}
                  {!isUser && msg.citations && msg.citations.length > 0 && (
                    <div className="chat-citations-card">
                      <div className="chat-citations-title">
                        <span>🏛️ Official Sources & Statutory Citations:</span>
                      </div>
                      <ul className="chat-citations-list">
                        {msg.citations.slice(0, 3).map((cit, cIdx) => (
                          <li key={cIdx}>{cit}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Speech Voice Output Controls on Assistant Responses */}
                  {!isUser && msg.text && (
                    <div className="chat-audio-controls">
                      <button
                        type="button"
                        onClick={() => toggleSpeech(msg.id, msg.text)}
                        className={`chat-audio-btn ${isPlaying ? 'playing' : ''} ${isAudioLoading ? 'loading' : ''}`}
                        title={isPlaying ? 'Pause Voice' : isPaused ? 'Resume Voice' : 'Listen with Voice'}
                      >
                        {isAudioLoading ? (
                          <>
                            <Loader2 size={14} className="animate-spin" />
                            <span>Loading Voice...</span>
                          </>
                        ) : isPlaying ? (
                          <>
                            <Pause size={14} />
                            <span>Pause Voice</span>
                            <span className="audio-wave-anim">
                              <span className="audio-wave-bar" />
                              <span className="audio-wave-bar" />
                              <span className="audio-wave-bar" />
                            </span>
                          </>
                        ) : isPaused ? (
                          <>
                            <Play size={14} />
                            <span>Resume Voice</span>
                          </>
                        ) : (
                          <>
                            <Volume2 size={14} />
                            <span>Listen (Normal Speed)</span>
                          </>
                        )}
                      </button>
                    </div>
                  )}
                </div>
                {!isUser && msg.officerRecommendation && (
                  <OfficerRecommendationCard officer={msg.officerRecommendation} />
                )}
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="chat-row chat-row-ai">
            <div className="chat-avatar chat-avatar-ai">
              <Bot size={16} />
            </div>
            <div className="typing-indicator">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-text">{t('assistantTyping')}</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form
        className="chat-input-bar"
        onSubmit={(e) => {
          e.preventDefault();
          handleTextSend(inputQuery);
        }}
      >
        <VoiceInput onVoiceResult={handleVoiceInput} disabled={isLoading} />

        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          placeholder={t('askPlaceholder')}
          disabled={isLoading}
          className="chat-text-input"
        />

        <button
          type="submit"
          disabled={!inputQuery.trim() || isLoading}
          className="kiosk-btn kiosk-btn-primary chat-send-btn"
        >
          <Send size={18} />
          <span>{t('send')}</span>
        </button>
      </form>
    </div>
  );
}
