import React, { useState, useEffect, memo } from 'react';
import { useNavigate } from 'react-router-dom';
import StatsDashboard from '../components/StatsDashboard';
import SkeletonLoader from '../components/SkeletonLoader';
import { getStats } from '../services/api';
import { useToast } from '../hooks/useToast';
import ToastContainer from '../components/ToastContainer';
import '../styles/Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();
  const toast = useToast();
  const [stats, setStats] = useState({
    totalScans: 0,
    criticalFound: 0,
    avgRiskScore: 0,
    detectionRate: 95
  });
  const [loading, setLoading] = useState(true);

  const recentScans = [
    { id: 1, name: 'TokenContract.sol', risk: 65, date: '2 hours ago', status: 'High Risk', vulnerabilities: 8 },
    { id: 2, name: 'NFTMarketplace.sol', risk: 35, date: '5 hours ago', status: 'Medium Risk', vulnerabilities: 3 },
    { id: 3, name: 'DeFiProtocol.sol', risk: 15, date: '1 day ago', status: 'Low Risk', vulnerabilities: 1 },
    { id: 4, name: 'StakingPool.sol', risk: 45, date: '2 days ago', status: 'Medium Risk', vulnerabilities: 5 },
  ];

  const securityTrends = [
    { month: 'Jan', scans: 45, issues: 12 },
    { month: 'Feb', scans: 52, issues: 8 },
    { month: 'Mar', scans: 48, issues: 15 },
    { month: 'Apr', scans: 67, issues: 10 },
  ];

  useEffect(() => {
    let isMounted = true;
    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await getStats();
        if (isMounted) {
          // Calculate stats from API data if available
          // Backend returns: { analysis: { total_scans, total_vulnerabilities, avg_risk_score } }
          const analysis = data.analysis || {};
          setStats({
            totalScans: analysis.total_scans || 0,
            criticalFound: analysis.total_vulnerabilities || 0,
            avgRiskScore: analysis.avg_risk_score || 0,
            detectionRate: 95
          });
        }
      } catch (error) {
        console.error('Failed to load stats:', error);
        // Silently use default stats - don't show warnings on every render
        if (isMounted) {
          setStats({
            totalScans: 0,
            criticalFound: 0,
            avgRiskScore: 0,
            detectionRate: 95
          });
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchStats();
    
    return () => {
      isMounted = false;
    };
  }, []); // Remove toast from dependencies to prevent re-renders

  const handleNewScan = () => {
    navigate('/analyze');
  };

  const handleExport = () => {
    toast.info('Export feature coming soon!');
  };

  return (
    <div className="dashboard-page">
      <ToastContainer toasts={toast.toasts} removeToast={toast.removeToast} />
      <div className="page-header">
        <div className="header-content">
          <div className="header-text">
            <h1>Dashboard</h1>
            <p>Overview of your security analysis</p>
          </div>
          <div className="header-actions">
            <button className="header-btn secondary" onClick={handleExport}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              Export
            </button>
            <button className="header-btn primary" onClick={handleNewScan}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
              New Scan
            </button>
          </div>
        </div>
      </div>

      {loading ? (
        <SkeletonLoader type="dashboard" />
      ) : (
        <StatsDashboard 
          totalScans={stats.totalScans}
          totalVulnerabilities={stats.criticalFound}
          avgRiskScore={stats.avgRiskScore}
          detectionRate={stats.detectionRate}
        />
      )}

      <div className="dashboard-grid">
        <div className="dashboard-card recent-activity-card">
          <div className="card-header">
            <h3>📈 Recent Activity</h3>
            <button className="view-all-btn">View All</button>
          </div>
          <div className="activity-list">
            {recentScans.map(scan => (
              <div key={scan.id} className="activity-item">
                <div className="activity-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                    <polyline points="14 2 14 8 20 8" stroke="currentColor" strokeWidth="2"/>
                  </svg>
                </div>
                <div className="activity-details">
                  <span className="activity-name">{scan.name}</span>
                  <span className="activity-meta">
                    <span className="activity-date">{scan.date}</span>
                    <span className="activity-vulnerabilities">{scan.vulnerabilities} issues found</span>
                  </span>
                </div>
                <div className="activity-status-wrapper">
                  <span className={`activity-status ${scan.status.toLowerCase().replace(' ', '-')}`}>
                    {scan.status}
                  </span>
                  <div className="risk-bar">
                    <div className="risk-fill" style={{width: `${scan.risk}%`}}></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="dashboard-card security-trends-card">
          <div className="card-header">
            <h3>📊 Security Trends</h3>
            <select className="time-filter">
              <option>Last 4 Months</option>
              <option>Last 6 Months</option>
              <option>Last Year</option>
            </select>
          </div>
          <div className="trends-chart">
            {securityTrends.map((trend, index) => (
              <div key={index} className="trend-bar-group">
                <div className="trend-bars">
                  <div className="trend-bar scans" style={{height: `${(trend.scans / 70) * 100}%`}}>
                    <span className="bar-value">{trend.scans}</span>
                  </div>
                  <div className="trend-bar issues" style={{height: `${(trend.issues / 70) * 100}%`}}>
                    <span className="bar-value">{trend.issues}</span>
                  </div>
                </div>
                <span className="trend-label">{trend.month}</span>
              </div>
            ))}
          </div>
          <div className="chart-legend">
            <div className="legend-item">
              <span className="legend-color scans"></span>
              <span>Total Scans</span>
            </div>
            <div className="legend-item">
              <span className="legend-color issues"></span>
              <span>Issues Found</span>
            </div>
          </div>
        </div>

        <div className="dashboard-card quick-actions-card">
          <h3>🎯 Quick Actions</h3>
          <div className="quick-actions">
            <button className="action-btn primary" onClick={handleNewScan}>
              <div className="action-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
                  <path d="m21 21-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <div className="action-content">
                <span className="action-title">New Scan</span>
                <span className="action-desc">Analyze contract</span>
              </div>
            </button>
            <button className="action-btn secondary">
              <div className="action-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M3 3v18h18" stroke="currentColor" strokeWidth="2"/>
                  <path d="m19 9-5 5-4-4-5 5" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <div className="action-content">
                <span className="action-title">View Reports</span>
                <span className="action-desc">Detailed analysis</span>
              </div>
            </button>
            <button className="action-btn secondary">
              <div className="action-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0z" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <div className="action-content">
                <span className="action-title">History</span>
                <span className="action-desc">Past scans</span>
              </div>
            </button>
            <button className="action-btn secondary">
              <div className="action-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
                  <path d="M12 1v6m0 6v6M1 12h6m6 0h6" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <div className="action-content">
                <span className="action-title">Settings</span>
                <span className="action-desc">Configure app</span>
              </div>
            </button>
          </div>
        </div>

        <div className="dashboard-card threat-intel-card">
          <div className="card-header">
            <h3>🔒 Threat Intelligence</h3>
            <span className="live-indicator">● Live</span>
          </div>
          <div className="threat-list">
            <div className="threat-item critical">
              <div className="threat-severity">Critical</div>
              <div className="threat-info">
                <span className="threat-title">Reentrancy Vulnerability</span>
                <span className="threat-count">3 detected this week</span>
              </div>
            </div>
            <div className="threat-item high">
              <div className="threat-severity">High</div>
              <div className="threat-info">
                <span className="threat-title">Integer Overflow</span>
                <span className="threat-count">5 detected this week</span>
              </div>
            </div>
            <div className="threat-item medium">
              <div className="threat-severity">Medium</div>
              <div className="threat-info">
                <span className="threat-title">Access Control Issues</span>
                <span className="threat-count">8 detected this week</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
