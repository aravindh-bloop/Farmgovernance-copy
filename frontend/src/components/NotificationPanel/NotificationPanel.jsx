import React from 'react';
import { Bell, AlertCircle, Info, Sparkles, CheckCircle2 } from 'lucide-react';

export default function NotificationPanel() {
  const alerts = [
    {
      id: 1,
      title: "PMFBY 72-Hour Claim Window Reminder",
      type: "urgent",
      message: "Farmers affected by localized hailstorm or inundation must report within 72 hours via Crop Insurance App or PACS.",
      date: "Today, 09:30 AM"
    },
    {
      id: 2,
      title: "PACS Computerization & ERP Live",
      type: "info",
      message: "Link Aadhaar with PACS ledger for 4% prompt interest subvention on KCC loans.",
      date: "Yesterday"
    },
    {
      id: 3,
      title: "Cooperative Election Authority Rules",
      type: "update",
      message: "Mandatory updated voter lists to be displayed 30 days prior to election date under MSCS Act 2023.",
      date: "2 days ago"
    }
  ];

  return (
    <div style={{
      background: '#ffffff',
      borderRadius: '16px',
      border: '1px solid #e2e8f0',
      padding: '20px',
      boxShadow: '0 4px 16px rgba(0,0,0,0.03)'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Bell size={18} color="#059669" />
          <h3 style={{ fontSize: '15px', fontWeight: '700', color: '#0f172a' }}>
            Live Cooperative & Scheme Alerts
          </h3>
        </div>
        <span className="badge badge-green">3 Active</span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {alerts.map((item) => (
          <div key={item.id} style={{
            padding: '12px',
            borderRadius: '10px',
            background: item.type === 'urgent' ? '#fff1f2' : '#f8fafc',
            border: item.type === 'urgent' ? '1px solid #fecdd3' : '1px solid #f1f5f9',
            fontSize: '13px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
              <strong style={{ color: item.type === 'urgent' ? '#be123c' : '#0f172a' }}>
                {item.title}
              </strong>
              <span style={{ fontSize: '11px', color: '#94a3b8' }}>{item.date}</span>
            </div>
            <p style={{ color: '#475569', fontSize: '12px', lineHeight: 1.4 }}>
              {item.message}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
