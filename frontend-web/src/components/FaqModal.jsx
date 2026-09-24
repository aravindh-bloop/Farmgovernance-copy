import React, { useState } from 'react';
import { TRANSLATIONS } from '../translations';
import { X, Search, ChevronDown, ChevronUp, HelpCircle, FileCheck, ShieldAlert, Award, Landmark } from 'lucide-react';

/**
 * FAQ & Help Modal Component
 * Displays searchable categorized questions and answers for self-service browsing.
 * NOTE: Mock Q&A dataset below can be swapped for real API data in production.
 */

// Mock FAQ Data Store
const FAQ_DATA = [
  {
    id: 1,
    category: 'registration',
    question: 'How do I become a member of a Primary Agricultural Credit Society (PACS)?',
    answer: 'To apply for PACS membership, submit your identity proof (Aadhaar/Voter ID), land record document (7/12 extract or Patta), and 2 passport photos at your village PACS office. The Managing Committee must process applications within 30 days.',
  },
  {
    id: 2,
    category: 'registration',
    question: 'What happens if my PACS membership application is rejected?',
    answer: 'If your application is rejected or not decided upon within 30 days, it is deemed a deemed refusal. You can file an appeal under Section 23 with the Assistant Registrar of Cooperative Societies (ARCS).',
  },
  {
    id: 3,
    category: 'schemes',
    question: 'What is the cutoff time to report crop damage under PMFBY?',
    answer: 'You must report crop loss due to localized calamities (hailstorm, inundation, landslide) within 72 hours of occurrence through the PMFBY Crop Insurance App, PACS secretary, or toll-free helpline 14447.',
  },
  {
    id: 4,
    category: 'schemes',
    question: 'What is the interest rate subvention on Kisan Credit Card (KCC) loans?',
    answer: 'Prompt paying farmers receive a 3% interest subvention, reducing the effective interest rate on short-term crop loans up to ₹3 Lakhs down to just 4% per annum.',
  },
  {
    id: 5,
    category: 'grievances',
    question: 'How can I track my submitted grievance status?',
    answer: 'You can quote your unique ticket ID (e.g. COOP-GRV-10293) at your sub-divisional ARCS office or enter it into the grievance tracking portal to check real-time resolution status.',
  },
  {
    id: 6,
    category: 'grievances',
    question: 'What matters can be appealed before the Cooperative Registrar?',
    answer: 'Matters regarding membership refusal, election disputes, audit discrepancies, loan recovery appeals, and committee disqualification can be appealed before the Registrar.',
  },
  {
    id: 7,
    category: 'pacs',
    question: 'What services are offered by computerized PACS outlets?',
    answer: 'Computerized PACS provide short-term crop loans, fertilizer & seed distribution, custom hiring of farm machinery, warehouse storage receipts, and micro-ATM banking services.',
  },
  {
    id: 8,
    category: 'pacs',
    question: 'Can non-members store produce in PACS godowns?',
    answer: 'Yes, non-members may store agricultural produce in PACS godowns subject to space availability, though members receive discounted storage tariff rates.',
  },
];

export default function FaqModal({ langCode, onClose }) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [expandedId, setExpandedId] = useState(1);

  // Filter Q&As based on category tab & search query
  const filteredFaqs = FAQ_DATA.filter((item) => {
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    const matchesSearch =
      item.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.answer.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const categories = [
    { id: 'all', label: t.faqCategories.all, icon: <HelpCircle size={15} /> },
    { id: 'registration', label: t.faqCategories.registration, icon: <FileCheck size={15} /> },
    { id: 'grievances', label: t.faqCategories.grievances, icon: <ShieldAlert size={15} /> },
    { id: 'schemes', label: t.faqCategories.schemes, icon: <Award size={15} /> },
    { id: 'pacs', label: t.faqCategories.pacs, icon: <Landmark size={15} /> },
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--bg-card-border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <HelpCircle size={22} color="#3b82f6" />
            <h2 style={{ fontSize: '1.25rem', fontWeight: '700', color: 'var(--text-primary)' }}>
              {t.faq}
            </h2>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              color: 'var(--text-muted)',
              padding: '0.4rem',
              borderRadius: '0.5rem',
              display: 'flex',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Search Bar & Category Filters */}
        <div style={{ padding: '1.25rem 1.5rem 0.5rem 1.5rem' }}>
          {/* Search Input */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            background: 'var(--bg-main)',
            border: '1px solid var(--bg-card-border)',
            borderRadius: '0.75rem',
            padding: '0.65rem 1rem',
            marginBottom: '1rem',
          }}>
            <Search size={18} color="var(--text-muted)" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder={t.faqSearchPlaceholder}
              style={{
                border: 'none',
                outline: 'none',
                background: 'transparent',
                width: '100%',
                color: 'var(--text-primary)',
                fontFamily: 'inherit',
                fontSize: '0.92rem',
              }}
            />
          </div>

          {/* Category Chips */}
          <div style={{
            display: 'flex',
            gap: '0.5rem',
            overflowX: 'auto',
            paddingBottom: '0.75rem',
          }}>
            {categories.map((cat) => {
              const isSelected = selectedCategory === cat.id;
              return (
                <button
                  key={cat.id}
                  onClick={() => setSelectedCategory(cat.id)}
                  style={{
                    padding: '0.45rem 0.85rem',
                    borderRadius: '2rem',
                    fontSize: '0.82rem',
                    fontWeight: '600',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.4rem',
                    whiteSpace: 'nowrap',
                    background: isSelected ? 'var(--primary-gradient)' : 'var(--bg-main)',
                    color: isSelected ? '#ffffff' : 'var(--text-secondary)',
                    border: isSelected ? '1px solid transparent' : '1px solid var(--bg-card-border)',
                  }}
                >
                  {cat.icon}
                  <span>{cat.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Q&A Accordion List */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '0.5rem 1.5rem 1.5rem 1.5rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.75rem',
        }}>
          {filteredFaqs.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
              No matching questions found. Try adjusting your search term.
            </div>
          ) : (
            filteredFaqs.map((faq) => {
              const isExpanded = expandedId === faq.id;
              return (
                <div
                  key={faq.id}
                  style={{
                    border: '1px solid var(--bg-card-border)',
                    borderRadius: '0.85rem',
                    overflow: 'hidden',
                    background: 'var(--bg-main)',
                  }}
                >
                  <button
                    onClick={() => setExpandedId(isExpanded ? null : faq.id)}
                    style={{
                      width: '100%',
                      padding: '1rem 1.25rem',
                      textAlign: 'left',
                      background: 'transparent',
                      color: 'var(--text-primary)',
                      fontWeight: '600',
                      fontSize: '0.95rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: '1rem',
                    }}
                  >
                    <span>{faq.question}</span>
                    {isExpanded ? <ChevronUp size={18} color="#3b82f6" /> : <ChevronDown size={18} color="var(--text-muted)" />}
                  </button>
                  {isExpanded && (
                    <div style={{
                      padding: '0 1.25rem 1.1rem 1.25rem',
                      fontSize: '0.88rem',
                      color: 'var(--text-secondary)',
                      lineHeight: '1.6',
                      borderTop: '1px dashed var(--bg-card-border)',
                      paddingTop: '0.85rem',
                    }}>
                      {faq.answer}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
