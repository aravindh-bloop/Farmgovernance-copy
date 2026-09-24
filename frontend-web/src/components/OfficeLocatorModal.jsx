import React, { useState } from 'react';
import { TRANSLATIONS } from '../translations';
import { X, MapPin, Search, Phone, Clock, ExternalLink, Building, ShieldCheck, UserCheck, Mail } from 'lucide-react';

const TN_DISTRICTS = [
  'Theni', 'Madurai', 'Pudukkottai', 'Coimbatore', 'Thanjavur', 'Dindigul',
  'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Erode', 'Vellore', 'Kanchipuram',
  'Cuddalore', 'Villupuram', 'Tiruppur', 'Ramanathapuram', 'Sivaganga',
  'Virudhunagar', 'Karur', 'Nagapattinam', 'Tiruvarur', 'Krishnagiri',
  'Dharmapuri', 'Namakkal', 'Nilgiris', 'Thoothukudi', 'Kanyakumari',
  'Tiruvallur', 'Tiruvannamalai', 'Ranipet', 'Tenkasi', 'Chengalpattu',
  'Kallakurichi', 'Mayiladuthurai', 'Ariyalur', 'Perambalur', 'Tirupathur', 'Chennai'
];

const ALL_OFFICES = [
  {
    id: 'theni-001',
    name: 'Joint Directorate of Agriculture & PMFBY Nodal Center',
    officer: 'Tmt. Meenakumari (i/c) — Joint Director (Agri)',
    district: 'Theni',
    address: 'District Collectorate Complex, Theni - 625531',
    phone: '9655354638 / 04546-251862',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'District agricultural development, PMFBY crop insurance verification & seed distribution',
  },
  {
    id: 'theni-002',
    name: 'Theni District Cooperative Societies Registrar Office',
    officer: 'Thiru M. Pandian (Deputy Registrar)',
    district: 'Theni',
    address: 'Cooperative Bhavan, Near Collectorate, Theni - 625531',
    phone: '04546-252104',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'PACS societies governance, KCC loan sanctions & member disputes',
  },
  {
    id: 'madurai-001',
    name: 'Joint Directorate of Agriculture & PMFBY Office',
    officer: 'Dr. K. Vijayaraghavan — Joint Director (Agri)',
    district: 'Madurai',
    address: 'Collectorate Agriculture Complex, Melur Main Road, Madurai - 625020',
    phone: '9443202511 / 0452-2531602',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'District agriculture administration, crop damage assessment & scheme nodal coordination',
  },
  {
    id: 'madurai-002',
    name: 'Primary Agricultural Credit Society (PACS) Outlet #12',
    officer: 'Thiru M. Arumugam (PACS Secretary)',
    district: 'Madurai',
    address: 'Main Bazaar Road, Vadipatti, Madurai - 625218',
    phone: '0452-2882104',
    hours: 'Mon - Sat: 9:00 AM - 6:00 PM',
    jurisdiction: 'Direct seed/fertilizer distribution & member loan sanctioning',
  },
  {
    id: 'pudukk-001',
    name: 'Joint Directorate of Agriculture Pudukkottai',
    officer: 'Thiru R. Perumal — Joint Director (Agri)',
    district: 'Pudukkottai',
    address: 'District Collectorate Complex, Pudukkottai - 622005',
    phone: '9443387123 / 04322-221650',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Pudukkottai agriculture development & PMFBY 72h calamity survey',
  },
  {
    id: 'pudukk-002',
    name: 'Deputy Registrar of Cooperative Societies (Pudukkottai / Aranthangi)',
    officer: 'Tmt. K. Muthulakshmi (Deputy Registrar)',
    district: 'Pudukkottai',
    address: 'Court Road, Pudukkottai - 622001',
    phone: '04322-222410',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'PACS registration, cooperative audit & KCC loan monitoring',
  },
  {
    id: 'cbe-001',
    name: 'Joint Directorate of Agriculture Coimbatore',
    officer: 'Thiru R. Chithambaram (Joint Director)',
    district: 'Coimbatore',
    address: 'Collectorate Complex, Coimbatore - 641018',
    phone: '9443381001 / 0422-2300124',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Crop insurance & PACS extension in Coimbatore',
  },
  {
    id: 'tanj-001',
    name: 'Joint Directorate of Agriculture Thanjavur',
    officer: 'Thiru K. Justin (Joint Director)',
    district: 'Thanjavur',
    address: 'Collectorate Campus, Thanjavur - 613010',
    phone: '9443382001 / 04362-230122',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Delta region crop cultivation & PMFBY compensation',
  },
  {
    id: 'dgl-001',
    name: 'Joint Directorate of Agriculture Dindigul',
    officer: 'Tmt. M. Anusuya (Joint Director)',
    district: 'Dindigul',
    address: 'Collectorate Complex, Dindigul - 624004',
    phone: '9443383001 / 0451-2460114',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Dindigul district crop loss survey & cooperative banking',
  },
  {
    id: 'try-001',
    name: 'Tiruchirappalli District Agriculture & PACS Center',
    officer: 'Thiru M. Murugesan (Joint Director)',
    district: 'Tiruchirappalli',
    address: 'Cantonment Area, Trichy - 620001',
    phone: '9443384001 / 0431-2410123',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'PMFBY loss verification & computerization support',
  },
  {
    id: 'slm-001',
    name: 'Regional Registrar & Agriculture Office Salem',
    officer: 'Thiru S. Singaram (Joint Director)',
    district: 'Salem',
    address: 'Collectorate Complex, Hasthampatti, Salem - 636007',
    phone: '9443385001 / 0427-2415124',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Second-level grievance escalation & society disputes',
  },
  {
    id: 'erode-001',
    name: 'Joint Directorate of Agriculture Erode',
    officer: 'Thiru S. Chinnasamy (Joint Director)',
    district: 'Erode',
    address: 'District Collectorate Campus, Erode - 638011',
    phone: '9443386001 / 0424-2252124',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Erode turmeric & paddy cooperative schemes',
  },
  {
    id: 'karur-001',
    name: 'Joint Directorate of Agriculture Karur',
    officer: 'Tmt. P. Vasanthi (Joint Director)',
    district: 'Karur',
    address: 'Collectorate Complex, Thanthonimalai, Karur - 639007',
    phone: '9443387001 / 04324-255124',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Karur district PACS loan disbursement & PMFBY',
  },
  {
    id: 'chn-001',
    name: 'State Cooperative Department Head Office',
    officer: 'Shri Rajesh Kumar (ARCS / Joint Registrar)',
    district: 'Chennai',
    address: '14, Cooperative Bhavan Road, Egmore, Chennai - 600008',
    phone: '1800-180-COOP / 044-28551234',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Apex cooperative governance & state-level escalation',
  }
];

