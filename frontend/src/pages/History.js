import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/History.css';

function History() {
  const navigate = useNavigate();
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

  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('All Types');
  const [riskFilter, setRiskFilter] = useState('All Risk Levels');

  const getRiskClass = (score) => {
    if (score > 70) return 'high';
    if (score > 40) return 'medium';
    return 'low';
  };

  const getRiskLevel = (score) => {
    if (score > 70) return 'High Risk';
    if (score > 40) return 'Medium Risk';
    return 'Low Risk';
  };

  const handleExportHistory = () => {
    const exportData = {
      report_type: "Auralis Analysis History Export",
      exported_at: new Date().toISOString(),
      total_analyses: historyItems.length,
      history: historyItems.map(item => ({
        timestamp: item.timestamp,
        type: item.type,
        name: item.name,
        risk_score: item.riskScore,
        vulnerabilities: item.vulnerabilities,
        status: item.status
      })),
      generated_by: "Auralis Smart Contract Security Auditor"
    };

    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `auralis-history-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleViewReport = (item) => {
    // Navigate to analyze page - in a real app, this would load the specific report
    navigate('/analyze');
  };

  const handleDownload = (item) => {
    const reportData = {
      report_type: "Auralis Security Analysis Report",
      analyzed_at: item.timestamp,
      analysis_type: item.type,
      contract_name: item.name,
      risk_assessment: {
        score: item.riskScore,
        level: getRiskLevel(item.riskScore)
      },
      vulnerabilities_found: item.vulnerabilities,
      status: item.status,
      generated_by: "Auralis Smart Contract Security Auditor"
    };

    const dataStr = JSON.stringify(reportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `auralis-report-${item.name}-${item.id}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Filter items based on search and filters
  const filteredItems = historyItems.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = typeFilter === 'All Types' || item.type === typeFilter;
    const matchesRisk = riskFilter === 'All Risk Levels' || getRiskLevel(item.riskScore) === riskFilter;
    return matchesSearch && matchesType && matchesRisk;
  });

  return (
    <div className="history-page">
      <div className="page-header">
        <div>
          <h1>Analysis History</h1>
          <p>View all your past security scans</p>
        </div>
        <button className="export-btn" onClick={handleExportHistory}>
          💾 Export History
        </button>
      </div>

      <div className="history-filters">
        <input 
          type="text" 
          placeholder="Search by name..." 
          className="search-input"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <select 
          className="filter-select"
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
        >
          <option>All Types</option>
          <option>Contract</option>
          <option>Repository</option>
        </select>
        <select 
          className="filter-select"
          value={riskFilter}
          onChange={(e) => setRiskFilter(e.target.value)}
        >
          <option>All Risk Levels</option>
          <option>High Risk</option>
          <option>Medium Risk</option>
          <option>Low Risk</option>
        </select>
      </div>

      <div className="history-list">
        {filteredItems.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No matching history items found
          </div>
        ) : (
          filteredItems.map(item => (
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
                <button className="view-btn" onClick={() => handleViewReport(item)}>View Report</button>
                <button className="download-btn" onClick={() => handleDownload(item)}>Download</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default History;
