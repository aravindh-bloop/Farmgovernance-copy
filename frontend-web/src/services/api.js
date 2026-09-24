/**
 * Web Frontend API Service Layer
 * Multilingual Cooperative Assistant — Web Application
 * 
 * NOTE: This is the web-facing API service layer for frontend-web (Port 5174).
 * It connects to the shared backend API (http://localhost:8000/api/v1) and mirrors
 * the exact response schema and mock behavior of the kiosk frontend service layer.
 */

const _apiRoot = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '');
const API_BASE_URL = _apiRoot.includes('/api/') ? _apiRoot : `${_apiRoot}/api/v1`;

// Connect to real backend API by default, fallback to mock if offline
const USE_MOCK = false;

/**
 * Send a text query to the assistant.
 * @param {string} text - User question/query
 * @param {string} language - ISO language code (e.g. 'en', 'hi', 'ta', 'kn', 'te', 'mr', 'gu', 'bn')
 * @returns {Promise<{ responseType: string, answer: string, officerRecommendation?: object }>}
 */
export async function sendTextQuery(text, language = 'en') {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/chat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text, language }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      return normalizeBackendResponse(data);
    } catch (err) {
      console.warn('API error, falling back to mock response:', err);
      return mockTextResponse(text, language);
    }
  }
  
  // Simulate natural delay for typing effect
  await new Promise(r => setTimeout(r, 600));
  return mockTextResponse(text, language);
}

/**
 * Send a voice recording for transcription + AI response.
 * @param {Blob} audioBlob - Audio recording blob
 * @param {string} language - ISO language code
 * @returns {Promise<{ responseType: string, answer: string, transcription: string, officerRecommendation?: object }>}
 */
export async function sendVoiceQuery(audioBlob, language = 'en') {
  if (!USE_MOCK) {
    try {
      const formData = new FormData();
      if (audioBlob) {
        formData.append('audio', audioBlob, 'recording.webm');
      }
      formData.append('language', language);
      const res = await fetch(`${API_BASE_URL}/chat/voice`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      return normalizeBackendResponse(data);
    } catch (err) {
      console.warn('API error, falling back to mock response:', err);
      return mockVoiceResponse(language);
    }
  }

  await new Promise(r => setTimeout(r, 800));
  return mockVoiceResponse(language);
}

const _ttsUrlCache = new Map();

/**
 * Fetch Text-to-Speech audio from the backend TTS engine (Pure Native Indic voice).
 * Features client-side in-memory caching and 3.5s timeout for fast response.
 * @param {string} text - The text to synthesize
 * @param {string} language - The language code (e.g. 'ta', 'hi', 'en', 'ml', 'te')
 * @returns {Promise<string|null>} Object URL pointing to the audio stream, or null
 */
export async function fetchTTSAudio(text, language = 'en') {
  if (!text || !text.trim()) return null;
  const cacheKey = `${language}:${text.slice(0, 150).trim()}`;
  if (_ttsUrlCache.has(cacheKey)) {
    return _ttsUrlCache.get(cacheKey);
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 3500);

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
      _ttsUrlCache.set(cacheKey, objUrl);
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
    responseType: data.response_type || data.responseType || data.domain || 'general',
    answer: data.answer || data.response || data.message || '',
    transcription: data.transcription || null,
    officerRecommendation: data.officer_recommendation || data.recommended_officer || data.officerRecommendation || null,
    citations: data.citations || [],
    verifiedFacts: data.verified_facts || [],
    trustScore: data.trust_score || 0.98,
  };
}

