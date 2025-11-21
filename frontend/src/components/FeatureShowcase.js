import React from 'react';
import '../styles/FeatureShowcase.css';

function FeatureShowcase() {
  const features = [
    {
      icon: '🤖',
      title: 'AI-Powered Analysis',
      description: 'Advanced Claude AI analyzes contracts for complex vulnerabilities',
      gradient: 'linear-gradient(135deg, #61dafb 0%, #4fa8c5 100%)'
    },
    {
      icon: '⚡',
      title: 'Static Pattern Matching',
      description: 'Lightning-fast detection of common security patterns',
      gradient: 'linear-gradient(135deg, #ffa500 0%, #ff6b35 100%)'
    },
    {
      icon: '🔄',
      title: 'Hybrid Orchestration',
      description: 'Combines multiple analysis engines for comprehensive audits',
      gradient: 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)'
    },
    {
      icon: '📊',
      title: 'DREAD Scoring',
      description: 'Industry-standard risk assessment methodology',
      gradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
    },
    {
      icon: '📁',
      title: 'Repository Scanning',
      description: 'Analyze entire GitHub repos with one click',
      gradient: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'
    },
    {
      icon: '📄',
      title: 'PDF Reports',
      description: 'Professional audit reports ready for stakeholders',
      gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
    }
  ];

  return (
    <div className="feature-showcase">
      <div className="showcase-header">
        <h2>🚀 Powerful Features</h2>
        <p>Enterprise-grade security analysis at your fingertips</p>
      </div>
      <div className="features-grid">
        {features.map((feature, index) => (
          <div 
            key={index} 
            className="feature-card"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="feature-icon-wrapper" style={{ background: feature.gradient }}>
              <span className="feature-icon">{feature.icon}</span>
            </div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
            <div className="feature-pulse" style={{ background: feature.gradient }} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default FeatureShowcase;
