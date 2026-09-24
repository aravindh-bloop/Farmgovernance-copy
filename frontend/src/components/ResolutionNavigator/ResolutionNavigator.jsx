import React from 'react';
import { Compass, CheckCircle2, ArrowRight, AlertTriangle, Clock } from 'lucide-react';
import OfficeOfficerCard from '../OfficeOfficerCard/OfficeOfficerCard';

export default function ResolutionNavigator({ procedure }) {
  if (!procedure) return null;

  const {
    grievance_category,
    severity,
    recommended_officers = [],
    procedural_steps = [],
    statutory_sla_days
  } = procedure;

  return (
    <div style={{
      marginTop: '20px',
      background: '#ffffff',
      border: '1px solid #fed7aa',
      borderRadius: '16px',
      padding: '20px',
      boxShadow: '0 8px 25px rgba(234, 88, 12, 0.08)'
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderBottom: '1px solid #ffedd5',
        paddingBottom: '14px',
        marginBottom: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '8px',
            background: '#fff7ed',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#ea580c'
          }}>
            <Compass size={22} />
          </div>
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: '800', color: '#9a3412' }}>
              Resolution Navigator & Escalation Hierarchy
            </h3>
            <p style={{ fontSize: '12px', color: '#7c2d12' }}>
              {grievance_category}
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          <span className="badge badge-amber">
            Severity: {severity}
          </span>
          {statutory_sla_days && (
            <span className="badge badge-blue">
              <Clock size={12} /> Statutory SLA: {statutory_sla_days} Days
            </span>
          )}
        </div>
      </div>

      {/* Step by Step Timeline */}
      {procedural_steps.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ fontSize: '13px', fontWeight: '700', color: '#475569', textTransform: 'uppercase', marginBottom: '12px' }}>
            Official Redressal Steps & Timelines
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {procedural_steps.map((step) => (
              <div key={step.step_no} style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px',
                padding: '12px 14px',
                background: '#fafaf9',
                borderRadius: '10px',
                border: '1px solid #f5f5f4'
              }}>
                <div style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  background: '#ea580c',
                  color: '#ffffff',
                  fontSize: '12px',
                  fontWeight: '700',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}>
                  {step.step_no}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2px' }}>
                    <strong style={{ fontSize: '14px', color: '#1c1917' }}>{step.title}</strong>
                    <span style={{ fontSize: '11px', fontWeight: '600', color: '#ea580c', background: '#ffedd5', padding: '1px 6px', borderRadius: '4px' }}>
                      {step.timeline}
                    </span>
                  </div>
                  <p style={{ fontSize: '13px', color: '#57534e' }}>{step.instruction}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommended Officers List */}
      {recommended_officers.length > 0 && (
        <div>
          <h4 style={{ fontSize: '13px', fontWeight: '700', color: '#475569', textTransform: 'uppercase', marginBottom: '12px' }}>
            Designated Jurisdictional Authorities
          </h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px' }}>
            {recommended_officers.map((officer, idx) => (
              <OfficeOfficerCard key={idx} officer={officer} tierTitle={officer.tier || `Authority Tier ${idx + 1}`} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
