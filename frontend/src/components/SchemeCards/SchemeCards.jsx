import React from 'react';
import { Award, CheckCircle2, FileText, ArrowRight } from 'lucide-react';

export default function SchemeCards({ schemes = [], onAskScheme }) {
  if (!schemes || schemes.length === 0) return null;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '20px' }}>
      {schemes.map((scheme, idx) => (
        <div
          key={idx}
          style={{
            background: '#ffffff',
            border: '1px solid #e2e8f0',
            borderRadius: '16px',
            padding: '20px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: '0 4px 12px rgba(0,0,0,0.03)'
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
              <span className="badge badge-amber">
                <Award size={12} /> {scheme.domain || 'Govt Scheme'}
              </span>
              <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '600' }}>{scheme.id}</span>
            </div>

            <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#0f172a', marginBottom: '8px' }}>
              {scheme.scheme_name || scheme.title}
            </h3>

            {scheme.financial_benefit && (
              <div style={{
                background: '#ecfdf5',
                borderLeft: '3px solid #059669',
                padding: '8px 12px',
                borderRadius: '6px',
                marginBottom: '12px',
                fontSize: '13px',
                color: '#065f46',
                fontWeight: '600'
              }}>
                💰 {scheme.financial_benefit}
              </div>
            )}

            {scheme.eligibility_criteria && (
              <div style={{ marginBottom: '12px' }}>
                <strong style={{ fontSize: '12px', color: '#475569', textTransform: 'uppercase' }}>Eligibility:</strong>
                <ul style={{ paddingLeft: '18px', marginTop: '6px', fontSize: '12px', color: '#334155' }}>
                  {scheme.eligibility_criteria.map((crit, i) => (
                    <li key={i} style={{ marginBottom: '4px' }}>{crit}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <div style={{ display: 'flex', gap: '8px', marginTop: '16px' }}>
            <button
              onClick={() => onAskScheme && onAskScheme(scheme.scheme_name || scheme.title)}
              className="kiosk-btn kiosk-btn-primary"
              style={{ flex: 1, padding: '8px 14px', fontSize: '13px' }}
            >
              <span>Ask AI Guide</span>
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
