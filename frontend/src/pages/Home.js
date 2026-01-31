import React, { useState, useEffect } from 'react';
import CodeEditor from '../components/CodeEditor';
import VulnerabilityReport from '../components/VulnerabilityReport';
import StatsDashboard from '../components/StatsDashboard';
import FeatureShowcase from '../components/FeatureShowcase';
import ToastContainer from '../components/ToastContainer';
import { analyzeContract, analyzeRepo } from '../services/api';
import { useToast } from '../hooks/useToast';
import '../styles/Home.css';

function Home() {
  const toast = useToast();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [highlightLine, setHighlightLine] = useState(null);
  const [repoUrl, setRepoUrl] = useState('');
  const [analysisMode, setAnalysisMode] = useState('code'); // 'code' or 'repo'
  const [analysisHistory, setAnalysisHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [stats, setStats] = useState({ totalScans: 0, criticalFound: 0, avgRiskScore: 0 });
  const [darkMode, setDarkMode] = useState(true);
  const [currentCode, setCurrentCode] = useState('');

  const handleAnalyze = async (code) => {
    if (!code.trim()) {
      toast.warning('Please enter contract code to analyze');
      return;
    }

    // Store code for export
    setCurrentCode(code);

    setLoading(true);
    setError(null);
    setAnalysisMode('code');
    try {
      toast.info('Starting analysis...');
      const result = await analyzeContract(code);
      setReport(result);

      // Add to history
      const historyItem = {
        id: Date.now(),
        timestamp: new Date().toLocaleString(),
        riskScore: result.risk_score,
        vulnerabilities: result.vulnerabilities.length,
        type: 'Contract',
        snippet: code.substring(0, 50) + '...'
      };
      setAnalysisHistory(prev => [historyItem, ...prev].slice(0, 10));

      // Update stats
      updateStats(result);

      const vulnCount = result.vulnerabilities?.length || 0;
      if (vulnCount > 0) {
        toast.warning(`Found ${vulnCount} vulnerability${vulnCount > 1 ? 'ies' : ''}`, 6000);
      } else {
        toast.success('No vulnerabilities detected!', 4000);
      }
    } catch (error) {
      setError(error.message || 'Failed to analyze contract. Please check if the backend is running.');
      toast.error(error.message || 'Analysis failed. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const updateStats = (result) => {
    setStats(prev => {
      const newTotal = prev.totalScans + 1;
      const criticalCount = result.vulnerabilities.filter(v =>
        v.severity === 'Critical' || v.severity === 'High'
      ).length;
      return {
        totalScans: newTotal,
        criticalFound: prev.criticalFound + criticalCount,
        avgRiskScore: Math.round((prev.avgRiskScore * prev.totalScans + result.risk_score) / newTotal)
      };
    });
  };

  const handleAnalyzeRepo = async () => {
    if (!repoUrl.trim()) {
      toast.error('Please enter a GitHub repository URL');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysisMode('repo');
    try {
      toast.info('Cloning and analyzing repository...');
      const result = await analyzeRepo(repoUrl);
      setReport(result);

      // Add to history
      const historyItem = {
        id: Date.now(),
        timestamp: new Date().toLocaleString(),
        riskScore: Math.round(result.total_vulnerabilities / result.files_analyzed * 10),
        vulnerabilities: result.total_vulnerabilities,
        type: 'Repository',
        snippet: repoUrl
      };
      setAnalysisHistory(prev => [historyItem, ...prev].slice(0, 10));

      toast.success(
        `Analyzed ${result.files_analyzed} file(s). Found ${result.total_vulnerabilities} vulnerability${result.total_vulnerabilities !== 1 ? 'ies' : ''}`,
        6000
      );
    } catch (error) {
      setError(error.message || 'Failed to analyze repository. Please check the URL and try again.');
      toast.error(error.message || 'Repository analysis failed. Please check the URL and try again.');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = () => {
    if (!report) {
      toast.warning('No report available to download');
      return;
    }
    try {
      const dataStr = JSON.stringify(report, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `auralis-report-${Date.now()}.json`;
      link.click();
      URL.revokeObjectURL(url);
      toast.success('Report downloaded successfully!');
    } catch (error) {
      toast.error('Failed to download report');
    }
  };

  const handleLineClick = (lineNumber) => {
    setHighlightLine(lineNumber);
  };

  return (
    <div className={`home ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <ToastContainer toasts={toast.toasts} removeToast={toast.removeToast} />
      <header className="home-header">
        <div className="header-top">
          <div className="brand">
            <div className="logo">🛡️</div>
            <div>
              <h1>Auralis</h1>
              <p>AI-Powered Smart Contract Security Auditor</p>
            </div>
          </div>
          <div className="header-controls">
            <button
              className="icon-btn history-btn"
              onClick={() => setShowHistory(!showHistory)}
              title="Analysis History"
            >
              📊 History ({analysisHistory.length})
            </button>
            <button
              className="icon-btn download-btn"
              onClick={downloadReport}
              disabled={!report}
              title="Download Report"
            >
              💾 Export
            </button>
          </div>
        </div>
        <StatsDashboard
          totalScans={stats.totalScans}
          totalVulnerabilities={stats.criticalFound}
          avgRiskScore={stats.avgRiskScore}
        />
      </header>

      {showHistory && (
        <div className="history-panel">
          <div className="history-header">
            <h3>📜 Recent Analysis History</h3>
            <button className="close-btn" onClick={() => setShowHistory(false)}>✕</button>
          </div>
          <div className="history-list">
            {analysisHistory.length === 0 ? (
              <div className="history-empty">No analysis history yet</div>
            ) : (
              analysisHistory.map(item => (
                <div key={item.id} className="history-item">
                  <div className="history-info">
                    <span className="history-type">{item.type}</span>
                    <span className="history-time">{item.timestamp}</span>
                  </div>
                  <div className="history-stats">
                    <span className={`risk-badge risk-${item.riskScore > 70 ? 'high' : item.riskScore > 40 ? 'medium' : 'low'}`}>
                      Risk: {item.riskScore}
                    </span>
                    <span className="vuln-count">🔍 {item.vulnerabilities} issues</span>
                  </div>
                  <div className="history-snippet">{item.snippet}</div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      <div className="home-content">
        <div className="input-section">
          <CodeEditor onAnalyze={handleAnalyze} highlightLine={highlightLine} />

          <div className="repo-scanner-section">
            <div className="section-divider">
              <span>OR</span>
            </div>
            <h3>🔗 Analyze GitHub Repository</h3>
            <div className="repo-input-group">
              <input
                type="text"
                className="repo-url-input"
                placeholder="https://github.com/username/repository"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAnalyzeRepo()}
              />
              <button
                className="analyze-repo-button"
                onClick={handleAnalyzeRepo}
                disabled={loading}
              >
                {loading && analysisMode === 'repo' ? 'Analyzing...' : 'Analyze Repo'}
              </button>
            </div>
          </div>
        </div>

        <VulnerabilityReport
          report={report}
          loading={loading}
          error={error}
          onLineClick={handleLineClick}
          isRepoAnalysis={analysisMode === 'repo'}
          contractCode={currentCode}
        />
      </div>

      <FeatureShowcase />
    </div>
  );
}

export default Home;
