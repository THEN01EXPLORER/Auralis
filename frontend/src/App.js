import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './styles/App.css';
import Sidebar from './components/Sidebar';
import ErrorBoundary from './components/ErrorBoundary';
import KeyboardShortcuts from './components/KeyboardShortcuts';
import SkeletonLoader from './components/SkeletonLoader';
import { ThemeProvider, useTheme } from './contexts/ThemeContext';
import { useKeyboardShortcuts } from './hooks/useKeyboardShortcuts';

// Lazy load pages for code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Analyze = lazy(() => import('./pages/Analyze'));
const History = lazy(() => import('./pages/History'));
const Reports = lazy(() => import('./pages/Reports'));
const Settings = lazy(() => import('./pages/Settings'));

function AppContent() {
  const navigate = useNavigate();
  const { toggleTheme } = useTheme();

  // Keyboard shortcuts
  useKeyboardShortcuts([
    { key: 'k', ctrl: true, action: () => navigate('/') },
    { key: 'a', ctrl: true, action: () => navigate('/analyze') },
    { key: 'h', ctrl: true, action: () => navigate('/history') },
    { key: 'r', ctrl: true, action: () => navigate('/reports') },
    { key: ',', ctrl: true, action: () => navigate('/settings') },
    { key: '/', action: () => document.querySelector('.shortcuts-toggle')?.click() },
    { key: 't', action: () => toggleTheme() },
  ]);

  const shortcuts = [
    { key: 'k', ctrl: true, description: 'Go to Dashboard' },
    { key: 'a', ctrl: true, description: 'Go to Analyze' },
    { key: 'h', ctrl: true, description: 'Go to History' },
    { key: 'r', ctrl: true, description: 'Go to Reports' },
    { key: ',', ctrl: true, description: 'Go to Settings' },
    { key: 't', description: 'Toggle light/dark theme' },
    { key: '/', description: 'Show keyboard shortcuts' },
  ];

  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <div className="App">
        <Sidebar />
        <main id="main-content" className="main-content" role="main">
          <Suspense fallback={<SkeletonLoader type="dashboard" />}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analyze" element={<Analyze />} />
              <Route path="/history" element={<History />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Suspense>
        </main>
      </div>
      <KeyboardShortcuts shortcuts={shortcuts} />
    </>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <Router>
          <AppContent />
        </Router>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
