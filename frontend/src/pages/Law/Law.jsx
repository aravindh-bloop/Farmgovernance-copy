import React, { useState, useEffect } from 'react';
import { Scale, BookOpen, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { api } from '../../services/api';

export default function Law({ onAskQuery }) {
  const [laws, setLaws] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchLaws() {
      try {
        const res = await api.getLaws();
        setLaws(res.data || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    fetchLaws();
  }, []);

  return (
    <div style={{ maxWidth: '1140px', margin: '0 auto' }}>
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: '#ecfdf5',
            color: '#059669',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Scale size={22} />
          </div>
          <div>
            <h2 style={{ fontSize: '22px', fontWeight: '800', color: '#064e3b' }}>
              Cooperative Societies Statutory Laws & Model Bylaws
            </h2>
            <p style={{ fontSize: '13px', color: '#64748b' }}>
              Official provisions under Multi-State Co-operative Societies (MSCS) Act 2002 & 2023 Amendments.
            </p>
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {laws.map((law, idx) => (
          <div
            key={idx}
            style={{
              background: '#ffffff',
              border: '1px solid #e2e8f0',
              borderRadius: '16px',
              padding: '24px',
              boxShadow: '0 4px 15px rgba(0,0,0,0.03)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
              <div>
                <span className="badge badge-green" style={{ marginBottom: '8px' }}>
                  {law.act_name}
                </span>
                <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#0f172a' }}>
                  {law.title || law.section}
                </h3>
              </div>
              <button
                onClick={() => onAskQuery && onAskQuery(`Explain legal provisions of ${law.section} in detail`)}
                className="kiosk-btn kiosk-btn-secondary"
                style={{ fontSize: '12px', padding: '6px 14px' }}
              >
                Ask Legal AI
              </button>
            </div>

            <p style={{ fontSize: '14px', color: '#475569', lineHeight: 1.6, marginBottom: '16px' }}>
              {law.summary}
            </p>

            {law.key_provisions && (
              <div style={{ marginBottom: '16px', background: '#f8fafc', padding: '14px', borderRadius: '10px' }}>
                <strong style={{ fontSize: '13px', color: '#334155' }}>Key Statutory Mandates:</strong>
                <ul style={{ paddingLeft: '20px', marginTop: '8px', fontSize: '13px', color: '#475569' }}>
                  {law.key_provisions.map((prov, i) => (
                    <li key={i} style={{ marginBottom: '6px' }}>{prov}</li>
                  ))}
                </ul>
              </div>
            )}

            {law.citations && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
                <span style={{ fontSize: '12px', fontWeight: '700', color: '#64748b' }}>Verified Citations:</span>
                {law.citations.map((c, i) => (
                  <span key={i} style={{
                    fontSize: '11px',
                    background: '#f0fdf4',
                    border: '1px solid #bbf7d0',
                    color: '#15803d',
                    padding: '2px 8px',
                    borderRadius: '6px'
                  }}>
                    {c}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
