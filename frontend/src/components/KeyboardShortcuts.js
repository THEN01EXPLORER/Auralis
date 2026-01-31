import React, { useState } from 'react';
import '../styles/KeyboardShortcuts.css';

function KeyboardShortcuts({ shortcuts }) {
  const [isOpen, setIsOpen] = useState(false);

  const formatKey = (shortcut) => {
    const parts = [];
    if (shortcut.ctrl) parts.push('Ctrl');
    if (shortcut.meta) parts.push('Cmd');
    if (shortcut.shift) parts.push('Shift');
    if (shortcut.alt) parts.push('Alt');
    parts.push(shortcut.key.toUpperCase());
    return parts.join(' + ');
  };

  if (!isOpen) {
    return (
      <button
        className="shortcuts-toggle"
        onClick={() => setIsOpen(true)}
        aria-label="Show keyboard shortcuts"
        title="Keyboard Shortcuts (?)"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
      </button>
    );
  }

  return (
    <div className="shortcuts-modal" onClick={() => setIsOpen(false)}>
      <div className="shortcuts-content" onClick={(e) => e.stopPropagation()}>
        <div className="shortcuts-header">
          <h2>⌨️ Keyboard Shortcuts</h2>
          <button className="shortcuts-close" onClick={() => setIsOpen(false)}>×</button>
        </div>
        <div className="shortcuts-list">
          {shortcuts.map((shortcut, index) => (
            <div key={index} className="shortcut-item">
              <div className="shortcut-description">{shortcut.description}</div>
              <div className="shortcut-keys">
                {formatKey(shortcut).split(' + ').map((key, i) => (
                  <kbd key={i} className="shortcut-key">{key}</kbd>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default KeyboardShortcuts;


