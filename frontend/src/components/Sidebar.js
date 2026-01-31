import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import '../styles/Sidebar.css';

function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false); // Default to expanded
  const location = useLocation();

  const menuItems = [
    { 
      path: '/', 
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
          <polyline points="9 22 9 12 15 12 15 22"/>
        </svg>
      ),
      label: 'Dashboard', 
      description: 'Overview & Analytics' 
    },
    { 
      path: '/analyze', 
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
      ),
      label: 'Analyze', 
      description: 'Scan Contracts' 
    },
    { 
      path: '/history', 
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/>
        </svg>
      ),
      label: 'History', 
      description: 'Past Scans' 
    },
    { 
      path: '/reports', 
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
      ),
      label: 'Reports', 
      description: 'Detailed Reports' 
    },
    { 
      path: '/settings', 
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="3"/>
          <path d="M12 1v6m0 6v6M1 12h6m6 0h6"/>
        </svg>
      ),
      label: 'Settings', 
      description: 'Configuration' 
    },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <div className="logo-section">
          <div className="logo-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" 
                    stroke="url(#logo-gradient)" 
                    strokeWidth="2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                    fill="url(#logo-gradient-fill)"/>
              <defs>
                <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#00f5ff"/>
                  <stop offset="100%" stopColor="#a855f7"/>
                </linearGradient>
                <linearGradient id="logo-gradient-fill" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#00f5ff" stopOpacity="0.1"/>
                  <stop offset="100%" stopColor="#a855f7" stopOpacity="0.1"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          {!isCollapsed && (
            <div className="logo-text">
              <h2>Auralis</h2>
              <p>Security Auditor</p>
            </div>
          )}
        </div>
        <button 
          className="collapse-btn" 
          onClick={() => setIsCollapsed(!isCollapsed)}
          title={isCollapsed ? 'Expand' : 'Collapse'}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            {isCollapsed ? (
              <path d="M9 18l6-6-6-6"/>
            ) : (
              <path d="M15 18l-6-6 6-6"/>
            )}
          </svg>
        </button>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
            title={isCollapsed ? item.label : ''}
            aria-label={item.label}
            aria-current={isActive(item.path) ? 'page' : undefined}
          >
            <span className="nav-icon">{item.icon}</span>
            {!isCollapsed && (
              <div className="nav-content">
                <span className="nav-label">{item.label}</span>
                <span className="nav-description">{item.description}</span>
              </div>
            )}
            {isActive(item.path) && <div className="active-indicator" />}
          </Link>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="social-links">
          <a 
            href="https://github.com/THEN01EXPLORER/Auralis" 
            target="_blank" 
            rel="noopener noreferrer"
            className="social-link"
            title="GitHub Repository"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
          </a>
          <a 
            href="https://twitter.com/intent/tweet?text=Check%20out%20Auralis%20-%20AI-powered%20smart%20contract%20security%20auditor!&url=https://auralis-tawny.vercel.app" 
            target="_blank" 
            rel="noopener noreferrer"
            className="social-link"
            title="Share on Twitter"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
            </svg>
          </a>
          <a 
            href="https://www.linkedin.com/sharing/share-offsite/?url=https://auralis-tawny.vercel.app" 
            target="_blank" 
            rel="noopener noreferrer"
            className="social-link"
            title="Share on LinkedIn"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
          </a>
        </div>
        {!isCollapsed && (
          <div className="version-info">
            <span>v1.0.0</span>
            <span className="dot">•</span>
            <span>20 Patterns</span>
          </div>
        )}
        <div className="sidebar-actions">
          <ThemeToggle />
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
