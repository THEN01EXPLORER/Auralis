/**
 * Input validation utilities for Auralis
 */

export const validateContractCode = (code) => {
  if (!code || typeof code !== 'string') {
    return { valid: false, error: 'Contract code is required' };
  }

  const trimmed = code.trim();
  
  if (trimmed.length === 0) {
    return { valid: false, error: 'Contract code cannot be empty' };
  }

  if (trimmed.length < 10) {
    return { valid: false, error: 'Contract code is too short (minimum 10 characters)' };
  }

  if (trimmed.length > 100000) {
    return { valid: false, error: 'Contract code is too long (maximum 100,000 characters)' };
  }

  // Check for basic Solidity keywords
  const solidityKeywords = ['pragma', 'contract', 'function', 'mapping', 'address', 'uint'];
  const hasSolidityKeyword = solidityKeywords.some(keyword => 
    trimmed.toLowerCase().includes(keyword.toLowerCase())
  );

  if (!hasSolidityKeyword) {
    return { 
      valid: true, 
      warning: 'Code may not be valid Solidity. Analysis will still proceed.' 
    };
  }

  return { valid: true };
};

export const validateGitHubUrl = (url) => {
  if (!url || typeof url !== 'string') {
    return { valid: false, error: 'GitHub URL is required' };
  }

  const trimmed = url.trim();
  
  if (trimmed.length === 0) {
    return { valid: false, error: 'GitHub URL cannot be empty' };
  }

  // Basic GitHub URL validation
  const githubUrlPattern = /^https?:\/\/(www\.)?github\.com\/[\w\-\.]+\/[\w\-\.]+(\/)?$/i;
  
  if (!githubUrlPattern.test(trimmed)) {
    return { valid: false, error: 'Please enter a valid GitHub repository URL (e.g., https://github.com/username/repo)' };
  }

  return { valid: true };
};

export const sanitizeInput = (input) => {
  if (typeof input !== 'string') {
    return '';
  }

  // Remove potentially dangerous characters while preserving code structure
  return input
    .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '') // Remove control characters
    .trim();
};

export const validateAnalysisRequest = (data) => {
  if (!data) {
    return { valid: false, error: 'Request data is required' };
  }

  if (data.code) {
    return validateContractCode(data.code);
  }

  if (data.github_url) {
    return validateGitHubUrl(data.github_url);
  }

  return { valid: false, error: 'Either contract code or GitHub URL is required' };
};

