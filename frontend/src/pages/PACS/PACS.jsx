import React from 'react';
import { Landmark, CheckCircle, Database, Store, ShoppingBag, Shield } from 'lucide-react';

export default function PACS({ onAskQuery }) {
  const activities = [
    { title: "Short & Medium Term Credit", desc: "KCC crop loans, dairy loans, farm mechanization credit.", icon: Landmark },
    { title: "Fertilizer & Seed Hubs", desc: "Regulated MRP distribution of Urea, DAP, NPK and certified seeds.", icon: ShoppingBag },
    { title: "Pradhan Mantri Jan Aushadhi", desc: "Dispensing high quality generic medicines at 50-90% discount.", icon: Store },
    { title: "Common Service Center (CSC)", desc: "Aadhaar e-KYC, PAN card, utility bill payments, land records.", icon: Database }
  ];

  return (
    <div style={{ maxWidth: '1140px', margin: '0 auto' }}>
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: '#f5f3ff',
            color: '#7c3aed',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Landmark size={22} />
          </div>
          <div>
            <h2 style={{ fontSize: '22px', fontWeight: '800', color: '#5b21b6' }}>
              Primary Agricultural Credit Societies (PACS) Multi-Service Hubs
            </h2>
            <p style={{ fontSize: '13px', color: '#64748b' }}>
              Guidelines under the Ministry of Cooperation for PACS ERP Computerization and Model Bye-laws.
            </p>
          </div>
        </div>
      </div>

      <div style={{
        background: '#ffffff',
        border: '1px solid #e2e8f0',
        borderRadius: '16px',
        padding: '28px',
        marginBottom: '28px',
        boxShadow: '0 4px 15px rgba(0,0,0,0.03)'
      }}>
        <h3 style={{ fontSize: '17px', fontWeight: '700', color: '#0f172a', marginBottom: '12px' }}>
          PACS Transformation into Multi-Purpose Economic Entities
        </h3>
        <p style={{ fontSize: '14px', color: '#475569', lineHeight: 1.6, marginBottom: '24px' }}>
          Under the national Model Bye-laws, PACS are no longer limited to simple credit disbursement. They can now engage in more than 25 diversified business activities to become self-reliant rural economic engines.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
          {activities.map((act, i) => {
            const Icon = act.icon;
            return (
              <div key={i} style={{ padding: '16px', borderRadius: '12px', background: '#f8fafc', border: '1px solid #f1f5f9' }}>
                <div style={{ color: '#7c3aed', marginBottom: '10px' }}>
                  <Icon size={24} />
                </div>
                <h4 style={{ fontSize: '15px', fontWeight: '700', color: '#0f172a', marginBottom: '4px' }}>
                  {act.title}
                </h4>
                <p style={{ fontSize: '12px', color: '#64748b', lineHeight: 1.4 }}>
                  {act.desc}
                </p>
              </div>
            );
          })}
        </div>

        <div style={{ marginTop: '24px', display: 'flex', justifyContent: 'flex-end' }}>
          <button
            onClick={() => onAskQuery && onAskQuery('What are the statutory rights and model bye-laws for PACS multi-purpose conversion?')}
            className="kiosk-btn kiosk-btn-primary"
          >
            <span>Ask AI About PACS Model Bylaws</span>
          </button>
        </div>
      </div>
    </div>
  );
}
