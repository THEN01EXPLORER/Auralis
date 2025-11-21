import React, { useState } from 'react';
import '../styles/History.css';

function History() {
  const [historyItems] = useState([
    {
      id: 1,
      timestamp: '2024-01-15 14:30',
      type: 'Contract',
      name: 'TokenContract.sol',
      riskScore: 65,
      vulnerabilities: 8,
      status: 'completed'
    },
    {
      id: 2,
      timestamp: '2024-01-15 10:15',
      type: 'Repository',
      name: 'github.com/user/defi-protocol',
      riskScore: 42,
      vulnerabilities: 5,
      status: 'completed'
    },
    {
      id: 3,
      timestamp: '2024-01-14 16:45',
      type: 'Contract',
      name: 'NFTMarketplace.sol',
      riskScore: 28,
      vulnerabilities: 3,
      status: 'completed'
    },
  ]);

  const getRiskClass = (score) => {
    if (score > 70) return 'high';
    if (score > 40) return 'medium';
    return 'low';
  };

  return (
    <div className="history-page">
      <div className="page-header">
        <div>
          <h1>Analysis History</h1>
          <p>View all your past security scans</p>
        </div>
        <button className="export-btn">
          💾 Export History
        </button>
      </div>

      <div className="history-filters">
        <input 
          type="text" 
          placeholder="Search by name..." 
          className="search-input"
        />
        <select className="filter-select">
          <option>All Types</option>
          <option>Contract</option>
          <option>Repository</option>
        </select>
        <select className="filter-select">
          <option>All Risk Levels</option>
          <option>High Risk</option>
          <option>Medium Risk</option>
          <option>Low Risk</option>
        </select>
      </div>

      <div className="history-list">
        {historyItems.map(item => (
          <div key={item.id} className="history-card">
            <div className="history-card-header">
              <div className="history-type-badge">{item.type}</div>
              <div className="history-timestamp">{item.timestamp}</div>
            </div>
            
            <div className="history-card-body">
              <h3>{item.name}</h3>
              <div className="history-stats">
                <div className="stat">
                  <span className="stat-label">Risk Score</span>
                  <span className={`stat-value risk-${getRiskClass(item.riskScore)}`}>
                    {item.riskScore}/100
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Vulnerabilities</span>
                  <span className="stat-value">{item.vulnerabilities}</span>
                </div>
              </div>
            </div>
            
            <div className="history-card-footer">
              <button className="view-btn">View Report</button>
              <button className="download-btn">Download</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;
