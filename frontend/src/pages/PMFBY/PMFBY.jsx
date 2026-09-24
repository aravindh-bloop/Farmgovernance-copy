import React from 'react';
import { Layers, AlertCircle, Clock, ShieldCheck, PhoneCall, CheckCircle } from 'lucide-react';

export default function PMFBY({ onAskQuery }) {
  const steps = [
    {
      step: 1,
      title: "72-Hour Calamity Intimation",
      desc: "Notify within 72 hours of localized hailstorm, flooding, or post-harvest cyclone damage via Crop Insurance App or 14447.",
      urgent: true
    },
    {
      step: 2,
      title: "Surveyor Appointment & Field Visit",
      desc: "Joint survey team (Insurance Loss Assessor + State Agriculture Officer) visits farm within 10 days.",
      urgent: false
    },
    {
      step: 3,
      title: "Loss Assessment & Approval",
      desc: "Loss percentage calculated based on crop cutting experiments or localized yield data.",
      urgent: false
    },
    {
      step: 4,
      title: "Direct DBT Settlement",
      desc: "Claim payout disbursed directly into Aadhaar-linked bank account within 3 weeks of assessment.",
      urgent: false
    }
  ];

  return (
    <div style={{ maxWidth: '1140px', margin: '0 auto' }}>
      <div style={{
        background: 'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)',
        borderRadius: '20px',
        padding: '32px',
        color: '#ffffff',
        marginBottom: '28px'
      }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(255,255,255,0.2)', padding: '4px 12px', borderRadius: '999px', fontSize: '12px', fontWeight: '700', marginBottom: '12px' }}>
          <Clock size={14} /> Mandatory 72-Hour Intimation Window
        </div>
        <h2 style={{ fontSize: '26px', fontWeight: '800', marginBottom: '10px' }}>
          Pradhan Mantri Fasal Bima Yojana (PMFBY) Claim Guide
        </h2>
        <p style={{ fontSize: '15px', color: '#e0f2fe', maxWidth: '750px', lineHeight: 1.6 }}>
          Comprehensive insurance coverage against non-preventable natural risks from pre-sowing to post-harvest.
        </p>

        <div style={{ display: 'flex', gap: '14px', marginTop: '20px', flexWrap: 'wrap' }}>
          <button
            onClick={() => onAskQuery && onAskQuery('How do I claim PMFBY crop insurance for hailstorm loss within 72 hours?')}
            className="kiosk-btn"
            style={{ background: '#ffffff', color: '#0369a1', fontWeight: '700' }}
          >
            Ask PMFBY Assistant
          </button>
          <a
            href="tel:14447"
            className="kiosk-btn"
            style={{ background: 'rgba(255,255,255,0.2)', color: '#ffffff', border: '1px solid rgba(255,255,255,0.4)' }}
          >
            <PhoneCall size={16} />
            <span>PMFBY Toll Free: 14447</span>
          </a>
        </div>
      </div>

      {/* 4-Step Claim Roadmap */}
      <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#0f172a', marginBottom: '16px' }}>
        Official 4-Step Crop Loss Claim Roadmap
      </h3>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '18px', marginBottom: '32px' }}>
        {steps.map((s) => (
          <div
            key={s.step}
            style={{
              background: '#ffffff',
              border: s.urgent ? '1px solid #fecdd3' : '1px solid #e2e8f0',
              borderRadius: '16px',
              padding: '20px',
              boxShadow: '0 4px 15px rgba(0,0,0,0.03)'
            }}
          >
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: s.urgent ? '#ef4444' : '#0284c7',
              color: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: '800',
              fontSize: '14px',
              marginBottom: '12px'
            }}>
              {s.step}
            </div>
            <h4 style={{ fontSize: '15px', fontWeight: '700', color: '#0f172a', marginBottom: '6px' }}>
              {s.title}
            </h4>
            <p style={{ fontSize: '13px', color: '#64748b', lineHeight: 1.5 }}>
              {s.desc}
            </p>
          </div>
        ))}
      </div>

      {/* Premium Table */}
      <div style={{
        background: '#ffffff',
        border: '1px solid #e2e8f0',
        borderRadius: '16px',
        padding: '24px'
      }}>
        <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#0f172a', marginBottom: '14px' }}>
          Statutory Farmer Premium Share Rates
        </h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
          <thead>
            <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0' }}>
              <th style={{ padding: '12px', textAlign: 'left', color: '#475569' }}>Crop Category</th>
              <th style={{ padding: '12px', textAlign: 'left', color: '#475569' }}>Farmer Premium Share</th>
              <th style={{ padding: '12px', textAlign: 'left', color: '#475569' }}>Government Subsidy</th>
            </tr>
          </thead>
          <tbody>
            <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
              <td style={{ padding: '12px', fontWeight: '600' }}>Kharif Food & Oilseeds (Paddy, Maize, Soybean)</td>
              <td style={{ padding: '12px', color: '#047857', fontWeight: '700' }}>Max 2.0% of Sum Insured</td>
              <td style={{ padding: '12px', color: '#64748b' }}>Balance shared 50:50 (Center & State)</td>
            </tr>
            <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
              <td style={{ padding: '12px', fontWeight: '600' }}>Rabi Food & Oilseeds (Wheat, Gram, Mustard)</td>
              <td style={{ padding: '12px', color: '#047857', fontWeight: '700' }}>Max 1.5% of Sum Insured</td>
              <td style={{ padding: '12px', color: '#64748b' }}>Balance shared 50:50 (Center & State)</td>
            </tr>
            <tr>
              <td style={{ padding: '12px', fontWeight: '600' }}>Annual Commercial & Horticultural Crops</td>
              <td style={{ padding: '12px', color: '#047857', fontWeight: '700' }}>Max 5.0% of Sum Insured</td>
              <td style={{ padding: '12px', color: '#64748b' }}>Balance shared 50:50 (Center & State)</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
