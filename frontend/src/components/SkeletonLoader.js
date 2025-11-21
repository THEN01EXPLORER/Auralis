import React from 'react';
import '../styles/SkeletonLoader.css';

function SkeletonLoader({ type = 'default', count = 1, className = '' }) {
  const skeletons = Array(count).fill(0);

  if (type === 'card') {
    return (
      <>
        {skeletons.map((_, i) => (
          <div key={i} className={`skeleton-card ${className}`}>
            <div className="skeleton-header">
              <div className="skeleton-avatar"></div>
              <div className="skeleton-text-group">
                <div className="skeleton-line skeleton-title"></div>
                <div className="skeleton-line skeleton-subtitle"></div>
              </div>
            </div>
            <div className="skeleton-content">
              <div className="skeleton-line"></div>
              <div className="skeleton-line"></div>
              <div className="skeleton-line skeleton-short"></div>
            </div>
          </div>
        ))}
      </>
    );
  }

  if (type === 'list') {
    return (
      <>
        {skeletons.map((_, i) => (
          <div key={i} className={`skeleton-list-item ${className}`}>
            <div className="skeleton-avatar"></div>
            <div className="skeleton-content">
              <div className="skeleton-line"></div>
              <div className="skeleton-line skeleton-short"></div>
            </div>
          </div>
        ))}
      </>
    );
  }

  if (type === 'dashboard') {
    return (
      <div className={`skeleton-dashboard ${className}`}>
        <div className="skeleton-stats">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton-stat-card">
              <div className="skeleton-icon"></div>
              <div className="skeleton-text-group">
                <div className="skeleton-line skeleton-title"></div>
                <div className="skeleton-line skeleton-subtitle"></div>
              </div>
            </div>
          ))}
        </div>
        <div className="skeleton-chart">
          <div className="skeleton-line skeleton-title"></div>
          <div className="skeleton-bars">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="skeleton-bar"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      {skeletons.map((_, i) => (
        <div key={i} className={`skeleton-default ${className}`}>
          <div className="skeleton-line"></div>
          <div className="skeleton-line"></div>
          <div className="skeleton-line skeleton-short"></div>
        </div>
      ))}
    </>
  );
}

export default SkeletonLoader;


