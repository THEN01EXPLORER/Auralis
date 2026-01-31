import client from '../api/client';

export const analyzeContract = async (contractCode, chainType = 'ethereum') => {
  try {
    const response = await client.post('/api/v1/analyze', {
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
    const response = await client.post('/api/v1/analyze_repo', {
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

export const analyzeRepoAsync = async (githubUrl) => {
  try {
    const response = await client.post('/api/v1/analyze_repo_async', {
      github_url: githubUrl
    });
    return response.data;
  } catch (error) {
    throw error; // Let component handle or wrap
  }
};

export const getJobStatus = async (taskId) => {
  try {
    const response = await client.get(`/api/v1/jobs/${taskId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const healthCheck = async () => {
  try {
    const response = await client.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export const getStats = async () => {
  try {
    const response = await client.get('/api/v1/stats');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch stats:', error);
    throw error;
  }
};

export const getSupportedPatterns = async () => {
  try {
    const response = await client.get('/api/v1/supported_patterns');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch supported patterns:', error);
    throw error;
  }
};
