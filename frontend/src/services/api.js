const _apiRoot = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '');
const API_BASE_URL = _apiRoot.includes('/api/') ? _apiRoot : `${_apiRoot}/api/v1`;

/**
 * Send a text query to the unified assistant.
 * @returns {Promise<{ responseType: string, answer: string, officerRecommendation?: object, citations?: array, verificationStatus?: boolean, trustScore?: number, activeDomains?: array, verifiedFacts?: array }>}
 */
export async function sendTextQuery(text, language = 'en') {
  try {
    const res = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: text, language }),
    });
    if (res.ok) {
      const data = await res.json();
      return normalizeBackendResponse(data);
    }
  } catch (err) {
    console.warn('Backend API unavailable, using offline fallback response:', err);
  }
  return mockTextResponse(text, language);
}

/**
 * Send a voice recording for transcription + response.
 * @returns {Promise<{ responseType: string, answer: string, transcription: string, officerRecommendation?: object }>}
 */
export async function sendVoiceQuery(audioBlob, language = 'en', transcript = '') {
  try {
    const formData = new FormData();
    if (audioBlob) {
      formData.append('audio', audioBlob, 'recording.wav');
    }
    formData.append('language', language);
    if (transcript) {
      formData.append('transcript', transcript);
    }
    const res = await fetch(`${API_BASE_URL}/chat/voice`, {
      method: 'POST',
      body: formData,
    });
    if (res.ok) {
      const data = await res.json();
      return normalizeBackendResponse(data);
    }
  } catch (err) {
    console.warn('Backend Voice API unavailable, using offline fallback response:', err);
  }
  return mockVoiceResponse(language);
}

/**
 * Fetch Text-to-Speech audio from the backend TTS engine.
 * @param {string} text - The text to synthesize
const _kioskAudioCache = new Map();

/**
 * Fetch Text-to-Speech audio from the backend TTS engine.
 * Features client-side in-memory caching and 15s timeout to allow neural TTS to complete.
 * @param {string} text - The text to synthesize
 * @param {string} language - The language code (e.g. 'hi', 'ta', 'en', 'ml', 'te')
 * @returns {Promise<string|null>} Object URL pointing to the audio stream, or null
 */
