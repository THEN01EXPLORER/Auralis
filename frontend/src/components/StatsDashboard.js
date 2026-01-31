import React, { memo } from 'react';
import '../styles/StatsDashboard.css';

const StatsDashboard = memo(function StatsDashboard({ totalScans = 0, totalVulnerabilities = 0, avgRiskScore = 0 }) {
  return (
    <div className="stats-dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🔍</div>
          <div className="stat-content">
            <div className="stat-value">{totalScans}</div>
            <div className="stat-label">Total Scans</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <div className="stat-value">{totalVulnerabilities}</div>
            <div className="stat-label">Critical Issues</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <div className="stat-value">{avgRiskScore}/100</div>
            <div className="stat-label">Avg Risk Score</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🤖</div>
          <div className="stat-content">
            <div className="stat-value">AI + Static</div>
            <div className="stat-label">Analysis Mode</div>
          </div>
        </div>
      </div>
    </div>
  );
});

export default StatsDashboard;
