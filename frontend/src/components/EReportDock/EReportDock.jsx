import React, { useEffect, useMemo, useRef, useState } from 'react';
import { FileText, Phone, X, Check, Loader2 } from 'lucide-react';

/**
 * Optional, deliberately quiet end-of-conversation action.
 *
 * It stays hidden until BOTH conditions hold:
 *   1. the citizen has stopped talking (idle), and
 *   2. the conversation is actually report-worthy (a complaint, escalation,
 *      registration or application question).
 * Everything else in the kiosk is voice-first; this is paperwork, so it lives
 * in the corner and never interrupts.
 */

// Multilingual enough to catch the way people actually phrase a problem.
const REPORTABLE = [
  // English
  'complaint', 'complain', 'grievance', 'escalat', 'not responding', 'no response',
  'delay', 'delayed', 'reject', 'refuse', 'refused', 'bribe', 'fraud', 'harass',
  'cheat', 'cheated', 'wrong', 'mistake', 'pending', 'refund', 'recover', 'money',
  'register', 'registration', 'apply', 'application', 'status', 'track', 'certificate',
  'membership', 'loan', 'insurance', 'claim', 'kcc', 'pmfby', 'pm-kisan',
  // Tamil
  'புகார', 'குறை', 'தாவலை', 'மேல்', 'தாமத', 'நிறுத்த', 'மறுப்பு', 'பணம்', 'அழைத்து',
  'பதிவு', 'விண்ணப்பிக்', 'நிலை', 'உறுப்பு', 'கடன்', 'உரிமம்',
  // Telugu
  'ఫిర్యాదు', 'అభ్యర్థన', 'ఆలస్యం', 'తిరస్కరించ', 'ధర money', 'ధరం', 'నమోదు', 'దరఖాస్తు',
  'స్టేటస్', 'సభ్యత్వం', 'రుణం', 'బీమా',
  // Hindi / Marathi
  'शिकायत', 'कष्ट', 'दिवरी', 'मना', 'अस्वीकार', 'पैसा', 'रजिस्टर', 'आवेदन', 'स्थिति',
  'सदस्यता', 'ऋण', 'बीमा', 'तक्की',
  // Kannada
  'ದೂರು', 'ಅರ್ಜಿ', 'ವಿಳಂಬ', 'ತಿರಸ್ಕರ', 'ಹಣಕಾಸು', 'ನೋಂದಣಿ', 'ಸ್ಥಿತಿ',
];

const IDLE_MS = 20000;
const PHONE_KEY = 'coop_user_phone';

/** Rough 10-digit Indian mobile check; keeps the entry honest without lying. */
function isValidIndianPhone(value) {
  return /^[6-9]\d{9}$/.test(String(value || '').replace(/\D/g, '').slice(-10));
}

export function isReportWorthy(turns) {
  if (!turns || turns.length === 0) return false;
  const asked = turns
    .filter((t) => t.role === 'user')
    .map((t) => String(t.text || '').toLowerCase())
    .join(' ');
  if (!asked.trim()) return false;
  return REPORTABLE.some((kw) => asked.includes(kw));
}

/** Build a printable plain-text E-Report of the conversation. */
export function buildEReport(turns, tag) {
  const lines = [];
  lines.push('COOPASSIST E-REPORT');
  lines.push('='.repeat(40));
  lines.push(`Kiosk reference : ${tag}`);
  lines.push(`Generated       : ${new Date().toLocaleString()}`);
  lines.push(`Turns exchanged : ${turns.length}`);
  lines.push('');
  lines.push('CITIZEN QUERIES');
  lines.push('-'.repeat(40));
  turns
    .filter((t) => t.role === 'user')
    .forEach((t, i) => lines.push(`${i + 1}. ${t.text}`));
  lines.push('');
  lines.push('ASSISTANT GUIDANCE / ESCALATION');
  lines.push('-'.repeat(40));
  turns
    .filter((t) => t.role === 'assistant')
    .forEach((t, i) => lines.push(`${i + 1}. ${t.text}`));
  lines.push('');
  lines.push('This report was generated from a voice conversation with CoopAssist.');
  lines.push('Please quote the kiosk reference when contacting your PACS or ARCS.');
  return lines.join('\n');
}

