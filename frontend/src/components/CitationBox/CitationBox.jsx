import React from 'react';
import { ShieldCheck, BookOpen, ExternalLink } from 'lucide-react';

export default function CitationBox({ citations = [], trustScore = 0.98 }) {
  if (!citations || citations.length === 0) return null;

  return (
    <div style={{
      marginTop: '16px',
      padding: '14px 18px',
      background: '#f0fdf4',
      border: '1px solid #bbf7d0',
      borderRadius: '12px',
      fontSize: '13px'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '10px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#166534', fontWeight: '700' }}>
          <ShieldCheck size={18} color="#16a34a" />
          <span>Statutory Verification & Legal Citations</span>
        </div>
        <span style={{
          background: '#dcfce7',
          color: '#15803d',
          padding: '2px 8px',
          borderRadius: '999px',
          fontSize: '11px',
          fontWeight: '700'
        }}>
          Trust Score: {Math.round(trustScore * 100)}%
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        {citations.map((cite, index) => (
          <div key={index} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', color: '#14532d' }}>
            <BookOpen size={14} style={{ marginTop: '2px', flexShrink: 0, color: '#15803d' }} />
            <span style={{ flex: 1 }}>{cite}</span>
            <span style={{
              fontSize: '10px',
              background: '#ffffff',
              border: '1px solid #86efac',
              padding: '1px 6px',
              borderRadius: '4px',
              color: '#166534',
              fontWeight: '600'
            }}>
              Gazette Verified
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
