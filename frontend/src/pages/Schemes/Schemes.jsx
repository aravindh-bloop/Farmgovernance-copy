import React, { useState, useEffect } from 'react';
import { Award, Filter, Sparkles } from 'lucide-react';
import { api } from '../../services/api';
import SchemeCards from '../../components/SchemeCards/SchemeCards';

export default function Schemes({ onAskQuery }) {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSchemes() {
      try {
        const res = await api.getSchemes();
        setSchemes(res.data || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    fetchSchemes();
  }, []);

  return (
    <div style={{ maxWidth: '1140px', margin: '0 auto' }}>
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: '#fffbeb',
            color: '#d97706',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Award size={22} />
          </div>
          <div>
            <h2 style={{ fontSize: '22px', fontWeight: '800', color: '#92400e' }}>
              Central & State Farmer Welfare Schemes
            </h2>
            <p style={{ fontSize: '13px', color: '#64748b' }}>
              Direct Benefit Transfer (DBT), Infrastructure Subventions, and Agri-Mechanization grants.
            </p>
          </div>
        </div>
      </div>

      <SchemeCards schemes={schemes} onAskScheme={onAskQuery} />
    </div>
  );
}