function mockTextResponse(text, language) {
  const q = text.toLowerCase();

  // Grievance / Complaint query
  if (
    q.includes('grievance') ||
    q.includes('complaint') ||
    q.includes('reject') ||
    q.includes('शिकायत') ||
    q.includes('புகார்') ||
    q.includes('ஒப்புதல்') ||
    q.includes('முறையீடு') ||
    q.includes('membership')
  ) {
    return {
      responseType: 'grievance',
      answer: getGrievanceAnswer(language),
      officerRecommendation: {
        name: 'Shri Rajesh Kumar',
        designation: 'Assistant Registrar of Cooperative Societies (ARCS)',
        phone: '1800-180-COOP',
        office: 'Sub-Divisional Cooperative Department Office',
        escalationStep: 1,
      },
    };
  }

  // Scheme Info query (PMFBY / KCC / Subsidy)
  if (
    q.includes('pmfby') ||
    q.includes('crop') ||
    q.includes('insurance') ||
    q.includes('scheme') ||
    q.includes('योजना') ||
    q.includes('बीमा') ||
    q.includes('காப்பீடு') ||
    q.includes('திட்டம்') ||
    q.includes('பயிர்')
  ) {
    return {
      responseType: 'scheme_info',
      answer: getSchemeAnswer(language),
      officerRecommendation: null,
    };
  }

  // Registration / PACS query
  if (
    q.includes('register') ||
    q.includes('pacs') ||
    q.includes('apply') ||
    q.includes('पंजीकरण') ||
    q.includes('பதிவு')
  ) {
    return {
      responseType: 'registration',
      answer: getRegistrationAnswer(language),
      officerRecommendation: {
        name: 'Smt. Lakshmi Sundaram',
        designation: 'PACS Cooperative Extension Officer',
        phone: '044-28551234',
        office: 'District Cooperative Central Office',
        escalationStep: 1,
      },
    };
  }

  // General fallback response
  return {
    responseType: 'general',
    answer: getGeneralAnswer(language),
    officerRecommendation: null,
  };
}

function mockVoiceResponse(language) {
  const samples = {
    en: 'What is the procedure for PMFBY crop insurance claim?',
    hi: 'प्रधानमंत्री फसल बीमा में क्लेम की प्रक्रिया क्या है?',
    ta: 'பயிர் காப்பீட்டு இழப்பீடு கோருவது எப்படி?',
    te: 'పంట భీమా క్లెయిమ్ ప్రక్రియ ఏమిటి?',
    kn: 'PMFBY ಬೆಳೆ ವಿಮೆ ವಿಮೆ ಕ್ಲೈಮ್ ಪ್ರಕ್ರಿಯೆ ಏನು?',
    mr: 'PACS सभासदत्व नाकारल्यास काय करावे?',
    gu: 'પીએમએફબીવાય પાક વીમા દાવાની પ્રક્રિયા શું છે?',
    bn: 'পিএমএফবিওয়াই ফসল বিমার দাবির প্রক্রিয়া কী?',
  };
  const transcription = samples[language] || samples.en;
  return { ...mockTextResponse(transcription, language), transcription };
}

function getGrievanceAnswer(lang) {
  const answers = {
    en: 'Your grievance regarding cooperative membership or service has been noted. Under Section 23 of the Cooperative Societies Act, you can escalate unresolved disputes to the Assistant Registrar of Cooperative Societies (ARCS) at your district/sub-division level. See contact recommendation below.',
    hi: 'सहकारी सदस्यता या सेवा से संबंधित आपकी शिकायत दर्ज कर ली गई है। सहकारी समिति अधिनियम की धारा 23 के तहत, आप इस मुद्दे को जिला/उप-मण्डल स्तर पर सहायक रजिस्ट्रार (ARCS) के समक्ष प्रस्तुत कर सकते हैं। नीचे अनुशंसित अधिकारी का संपर्क देखें।',
    ta: 'கூட்டுறவு உறுப்பினர் அல்லது சேவை தொடர்பான உங்கள் புகார் குறிக்கப்பட்டுள்ளது. கூட்டுறவு சங்கங்களின் சட்டப்பிரிவு 23-ன் கீழ், உங்கள் மாவட்ட உதவிப் பதிவாளரிடம் (ARCS) முறையீடு செய்யலாம். பரிந்துரைக்கப்பட்ட அதிகாரி விவரங்களை கீழே பார்க்கவும்.',
    te: 'సహకార సభ్యత్వం లేదా సేవపై మీ ఫిర్యాదు నమోదు చేయబడింది. మీరు జిల్లా సహాయక రిజిస్ట్రార్ (ARCS)కి అప్పీలు చేయవచ్చు.',
    kn: 'ಸಹಕಾರ ಸದಸ್ಯತ್ವದ ಕುರಿತು ನಿಮ್ಮ ದೂರನ್ನು ದಾಖಲಿಸಿಕೊಳ್ಳಲಾಗಿದೆ. ಜಿಲ್ಲಾ ಸಹಕಾರ ಸಹಾಯಕ ರಿಜಿಸ್ಟ್ರಾರ್ (ARCS) ಅವರನ್ನು ಸಂಪರ್ಕಿಸಬಹುದು.',
    mr: 'सहकारी सभासदत्वाबाबतची तुमची तक्रार नोंदवली गेली आहे. तुम्ही सहाय्यक निबंधक (ARCS) यांच्याकडे दाद मागू शकता.',
    gu: 'સહકારી સભ્યપદ અંગેની તમારી ફરિયાદ નોંધાઈ ગઈ છે. તમે આસિસ્ટન્ટ રજિસ્ટ્રાર (ARCS)નો સંપર્ક કરી શકો છો.',
    bn: 'সমবায় সদস্যপদ সংক্রান্ত আপনার অভিযোগ নথিভুক্ত করা হয়েছে। আপনি সহকারী নিবন্ধকের (ARCS) নিকট আপিল করতে পারেন।',
  };
  return answers[lang] || answers.en;
}

