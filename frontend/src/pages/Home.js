import React, { useState } from 'react';
import CodeEditor from '../components/CodeEditor';
import VulnerabilityReport from '../components/VulnerabilityReport';
import { analyzeContract } from '../services/api';
import '../styles/Home.css';

function Home() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [highlightLine, setHighlightLine] = useState(null);

  const handleAnalyze = async (code) => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeContract(code);
      setReport(result);
    } catch (error) {
      setError(error.message || 'Failed to analyze contract. Please check if the backend is running.');
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
        <CodeEditor onAnalyze={handleAnalyze} highlightLine={highlightLine} />
        <VulnerabilityReport report={report} loading={loading} error={error} onLineClick={handleLineClick} />
      </div>
    </div>
  );
}

export default Home;
