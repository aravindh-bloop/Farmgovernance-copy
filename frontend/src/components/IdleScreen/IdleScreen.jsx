import React from 'react';
import { Mic } from 'lucide-react';
import './IdleScreen.css';

const IdleScreen = ({ onWakeUp }) => {
  return (
    <div className="idle-screen" onClick={onWakeUp}>
      <div className="idle-background" />
      <div className="idle-content">
        <h1>Welcome to the Cooperative Kiosk</h1>
        <p>Tap anywhere or click the microphone to start</p>
        <button className="idle-voice-button" onClick={(e) => {
          e.stopPropagation();
          onWakeUp();
        }}>
          <div className="idle-mic-ring"></div>
          <div className="idle-mic-ring delay-1"></div>
          <Mic size={48} className="idle-mic-icon" />
        </button>
      </div>
    </div>
  );
};

export default IdleScreen;