function getSchemeAnswer(lang) {
  const answers = {
    en: 'Under PMFBY (Pradhan Mantri Fasal Bima Yojana), crop loss must be reported within 72 hours of a localized calamity (hailstorm, inundation, landslide). You can lodge a claim through your local PACS Secretary, toll-free number 14447, or the Crop Insurance Mobile App.',
    hi: 'PMFBY (प्रधानमंत्री फसल बीमा योजना) के तहत, ओलावृष्टि या जलभराव से हुई फसल क्षति की सूचना 72 घंटे के भीतर देना अनिवार्य है। आप अपने PACS सचिव, टोल-फ्री 14447 या फसल बीमा ऐप के माध्यम से क्लेम दर्ज करा सकते हैं।',
    ta: 'PMFBY திட்டத்தின் கீழ், ஆலங்கட்டி மழை அல்லது வெள்ளத்தால் ஏற்படும் பயிர் சேதத்தை 72 மணி நேரத்திற்குள் தெரிவிக்க வேண்டும். உங்கள் PACS செயலாளர் அல்லது 14447 கட்டணமில்லா எண்ணை அணுகவும்.',
    te: 'PMFBY కింద, తీవ్రమైన పంట నష్టం జరిగిన 72 గంటల్లోగా మీ PACS కార్యదర్శి లేదా 14447 ద్వారా నివేదించాలి.',
    kn: 'PMFBY ಯೋಜನೆ ಅಡಿಯಲ್ಲಿ ಬೆಳೆ ಹಾನಿಯನ್ನು 72 ಗಂಟೆಗಳ ಒಳಗೆ PACS ಕಾರ್ಯದರ್ಶಿ ಅಥವಾ 14447 ಗೆ ವರದಿ ಮಾಡಬೇಕು.',
    mr: 'PMFBY अंतर्गत, पीक नुकसानीची माहिती ७२ तासांच्या आत PACS सचिव किंवा १४४४७ वर देणे आवश्यक आहे.',
    gu: 'PMFBY હેઠળ પાક નુકસાનની જાણ ૭૨ કલાકમાં PACS મંત્રી અથવા ૧૪૪૪૭ પર કરવી આવશ્યક છે.',
    bn: 'PMFBY-এর অধীনে ফসল ক্ষতির তথ্য ৭২ ঘণ্টার মধ্যে আপনার PACS সম্পাদক বা ১৪৪৪৭ নম্বরে জানাতে হবে।',
  };
  return answers[lang] || answers.en;
}

