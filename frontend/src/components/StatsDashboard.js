import React, { memo } from 'react';
import '../styles/StatsDashboard.css';

const StatsDashboard = memo(function StatsDashboard({ totalScans = 0, totalVulnerabilities = 0, avgRiskScore = 0, detectionRate = 95 }) {
  const getPerformanceGrade = () => {
    if (avgRiskScore < 30) return { grade: 'A+', color: '#4bff4b', label: 'Excellent' };
    if (avgRiskScore < 50) return { grade: 'B+', color: '#61dafb', label: 'Good' };
    if (avgRiskScore < 70) return { grade: 'C+', color: '#ffa500', label: 'Fair' };
    return { grade: 'D', color: '#ff4b4b', label: 'Needs Improvement' };
  };

  const performance = getPerformanceGrade();

  return (
    <div className="stats-dashboard">
      <div className="dashboard-header">
        <h2>📊 Analysis Dashboard</h2>
        <div className="performance-badge" style={{ borderColor: performance.color }}>
          <div className="grade" style={{ color: performance.color }}>{performance.grade}</div>
          <div className="grade-label">{performance.label}</div>
        </div>
      </div>
      
      <div className="stats-grid">
        <div className="stat-box">
          <div className="stat-icon">🔍</div>
          <div className="stat-info">
            <div className="stat-number">{totalScans}</div>
            <div className="stat-text">Contracts Analyzed</div>
          </div>
        </div>
        
        <div className="stat-box critical">
          <div className="stat-icon">⚠️</div>
          <div className="stat-info">
            <div className="stat-number">{totalVulnerabilities}</div>
            <div className="stat-text">Critical Issues Found</div>
          </div>
        </div>
        
        <div className="stat-box">
          <div className="stat-icon">📈</div>
          <div className="stat-info">
            <div className="stat-number">{avgRiskScore}/100</div>
            <div className="stat-text">Average Risk Score</div>
          </div>
        </div>
        
        <div className="stat-box">
          <div className="stat-icon">🎯</div>
          <div className="stat-info">
            <div className="stat-number">{detectionRate}%</div>
            <div className="stat-text">Detection Rate</div>
          </div>
        </div>
      </div>
      
      <div className="progress-section">
        <div className="progress-label">
          <span>Security Score</span>
          <span>{100 - avgRiskScore}/100</span>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ 
              width: `${100 - avgRiskScore}%`,
              background: avgRiskScore < 50 ? '#4bff4b' : avgRiskScore < 70 ? '#ffa500' : '#ff4b4b'
            }}
          />
        </div>
      </div>
    </div>
  );
});

export default StatsDashboard;
