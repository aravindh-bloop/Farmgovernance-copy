import React, { useState, useRef } from 'react';
import { Mic, Square } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export default function VoiceInput({ onVoiceResult, disabled }) {
  const { language, t } = useLanguage();
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const recognitionRef = useRef(null);

  const startRecording = async () => {
    setIsRecording(true);
    audioChunksRef.current = [];

    // Map language code to speech recognition locale
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
      or: 'or-IN',
    };

    let transcriptText = '';

    // Try Web Speech API if supported
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      try {
        const recognition = new SpeechRecognition();
        recognition.lang = langLocales[language] || 'en-IN';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = (event) => {
          if (event.results && event.results[0] && event.results[0][0]) {
            transcriptText = event.results[0][0].transcript;
          }
        };
        recognition.onerror = () => {};
        recognition.start();
        recognitionRef.current = recognition;
      } catch (err) {
        console.warn('SpeechRecognition init error:', err);
      }
    }

    // Try MediaStream recording
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
          stream.getTracks().forEach((track) => track.stop());
          if (onVoiceResult) {
            onVoiceResult(audioBlob, transcriptText);
          }
        };

        mediaRecorder.start();
      } else {
        // Fallback for environment without mic hardware
        mediaRecorderRef.current = null;
      }
    } catch (err) {
      console.warn('Microphone access not available or denied:', err);
      mediaRecorderRef.current = null;
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {}
    }

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    } else {
      // Fallback invocation if mediaRecorder wasn't active
      if (onVoiceResult) {
        onVoiceResult(null, '');
      }
    }
  };

  const handleMicClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
      <button
        type="button"
        onClick={handleMicClick}
        disabled={disabled}
        className={`voice-btn ${isRecording ? 'voice-btn-recording' : ''}`}
        aria-label={isRecording ? t('listening') : t('voiceSearch')}
      >
        {isRecording ? <Square size={22} fill="currentColor" /> : <Mic size={22} />}
      </button>
      {isRecording && (
        <div className="recording-indicator">
          <span className="recording-dot" />
          <span className="recording-dot" />
          <span className="recording-dot" />
          <span style={{ fontSize: '11px', color: '#ef4444', fontWeight: '600', marginLeft: '4px' }}>
            {t('listening')}
          </span>
        </div>
      )}
    </div>
  );
}


