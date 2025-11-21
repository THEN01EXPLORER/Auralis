import React from 'react';
import '../styles/ProgressIndicator.css';

function ProgressIndicator({ progress, message = 'Analyzing...', showPercentage = true }) {
  return (
    <div className="progress-indicator">
      <div className="progress-header">
        <div className="progress-spinner">
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
        </div>
        <div className="progress-info">
          <span className="progress-message">{message}</span>
          {showPercentage && progress !== null && (
            <span className="progress-percentage">{Math.round(progress)}%</span>
          )}
        </div>
      </div>
      {progress !== null && (
        <div className="progress-bar-container">
          <div 
            className="progress-bar-fill" 
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      )}
    </div>
  );
}

export default ProgressIndicator;


