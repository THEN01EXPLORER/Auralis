import React, { useState, useEffect } from 'react';
import '../styles/Settings.css';

function Settings() {
  const [settings, setSettings] = useState({
    notifications: true,
    autoScan: false,
    darkMode: true,
  });

  // Load settings from localStorage on mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('auralisSettings');
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings));
    }
  }, []);

  // Save settings to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('auralisSettings', JSON.stringify(settings));
  }, [settings]);

  const handleToggle = (key) => {
    setSettings(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleSelectChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="settings-page">
      <div className="page-header">
        <div>
          <h1>Settings</h1>
          <p>Configure your Auralis preferences</p>
        </div>
      </div>

      <div className="settings-grid">
        <div className="settings-card">
          <h3>⚙️ General Settings</h3>
          
          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-title">Enable Notifications</div>
              <div className="setting-description">Receive alerts for scan completions</div>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.notifications}
                onChange={() => handleToggle('notifications')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-title">Auto-Scan on Upload</div>
              <div className="setting-description">Automatically analyze uploaded contracts</div>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.autoScan}
                onChange={() => handleToggle('autoScan')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-title">Dark Mode</div>
              <div className="setting-description">Use dark theme interface</div>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.darkMode}
                onChange={() => handleToggle('darkMode')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>

        <div className="settings-card">
          <h3>📊 Analysis Preferences</h3>
          
          <div className="setting-item">
            <label className="setting-label">Scan Depth</label>
            <select 
              className="setting-select"
              value={settings.scanDepth || 'Standard Scan'}
              onChange={(e) => handleSelectChange('scanDepth', e.target.value)}
            >
              <option>Quick Scan</option>
              <option>Standard Scan</option>
              <option>Deep Scan</option>
            </select>
          </div>

          <div className="setting-item">
            <label className="setting-label">Report Format</label>
            <select 
              className="setting-select"
              value={settings.reportFormat || 'JSON'}
              onChange={(e) => handleSelectChange('reportFormat', e.target.value)}
            >
              <option>JSON</option>
              <option>PDF</option>
              <option>HTML</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