function getRegistrationAnswer(lang) {
  const answers = {
    en: 'To register for Primary Agricultural Credit Society (PACS) membership, present your Aadhaar card, Land Record Extract (7/12 or Patta), and 2 passport photos at your nearest PACS office or apply online through the State Cooperative Portal.',
    hi: 'प्राथमिक कृषि ऋण समिति (PACS) की सदस्यता के लिए आधार कार्ड, भू-अभिलेख (खसरा/खतौनी) और 2 पासपोर्ट फोटो के साथ निकटतम PACS कार्यालय में आवेदन करें या राज्य सहकारी पोर्टल पर ऑनलाइन आवेदन करें।',
    ta: 'PACS உறுப்பினராகப் பதிவு செய்ய, ஆதார் அட்டை, நிலப் பட்டா சான்று மற்றும் 2 பாஸ்போர்ட் அளவிலான புகைப்படங்களுடன் உங்கள் அருகிலுள்ள PACS அலுவலகத்தை அணுகவும்.',
    te: 'PACS సభ్యత్వం కోసం ఆధార్ కార్డ్, భూమి రికార్డు మరియు 2 ఫోటోలతో సమీప PACS కార్యాలయాన్ని సంప్రదించండి.',
    kn: 'PACS ಸದಸ್ಯತ್ವಕ್ಕೆ ಆಧಾರ್ ಕಾರ್ಡ್, ಜಮೀನು ಪಹಣಿ ಮತ್ತು 2 ಫೋಟೋಗಳೊಂದಿಗೆ ಹತ್ತಿರದ PACS ಕಚೇರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.',
    mr: 'PACS सभासदत्वासाठी आधार कार्ड, ७/१२ उतारा आणि २ पासपोर्ट फोटोसह जवळच्या PACS कार्यालयात अर्ज करा.',
    gu: 'PACS સભ્યપદ માટે આધાર કાર્ડ, જમીનનો ઉતારો અને ૨ ફોટો સાથે નજીકની PACS કચેરીનો સંપર્ક કરો.',
    bn: 'PACS সদস্যপদের জন্য আধার কার্ড, জমির খতিয়ান এবং ২ কপি ছবি সহ নিকটস্থ PACS অফিসে যোগাযোগ করুন।',
  };
  return answers[lang] || answers.en;
}

function getGeneralAnswer(lang) {
  const answers = {
    en: 'Welcome to the Multilingual Cooperative Assistant! I can help you with PACS services, Kisan Credit Card (KCC) loans, PMFBY crop insurance claims, cooperative registration, and dispute escalation. How may I assist you today?',
    hi: 'बहुभाषी सहकारी सहायक में आपका स्वागत है! मैं PACS सेवाओं, केसीसी (KCC) ऋण, फसल बीमा दावों और शिकायत निवारण में आपकी सहायता कर सकता हूँ। आज मैं आपकी क्या सहायता कर सकता हूँ?',
    ta: 'பன்மொழி கூட்டுறவு உதவியாளருக்கு நல்வரவு! PACS சேவைகள், KCC கடன்கள், பயிர் காப்பீடு மற்றும் புகார் நிவர்த்தி ஆகியவற்றில் உதவ முடியும். உங்களுக்கு எவ்வாறு உதவட்டும்?',
    te: 'బహుభాషా సహకార సహాయకునికి స్వాగతం! PACS సేవలు, KCC రుణాలు మరియు పంట భీమా వివరాలలో నేను సహాయపడగలను.',
    kn: 'ಬಹುಭಾಷಾ ಸಹಕಾರ ಸಹಾಯಕಕ್ಕೆ ಸ್ವಾಗತ! PACS ಸೇವೆಗಳು, KCC ಸಾಲಗಳು ಮತ್ತು ಬೆಳೆ ವಿಮೆ ವಿವರಗಳಲ್ಲಿ ನಾನು ನೆರವಾಗಬಲ್ಲೆ.',
    mr: 'बहुभाषिक सहकारी सहाय्यकामध्ये आपले स्वागत आहे! मी तुम्हाला PACS सेवा, KCC कर्जे आणि पीक विम्यात मदत करू शकतो.',
    gu: 'બહુભાષી સહકારી સહાયકમાં આપનું સ્વાગત છે! હું તમને PACS સેવાઓ અને પાક વીમામાં મદદ કરી શકું છું.',
    bn: 'বহুভাষিক সমবায় সহকারীতে আপনাকে স্বাগতম! আমি আপনাকে PACS পরিষেবা, KCC ঋণ এবং ফসল বিমায় সাহায্য করতে পারি।',
  };
  return answers[lang] || answers.en;
}
