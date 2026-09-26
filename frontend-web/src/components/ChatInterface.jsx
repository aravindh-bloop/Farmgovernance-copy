import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { TRANSLATIONS, LANGUAGES } from '../translations';
import { formatStepsLineByLine } from '../utils/formatSteps';
import { fetchTTSAudio } from '../services/api';
import {
  Send,
  Mic,
  MicOff,
  Download,
  User,
  Bot,
  PhoneCall,
  Building,
  AlertCircle,
  ShieldCheck,
  Volume2,
  Pause,
  Play,
  Loader2,
  ExternalLink,
  BookOpen,
  Sparkles,
  ChevronLeft,
  ChevronRight,
  Globe,
  Mail,
} from 'lucide-react';

/**
 * Unified ChatGPT-Style Professional Chat Interface
 * Features:
 * 1. Horizontal Sliding Language Selector inside Chat
 * 2. Markdown prose rendering with citations and officer cards
 * 3. Web Speech Recognition STT and browser TTS voice synthesis
 * 4. Hides topic shortcuts once user starts typing or has messages
 */
export default function ChatInterface({
  messages,
  langCode,
  onSelectLanguage,
  onSendMessage,
  onSendVoice,
  isLoading,
  onDownloadPdf,
  inputText,
  setInputText,
}) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const [isRecording, setIsRecording] = useState(false);
  const [audioState, setAudioState] = useState({ messageId: null, status: 'idle' });
  const currentAudioRef = useRef(null);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  const langSliderRef = useRef(null);

  // Auto-scroll to bottom of chat history on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Cleanup speech audio on unmount
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

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!inputText.trim() || isLoading) return;
    onSendMessage(inputText.trim());
    setInputText('');
  };

  const scrollLangSlider = (direction) => {
    if (langSliderRef.current) {
      const amount = direction === 'left' ? -200 : 200;
      langSliderRef.current.scrollBy({ left: amount, behavior: 'smooth' });
    }
  };

  // Web Speech API Voice Recognition
  const handleToggleRecording = () => {
    if (isRecording) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsRecording(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech Recognition is not supported by your browser. Please use Google Chrome or Edge.');
      return;
    }

    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

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

    recognition.lang = langLocales[langCode] || 'en-IN';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsRecording(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setIsRecording(false);
      if (transcript && transcript.trim()) {
        if (onSendVoice) {
          onSendVoice(new Blob(['voice-recorded'], { type: 'audio/webm' }), transcript);
        } else {
          onSendMessage(transcript);
        }
      }
    };

    recognition.onerror = () => {
      setIsRecording(false);
    };

    recognition.onend = () => {
      setIsRecording(false);
    };

    try {
      recognition.start();
    } catch {
      setIsRecording(false);
    }
  };

  // Helper to find best native TTS voice for selected language
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
        mr: ['marathi', 'मराठी', 'aarohi', 'manohar'],
        bn: ['bengali', 'বাংলা', 'bashkar', 'tanishaa'],
        gu: ['gujarati', 'ગુજરાતી', 'niranjan', 'dhwani'],
        pa: ['punjabi', 'ਪੰਜਾਬੀ', 'rajan'],
        en: ['english', 'india', 'en-in', 'natural'],
      };
      const kws = nameKeywords[prefix] || [];
      match = voices.find((v) => kws.some((kw) => v.name.toLowerCase().includes(kw)));
    }

    // 3. Fallback to any Indian accent voice if specific Indic voice not locally installed
    if (!match && prefix !== 'en') {
      match = voices.find((v) => v.lang.includes('IN') || v.name.toLowerCase().includes('india'));
    }

    return match || null;
  };

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

  const fallbackSpeechSynthesis = (messageId, text, code) => {
    if (!window.speechSynthesis) {
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

    const targetLocale = langLocales[code] || 'en-IN';
    const chosenVoice = getVoiceForLanguage(code);

    if (chosenVoice) {
      utterance.voice = chosenVoice;
      utterance.lang = chosenVoice.lang;
    } else {
      utterance.lang = targetLocale;
    }

    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    utterance.onstart = () => setAudioState({ messageId, status: 'playing' });
    utterance.onend = () => setAudioState({ messageId: null, status: 'idle' });
    utterance.onerror = () => setAudioState({ messageId: null, status: 'idle' });

    window.speechSynthesis.speak(utterance);
  };

  const detectScriptLanguage = (str) => {
    if (!str) return langCode || 'en';
    if (/[\u0B80-\u0BFF]/.test(str)) return 'ta'; // Tamil
    if (/[\u0900-\u097F]/.test(str)) return 'hi'; // Hindi
    if (/[\u0C00-\u0C7F]/.test(str)) return 'te'; // Telugu
    if (/[\u0C80-\u0CFF]/.test(str)) return 'kn'; // Kannada
    if (/[\u0D00-\u0D7F]/.test(str)) return 'ml'; // Malayalam
    if (/[\u0980-\u09FF]/.test(str)) return 'bn'; // Bengali
    if (/[\u0A80-\u0AFF]/.test(str)) return 'gu'; // Gujarati
    if (/[\u0A00-\u0A7F]/.test(str)) return 'pa'; // Punjabi
    return langCode || 'en';
  };

  // Pure Native Indic Text-To-Speech Synthesis via Backend Neural Voice Engine
  const toggleSpeech = async (messageId, text) => {
    // 1. If already playing this message -> pause
    if (audioState.messageId === messageId && audioState.status === 'playing') {
      if (currentAudioRef.current) {
        currentAudioRef.current.pause();
      } else if (window.speechSynthesis) {
        window.speechSynthesis.pause();
      }
      setAudioState({ messageId, status: 'paused' });
      return;
    }

    // 2. If paused on this message -> resume
    if (audioState.messageId === messageId && audioState.status === 'paused') {
      if (currentAudioRef.current) {
        currentAudioRef.current.play();
        setAudioState({ messageId, status: 'playing' });
        return;
      } else if (window.speechSynthesis) {
        window.speechSynthesis.resume();
        setAudioState({ messageId, status: 'playing' });
        return;
      }
    }

    // 3. New speech request -> stop previous and fetch native TTS audio
    stopCurrentAudio();
    if (!text) return;

    setAudioState({ messageId, status: 'loading' });

    // Safety guard: never allow the "Generating Voice..." spinner to hang forever.
    setTimeout(() => {
      setAudioState((prev) =>
        prev.messageId === messageId && prev.status === 'loading'
          ? { messageId: null, status: 'idle' }
          : prev
      );
    }, 18000);

    const cleanText = text.replace(/[#*`📌⚠️🏛️🌾⚖️💳🛡️💊🚜📲🏗️💻🧮📊🔒•]/g, '').trim();
    // Prefer the user's chosen language for neural TTS; only sniff the script
    // when the choice is English. This stops Devanagari answers (hi/mr) always
    // being read as Hindi.
    const effectiveLang =
      langCode && langCode !== 'en' ? langCode : detectScriptLanguage(cleanText);
    const speakText = cleanText.slice(0, 230);

    try {
      // Fetch Pure Native Voice from Backend (/api/v1/chat/tts)
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
          console.warn('Backend audio element playback error, falling back to Web Speech');
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

      // If backend TTS did not return audio, fall back directly to Web Speech Synthesis
      fallbackSpeechSynthesis(messageId, speakText, effectiveLang);
    } catch (err) {
      console.warn('Backend TTS playback failed, using Web Speech fallback:', err);
      fallbackSpeechSynthesis(messageId, speakText, effectiveLang);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      overflow: 'hidden',
      position: 'relative',
    }}>
      {/* Horizontal Sliding Language Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.4rem',
        background: 'var(--bg-main)',
        padding: '0.5rem 0.65rem',
        borderRadius: '0.85rem',
        border: '1px solid var(--bg-card-border)',
        marginBottom: '0.85rem',
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.35rem',
          fontSize: '0.78rem',
          fontWeight: '700',
          color: 'var(--text-muted)',
          paddingRight: '0.4rem',
          borderRight: '1px solid var(--bg-card-border)',
          whiteSpace: 'nowrap',
        }}>
          <Globe size={14} color="#3b82f6" />
          <span>Language:</span>
        </div>

        <button
          type="button"
          onClick={() => scrollLangSlider('left')}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '2px',
            display: 'flex',
          }}
        >
          <ChevronLeft size={16} />
        </button>

        {/* Scrollable Language Chips */}
        <div
          ref={langSliderRef}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.45rem',
            overflowX: 'auto',
            scrollBehavior: 'smooth',
            scrollbarWidth: 'none',
            msOverflowStyle: 'none',
            flex: 1,
            padding: '2px 0',
          }}
        >
          {LANGUAGES.map((lang) => {
            const isActive = lang.code === langCode;
            return (
              <button
                key={lang.code}
                type="button"
                onClick={() => onSelectLanguage(lang.code)}
                style={{
                  padding: '0.3rem 0.75rem',
                  borderRadius: '999px',
                  fontSize: '0.82rem',
                  fontWeight: isActive ? '700' : '500',
                  border: isActive ? '1.5px solid #2563eb' : '1px solid var(--bg-card-border)',
                  background: isActive ? 'var(--primary-gradient)' : 'var(--bg-card)',
                  color: isActive ? '#ffffff' : 'var(--text-primary)',
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                  boxShadow: isActive ? '0 2px 8px rgba(37, 99, 235, 0.3)' : 'none',
                  transition: 'all 0.2s ease',
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
          onClick={() => scrollLangSlider('right')}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '2px',
            display: 'flex',
          }}
        >
          <ChevronRight size={16} />
        </button>
      </div>

      {/* Top Action Bar */}
      {messages.length > 0 && (
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          paddingBottom: '0.85rem',
          borderBottom: '1px solid var(--bg-card-border)',
          marginBottom: '1rem',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.35rem',
              fontSize: '0.82rem',
              fontWeight: '600',
              padding: '0.2rem 0.6rem',
              borderRadius: '999px',
              background: 'rgba(16, 185, 129, 0.1)',
              color: '#10b981',
              border: '1px solid rgba(16, 185, 129, 0.25)',
            }}>
              <ShieldCheck size={13} />
              AI Verified Active Session
            </span>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              ({messages.length} {messages.length === 1 ? 'exchange' : 'exchanges'})
            </span>
          </div>

          <button
            onClick={onDownloadPdf}
            className="btn-secondary"
            style={{
              padding: '0.45rem 0.85rem',
              fontSize: '0.82rem',
              borderColor: 'rgba(16, 185, 129, 0.4)',
              color: '#10b981',
              background: 'rgba(16, 185, 129, 0.08)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
            }}
          >
            <Download size={14} color="#10b981" />
            <span>{t.downloadPdf || 'Download PDF'}</span>
          </button>
        </div>
      )}

      {/* Messages Scroll Area */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        paddingRight: '0.5rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '1.25rem',
        marginBottom: '1.25rem',
      }}>
        {messages.length === 0 && (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%',
            minHeight: '260px',
            textAlign: 'center',
            color: 'var(--text-muted)',
            gap: '0.85rem',
          }}>
            <div style={{
              width: '52px',
              height: '52px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, rgba(37,99,235,0.12) 0%, rgba(16,185,129,0.12) 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#2563eb',
            }}>
              <Sparkles size={26} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
                How can I assist your cooperative or farming query today?
              </h3>
              <p style={{ fontSize: '0.88rem', maxWidth: '440px', lineHeight: '1.5' }}>
                Type your question or click the microphone button below. Supports English, தமிழ், हिन्दी, and 11 Indian languages.
              </p>
            </div>
          </div>
        )}

        {messages.map((msg, idx) => {
          const isUser = msg.sender === 'user';
          const isCurrentAudio = audioState.messageId === (msg.id || idx);
          const isPlaying = isCurrentAudio && audioState.status === 'playing';
          const isPaused = isCurrentAudio && audioState.status === 'paused';
          const isAudioLoading = isCurrentAudio && audioState.status === 'loading';

          return (
            <div
              key={msg.id || idx}
              style={{
                display: 'flex',
                justifyContent: isUser ? 'flex-end' : 'flex-start',
                gap: '0.75rem',
                alignItems: 'flex-start',
              }}
            >
              {/* Avatar for Assistant */}
              {!isUser && (
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: 'var(--primary-gradient)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#fff',
                  flexShrink: 0,
                  boxShadow: 'var(--shadow-sm)',
                }}>
                  <Bot size={20} />
                </div>
              )}

              {/* Chat Bubble Container */}
              <div style={{ maxWidth: '85%', minWidth: '260px' }}>
                {/* Voice transcription badge if user spoke */}
                {isUser && msg.isVoice && (
                  <div style={{
                    fontSize: '0.78rem',
                    color: '#2563eb',
                    marginBottom: '0.25rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'flex-end',
                    gap: '0.3rem',
                    fontWeight: '600',
                  }}>
                    <Mic size={12} />
                    <span>Spoken Voice Query</span>
                  </div>
                )}

                {/* Main Bubble Content */}
                <div style={{
                  background: isUser ? 'var(--chat-user-bg)' : 'var(--chat-assistant-bg)',
                  color: isUser ? 'var(--chat-user-text)' : 'var(--chat-assistant-text)',
                  border: isUser ? 'none' : '1px solid var(--chat-assistant-border)',
                  padding: '1.1rem 1.3rem',
                  borderRadius: isUser ? '1.25rem 1.25rem 0.25rem 1.25rem' : '1.25rem 1.25rem 1.25rem 0.25rem',
                  boxShadow: 'var(--shadow-sm)',
                  fontSize: '0.96rem',
                  lineHeight: '1.65',
                  wordBreak: 'break-word',
                }}>
                  {/* Meta Bar for AI: Verified Badges */}
                  {!isUser && (
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      flexWrap: 'wrap',
                      gap: '0.45rem',
                      marginBottom: '0.85rem',
                      paddingBottom: '0.65rem',
                      borderBottom: '1px solid var(--bg-card-border)',
                    }}>
                      <span style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.3rem',
                        fontSize: '0.78rem',
                        fontWeight: '700',
                        padding: '0.2rem 0.55rem',
                        borderRadius: '999px',
                        background: 'rgba(16, 185, 129, 0.12)',
                        color: '#059669',
                        border: '1px solid rgba(16, 185, 129, 0.3)',
                      }}>
                        <ShieldCheck size={13} />
                        100% Verified Accuracy
                      </span>

                      {msg.responseType && (
                        <span style={{
                          fontSize: '0.78rem',
                          fontWeight: '600',
                          padding: '0.2rem 0.55rem',
                          borderRadius: '999px',
                          background: 'rgba(37, 99, 235, 0.1)',
                          color: '#2563eb',
                          border: '1px solid rgba(37, 99, 235, 0.25)',
                        }}>
                          {msg.responseType === 'pacs_pmfby' || msg.responseType === 'scheme_info'
                            ? '🌾 PACS & Crop Advisory'
                            : msg.responseType === 'grievance'
                            ? '⚖️ Grievance Redressal'
                            : msg.responseType === 'cooperative_law'
                            ? '🏛️ Cooperative Law'
                            : msg.responseType === 'financial_literacy'
                            ? '💳 Financial Literacy (KCC)'
                            : '📋 Cooperative Governance'}
                        </span>
                      )}
                    </div>
                  )}

                  {/* Markdown Parsed Output for AI, Text for User */}
                  {isUser ? (
                    <div style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</div>
                  ) : (
                    <div className="markdown-prose">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {formatStepsLineByLine(msg.text || '')}
                      </ReactMarkdown>
                    </div>
                  )}

                  {/* Official Statutory Citations Box */}
                  {!isUser && msg.citations && msg.citations.length > 0 && (
                    <div style={{
                      marginTop: '1rem',
                      padding: '0.75rem 1rem',
                      borderRadius: '0.75rem',
                      background: 'rgba(241, 245, 249, 0.8)',
                      border: '1px solid #cbd5e1',
                      fontSize: '0.84rem',
                    }}>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.4rem',
                        fontWeight: '700',
                        color: '#334155',
                        marginBottom: '0.35rem',
                      }}>
                        <BookOpen size={14} color="#0284c7" />
                        <span>Official Sources & Statutory Citations:</span>
                      </div>
                      <ul style={{ paddingLeft: '1.2rem', margin: 0, color: '#475569', lineHeight: '1.5' }}>
                        {msg.citations.slice(0, 3).map((cit, cIdx) => (
                          <li key={cIdx}>{cit}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Speech Voice Output Controls */}
                  {!isUser && msg.text && (
                    <div style={{ marginTop: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <button
                        type="button"
                        onClick={() => toggleSpeech(msg.id || idx, msg.text)}
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.45rem',
                          padding: '0.4rem 0.85rem',
                          fontSize: '0.82rem',
                          fontWeight: '600',
                          borderRadius: '999px',
                          border: isPlaying ? '1px solid #10b981' : '1px solid #cbd5e1',
                          background: isPlaying ? 'rgba(16, 185, 129, 0.12)' : 'transparent',
                          color: isPlaying ? '#059669' : 'var(--text-secondary)',
                          cursor: 'pointer',
                          transition: 'all 0.2s ease',
                        }}
                      >
                        {isAudioLoading ? (
                          <>
                            <Loader2 size={13} className="animate-spin" />
                            <span>Generating Voice...</span>
                          </>
                        ) : isPlaying ? (
                          <>
                            <Pause size={13} color="#059669" />
                            <span>Pause Voice</span>
                            <span className="audio-wave-anim">
                              <span className="audio-wave-bar" />
                              <span className="audio-wave-bar" />
                              <span className="audio-wave-bar" />
                            </span>
                          </>
                        ) : isPaused ? (
                          <>
                            <Play size={13} />
                            <span>Resume Voice</span>
                          </>
                        ) : (
                          <>
                            <Volume2 size={13} />
                            <span>Listen (Speech Voice)</span>
                          </>
                        )}
                      </button>
                    </div>
                  )}
                </div>

                {/* Officer Recommendation Card */}
                {!isUser && msg.officerRecommendation && (
                  <div style={{
                    marginTop: '0.85rem',
                    background: 'linear-gradient(135deg, rgba(254, 242, 242, 0.95) 0%, rgba(255, 237, 213, 0.95) 100%)',
                    border: '1px solid rgba(239, 68, 68, 0.3)',
                    borderRadius: '1rem',
                    padding: '1.1rem',
                    boxShadow: 'var(--shadow-sm)',
                  }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      color: '#b91c1c',
                      fontWeight: '700',
                      fontSize: '0.88rem',
                      marginBottom: '0.65rem',
                      borderBottom: '1px solid rgba(239, 68, 68, 0.2)',
                      paddingBottom: '0.45rem',
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                        <AlertCircle size={16} />
                        <span>Recommended Jurisdictional Officer</span>
                      </div>
                      <span style={{
                        fontSize: '0.72rem',
                        background: '#ef4444',
                        color: '#fff',
                        padding: '0.15rem 0.5rem',
                        borderRadius: '999px',
                        fontWeight: '600',
                      }}>
                        Direct Escalation
                      </span>
                    </div>

                    <div style={{ fontSize: '0.88rem', color: '#1f2937' }}>
                      <div style={{ fontWeight: '800', fontSize: '1.05rem', color: '#111827', marginBottom: '0.2rem' }}>
                        {msg.officerRecommendation.name}
                      </div>
                      <div style={{ color: '#4b5563', fontWeight: '600', marginBottom: '0.5rem' }}>
                        {msg.officerRecommendation.designation_or_role || msg.officerRecommendation.designation}
                      </div>
                      
                      {(msg.officerRecommendation.place_or_address || msg.officerRecommendation.office || msg.officerRecommendation.department) && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: '#4b5563', fontSize: '0.84rem', marginBottom: '0.35rem' }}>
                          <Building size={14} color="#6b7280" />
                          <span>{msg.officerRecommendation.place_or_address || msg.officerRecommendation.office || msg.officerRecommendation.department}</span>
                        </div>
                      )}

                      {(msg.officerRecommendation.mobile || msg.officerRecommendation.phone || msg.officerRecommendation.landline) && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', marginTop: '0.4rem', color: '#047857', fontWeight: '700', fontSize: '0.92rem' }}>
                          <PhoneCall size={15} color="#059669" />
                          <a
                            href={`tel:${msg.officerRecommendation.mobile || msg.officerRecommendation.phone || msg.officerRecommendation.landline}`}
                            style={{ color: '#059669', textDecoration: 'none' }}
                          >
                            {msg.officerRecommendation.mobile || msg.officerRecommendation.phone || msg.officerRecommendation.landline}
                          </a>
                        </div>
                      )}

                      {msg.officerRecommendation.email && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', marginTop: '0.3rem', color: '#2563eb', fontSize: '0.84rem' }}>
                          <Mail size={14} />
                          <a href={`mailto:${msg.officerRecommendation.email}`} style={{ color: '#2563eb', textDecoration: 'none' }}>
                            {msg.officerRecommendation.email}
                          </a>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Timestamp */}
                <div style={{
                  fontSize: '0.72rem',
                  color: 'var(--text-muted)',
                  marginTop: '0.35rem',
                  textAlign: isUser ? 'right' : 'left',
                }}>
                  {msg.timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>

              {/* Avatar for User */}
              {isUser && (
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: 'var(--accent-gradient)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#fff',
                  flexShrink: 0,
                  boxShadow: 'var(--shadow-sm)',
                }}>
                  <User size={20} />
                </div>
              )}
            </div>
          );
        })}

        {isLoading && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'var(--primary-gradient)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
              flexShrink: 0,
            }}>
              <Bot size={20} />
            </div>
            <div style={{
              background: 'var(--chat-assistant-bg)',
              border: '1px solid var(--chat-assistant-border)',
              padding: '0.75rem 1.1rem',
              borderRadius: '1.25rem 1.25rem 1.25rem 0.25rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              fontSize: '0.88rem',
              color: 'var(--text-secondary)',
            }}>
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span style={{ marginLeft: '0.3rem', fontStyle: 'italic' }}>
                {t.assistantTyping || 'Generating verified legal response...'}
              </span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input Bar */}
      <form
        onSubmit={handleSubmit}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.65rem',
          padding: '0.5rem',
          background: 'var(--bg-card)',
          border: '1px solid var(--bg-card-border)',
          borderRadius: '1rem',
          boxShadow: 'var(--shadow-md)',
        }}
      >
        <button
          type="button"
          onClick={handleToggleRecording}
          title={isRecording ? 'Stop Recording' : 'Speak with Microphone'}
          style={{
            width: '42px',
            height: '42px',
            borderRadius: '50%',
            border: 'none',
            background: isRecording ? '#ef4444' : 'rgba(37, 99, 235, 0.1)',
            color: isRecording ? '#fff' : '#2563eb',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            flexShrink: 0,
            animation: isRecording ? 'pulse 1.5s infinite' : 'none',
          }}
        >
          {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
        </button>

        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={isRecording ? 'Listening... Speak your question now' : (t.typePlaceholder || 'Ask anything about PACS, PMFBY, KCC loans, complaints in any language...')}
          disabled={isLoading}
          style={{
            flex: 1,
            border: 'none',
            outline: 'none',
            background: 'transparent',
            color: 'var(--text-primary)',
            fontSize: '0.96rem',
            padding: '0.5rem 0.25rem',
          }}
        />

        <button
          type="submit"
          disabled={!inputText.trim() || isLoading}
          style={{
            width: '42px',
            height: '42px',
            borderRadius: '50%',
            border: 'none',
            background: inputText.trim() && !isLoading ? 'var(--primary-gradient)' : 'rgba(148, 163, 184, 0.2)',
            color: inputText.trim() && !isLoading ? '#ffffff' : 'var(--text-muted)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: inputText.trim() && !isLoading ? 'pointer' : 'not-allowed',
            transition: 'all 0.2s ease',
            flexShrink: 0,
          }}
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