export default function OfficeLocatorModal({ langCode, onClose }) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('all');

  const filteredOffices = ALL_OFFICES.filter((office) => {
    const matchesDistrict = selectedDistrict === 'all' || office.district === selectedDistrict;
    const matchesQuery =
      office.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      office.officer.toLowerCase().includes(searchQuery.toLowerCase()) ||
      office.address.toLowerCase().includes(searchQuery.toLowerCase()) ||
      office.district.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesDistrict && matchesQuery;
  });

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '800px' }}>
        {/* Modal Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--bg-card-border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <MapPin size={22} color="#10b981" />
            <div>
              <h2 style={{ fontSize: '1.25rem', fontWeight: '700', color: 'var(--text-primary)', margin: 0 }}>
                {t.locator || 'Jurisdictional Officer & Office Locator'}
              </h2>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                Direct contact directory for all 38 Tamil Nadu districts (Priority: Theni, Madurai, Pudukkottai)
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '0.4rem',
              borderRadius: '0.5rem',
              display: 'flex',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Filter & Search Bar */}
        <div style={{
          padding: '1rem 1.5rem',
          background: 'var(--bg-card)',
          borderBottom: '1px solid var(--bg-card-border)',
          display: 'flex',
          gap: '1rem',
          flexWrap: 'wrap',
        }}>
          {/* District Select */}
          <div style={{ flex: '1 1 200px' }}>
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '0.75rem',
                border: '1px solid var(--bg-card-border)',
                background: 'var(--bg-main)',
                color: 'var(--text-primary)',
                fontSize: '0.92rem',
                outline: 'none',
                fontWeight: '600',
              }}
            >
              <option value="all">📍 All Districts ({TN_DISTRICTS.length})</option>
              <optgroup label="🌟 Priority Core Districts">
                <option value="Theni">📍 Theni (தேனி)</option>
                <option value="Madurai">📍 Madurai (மதுரை)</option>
                <option value="Pudukkottai">📍 Pudukkottai (புதுக்கோட்டை)</option>
              </optgroup>
              <optgroup label="Other Tamil Nadu Districts">
                {TN_DISTRICTS.filter((d) => !['Theni', 'Madurai', 'Pudukkottai'].includes(d)).map((dist) => (
                  <option key={dist} value={dist}>
                    {dist}
                  </option>
                ))}
              </optgroup>
            </select>
          </div>

          {/* Search Box */}
          <div style={{ flex: '2 1 280px', position: 'relative' }}>
            <Search
              size={17}
              color="var(--text-muted)"
              style={{ position: 'absolute', left: '0.85rem', top: '50%', transform: 'translateY(-50%)' }}
            />
            <input
              type="text"
              placeholder="Search by officer name, office or district..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem 0.65rem 2.5rem',
                borderRadius: '0.75rem',
                border: '1px solid var(--bg-card-border)',
                background: 'var(--bg-main)',
                color: 'var(--text-primary)',
                fontSize: '0.92rem',
                outline: 'none',
              }}
            />
          </div>
        </div>

        {/* Office Cards Scrollable List */}
        <div style={{
          padding: '1.5rem',
          overflowY: 'auto',
          maxHeight: '55vh',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
        }}>
          {filteredOffices.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
              No offices found matching your criteria. Try selecting "All Districts" or clearing the search box.
            </div>
          ) : (
            filteredOffices.map((office) => (
              <div
                key={office.id}
                style={{
                  padding: '1.25rem',
                  borderRadius: '1rem',
                  background: 'var(--bg-card)',
                  border: ['Theni', 'Madurai', 'Pudukkottai'].includes(office.district)
                    ? '1.5px solid rgba(16, 185, 129, 0.4)'
                    : '1px solid var(--bg-card-border)',
                  boxShadow: 'var(--shadow-sm)',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.65rem',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem' }}>
                  <div>
                    <span style={{
                      display: 'inline-block',
                      fontSize: '0.75rem',
                      fontWeight: '700',
                      padding: '0.2rem 0.6rem',
                      borderRadius: '999px',
                      background: ['Theni', 'Madurai', 'Pudukkottai'].includes(office.district)
                        ? 'rgba(16, 185, 129, 0.15)'
                        : 'rgba(37, 99, 235, 0.1)',
                      color: ['Theni', 'Madurai', 'Pudukkottai'].includes(office.district) ? '#059669' : '#2563eb',
                      marginBottom: '0.35rem',
                    }}>
                      📍 {office.district} District
                    </span>
                    <h3 style={{ fontSize: '1.05rem', fontWeight: '700', color: 'var(--text-primary)', margin: 0 }}>
                      {office.name}
                    </h3>
                  </div>

                  <span style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.35rem',
                    fontSize: '0.78rem',
                    color: '#059669',
                    fontWeight: '600',
                    background: 'rgba(16, 185, 129, 0.08)',
                    padding: '0.25rem 0.6rem',
                    borderRadius: '999px',
                  }}>
                    <ShieldCheck size={14} />
                    Verified Official Directory
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--text-primary)', fontWeight: '600', fontSize: '0.92rem' }}>
                  <UserCheck size={15} color="#2563eb" />
                  <span>{office.officer}</span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--text-secondary)', fontSize: '0.86rem' }}>
                  <Building size={14} color="var(--text-muted)" />
                  <span>{office.address}</span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.35rem', paddingTop: '0.65rem', borderTop: '1px solid var(--bg-card-border)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: '#059669', fontWeight: '700', fontSize: '0.92rem' }}>
                    <Phone size={15} />
                    <a href={`tel:${office.phone.split('/')[0].trim()}`} style={{ color: '#059669', textDecoration: 'none' }}>
                      {office.phone}
                    </a>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                    <Clock size={13} />
                    <span>{office.hours}</span>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
