import React, { useState } from 'react';
import CodeEditor from '../components/CodeEditor';
import VulnerabilityReport from '../components/VulnerabilityReport';
import { analyzeContract, analyzeRepo } from '../services/api';
import '../styles/Home.css';

function Home() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [highlightLine, setHighlightLine] = useState(null);
  const [repoUrl, setRepoUrl] = useState('');
  const [analysisMode, setAnalysisMode] = useState('code'); // 'code' or 'repo'

  const handleAnalyze = async (code) => {
    setLoading(true);
    setError(null);
    setAnalysisMode('code');
    try {
      const result = await analyzeContract(code);
      setReport(result);
    } catch (error) {
      setError(error.message || 'Failed to analyze contract. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeRepo = async () => {
    if (!repoUrl.trim()) {
      setError('Please enter a GitHub repository URL');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysisMode('repo');
    try {
      const result = await analyzeRepo(repoUrl);
      setReport(result);
    } catch (error) {
      setError(error.message || 'Failed to analyze repository. Please check the URL and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLineClick = (lineNumber) => {
    setHighlightLine(lineNumber);
  };

  return (
    <div className="home">
      <header className="home-header">
        <h1>Auralis</h1>
        <p>Smart Contract Security Auditor</p>
      </header>
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
        />
      </div>
    </div>
  );
}

export default Home;
