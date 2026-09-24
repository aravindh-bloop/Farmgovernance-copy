import React, { useState } from 'react';
import { ShieldAlert, Send, CheckCircle2, AlertCircle, FileText } from 'lucide-react';
import { api } from '../../services/api';
import ResolutionNavigator from '../ResolutionNavigator/ResolutionNavigator';

export default function GrievancePanel({ currentLang }) {
  const [formData, setFormData] = useState({
    applicant_name: '',
    mobile: '',
    district: '',
    category: 'PMFBY Crop Insurance Claim Rejection / Delay',
    complaint_details: '',
    language: currentLang
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const categories = [
    "PMFBY Crop Insurance Claim Rejection / Delay",
    "Illegal Denial of PACS Membership",
    "PACS Loan Disbursement Delay or Denial",
    "Fertilizer / Seed Overcharging at PACS",
    "Cooperative Society Election Malpractice"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.applicant_name || !formData.district || !formData.complaint_details) {
      alert('Please fill in applicant name, district and complaint details.');
      return;
    }

    setLoading(true);
    try {
      const resp = await api.registerGrievance(formData);
      setResult(resp);
    } catch (err) {
      console.error(err);
      alert('Failed to register grievance. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <div style={{
        background: '#ffffff',
        border: '1px solid #fed7aa',
        borderRadius: '16px',
        padding: '24px',
        boxShadow: '0 8px 30px rgba(0,0,0,0.04)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
          <div style={{
            width: '44px',
            height: '44px',
            borderRadius: '12px',
            background: '#fff7ed',
            color: '#ea580c',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <ShieldAlert size={24} />
          </div>
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: '800', color: '#7c2d12' }}>
              Citizen Cooperative Grievance Portal & Resolution Navigator
            </h2>
            <p style={{ fontSize: '13px', color: '#9a3412' }}>
              Direct statutory escalation to District Registrar, DAO, or Cooperative Ombudsman with verified SLA tracking.
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: '600', color: '#334155', marginBottom: '6px' }}>
              Farmer / Applicant Full Name *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Ramesh Patil / K. Ramasamy"
              value={formData.applicant_name}
              onChange={(e) => setFormData({ ...formData, applicant_name: e.target.value })}
              style={{
                width: '100%',
                padding: '10px 14px',
                borderRadius: '8px',
                border: '1px solid #cbd5e1',
                fontSize: '14px'
              }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: '600', color: '#334155', marginBottom: '6px' }}>
              Mobile Number *
            </label>
            <input
              type="tel"
              required
              placeholder="10-digit mobile number"
              value={formData.mobile}
              onChange={(e) => setFormData({ ...formData, mobile: e.target.value })}
              style={{
                width: '100%',
                padding: '10px 14px',
                borderRadius: '8px',
                border: '1px solid #cbd5e1',
                fontSize: '14px'
              }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: '600', color: '#334155', marginBottom: '6px' }}>
              District & State *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Nashik, Maharashtra"
              value={formData.district}
              onChange={(e) => setFormData({ ...formData, district: e.target.value })}
              style={{
                width: '100%',
                padding: '10px 14px',
                borderRadius: '8px',
                border: '1px solid #cbd5e1',
                fontSize: '14px'
              }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: '600', color: '#334155', marginBottom: '6px' }}>
              Grievance Category *
            </label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              style={{
                width: '100%',
                padding: '10px 14px',
                borderRadius: '8px',
                border: '1px solid #cbd5e1',
                fontSize: '14px',
                background: '#ffffff'
              }}
            >
              {categories.map((cat, i) => (
                <option key={i} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div style={{ gridColumn: '1 / -1' }}>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: '600', color: '#334155', marginBottom: '6px' }}>
              Detailed Grievance Description *
            </label>
            <textarea
              required
              rows={4}
              placeholder="Describe the issue, date of application, PACS name, policy ID or officer involved..."
              value={formData.complaint_details}
              onChange={(e) => setFormData({ ...formData, complaint_details: e.target.value })}
              style={{
                width: '100%',
                padding: '12px 14px',
                borderRadius: '8px',
                border: '1px solid #cbd5e1',
                fontSize: '14px',
                resize: 'vertical'
              }}
            />
          </div>

          <div style={{ gridColumn: '1 / -1', display: 'flex', justifyContent: 'flex-end', marginTop: '10px' }}>
            <button
              type="submit"
              disabled={loading}
              className="kiosk-btn kiosk-btn-accent"
              style={{ padding: '12px 28px', fontSize: '15px' }}
            >
              <Send size={18} />
              <span>{loading ? 'Submitting & Routing...' : 'Generate Resolution Roadmap & File'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* Result Display */}
      {result && result.ticket && (
        <div style={{ marginTop: '24px' }}>
          <div style={{
            background: '#f0fdf4',
            border: '1px solid #86efac',
            borderRadius: '16px',
            padding: '20px',
            marginBottom: '20px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#15803d', marginBottom: '8px' }}>
              <CheckCircle2 size={24} />
              <h3 style={{ fontSize: '18px', fontWeight: '800' }}>
                Grievance Formally Registered: {result.ticket.ticket_id}
              </h3>
            </div>
            <p style={{ fontSize: '14px', color: '#166534' }}>
              Your grievance has been classified and automatically routed to the designated statutory authority with an SLA of <strong>{result.ticket.sla_days} Days</strong>.
            </p>
          </div>

          <ResolutionNavigator
            procedure={{
              grievance_category: result.ticket.category,
              severity: 'High',
              statutory_sla_days: result.ticket.sla_days,
              recommended_officers: [result.ticket.assigned_officer],
              procedural_steps: result.procedure_steps || []
            }}
          />
        </div>
      )}
    </div>
  );
}
