import React from 'react';
import { FileText, Percent, ShieldCheck, CreditCard, AlertTriangle } from 'lucide-react';

export default function FinancialLiteracy({ onAskQuery }) {
  return (
    <div style={{ maxWidth: '1140px', margin: '0 auto' }}>
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: '#f0fdfa',
            color: '#0d9488',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <FileText size={22} />
          </div>
          <div>
            <h2 style={{ fontSize: '22px', fontWeight: '800', color: '#115e59' }}>
              Financial Literacy, KCC & Interest Subvention
            </h2>
            <p style={{ fontSize: '13px', color: '#64748b' }}>
              Understand your credit rights, Scale of Finance calculation, and safe digital banking at PACS micro-ATMs.
            </p>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
        {/* KCC Card */}
        <div style={{
          background: '#ffffff',
          border: '1px solid #e2e8f0',
          borderRadius: '16px',
          padding: '24px',
          boxShadow: '0 4px 15px rgba(0,0,0,0.03)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#0d9488', marginBottom: '14px' }}>
            <Percent size={22} />
            <h3 style={{ fontSize: '17px', fontWeight: '700', color: '#0f172a' }}>
              4.0% Effective KCC Interest Formula
            </h3>
          </div>
          <p style={{ fontSize: '14px', color: '#475569', lineHeight: 1.6, marginBottom: '16px' }}>
            The headline agricultural loan interest rate is 7.0% per annum for credit up to ₹3 Lakhs. If you repay your loan on or before the due date, the Central Government provides a <strong>3.0% Prompt Repayment Incentive (PRI)</strong>, bringing your actual interest cost down to <strong>4.0%</strong>.
          </p>
          <div style={{ background: '#f0fdfa', padding: '12px', borderRadius: '8px', fontSize: '13px', color: '#134e4a' }}>
            ✓ 7% Base Rate - 3% Prompt Subvention = <strong>4% Net Interest</strong>
          </div>
        </div>

        {/* Digital Banking Safety */}
        <div style={{
          background: '#ffffff',
          border: '1px solid #e2e8f0',
          borderRadius: '16px',
          padding: '24px',
          boxShadow: '0 4px 15px rgba(0,0,0,0.03)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#dc2626', marginBottom: '14px' }}>
            <ShieldCheck size={22} color="#059669" />
            <h3 style={{ fontSize: '17px', fontWeight: '700', color: '#0f172a' }}>
              Safe AEPS & Micro-ATM Banking
            </h3>
          </div>
          <ul style={{ paddingLeft: '18px', fontSize: '13px', color: '#475569', lineHeight: 1.6 }}>
            <li style={{ marginBottom: '8px' }}>Never share OTP or banking PINs with unauthorized persons or field agents.</li>
            <li style={{ marginBottom: '8px' }}>Always demand printed or SMS receipt for biometric transactions at PACS micro-ATMs.</li>
            <li>Ensure DBT is mapped to your active Aadhaar-linked savings account.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
