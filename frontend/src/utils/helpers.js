/**
 * Speech synthesis & helper functions for the Cooperative AI Portal.
 */

export const speakText = (text, langCode = 'hi') => {
  if (!('speechSynthesis' in window)) {
    console.warn('Speech synthesis not supported by this browser.');
    return;
  }

  window.speechSynthesis.cancel(); // Cancel any ongoing speech

  // Strip markdown formatting characters for clean speech
  const cleanText = text
    .replace(/#{1,6}\s+/g, '')
    .replace(/\*\*/g, '')
    .replace(/\*/g, '')
    .replace(/`/g, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

  const utterance = new SpeechSynthesisUtterance(cleanText);
  
  // Map language codes
  const langMap = {
    hi: 'hi-IN',
    ta: 'ta-IN',
    te: 'te-IN',
    mr: 'mr-IN',
    gu: 'gu-IN',
    bn: 'bn-IN',
    kn: 'kn-IN',
    ml: 'ml-IN',
    en: 'en-IN'
  };

  utterance.lang = langMap[langCode] || 'en-IN';
  utterance.rate = 0.95; // Clear pace for rural users
  utterance.pitch = 1.0;

  window.speechSynthesis.speak(utterance);
};

export const stopSpeech = () => {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
};
