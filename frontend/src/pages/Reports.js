import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Reports.css';

function Reports() {
  const navigate = useNavigate();
  const [reports, setReports] = useState([
    { id: 1, title: 'Weekly Security Summary', date: '2024-01-15', scans: 45, issues: 12 },
    { id: 2, title: 'Monthly Audit Report', date: '2024-01-01', scans: 156, issues: 38 },
    { id: 3, title: 'Critical Vulnerabilities', date: '2024-01-10', scans: 23, issues: 23 },
  ]);

  const handleGenerateReport = () => {
    const newReport = {
      id: reports.length + 1,
      title: `Report ${new Date().toLocaleDateString()}`,
      date: new Date().toISOString().split('T')[0],
      scans: Math.floor(Math.random() * 50) + 10,
      issues: Math.floor(Math.random() * 30) + 5
    };
    
    setReports(prev => [newReport, ...prev]);
    
    // Auto-download the generated report
    const reportData = {
      report_type: "Auralis Security Analysis Report",
      generated_at: new Date().toISOString(),
      title: newReport.title,
      date: newReport.date,
      summary: {
        total_scans: newReport.scans,
        total_issues: newReport.issues,
        scan_period: "Current period",
        analysis_coverage: "All Solidity contracts"
      },
      generated_by: "Auralis Smart Contract Security Auditor"
    };

    const dataStr = JSON.stringify(reportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `auralis-report-${newReport.date}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleViewReport = (report) => {
    const reportData = {
      report_type: "Auralis Security Analysis Report",
      title: report.title,
      generated_at: report.date,
      summary: {
        total_scans: report.scans,
        total_issues: report.issues,
        scan_period: "Report period",
        analysis_coverage: "All analyzed contracts"
      },
      generated_by: "Auralis Smart Contract Security Auditor"
    };

    const dataStr = JSON.stringify(reportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${report.title.replace(/\s+/g, '-').toLowerCase()}-${report.id}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="reports-page">
      <div className="page-header">
        <div>
          <h1>Reports</h1>
          <p>Detailed security analysis reports</p>
        </div>
        <button className="generate-btn" onClick={handleGenerateReport}>
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
            <button className="view-report-btn" onClick={() => handleViewReport(report)}>
              View Report
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Reports;
