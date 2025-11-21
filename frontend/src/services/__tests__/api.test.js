import axios from 'axios';
import { analyzeContract, analyzeRepo } from '../api';

jest.mock('axios', () => {
  const mockAxios = {
    post: jest.fn(),
    get: jest.fn()
  };
  mockAxios.create = () => mockAxios;
  return {
    __esModule: true,
    default: mockAxios
  };
});

describe('API Client', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('analyzeContract', () => {
    test('sends contract code to analyze endpoint', async () => {
      const mockResponse = {
        analysis_id: 'test-123',
        risk_score: 75,
        vulnerabilities: [],
        summary: 'Test summary'
      };

      axios.post.mockResolvedValueOnce({ data: mockResponse });

      const code = 'pragma solidity ^0.8.0;';
      const result = await analyzeContract(code);

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/analyze'),
        { code: code }
      );

      expect(result).toEqual(mockResponse);
    });

    test('throws error when server responds with error', async () => {
      axios.post.mockRejectedValueOnce({
        response: {
          data: { detail: 'Internal error' },
          statusText: 'Internal Server Error'
        }
      });

      await expect(analyzeContract('code')).rejects.toThrow(/Server error/);
    });

    test('throws error when request cannot reach server', async () => {
      axios.post.mockRejectedValueOnce({ request: {} });

      await expect(analyzeContract('code')).rejects.toThrow(/Cannot connect/);
    });

    test('throws error when request setup fails', async () => {
      axios.post.mockRejectedValueOnce(new Error('Network error'));

      await expect(analyzeContract('code')).rejects.toThrow('Failed to analyze contract');
    });
  });

  describe('analyzeRepo', () => {
    test('sends repository URL to analyze_repo endpoint', async () => {
      const mockResponse = {
        repository_url: 'https://github.com/test/repo',
        files_analyzed: 3,
        total_vulnerabilities: 5,
        processing_time_ms: 5000,
        results: {}
      };

      axios.post.mockResolvedValueOnce({ data: mockResponse });

      const repoUrl = 'https://github.com/test/repo';
      const result = await analyzeRepo(repoUrl);

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/analyze_repo'),
        { github_url: repoUrl }
      );

      expect(result).toEqual(mockResponse);
    });

    test('throws error when server responds with error', async () => {
      axios.post.mockRejectedValueOnce({
        response: {
          data: { detail: 'Bad Request' },
          statusText: 'Bad Request'
        }
      });

      await expect(analyzeRepo('https://github.com/test/repo')).rejects.toThrow(/Server error/);
    });

    test('throws error when request cannot reach server', async () => {
      axios.post.mockRejectedValueOnce({ request: {} });

      await expect(analyzeRepo('https://github.com/test/repo')).rejects.toThrow(/Cannot connect/);
    });

    test('throws error when request setup fails', async () => {
      axios.post.mockRejectedValueOnce(new Error('Network error'));

      await expect(analyzeRepo('https://github.com/test/repo')).rejects.toThrow('Failed to analyze repository');
    });
  });

  describe('API endpoint configuration', () => {
    test('uses correct API base URL', async () => {
      axios.post.mockResolvedValueOnce({ data: { vulnerabilities: [] } });

      await analyzeContract('test');

      const callUrl = axios.post.mock.calls[0][0];
      expect(callUrl).toMatch(/\/api\/v1\/analyze/);
    });
  });
});
