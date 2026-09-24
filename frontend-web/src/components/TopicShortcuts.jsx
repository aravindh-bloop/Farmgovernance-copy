import React from 'react';
import { TRANSLATIONS } from '../translations';
import { FileText, ShieldAlert, CreditCard, Building2, ChevronRight, Sparkles } from 'lucide-react';

/**
 * Quick-Access Topic Shortcuts Grid
 * Displays interactive query suggestion cards when no conversation history exists yet.
 */
export default function TopicShortcuts({ langCode, onSelectTopic }) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;

  const topics = [
    {
      id: 'grievance',
      icon: <ShieldAlert size={24} color="#ef4444" />,
      title: t.grievanceTitle,
      desc: t.grievanceDesc,
      query: {
        en: 'I want to file a grievance regarding PACS membership rejection',
        hi: 'मैं PACS सदस्यता अस्वीकृति के संबंध में शिकायत दर्ज करना चाहता हूँ',
        ta: 'PACS உறுப்பினர் நிராகரிப்பு குறித்து புகார் அளிக்க விரும்புகிறேன்',
        kn: 'PACS ಸದಸ್ಯತ್ವ ನಿರಾಕರಣೆಯ ಕುರಿತು ದೂರು ದಾಖಲಿಸಲು ಬಯಸುತ್ತೇನೆ',
        te: 'PACS సభ్యత్వ తిరస్కరణపై ఫిర్యాదు చేయాలనుకుంటున్నాను',
        mr: 'मला PACS सभासदत्व नाकारल्याबद्दल तक्रार करायची आहे',
        gu: 'હું PACS સભ્યપદ ના મંજૂર અંગે ફરિયાદ નોંધાવવા માંગુ છું',
        bn: 'আমি PACS সদস্যপদ বাতিলের বিষয়ে একটি অভিযোগ দায়ের করতে চাই',
      },
      gradient: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(248, 113, 113, 0.05) 100%)',
    },
    {
      id: 'scheme',
      icon: <FileText size={24} color="#3b82f6" />,
      title: t.schemeTitle,
      desc: t.schemeDesc,
      query: {
        en: 'What is the procedure for PMFBY crop insurance claim and 72-hour loss reporting?',
        hi: 'PMFBY फसल बीमा दावे और 72 घंटे में फसल क्षति की सूचना की प्रक्रिया क्या है?',
        ta: 'PMFBY பயிர் காப்பீட்டு உரிமை கோரல் மற்றும் 72 மணிநேர அறிக்கை செயல்முறை என்ன?',
        kn: 'PMFBY ಬೆಳೆ ವಿಮೆ ಕ್ಲೈಮ್ ಮತ್ತು 72 ಗಂಟೆಗಳ ವರದಿ ಪ್ರಕ್ರಿಯೆ ಏನು?',
        te: 'PMFBY పంట భీమా క్లెయిమ్ విధానం మరియు 72 గంటల నివేదిక ప్రక్రియ ఏమిటి?',
        mr: 'PMFBY पीक विमा दावा आणि ७२ तासांत नुकसानीची माहिती देण्याची प्रक्रिया काय आहे?',
        gu: 'PMFBY પાક વીમા દાવા અને ૭૨ કલાકમાં નુકસાનની જાણ કરવાની પ્રક્રિયા શું છે?',
        bn: 'PMFBY ফসল বিমার দাবি এবং ৭২ ঘণ্টার মধ্যে তথ্য জানানোর প্রক্রিয়া কী?',
      },
      gradient: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(96, 165, 250, 0.05) 100%)',
    },
    {
      id: 'registration',
      icon: <Building2 size={24} color="#10b981" />,
      title: t.registrationTitle,
      desc: t.registrationDesc,
      query: {
        en: 'What documents are required to register for PACS membership?',
        hi: 'PACS सदस्यता के लिए पंजीकरण करने हेतु कौन से दस्तावेज आवश्यक हैं?',
        ta: 'PACS உறுப்பினர் பதிவுக்கு என்ன ஆவணங்கள் தேவை?',
        kn: 'PACS ಸದಸ್ಯತ್ವ ನೋಂದಣಿಗೆ ಯಾವ ದಾಖಲೆಗಳು ಬೇಕು?',
        te: 'PACS సభ్యత్వ నమోదుకు ఏ పత్రాలు అవసరం?',
        mr: 'PACS सभासदत्व नोंदणीसाठी कोणती कागदपत्रे आवश्यक आहेत?',
        gu: 'PACS સભ્યપદ નોંધણી માટે કયા કાગળો જરૂરી છે?',
        bn: 'PACS সদস্যপদ রেজিস্ট্রেশনের জন্য কী কী নথি প্রয়োজন?',
      },
      gradient: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.05) 100%)',
    },
    {
      id: 'kcc',
      icon: <CreditCard size={24} color="#8b5cf6" />,
      title: t.kccTitle,
      desc: t.kccDesc,
      query: {
        en: 'How to apply for Kisan Credit Card (KCC) loan through cooperative society?',
        hi: 'सहकारी समिति के माध्यम से किसान क्रेडिट कार्ड (KCC) ऋण के लिए आवेदन कैसे करें?',
        ta: 'கூட்டுறவு சங்கம் மூலம் கிசான் கிரெடிட் கார்டு (KCC) கடனுக்கு விண்ணப்பிப்பது எப்படி?',
        kn: 'ಸಹಕಾರ ಸಂಘದ ಮೂಲಕ ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ (KCC) ಸಾಲಕ್ಕೆ ಅರ್ಜಿ ಸಲ್ಲಿಸುವುದು ಹೇಗೆ?',
        te: 'సహకార సంఘం ద్వారా కిసాన్ క్రెడిట్ కార్డ్ (KCC) రుణానికి ఎలా దరఖాస్తు చేయాలి?',
        mr: 'सहकारी संस्थेमार्फत किसान क्रेडिट कार्ड (KCC) कर्जासाठी कसा अर्ज करावा?',
        gu: 'સહકારી મંડળી મારફતે કિસાન ક્રેડિટ કાર્ડ (KCC) લોન માટે કેવી રીતે અરજી કરવી?',
        bn: 'সমবায় সমিতির মাধ্যমে কিষাণ ক্রেডিট কার্ড (KCC) ঋণের জন্য কীভাবে আবেদন করবেন?',
      },
      gradient: 'linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(167, 139, 250, 0.05) 100%)',
    },
  ];

  return (
    <div style={{ padding: '1rem 0' }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        marginBottom: '1.25rem',
        color: 'var(--text-secondary)',
      }}>
        <Sparkles size={18} color="#3b82f6" />
        <h3 style={{ fontSize: '1rem', fontWeight: '600' }}>
          {t.quickTopicsTitle}
        </h3>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
        gap: '1rem',
      }}>
        {topics.map((item) => {
          const textQuery = item.query[langCode] || item.query.en;
          return (
            <div
              key={item.id}
              onClick={() => onSelectTopic(textQuery)}
              style={{
                background: item.gradient,
                border: '1px solid var(--bg-card-border)',
                borderRadius: '1rem',
                padding: '1.25rem',
                cursor: 'pointer',
                transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-3px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.85rem' }}>
                  <div style={{
                    padding: '0.6rem',
                    borderRadius: '0.75rem',
                    background: 'var(--bg-card)',
                    display: 'inline-flex',
                    boxShadow: 'var(--shadow-sm)',
                  }}>
                    {item.icon}
                  </div>
                  <ChevronRight size={18} color="var(--text-muted)" />
                </div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '0.35rem', color: 'var(--text-primary)' }}>
                  {item.title}
                </h4>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                  {item.desc}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
