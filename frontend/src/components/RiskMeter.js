import React from 'react';
import '../styles/RiskMeter.css';

function RiskMeter({ score }) {
  const getColor = () => {
    if (score >= 75) return '#ff0000';
    if (score >= 50) return '#ff9900';
    if (score >= 25) return '#ffcc00';
    return '#00ff00';
  };

  const getLabel = () => {
    if (score >= 75) return 'CRITICAL';
    if (score >= 50) return 'HIGH';
    if (score >= 25) return 'MEDIUM';
    return 'LOW';
  };

  return (
    <div className="risk-meter">
      <h3>Risk Score</h3>
      <div className="meter-container">
        <div className="meter-bar">
          <div 
            className="meter-fill"
            style={{ width: `${score}%`, backgroundColor: getColor() }}
          />
        </div>
        <div className="meter-info">
          <span className="meter-score">{score}/100</span>
          <span className="meter-label" style={{ color: getColor() }}>
            {getLabel()}
          </span>
        </div>
      </div>
    </div>
  );
}

export default RiskMeter;
