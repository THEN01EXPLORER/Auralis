import React, { useState } from 'react';
import CodeEditor from '../components/CodeEditor';
import VulnerabilityReport from '../components/VulnerabilityReport';
import { analyzeContract } from '../services/api';
import '../styles/Home.css';

function Home() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (code) => {
    setLoading(true);
    try {
      const result = await analyzeContract(code);
      setReport(result);
    } catch (error) {
      alert('Error analyzing contract. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home">
      <header className="home-header">
        <h1>Auralis</h1>
        <p>Smart Contract Security Auditor</p>
      </header>
      <div className="home-content">
        <CodeEditor onAnalyze={handleAnalyze} />
        <VulnerabilityReport report={report} loading={loading} />
      </div>
    </div>
  );
}

export default Home;
