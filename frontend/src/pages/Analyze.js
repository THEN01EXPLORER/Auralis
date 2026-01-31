import React, { useState, memo, useCallback } from 'react';
import CodeEditor from '../components/CodeEditor';
import VulnerabilityReport from '../components/VulnerabilityReport';
import ProgressIndicator from '../components/ProgressIndicator';
import ToastContainer from '../components/ToastContainer';
import { analyzeContract, analyzeRepo } from '../services/api';
import { useToast } from '../hooks/useToast';
import { validateContractCode, validateGitHubUrl, sanitizeInput } from '../utils/validation';
import '../styles/Analyze.css';

const Analyze = memo(function Analyze() {
  const toast = useToast();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);
  const [highlightLine, setHighlightLine] = useState(null);
  const [repoUrl, setRepoUrl] = useState('');
  const [analysisMode, setAnalysisMode] = useState('code');
  const [currentCode, setCurrentCode] = useState('');

  const handleAnalyze = useCallback(async (code) => {
    // Validate input
    const validation = validateContractCode(code);
    if (!validation.valid) {
      toast.error(validation.error);
      return;
    }
    if (validation.warning) {
      toast.warning(validation.warning, 4000);
    }

    // Sanitize input
    const sanitizedCode = sanitizeInput(code);
    if (!sanitizedCode) {
      toast.error('Invalid contract code');
      return;
    }

    // Store the current code for export
    setCurrentCode(sanitizedCode);

    setLoading(true);
    setError(null);
    setProgress(0);
    setAnalysisMode('code');

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 300);

      toast.info('Starting analysis...');
      const result = await analyzeContract(sanitizedCode);

      clearInterval(progressInterval);
      setProgress(100);
      setReport(result);

      const vulnCount = result.vulnerabilities?.length || 0;
      if (vulnCount > 0) {
        toast.warning(`Found ${vulnCount} vulnerability${vulnCount > 1 ? 'ies' : ''}`, 6000);
      } else {
        toast.success('No vulnerabilities detected!', 4000);
      }

      setTimeout(() => setProgress(null), 1000);
    } catch (error) {
      setError(error.message || 'Failed to analyze contract');
      toast.error(error.message || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const handleAnalyzeRepo = useCallback(async () => {
    // Validate GitHub URL
    const validation = validateGitHubUrl(repoUrl);
    if (!validation.valid) {
      toast.error(validation.error);
      return;
    }

    setLoading(true);
    setError(null);
    setProgress(0);
    setAnalysisMode('repo');

    try {
      toast.info('Starting repository scan...');
      
      // Simulate progress for better UX since we are switching to sync
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) {
            return prev;
          }
          return prev + 5;
        });
      }, 500);

      // Import the synchronous API function
      const { analyzeRepo } = require('../services/api');

      // Call synchronous endpoint (No Auth Required)
      const result = await analyzeRepo(repoUrl);

      clearInterval(progressInterval);
      setProgress(100);
      setReport(result);

      toast.success(
        `Analyzed ${result.files_analyzed || '?'} file(s). Found ${result.total_vulnerabilities || 0} vulnerabilities`,
        6000
      );
      
    } catch (error) {
      console.error('Repo analysis error:', error);
      setError(typeof error === 'string' ? error : error.message || 'Failed to analyze repository');
      toast.error(typeof error === 'string' ? error : error.message || 'Repository analysis failed. Please check the URL and try again.');
    } finally {
      setLoading(false);
      setTimeout(() => setProgress(null), 1000);
    }
  }, [repoUrl, toast]);

  const handleLineClick = useCallback((lineNumber) => {
    setHighlightLine(lineNumber);
  }, []);

  return (
    <div className="analyze-page">
      <ToastContainer toasts={toast.toasts} removeToast={toast.removeToast} />
      <div className="page-header">
        <div>
          <h1>Analyze Smart Contracts</h1>
          <p>Scan your contracts for vulnerabilities and security issues</p>
        </div>
      </div>

      <div className="analyze-content">
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
                onKeyPress={(e) => e.key === 'Enter' && !loading && handleAnalyzeRepo()}
                disabled={loading}
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

        {loading && progress !== null && (
          <ProgressIndicator
            progress={progress}
            message={analysisMode === 'repo' ? 'Analyzing repository...' : 'Analyzing contract...'}
          />
        )}

        <VulnerabilityReport
          report={report}
          loading={loading && progress === null}
          error={error}
          onLineClick={handleLineClick}
          isRepoAnalysis={analysisMode === 'repo'}
          contractCode={currentCode}
        />
      </div>
    </div>
  );
});

export default Analyze;
