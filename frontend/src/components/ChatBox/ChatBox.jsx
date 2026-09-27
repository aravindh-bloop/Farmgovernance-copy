import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Volume2, VolumeX, Pause, Play, Loader2, Globe, ChevronLeft, ChevronRight, MessageCircleQuestion } from 'lucide-react';
import { sendTextQuery, sendVoiceQuery, fetchTTSAudio } from '../../services/api';
import { useLanguage } from '../../context/LanguageContext';
import VoiceInput from '../VoiceInput/VoiceInput';
import OfficerRecommendationCard from '../OfficerRecommendationCard/OfficerRecommendationCard';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { formatStepsLineByLine } from '../../utils/formatSteps';

// The backend picks what to ask next; the wording lives here so the question
// reaches the citizen in the language they are reading.
const FOLLOW_UP_KEYS = {
  steps: 'followUpSteps',
  eligibility: 'followUpEligibility',
  documents: 'followUpDocuments',
  amount: 'followUpAmount',
  contact: 'followUpContact',
};

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

export default function ChatBox({ initialQuery = '', onConversationState, autoListen = false }) {
  const { language, setLanguage, t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [audioState, setAudioState] = useState({ messageId: null, status: 'idle' });
  const currentAudioRef = useRef(null);
  const speechRunRef = useRef(null);
  const audioUnlockedRef = useRef(false);
  // The answer is held back until the voice is ready, then revealed word by word
  // in step with the speech. The citizen reads along instead of watching a
  // finished paragraph appear before anyone has said a word.
  const [revealed, setRevealed] = useState({});
  // Mirror of `revealed` so the reveal helpers can read the current word count
  // without waiting for the next render.
  const revealedRef = useRef({});
  const setRevealCount = (messageId, count) => {
    if (revealedRef.current[messageId] === count) return;
    revealedRef.current = { ...revealedRef.current, [messageId]: count };
    setRevealed(revealedRef.current);
  };
  const revealTimerRef = useRef(null);
  const messagesEndRef = useRef(null);
  const sliderRef = useRef(null);
  const voiceInputRef = useRef(null);

  // One press on the kiosk orb should open the window already listening, so the
  // citizen can just start talking. Only for the empty-orb entry point: a
  // service card already supplies a question to answer.
  //
  // No "already fired" ref here on purpose: StrictMode mounts, unmounts and
  // remounts in development, and a one-shot guard would swallow the timer on
  // the second pass and never start listening. Depending on the prop alone
  // means the effect re-arms itself and fires exactly once per mount.
  useEffect(() => {
    if (!autoListen) return undefined;
    const id = setTimeout(() => voiceInputRef.current?.start(), 260);
    return () => clearTimeout(id);
  }, [autoListen]);

  // Unlock browser autoplay on first interaction so assistant answers can
  // auto-speak on the touch kiosk (Chromium blocks play() until a user gesture).
  useEffect(() => {
    const unlock = () => {
      if (audioUnlockedRef.current) return;
      audioUnlockedRef.current = true;
      try {
        const Ctx = window.AudioContext || window.webkitAudioContext;
        if (Ctx) {
          const ctx = new Ctx();
          ctx.resume();
          const src = ctx.createBufferSource();
          src.buffer = ctx.createBuffer(1, 1, 22050);
          src.connect(ctx.destination);
          src.start(0);
        }
        if (window.speechSynthesis) {
          // The Web Speech fallback is blocked by the same autoplay policy.
          window.speechSynthesis.resume();
        }
      } catch (e) {
        /* audio unlock unsupported — per-message speaker button still works */
      }
    };
    window.addEventListener('pointerdown', unlock, { once: true });
    window.addEventListener('touchstart', unlock, { once: true });
    return () => {
      window.removeEventListener('pointerdown', unlock);
      window.removeEventListener('touchstart', unlock);
    };
  }, []);

  const buildHistory = (msgs) =>
    (msgs || [])
      .filter(
        (m) =>
          m && typeof m.text === 'string' && m.text.trim() &&
          (m.sender === 'user' || m.sender === 'assistant' || m.sender === 'ai')
      )
      .slice(-8)
      .map((m) => ({
        role: m.sender === 'user' ? 'user' : 'assistant',
        content: m.text
          .replace(/^🎙️\s*/, '')
          .replace(/^"|"$/g, '')
          .trim(),
      }))
      .filter((m) => m.content);

  const scrollSlider = (direction) => {
    if (sliderRef.current) {
      const amount = direction === 'left' ? -180 : 180;
      sliderRef.current.scrollBy({ left: amount, behavior: 'smooth' });
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // A voice kiosk has nobody touching the screen while it is being spoken to, so
  // the app-level idle timer would slam the idle screen over a live conversation.
  // Every new turn counts as activity, including the assistant's spoken reply.
  useEffect(() => {
    if (!messages.length) return;
    document.dispatchEvent(new Event('coop:activity'));
  }, [messages.length, isLoading]);

  // Report conversation progress upward so optional after-conversation actions
  // (the E-Report) only appear once the citizen has actually finished talking.
  useEffect(() => {
    if (!onConversationState) return;
    onConversationState({
      isLoading,
      turns: messages
        .filter((m) => m && typeof m.text === 'string' && m.text.trim())
        .map((m) => ({ role: m.sender === 'user' ? 'user' : 'assistant', text: m.text })),
    });
  }, [messages, isLoading, onConversationState]);

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
    if (speechRunRef.current) {
      speechRunRef.current.cancelled = true;
      speechRunRef.current = null;
    }
    if (revealTimerRef.current) {
      clearInterval(revealTimerRef.current);
      revealTimerRef.current = null;
    }
    if (currentAudioRef.current) {
      currentAudioRef.current.onended = null;
      currentAudioRef.current.onerror = null;
      currentAudioRef.current.pause();
      currentAudioRef.current.src = '';
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

  // Progress a message from "no words shown" to "every word shown" across the
  // lifetime of its speech. getProgress returns 0..1 and is driven by the audio
  // clock, or by a timer when we only have the Web Speech fallback.
  // Never let the placeholder flash past in a single frame.
  const REVEAL_FLOOR_MS = 280;

  // options.ceiling  - stop the ramp at this ratio (1 = the whole answer)
  // options.from     - start from this word count instead of rewinding to zero
  // options.isPaused - freeze while the citizen has paused the voice
  const beginReveal = (messageId, text, getProgress, estimatedSeconds, options = {}) => {
    const total = text.split(' ').length;
    if (!total) return;
    const ceiling = Math.max(0, Math.min(1, options.ceiling ?? 1));
    const isPaused = options.isPaused || (() => false);
    const from = Math.max(0, Math.min(total, Number(options.from) || 0));
    const remaining = total - from;
    const startedAt = Date.now();
    // Claim the message at zero words straight away, otherwise the render that
    // flips voiceReady to true lands before the first animation frame and the
    // entire answer flashes on screen for a single frame.
    setRevealCount(messageId, from);
    // If the audio clock stops advancing - a stalled or buffering stream happens
    // on kiosk browsers with poor networks - the words would freeze on screen
    // forever while the voice is still meant to be reading. After STALL_MS
    // without progress, fall back to a wall-clock estimate, and resync to the
    // real clock as soon as it starts moving again.
    const STALL_MS = 1200;
    let lastProgress = 0;
    let lastAdvance = 0;
    const tick = () => {
      // Only throttle during the first REVEAL_FLOOR_MS, so a quick answer cannot
      // snap open, and a long one still tracks the voice afterwards.
      const elapsed = Date.now() - startedAt;
      // A pause the citizen asked for is not a stalled stream: hold the text
      // exactly where it is instead of racing ahead on the wall clock.
      if (isPaused()) {
        lastAdvance = elapsed;
        return;
      }
      const cap = elapsed < REVEAL_FLOOR_MS ? elapsed / REVEAL_FLOOR_MS : 1;
      let progress = getProgress();
      if (progress > lastProgress + 0.0005) {
        lastProgress = progress;
        lastAdvance = elapsed;
      } else if (elapsed - lastAdvance > STALL_MS && estimatedSeconds > 0) {
        // Never let the estimate push past the point the voice will actually
        // reach, or the withheld detail flashes in before the voice finishes.
        progress = Math.max(progress, Math.min(ceiling, elapsed / (estimatedSeconds * 1000)));
        lastProgress = progress;
        lastAdvance = elapsed;
      }
      const ratio = Math.max(0, Math.min(ceiling, Math.min(progress, cap)));
      const count = remaining <= 0
        ? total
        : Math.min(total, from + Math.max(1, Math.ceil(ratio * remaining)));
      setRevealCount(messageId, count);
      if (ratio < ceiling) return;
      clearInterval(revealTimerRef.current);
      revealTimerRef.current = null;
    };
    if (revealTimerRef.current) clearInterval(revealTimerRef.current);
    revealTimerRef.current = setInterval(tick, 60);
  };

  // Fill in whatever the voice chose not to read, over about three quarters of
  // a second, so the screen still ends up with the whole answer.
  const revealRemainder = (messageId, text) => {
    const startedAt = Date.now();
    const span = 750;
    // Continue from the lead the voice already read rather than snapping the
    // text back to zero and re-revealing it.
    beginReveal(messageId, text, () => (Date.now() - startedAt) / span, span / 1000, {
      from: revealedRef.current[messageId] || 0
    });
  };

  const finishReveal = (messageId, text) => {
    if (revealTimerRef.current) {
      clearInterval(revealTimerRef.current);
      revealTimerRef.current = null;
    }
    setRevealCount(messageId, text.split(' ').length);
  };

  // Held-back text: only the words the voice has actually spoken so far.
  const isStillBeingSpoken = (message) => {
    const shown = revealed[message.id];
    return shown !== undefined && shown < message.text.split(' ').length;
  };

  const visibleTextFor = (message) => {
    const shown = revealed[message.id];
    if (shown === undefined) return message.text;
    if (shown >= message.text.split(' ').length) return message.text;
    return message.text.split(' ').slice(0, shown).join(' ');
  };

  // How much of the answer the voice has actually spoken, as 0..1.
  // Prefers the real audio clock; falls back to elapsed time against an
  // estimated speaking length when the duration is not known yet.
  const estimateSpeakSeconds = (text) => Math.max(2, text.split(' ').length / 2.6);

  const revealProgressFor = (audioEl, text) => {
    const estimate = estimateSpeakSeconds(text);
    if (!audioEl) return 0;
    const t = audioEl.currentTime || 0;
    if (Number.isFinite(audioEl.duration) && audioEl.duration > 0) {
      return Math.min(1, t / audioEl.duration);
    }
    if (t > 0) return Math.min(1, t / estimate);
    return 0;
  };

  // ── Speaking a long answer ────────────────────────────────────────────────
  // The voice used to be handed the whole answer at once, which meant waiting
  // for every second of audio to be synthesised before a single word was
  // spoken. It is now handed the answer in sentence-sized pieces: the first
  // piece starts as soon as it lands (roughly a fifth of the reply), and the
  // rest are fetched in the background while the voice is already talking, so
  // the speech runs on without a gap.
  const SPEECH_CHUNK_CHARS = 260;
  const SPEECH_CHUNK_MIN = 70;
  const PREFETCH_CONCURRENCY = 2;
  const countWords = (value) => (value ? value.trim().split(/\s+/).filter(Boolean).length : 0);

  const stripSpeechMarkup = (value) =>
    (value || '')
      .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')   // links -> their label
      .replace(/[#*`~|>]/g, ' ')
      // \U is not a JavaScript escape: it put the literal characters
      // U/0/1/F/A into the class, so it silently deleted letters and digits
      // from every answer (PMFBY -> "Y", "4%" -> "%", "3 lakh" -> "lakh").
      .replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu, ' ') // emoji
      .replace(/\s+/g, ' ')
      .trim();

  // Split on sentence ends, then group sentences into pieces small enough that
  // the first one is quick to synthesise but big enough to sound like speech
  // rather than a series of clipped fragments.
  const splitSpeechChunks = (value) => {
    const clean = stripSpeechMarkup(value);
    if (!clean) return [];
    const sentences = clean
      .split(/(?<=[.!?।॥])\s+/)
      .map((sentence) => sentence.trim())
      .filter(Boolean);
    if (!sentences.length) return [clean.slice(0, SPEECH_CHUNK_CHARS)];

    const chunks = [];
    let current = '';
    for (const sentence of sentences) {
      // A single very long sentence still has to be broken up somewhere.
      if (sentence.length > SPEECH_CHUNK_CHARS) {
        if (current) { chunks.push(current); current = ''; }
        for (let i = 0; i < sentence.length; i += SPEECH_CHUNK_CHARS) {
          chunks.push(sentence.slice(i, i + SPEECH_CHUNK_CHARS).trim());
        }
        continue;
      }
      if (!current) {
        current = sentence;
      } else if (current.length + sentence.length + 1 <= SPEECH_CHUNK_CHARS) {
        current += ' ' + sentence;
      } else {
        chunks.push(current);
        current = sentence;
      }
    }
    if (current) {
      if (chunks.length && current.length < SPEECH_CHUNK_MIN) {
        chunks[chunks.length - 1] += ' ' + current;
      } else {
        chunks.push(current);
      }
    }
    return chunks.filter(Boolean);
  };

  // How much of the *answer on screen* the spoken text accounts for. When the
  // voice only reads the lead, the reveal follows that lead and the remaining
  // detail is shown once the voice stops.
  const spokenWordTarget = (answerText, spokenText) => {
    const answerWords = countWords(answerText);
    const spokenWords = countWords(spokenText);
    if (!answerWords) return 0;
    if (spokenWords >= answerWords) return answerWords;

    const norm = (value) => stripSpeechMarkup(value).toLowerCase();
    const needle = norm(spokenText);
    const hay = norm(answerText);
    // Anchor on the closing words of what was spoken and find where they land
    // in the full answer.
    const tail = needle.slice(-60);
    const at = tail.length > 12 ? hay.lastIndexOf(tail) : -1;
    if (at >= 0) {
      const covered = hay.slice(0, at + tail.length).trim();
      const target = countWords(covered);
      if (target > 0) return Math.min(answerWords, target);
    }
    // Fall back to the share of the answer that was actually spoken.
    return Math.min(answerWords, Math.max(1, Math.round((spokenWords / answerWords) * answerWords)));
  };

  const playAssistantSpeech = async (messageId, answerText, langCode, spokenText) => {
    stopCurrentAudio();
    const fullAnswer = answerText || '';
    // The backend decides how much of the answer is worth saying out loud. If
    // it did not say (an older backend, or a cached answer) the whole answer is
    // read, which is what the citizen asked for.
    const text = stripSpeechMarkup(spokenText || fullAnswer);
    if (!text) return;

    const effectiveLang =
      langCode && langCode !== 'en' ? langCode : detectScriptLanguage(text) || language || 'en';
    setAudioState({ messageId, status: 'loading' });

    // Safety guard: never leave the voice waiting forever.
    const guard = setTimeout(() => {
      setAudioState((prev) =>
        prev.messageId === messageId && prev.status === 'loading'
          ? { messageId: null, status: 'idle' }
          : prev
      );
    }, 18000);

    const chunks = splitSpeechChunks(text);
    if (!chunks.length) { clearTimeout(guard); return; }

    const run = {
      cancelled: false,
      paused: false,
      failed: false,
      chunks,
      urls: new Array(chunks.length).fill(null),
      totalWords: countWords(text),
      targetWords: spokenWordTarget(fullAnswer, text),
      inFlight: 0,
      pending: new Set(),
    };
    speechRunRef.current = run;

    const fetchChunk = async (index) => {
      if (run.cancelled || index >= chunks.length) return null;
      if (run.urls[index]) return run.urls[index];
      // Never ask twice for the same piece: the main loop and the prefetcher
      // can both reach for it.
      if (run.pending.has(index)) return null;
      if (run.inFlight >= PREFETCH_CONCURRENCY) return null;
      run.pending.add(index);
      run.inFlight += 1;
      try {
        const url = await fetchTTSAudio(chunks[index], effectiveLang);
        if (url && !run.cancelled) run.urls[index] = url;
        return url;
      } catch {
        // A refusal from the provider, not a piece that is still coming.
        run.failed = true;
        return null;
      } finally {
        run.inFlight -= 1;
        run.pending.delete(index);
      }
    };

    // Keep the queue ahead of the voice: whenever a slot frees up, go and get
    // the next piece so it is ready the moment the current one ends.
    const pumpPrefetch = () => {
      if (run.cancelled) return;
      for (let i = run.index + 1; i < chunks.length; i += 1) {
        if (run.inFlight >= PREFETCH_CONCURRENCY) break;
        if (run.urls[i] || run.pending.has(i)) continue;
        fetchChunk(i);
      }
    };

    const revealGlobal = (run_, wordsBefore, chunkText, getChunkProgress) => {
      const spoken = wordsBefore + countWords(chunkText) * Math.max(0, Math.min(1, getChunkProgress()));
      const share = run_.totalWords ? spoken / run_.totalWords : 1;
      const answerWords = countWords(fullAnswer);
      const shown = Math.max(1, Math.round(share * (run_.targetWords || answerWords)));
      return { shown: Math.min(shown, run_.targetWords || answerWords || shown), of: answerWords };
    };

    // One reveal session spans the whole reply. These are read through the
    // closure the session samples, so crossing into the next piece carries the
    // text forward instead of restarting it.
    const revealState = { wordsBefore: 0, index: 0, audio: null, ratio: 0, started: false };
    // The voice only reads this much of the answer, so the reveal must stop
    // here and hand over to the remainder fill instead of running to the end.
    const answerWords = countWords(fullAnswer);
    const revealCeiling = answerWords ? Math.min(1, (run.targetWords || answerWords) / answerWords) : 1;
    let startedSpeaking = false;
    let fellBack = false;

    try {
      for (let index = 0; index < chunks.length; index += 1) {
        if (run.cancelled) { clearTimeout(guard); return; }
        run.index = index;

        let url = run.urls[index];
        if (!url) {
          url = await fetchChunk(index);
          // Give the background fetcher a moment to catch up rather than
          // dropping straight into a silent gap.
          if (!url && !run.failed) {
            // Only worth waiting if the background fetcher is genuinely still
            // working on this piece. If the provider refused it, there is
            // nothing to wait for.
            url = await new Promise((resolve) => {
              let waited = 0;
              const poll = setInterval(() => {
                waited += 120;
                if (run.cancelled || run.failed || run.urls[index] || waited > 12000) {
                  clearInterval(poll);
                  resolve(run.cancelled ? null : run.urls[index]);
                }
              }, 120);
            });
          }
        }
        if (run.cancelled) { clearTimeout(guard); return; }

        // One refusal means the voice is not coming: stop asking and hand the
        // reply to the browser voice straight away, rather than waiting again
        // for every remaining piece.
        if (!url) { fellBack = true; break; }

        const played = await new Promise((resolve) => {
          const audio = new Audio(url);
          audio.playbackRate = 1.0;
          run.audio = audio;
          currentAudioRef.current = audio;
          revealState.index = index;
          revealState.audio = audio;

          audio.onplay = () => {
            if (run.cancelled) return;
            startedSpeaking = true;
            setAudioState({ messageId, status: 'playing' });
            setMessages((prev) =>
              prev.map((m) => (m.id === messageId ? { ...m, voiceReady: true } : m))
            );
            revealState.index = index;
            revealState.audio = audio;
            // beginReveal claims the message at zero words, so calling it again
            // for every piece would throw the visible text back to the start at
            // each chunk boundary. Start it once and let it follow the queue.
            if (!revealState.started) {
              revealState.started = true;
              beginReveal(
                messageId,
                fullAnswer,
                () => {
                  const audioNow = revealState.audio;
                  const chunkNow = chunks[revealState.index] || '';
                  const g = revealGlobal(run, revealState.wordsBefore, chunkNow, () =>
                    audioNow ? revealProgressFor(audioNow, chunkNow) : 1
                  );
                  // beginReveal wants a 0..1 ratio; a raw word count saturates
                  // the clamp and dumps the whole answer on screen at once.
                  revealState.ratio = Math.max(0, Math.min(1, g.shown / (g.of || 1)));
                  return revealState.ratio;
                },
                estimateSpeakSeconds(text),
                { ceiling: revealCeiling, isPaused: () => run.paused }
              );
            }
            // Only once the voice is actually audible do we go and get the rest.
            if (index === 0) pumpPrefetch();
          };
          audio.onended = () => resolve(true);
          audio.onerror = () => resolve(false);
          audio.onpause = () => {
            if (audio.currentTime < audio.duration) setAudioState({ messageId, status: 'paused' });
          };

          audio.play().catch(() => resolve(false));
        });

        currentAudioRef.current = null;
        run.audio = null;
        revealState.audio = null;

        if (run.cancelled) { clearTimeout(guard); return; }
        if (!played) { fellBack = true; break; }

        revealState.wordsBefore += countWords(chunks[index]);
        if (index < chunks.length - 1) pumpPrefetch();
      }
    } catch (err) {
      console.warn('Backend audio play error, falling back to Web Speech:', err);
      fellBack = true;
    }

    clearTimeout(guard);
    if (run.cancelled) return;

    if (fellBack) {
      // Something in the chain broke. Hand the whole spoken part to the browser
      // voice so the citizen still hears the answer.
      speechRunRef.current = null;
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? { ...m, voiceReady: true } : m))
      );
      fallbackSpeechSynthesis(messageId, text, effectiveLang);
      return;
    }

    speechRunRef.current = null;
    setAudioState({ messageId: null, status: 'idle' });

    if (startedSpeaking) {
      if (run.targetWords >= countWords(fullAnswer)) {
        finishReveal(messageId, fullAnswer);
      } else {
        // The voice read the lead; the detail that was held back now fills in
        // so the screen ends up complete either way.
        revealRemainder(messageId, fullAnswer);
      }
    } else {
      finishReveal(messageId, fullAnswer);
    }
  };

  /**
   * Called only when every audio path has failed. Leaving the button in the
   * neutral state made a total TTS failure look identical to "working", which
   * is very hard to diagnose on a kiosk, so say so on the button itself.
   */
  const markVoiceUnavailable = (messageId, reason) => {
    console.error('Voice output unavailable:', reason);
    setAudioState({ messageId, status: 'error' });
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
      markVoiceUnavailable(messageId, 'browser has no speechSynthesis');
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? { ...m, voiceReady: true } : m))
      );
      finishReveal(messageId, text);
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
        // No native voice for this language: stay silent rather than reading an
        // Indian answer in a British voice, but tell the user why.
        markVoiceUnavailable(messageId, `no ${targetLang} system voice installed`);
        return;
      }
      utterance.lang = targetLocale;
    }

    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    const speakSeconds = Math.max(2, (cleanText.split(' ').length / 2.6));
    const startedAt = { t: 0 };

    utterance.onstart = () => {
      setAudioState({ messageId, status: 'playing' });
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? { ...m, voiceReady: true } : m))
      );
      startedAt.t = Date.now();
      beginReveal(messageId, text, () => Math.min(1, (Date.now() - startedAt.t) / (speakSeconds * 1000)), speakSeconds);
    };
    utterance.onend = () => {
      setAudioState({ messageId: null, status: 'idle' });
      finishReveal(messageId, text);
    };
    utterance.onerror = (e) => {
      // 'not-allowed' means autoplay was blocked; anything else means the
      // system voice itself failed. Either way the user needs to see it.
      markVoiceUnavailable(messageId, `speechSynthesis error: ${e?.error || 'unknown'}`);
      // Never leave the answer hidden behind a placeholder just because the
      // voice failed: show all of it.
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? { ...m, voiceReady: true } : m))
      );
      finishReveal(messageId, text);
    };

    window.speechSynthesis.speak(utterance);
  };

  const toggleSpeech = (messageId, text, readAloud) => {
    if (audioState.messageId === messageId && audioState.status === 'playing') {
      if (currentAudioRef.current) {
        currentAudioRef.current.pause();
      } else if (window.speechSynthesis) {
        window.speechSynthesis.pause();
      }
      if (speechRunRef.current) speechRunRef.current.paused = true;
      setAudioState({ messageId, status: 'paused' });
    } else if (audioState.messageId === messageId && audioState.status === 'paused') {
      if (currentAudioRef.current) {
        currentAudioRef.current.play();
      } else if (window.speechSynthesis) {
        window.speechSynthesis.resume();
      }
      if (speechRunRef.current) speechRunRef.current.paused = false;
      setAudioState({ messageId, status: 'playing' });
    } else {
      playAssistantSpeech(messageId, text, language, readAloud);
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
        voiceReady: false,
        responseType: response.responseType || response.domain,
        officerRecommendation: response.recommended_officer || response.officerRecommendation,
        citations: response.citations || [],
        verificationStatus: response.verificationStatus,
        trustScore: response.trustScore || 0.98,
        activeDomains: response.activeDomains || [response.domain || 'general'],
        verifiedFacts: response.verifiedFacts || [],
        sourceAuthority: response.sourceAuthority,
        // What the backend decided is worth saying, and what to ask next.
        // Without a plan the whole answer is read out.
        readAloud: response.read_aloud || response.readAloud || '',
        followUpKind: response.follow_up_kind || response.followUpKind || null,
        detailWithheld: response.detail_withheld ?? response.detailWithheld ?? false,
      },
    ]);

    // Auto-start with voice speech on output
    if (response.answer) {
      setTimeout(() => {
        playAssistantSpeech(
          newMsgId,
          response.answer,
          language,
          response.read_aloud || response.readAloud || ''
        );
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
      const response = await sendTextQuery(trimmed, language, buildHistory(messages));
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

  // A follow-up is offered only while there is something left to read out. Once
  // the citizen takes it, the chip retires so the thread does not accumulate
  // questions nobody asked.
  const askFollowUp = (messageId, kind) => {
    const key = FOLLOW_UP_KEYS[kind];
    const question = key ? t(key) : '';
    if (!question) return;
    setMessages((prev) =>
      prev.map((m) => (m.id === messageId ? { ...m, followUpUsed: true } : m))
    );
    handleTextSend(question);
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

        const response = await sendTextQuery(spokenText, language, buildHistory(messages));
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
          const isAudioError = isCurrentAudio && audioState.status === 'error';

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

                  {!isUser && msg.voiceReady === false ? (
                    /* Voice not ready yet. The words would spoil the silence and
                       arrive before anyone has spoken, so hold a quiet
                       placeholder shaped like the answer instead. */
                    <div className="answer-pending">
                      <span className="answer-pending__line" />
                      <span className="answer-pending__line" />
                      <span className="answer-pending__line" />
                    </div>
                  ) : isUser ? (
                    msg.text
                  ) : isStillBeingSpoken(msg) ? (
                    <span className="reveal-partial">{visibleTextFor(msg)}</span>
                  ) : (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {formatStepsLineByLine(visibleTextFor(msg))}
                    </ReactMarkdown>
                  )}

                  {/* Verified Statutory Citations */}
                  {!isUser && msg.voiceReady !== false && msg.citations && msg.citations.length > 0 && (
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
                        onClick={() => toggleSpeech(msg.id, msg.text, msg.readAloud)}
                        className={`chat-audio-btn ${isPlaying ? 'playing' : ''} ${isAudioLoading ? 'loading' : ''} ${isAudioError ? 'error' : ''}`}
                        title={isPlaying ? 'Pause Voice' : isPaused ? 'Resume Voice' : isAudioError ? 'Voice failed - tap to retry' : 'Listen with Voice'}
                      >
                        {isAudioError ? (
                          <>
                            <VolumeX size={14} />
                            <span>Voice unavailable - tap to retry</span>
                          </>
                        ) : isAudioLoading ? (
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
                {!isUser && msg.followUpKind && !msg.followUpUsed && FOLLOW_UP_KEYS[msg.followUpKind] && (
                  <button
                    type="button"
                    className="chat-followup"
                    onClick={() => askFollowUp(msg.id, msg.followUpKind)}
                  >
                    <MessageCircleQuestion size={15} />
                    <span>{t(FOLLOW_UP_KEYS[msg.followUpKind])}</span>
                  </button>
                )}
                {!isUser && msg.officerRecommendation && (
                  <OfficerRecommendationCard officer={msg.officerRecommendation} />
                )}
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="chat-row chat-row-ai">
            <div className="chat-avatar chat-avatar-ai chat-avatar-busy">
              <Bot size={16} />
            </div>
            <div className="thinking-pulse" role="status" aria-label="Preparing a reply">
              <span className="thinking-pulse__bar" />
              <span className="thinking-pulse__bar" />
              <span className="thinking-pulse__bar" />
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
        <VoiceInput ref={voiceInputRef} onVoiceResult={handleVoiceInput} disabled={isLoading} />

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
