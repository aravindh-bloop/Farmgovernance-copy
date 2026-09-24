import React from 'react';
import { UserCheck, Building, Clock, FileCheck, Phone, Mail } from 'lucide-react';

export default function OfficeOfficerCard({ officer, tierTitle }) {
  if (!officer) return null;

  return (
    <div style={{
      background: '#ffffff',
      border: '1px solid #e2e8f0',
      borderRadius: '12px',
      padding: '16px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.03)',
      transition: 'transform 0.2s',
      marginBottom: '12px'
    }}>
      {tierTitle && (
        <div style={{
          fontSize: '11px',
          fontWeight: '700',
          color: '#047857',
          textTransform: 'uppercase',
          marginBottom: '8px',
          letterSpacing: '0.5px'
        }}>
          {tierTitle}
        </div>
      )}

      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
        <div style={{
          width: '38px',
          height: '38px',
          borderRadius: '10px',
          background: '#ecfdf5',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#059669',
          flexShrink: 0
        }}>
          <UserCheck size={20} />
        </div>

        <div style={{ flex: 1 }}>
          <h4 style={{ fontSize: '15px', fontWeight: '700', color: '#0f172a', marginBottom: '2px' }}>
            {officer.officer_designation || officer.designation}
          </h4>
          <p style={{ fontSize: '13px', color: '#475569', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Building size={14} color="#64748b" />
            {officer.office_title || officer.jurisdiction}
          </p>

          {officer.action_required && (
            <div style={{
              marginTop: '10px',
              padding: '8px 12px',
              background: '#f8fafc',
              borderRadius: '8px',
              borderLeft: '3px solid #059669',
              fontSize: '12px',
              color: '#334155'
            }}>
              <strong>Action:</strong> {officer.action_required}
            </div>
          )}

          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '12px',
            marginTop: '10px',
            fontSize: '12px',
            color: '#64748b'
          }}>
            {officer.sla && (
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#b45309', fontWeight: '600' }}>
                <Clock size={14} /> Statutory SLA: {officer.sla}
              </span>
            )}
            {officer.contact_directory?.helpline && (
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#0369a1' }}>
                <Phone size={14} /> {officer.contact_directory.helpline}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
