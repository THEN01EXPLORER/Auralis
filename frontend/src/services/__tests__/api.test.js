import client from '../api/client';
import { analyzeContract, analyzeRepo } from '../api';

// Mock the client default export
jest.mock('../api/client', () => {
  return {
    post: jest.fn(),
    get: jest.fn(),
    interceptors: {
      request: { use: jest.fn() },
      response: { use: jest.fn() }
    }
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

      client.post.mockResolvedValueOnce({ data: mockResponse });

      const code = 'pragma solidity ^0.8.0;';
      const result = await analyzeContract(code);

      expect(client.post).toHaveBeenCalledWith(
        '/api/v1/analyze',
        { code: code }
      );

      expect(result).toEqual(mockResponse);
    });

    test('throws error when server responds with error', async () => {
      client.post.mockRejectedValueOnce({
        response: {
          data: { detail: 'Internal error' },
          statusText: 'Internal Server Error'
        }
      });

      await expect(analyzeContract('code')).rejects.toThrow(/Server error/);
    });
  });

  describe('analyzeRepo', () => {
    test('sends repository URL to analyze_repo endpoint', async () => {
      const mockResponse = {
        repository_url: 'https://github.com/test/repo',
        files_analyzed: 3,
        total_vulnerabilities: 5,
        results: {}
      };

      client.post.mockResolvedValueOnce({ data: mockResponse });

      const repoUrl = 'https://github.com/test/repo';
      const result = await analyzeRepo(repoUrl);

      expect(client.post).toHaveBeenCalledWith(
        '/api/v1/analyze_repo',
        { github_url: repoUrl }
      );

      expect(result).toEqual(mockResponse);
    });
  });
});
