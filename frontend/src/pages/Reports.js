import React from 'react';
import '../styles/Reports.css';

function Reports() {
  const reports = [
    { id: 1, title: 'Weekly Security Summary', date: '2024-01-15', scans: 45, issues: 12 },
    { id: 2, title: 'Monthly Audit Report', date: '2024-01-01', scans: 156, issues: 38 },
    { id: 3, title: 'Critical Vulnerabilities', date: '2024-01-10', scans: 23, issues: 23 },
  ];

  return (
    <div className="reports-page">
      <div className="page-header">
        <div>
          <h1>Reports</h1>
          <p>Detailed security analysis reports</p>
        </div>
        <button className="generate-btn">
          ✨ Generate New Report
        </button>
      </div>

      <div className="reports-grid">
        {reports.map(report => (
          <div key={report.id} className="report-card">
            <div className="report-icon">📄</div>
            <h3>{report.title}</h3>
            <p className="report-date">{report.date}</p>
            <div className="report-stats">
              <div className="report-stat">
                <span className="stat-number">{report.scans}</span>
                <span className="stat-label">Scans</span>
              </div>
              <div className="report-stat">
                <span className="stat-number">{report.issues}</span>
                <span className="stat-label">Issues</span>
              </div>
            </div>
            <button className="view-report-btn">View Report</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Reports;