export default function EReportDock({ turns = [], isLoading = false, userTag = '' }) {
  const [idle, setIdle] = useState(false);
  const [open, setOpen] = useState(false);
  const [stage, setStage] = useState('ask'); // ask -> sending -> done
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');
  const timerRef = useRef(null);

  const reportable = useMemo(() => isReportWorthy(turns), [turns]);
  const visible = reportable && idle && !isLoading;

  // Reset whenever the citizen starts talking again.
  useEffect(() => {
    setIdle(false);
    setStage('ask');
    setError('');
  }, [turns.length]);

  // Arm the idle timer only once there is something worth reporting.
  useEffect(() => {
    if (!reportable || isLoading) return undefined;
    timerRef.current = setTimeout(() => setIdle(true), IDLE_MS);
    return () => clearTimeout(timerRef.current);
  }, [turns, reportable, isLoading]);

  useEffect(() => {
    try {
      setPhone(localStorage.getItem(PHONE_KEY) || '');
    } catch {
      setPhone('');
    }
  }, []);

  if (!visible) return null;

  const submit = (event) => {
    event.preventDefault();
    const digits = phone.replace(/\D/g, '').slice(-10);
    if (!isValidIndianPhone(digits)) {
      setError('Please enter a valid 10-digit mobile number.');
      return;
    }
    setError('');
    setStage('sending');
    try {
      localStorage.setItem(PHONE_KEY, digits);
    } catch {
      /* private mode: the report still generates, it just will not be remembered */
    }
    // NOTE: no SMS gateway is wired up yet. The report is generated and shown on
    // screen, and the citizen is told that honestly rather than being shown a
    // delivery confirmation that did not happen. Connect a gateway here to make
    // this a real send.
    setTimeout(() => setStage('done'), 900);
  };

  return (
    <div className="ereport-dock">
      {open && (
        <div className="ereport-card" role="dialog" aria-label="Get E-Report">
          <div className="ereport-head">
            <span><FileText size={14} /> E-Report</span>
            <button onClick={() => setOpen(false)} aria-label="Close E-Report"><X size={14} /></button>
          </div>

          {stage === 'done' ? (
            <div className="ereport-done">
              <Check size={18} />
              <p>Your E-Report is ready below.</p>
              <p className="ereport-done-note">
                SMS delivery is not enabled on this kiosk yet, so a copy has not been
                sent to your number. Please screenshot or note the reference.
              </p>
              <details className="ereport-preview">
                <summary>View report</summary>
                <pre>{buildEReport(turns, userTag)}</pre>
              </details>
            </div>
          ) : (
            <form onSubmit={submit} className="ereport-form">
              <p className="ereport-hint">
                Get a written summary of this conversation, the advice given and the
                escalation path.
              </p>
              <label className="ereport-phone">
                <Phone size={14} />
                <input
                  type="tel"
                  inputMode="numeric"
                  maxLength={10}
                  placeholder="10-digit mobile number"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value.replace(/\D/g, '').slice(0, 10))}
                  aria-label="Mobile number"
                />
              </label>
              {error && <p className="ereport-error">{error}</p>}
              <button type="submit" className="ereport-submit" disabled={stage === 'sending'}>
                {stage === 'sending' ? (
                  <>
                    <Loader2 size={14} className="animate-spin" />
                    <span>Sending...</span>
                  </>
                ) : (
                  <>
                    <FileText size={14} />
                    <span>Get E-Report</span>
                  </>
                )}
              </button>
              <p className="ereport-optional">Optional — your number is stored only on this kiosk.</p>
            </form>
          )}
        </div>
      )}

      {!open && (
        <button className="ereport-chip" onClick={() => setOpen(true)}>
          <FileText size={14} />
          <span>Get E-Report</span>
        </button>
      )}
    </div>
  );
}
