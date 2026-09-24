import React from 'react';
import { 
  Scale, Award, Layers, Landmark, FileText, ShieldAlert, ArrowUpRight
} from 'lucide-react';

export default function DomainCards({ onSelectDomain, currentLang }) {
  const domains = [
    {
      id: 'law',
      title: 'Cooperative Law & MSCS',
      titleHi: 'सहकारी कानून व नियम',
      desc: 'MSCS Act 2002, 2023 Amendments, Model State Bylaws, Voting & Arbitration rules under Sec 84.',
      icon: Scale,
      color: '#059669',
      bgColor: '#ecfdf5',
      badge: 'Statutory'
    },
    {
      id: 'pmfby',
      title: 'PMFBY Crop Insurance',
      titleHi: 'प्रधानमंत्री फसल बीमा (PMFBY)',
      desc: '72-hour localized calamity intimation, Kharif/Rabi claims, joint surveys & grievance portal.',
      icon: Layers,
      color: '#0284c7',
      bgColor: '#f0f9ff',
      badge: '72h SLA'
    },
    {
      id: 'pacs',
      title: 'PACS Services & Multi-Use',
      titleHi: 'पैक्स (PACS) बहुउद्देशीय सेवाएं',
      desc: 'Model PACS Bye-laws, ERP computerization, Jan Aushadhi & PMKSK center conversion.',
      icon: Landmark,
      color: '#7c3aed',
      bgColor: '#f5f3ff',
      badge: '63,000+ PACS'
    },
    {
      id: 'schemes',
      title: 'Farmer Welfare Schemes',
      titleHi: 'सरकारी कृषक योजनाएं',
      desc: 'PM-KISAN DBT installments, Agriculture Infrastructure Fund (AIF), Farm mechanization.',
      icon: Award,
      color: '#d97706',
      bgColor: '#fffbeb',
      badge: 'DBT Direct'
    },
    {
      id: 'financial',
      title: 'Financial Literacy & KCC',
      titleHi: 'वित्तीय साक्षरता एवं KCC',
      desc: 'Kisan Credit Card Scale of Finance, 4% effective interest subvention, micro-ATM security.',
      icon: FileText,
      color: '#0d9488',
      bgColor: '#f0fdfa',
      badge: '4% Subvention'
    },
    {
      id: 'grievance',
      title: 'Resolution Navigator',
      titleHi: 'शिकायत समाधान नेविगेटर',
      desc: 'Identify right officers, required documents, statutory SLA and escalation hierarchy.',
      icon: ShieldAlert,
      color: '#dc2626',
      bgColor: '#fef2f2',
      badge: 'Escalation'
    }
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
      gap: '20px',
      marginTop: '24px'
    }}>
      {domains.map((dom) => {
        const Icon = dom.icon;
        return (
          <div
            key={dom.id}
            onClick={() => onSelectDomain(dom.id)}
            style={{
              background: '#ffffff',
              border: '1px solid #e2e8f0',
              borderRadius: '16px',
              padding: '24px',
              cursor: 'pointer',
              transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              boxShadow: '0 4px 15px rgba(0,0,0,0.03)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.borderColor = dom.color;
              e.currentTarget.style.boxShadow = '0 12px 28px rgba(0,0,0,0.08)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.borderColor = '#e2e8f0';
              e.currentTarget.style.boxShadow = '0 4px 15px rgba(0,0,0,0.03)';
            }}
          >
            <div>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '16px'
              }}>
                <div style={{
                  width: '48px',
                  height: '48px',
                  borderRadius: '14px',
                  background: dom.bgColor,
                  color: dom.color,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Icon size={24} />
                </div>
                <span style={{
                  fontSize: '11px',
                  fontWeight: '700',
                  background: dom.bgColor,
                  color: dom.color,
                  padding: '4px 10px',
                  borderRadius: '999px'
                }}>
                  {dom.badge}
                </span>
              </div>

              <h3 style={{ fontSize: '17px', fontWeight: '700', color: '#0f172a', marginBottom: '6px' }}>
                {currentLang === 'hi' ? dom.titleHi : dom.title}
              </h3>
              <p style={{ fontSize: '13px', color: '#64748b', lineHeight: 1.5 }}>
                {dom.desc}
              </p>
            </div>

            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              marginTop: '18px',
              color: dom.color,
              fontWeight: '600',
              fontSize: '13px'
            }}>
              <span>Explore Module</span>
              <ArrowUpRight size={16} />
            </div>
          </div>
        );
      })}
    </div>
  );
}
