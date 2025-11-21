import axios from 'axios';

// DEPLOYMENT: Replace this URL with your API Gateway Invoke URL
// Example: https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const analyzeContract = async (contractCode, chainType = 'ethereum') => {
  try {
    // Use /api/v1 prefix for production API
    const response = await axios.post(`${API_BASE_URL}/api/v1/analyze`, {
      code: contractCode
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(`Server error: ${error.response.data.detail || error.response.statusText}`);
    } else if (error.request) {
      throw new Error('Cannot connect to backend. Please ensure the server is running.');
    } else {
      throw new Error('Failed to analyze contract. Please try again.');
    }
  }
};

export const analyzeRepo = async (githubUrl) => {
  try {
    // Use /api/v1 prefix for production API
    const response = await axios.post(`${API_BASE_URL}/api/v1/analyze_repo`, {
      github_url: githubUrl
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(`Server error: ${error.response.data.detail || error.response.statusText}`);
    } else if (error.request) {
      throw new Error('Cannot connect to backend. Please ensure the server is running.');
    } else {
      throw new Error('Failed to analyze repository. Please try again.');
    }
  }
};

export const healthCheck = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export const getStats = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/v1/stats`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch stats:', error);
    throw error;
  }
};

export const getSupportedPatterns = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/v1/supported_patterns`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch supported patterns:', error);
    throw error;
  }
};