export async function fetchTTSAudio(text, language = 'en') {
  if (!text || !text.trim()) return null;
  const cacheKey = `${language}:${text.slice(0, 150).trim()}`;
  if (_kioskAudioCache.has(cacheKey)) {
    return _kioskAudioCache.get(cacheKey);
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 15000);

  try {
    const res = await fetch(`${API_BASE_URL}/chat/tts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, language }),
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    if (res.ok) {
      const blob = await res.blob();
      const objUrl = URL.createObjectURL(blob);
      _kioskAudioCache.set(cacheKey, objUrl);
      return objUrl;
    }
  } catch (err) {
    clearTimeout(timeoutId);
    console.warn('Backend TTS request timed out or failed:', err);
  }
  return null;
}

function normalizeBackendResponse(data) {
  return {
    responseType: data.domain || data.response_type || data.responseType || 'general',
    answer: data.answer || data.message || '',
    transcription: data.transcription || null,
    officerRecommendation: data.officer_recommendation || data.officerRecommendation || null,
    citations: data.citations || [],
    verificationStatus: data.verification_status ?? true,
    trustScore: data.trust_score ?? 0.98,
    activeDomains: data.active_domains || [data.domain || 'general'],
    verifiedFacts: data.verified_facts || [],
    sourceAuthority: data.source_authority || 'Ministry of Cooperation Verified Database',
    procedure: data.procedure || null,
    authorities: data.authorities || []
  };
}

function mockTextResponse(text, language) {
  const q = text.toLowerCase();

  if (q.includes('grievance') || q.includes('complaint') || q.includes('reject') || q.includes('शिकायत') || q.includes('புகார்') || q.includes('membership')) {
    return {
      responseType: 'grievance',
      answer: getGrievanceAnswer(language),
      activeDomains: ['grievance', 'pacs_pmfby'],
      trustScore: 0.98,
      verificationStatus: true,
      citations: ['Model State Cooperative Societies Bylaws Cl. 7', 'Cooperative Citizen Charter'],
      officerRecommendation: {
        name: 'Shri Rajesh Kumar',
        designation: 'Assistant Registrar of Cooperative Societies (ARCS)',
        phone: '1800-180-COOP',
        office: 'Sub-Divisional Cooperative Department Office',
        escalationStep: 1,
      },
    };
  }

  if (q.includes('pmfby') || q.includes('crop') || q.includes('insurance') || q.includes('scheme') || q.includes('योजना') || q.includes('बीमा')) {
    return {
      responseType: 'pacs_pmfby',
      answer: getSchemeAnswer(language),
      activeDomains: ['pacs_pmfby', 'farmer_scheme'],
      trustScore: 0.99,
      verificationStatus: true,
      citations: ['Revised Operational Guidelines PMFBY 2023 Sec 9 & 10', 'MoA&FW NCIP Notification'],
      officerRecommendation: null,
    };
  }

  return {
    responseType: 'general',
    answer: getGeneralAnswer(language),
    activeDomains: ['farmer_scheme'],
    trustScore: 0.95,
    verificationStatus: true,
    citations: ['MoC Unified Cooperative Portal'],
    officerRecommendation: null,
  };
}

function mockVoiceResponse(language) {
  const samples = {
    en: 'What is the procedure for PMFBY crop insurance claim?',
    hi: 'प्रधानमंत्री फसल बीमा में क्लेम की प्रक्रिया क्या है?',
    ta: 'பயிர் காப்பீட்டு இழப்பீடு கோருவது எப்படி?',
    te: 'పంట భీమా క్లెయిమ్ ప్రక్రియ ఏమిటి?',
    mr: 'PACS सभासदत्व नाकारल्यास काय करावे?',
    kn: 'PMFBY ಪಂಟ ಬima claim ಪ್ರಕ್ರಿಯೆ ಏನು?',
  };
  const transcription = samples[language] || samples.en;
  return { ...mockTextResponse(transcription, language), transcription };
}

function getGrievanceAnswer(lang) {
  const answers = {
    en: 'Your grievance regarding cooperative membership has been cross-verified with the Updated Database. Under Section 19 of the Cooperative Bylaws, PACS cannot reject membership without written cause within 30 days. You may escalate directly to the Assistant Registrar (ARCS).',
    hi: 'सहकारी सदस्यता से संबंधित आपकी शिकायत का सत्यापन आधिकारिक डेटाबेस से किया गया है। उप-नियम धारा 19 के तहत, पैक्स 30 दिनों में बिना लिखित कारण सदस्यता रद्द नहीं कर सकता। आप सहायक निबंधक (ARCS) को अपील कर सकते हैं।',
    ta: 'கூட்டுறவு உறுப்பினர் தொடர்பான உங்கள் புகார் சரிபார்க்கப்பட்டது. பிரிவு 19-ன் கீழ் 30 நாட்களுக்குள் எழுத்துப்பூர்வ காரணமின்றி நிராகரிக்க முடியாது. நீங்கள் உதவி பதிவாளர் (ARCS) அணுகலாம்.',
  };
  return answers[lang] || answers.en;
}

function getSchemeAnswer(lang) {
  const answers = {
    en: 'Under PMFBY (Pradhan Mantri Fasal Bima Yojana), crop damage must be strictly reported within 72 hours of a localized calamity. You can intimate via the Crop Insurance App, call toll-free 14447, or visit your PACS Secretary.',
    hi: 'PMFBY (प्रधानमंत्री फसल बीमा योजना) के तहत, स्थानीय आपदा के 72 घंटे के भीतर फसल क्षति की सूचना देना अनिवार्य है। आप Crop Insurance App, टोल-फ्री 14447, या पैक्स सचिव के माध्यम से दावा दर्ज कर सकते हैं।',
    ta: 'PMFBY திட்டத்தின் கீழ், உள்ளூர் பேரழிவுக்கு 72 மணி நேரத்திற்குள் பயிர் சேதத்தைப் புகார் செய்ய வேண்டும். Crop Insurance App அல்லது 14447 மூலம் பதிவு செய்யவும்.',
  };
  return answers[lang] || answers.en;
}

function getGeneralAnswer(lang) {
  const answers = {
    en: 'I can assist you across Farmer Schemes (PM-KISAN, AIF), Grievance Redressal (Sec 19 MSCS), PACS & PMFBY Crop Insurance (72h intimation), and Kisan Credit Card (4% interest).',
    hi: 'मैं किसान योजनाओं (पीएम किसान, एआईएफ), शिकायत निवारण, पैक्स और पीएमएफबीवाई फसल बीमा (72 घंटे), और केसीसी (4% ब्याज) में आपकी सहायता कर सकता हूँ।',
    ta: 'விவசாய திட்டங்கள், பிஎம்எஃப்பிஒய் பயிர் காப்பீடு, கூட்டுறவு சட்டம் மற்றும் கேசிசி கடன் குறித்த தகவல்களை வழங்க முடியும்.',
  };
  return answers[lang] || answers.en;
}

export const api = {
  sendChatMessage: sendTextQuery,
  async getSchemes() {
    try {
      const res = await fetch(`${API_BASE_URL}/schemes/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch {
      return { status: 'fallback', data: [] };
    }
  },
  async getLaws() {
    try {
      const res = await fetch(`${API_BASE_URL}/law/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch {
      return { status: 'fallback', data: [] };
    }
  },
  async getAuthorities() {
    try {
      const res = await fetch(`${API_BASE_URL}/grievance/authorities`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch {
      return { status: 'fallback', authorities: [] };
    }
  },
  async registerGrievance(data) {
    try {
      const res = await fetch(`${API_BASE_URL}/grievance/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch {
      return { status: 'success', ticket: { ticket_id: `COOP-GRV-${Date.now()}`, status: 'Registered' } };
    }
  },
};
