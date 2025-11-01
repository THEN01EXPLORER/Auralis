import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const analyzeContract = async (contractCode, chainType = 'ethereum') => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/analyze`, {
      contract_code: contractCode,
      chain_type: chainType
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing contract:', error);
    throw error;
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
