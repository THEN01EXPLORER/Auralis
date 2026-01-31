import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


class TestRateLimiting:
    """Test rate limiting functionality."""

    def test_health_endpoint_not_rate_limited(self):
        """Health endpoint should not be rate limited."""
        # Make multiple requests to health endpoint
        for _ in range(100):
            response = client.get("/health")
            assert response.status_code == 200

    def test_root_endpoint_not_rate_limited(self):
        """Root endpoint should not be rate limited."""
        # Make multiple requests to root endpoint
        for _ in range(100):
            response = client.get("/")
            assert response.status_code == 200

    def test_analyze_endpoint_rate_limit(self):
        """Analyze endpoint should be rate limited to 60 requests per minute."""
        contract_code = """
        pragma solidity ^0.8.0;
        contract Test {
            function test() public {}
        }
        """
        
        # Make requests up to the limit
        for i in range(60):
            response = client.post(
                "/api/v1/analyze",
                json={"code": contract_code}
            )
            # Should succeed (200 or 503 if AI unavailable, but not 429)
            assert response.status_code != 429, f"Rate limited at request {i+1}"

    def test_rate_limit_exceeded_response_format(self):
        """Rate limit exceeded should return proper error format."""
        contract_code = """
        pragma solidity ^0.8.0;
        contract Test {
            function test() public {}
        }
        """
        
        # Make requests to exceed the limit
        for _ in range(65):
            response = client.post(
                "/api/v1/analyze",
                json={"code": contract_code}
            )
            if response.status_code == 429:
                # Check response format
                data = response.json()
                assert "error" in data
                assert "detail" in data
                assert "retry_after" in data
                assert response.headers.get("Retry-After") == "60"
                break

    def test_repo_analyze_endpoint_rate_limit(self):
        """Repo analyze endpoint should have stricter rate limit (10/minute)."""
        repo_url = "https://github.com/test/repo"
        
        # Make requests up to the limit
        for i in range(10):
            response = client.post(
                "/api/v1/analyze_repo",
                json={"github_url": repo_url}
            )
            # Should not be rate limited yet
            assert response.status_code != 429, f"Rate limited at request {i+1}"

    def test_dread_score_endpoint_rate_limit(self):
        """DREAD score endpoint should be rate limited to 60 requests per minute."""
        contract_code = """
        pragma solidity ^0.8.0;
        contract Test {
            function test() public {}
        }
        """
        
        # Make requests up to the limit
        for i in range(60):
            response = client.post(
                "/api/v1/dread_score",
                json={"code": contract_code}
            )
            # Should succeed (200 or 503 if AI unavailable, but not 429)
            assert response.status_code != 429, f"Rate limited at request {i+1}"

    def test_generate_report_endpoint_rate_limit(self):
        """Generate report endpoint should be rate limited to 30 requests per minute."""
        contract_code = """
        pragma solidity ^0.8.0;
        contract Test {
            function test() public {}
        }
        """
        
        # Make requests up to the limit
        for i in range(30):
            response = client.post(
                "/api/v1/generate_report",
                json={"code": contract_code}
            )
            # Should succeed (200 or 503 if AI unavailable, but not 429)
            assert response.status_code != 429, f"Rate limited at request {i+1}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
