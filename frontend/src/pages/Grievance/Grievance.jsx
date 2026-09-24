import React from 'react';
import GrievancePanel from '../../components/GrievancePanel/GrievancePanel';

export default function Grievance({ currentLang }) {
  return (
    <div style={{ maxWidth: '1140px', margin: '0 auto' }}>
      <GrievancePanel currentLang={currentLang} />
    </div>
  );
}
