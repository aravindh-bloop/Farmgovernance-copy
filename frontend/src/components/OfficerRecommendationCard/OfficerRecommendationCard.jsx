import React from 'react';
import { UserCheck, Building, Phone, Mail, MapPin, ExternalLink, ShieldCheck } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export default function OfficerRecommendationCard({ officer }) {
  const { t } = useLanguage();

  if (!officer) return null;

  const role = officer.designation_or_role || officer.designation || 'Designated Jurisdictional Officer';
  const officeName = officer.place_or_address || officer.office || officer.head_quarters || officer.department;
  const contactNumber = officer.mobile || officer.landline || officer.phone;
  const email = officer.email;
  const district = officer.district;
  const source = officer.source;

  return (
    <div className="officer-card">
      <div className="officer-card-header">
        <UserCheck size={18} />
        <span>{t('officerRecommendation') || 'Recommended Jurisdictional Authority'}</span>
        <span style={{ marginLeft: 'auto', fontSize: '11px', display: 'flex', alignItems: 'center', gap: '4px', background: 'rgba(255,255,255,0.2)', padding: '2px 8px', borderRadius: '999px' }}>
          <ShieldCheck size={12} /> Verified Record
        </span>
      </div>

      <div className="officer-card-body">
        {officer.name && (
          <h4 className="officer-name">{officer.name}</h4>
        )}
        
        <p className="officer-detail">
          <strong>{t('designation') || 'Designation'}:</strong>{' '}
          {role}
        </p>

        {officer.department && (
          <p className="officer-detail">
            <strong>Department:</strong> {officer.department} {district ? `(${district} District)` : ''}
          </p>
        )}

        {officeName && (
          <p className="officer-detail">
            <Building size={14} />
            <strong>{t('office') || 'Office / Location'}:</strong> {officeName}
          </p>
        )}

        {contactNumber && (
          <p className="officer-detail">
            <Phone size={14} />
            <strong>{t('contact') || 'Contact'}:</strong>{' '}
            <a href={`tel:${contactNumber}`} style={{ color: 'var(--color-primary)', fontWeight: '600', textDecoration: 'none' }}>
              {contactNumber}
            </a>
          </p>
        )}

        {email && (
          <p className="officer-detail">
            <Mail size={14} />
            <strong>Email:</strong>{' '}
            <a href={`mailto:${email}`} style={{ color: 'var(--color-primary)', textDecoration: 'none' }}>
              {email}
            </a>
          </p>
        )}

        {source && (
          <div style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px dashed #fed7aa', fontSize: '11px', color: '#9a3412', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <ExternalLink size={12} />
            <span>Verified Source:</span>
            <a href={source} target="_blank" rel="noopener noreferrer" style={{ color: '#c2410c', fontWeight: '600', textDecoration: 'underline' }}>
              Official Directory Portal
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
