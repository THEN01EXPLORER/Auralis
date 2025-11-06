import pytest
import os
import asyncio
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.services.analyzer import VulnerabilityAnalyzer
from app.services.bedrock_analyzer import BedrockAnalyzer
from app.services.analysis_orchestrator import AnalysisOrchestrator
from app.models.contract import Vulnerability, RemediationDetails, BedrockAnalysisResult
import sys
sys.path.append('..')
from main import app

client = TestClient(app)

# Sample vulnerable contract for testing
VULNERABLE_CONTRACT = """
pragma solidity ^0.8.0;

contract VulnerableContract {
    mapping(address => uint256) public balances;
    
    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");
        
        // Vulnerable: external call before state change
        msg.sender.call{value: amount}("");
        balances[msg.sender] = 0;
    }
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function emergencyWithdraw() public {
        // Vulnerable: no access control
        payable(msg.sender).transfer(address(this).balance);
    }
    
    function checkTime() public view returns (bool) {
        // Vulnerable: timestamp dependence
        return block.timestamp > 1234567890;
    }
}
"""

class TestEndToEndAnalysisFlow:
    """Test end-to-end analysis flow with sample vulnerable contract."""
    
    def test_api_endpoint_with_vulnerable_contract(self):
        """Test /api/v1/analyze endpoint with vulnerable contract code."""
        response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "analysis_id" in data
        assert "risk_score" in data
        assert "vulnerabilities" in data
        assert "summary" in data
        assert "analysis_method" in data
        assert "ai_available" in data
        assert "processing_time_ms" in data
        
        # Verify vulnerabilities are detected
        vulnerabilities = data["vulnerabilities"]
        assert len(vulnerabilities) > 0
        
        # Check for expected vulnerability types
        vuln_types = [v["type"] for v in vulnerabilities]
        assert any("Re-entrancy" in vtype for vtype in vuln_types)
        
        # Verify vulnerability structure
        for vuln in vulnerabilities:
            assert "type" in vuln
            assert "line" in vuln
            assert "severity" in vuln
            assert "confidence" in vuln
            assert "description" in vuln
            assert "recommendation" in vuln
            assert isinstance(vuln["line"], int)
            assert vuln["severity"] in ["Critical", "High", "Medium", "Low"]
            assert 0 <= vuln["confidence"] <= 100
        
        # Verify risk score is reasonable
        assert 0 <= data["risk_score"] <= 100
        assert data["risk_score"] > 0  # Should detect vulnerabilities
        
        # Verify processing time is recorded
        assert data["processing_time_ms"] >= 0  # Allow 0ms for fast tests
    
    @patch.dict(os.environ, {"ENABLE_AI_ANALYSIS": "true"})
    def test_hybrid_analysis_with_mock_ai(self):
        """Test hybrid analysis flow with mocked AI analyzer."""
        # Mock AI analyzer response
        mock_ai_vulns = [
            Vulnerability(
                type="Smart Contract Logic Error",
                severity="High",
                line=15,
                description="AI detected potential logic flaw in withdrawal function",
                recommendation="Review withdrawal logic for edge cases",
                confidence=0.92,
                source="ai",
                remediation=RemediationDetails(
                    explanation="The withdrawal function may have logic issues",
                    code_example="// Add proper validation here"
                )
            )
        ]
        
        mock_bedrock_result = BedrockAnalysisResult(
            success=True,
            vulnerabilities=mock_ai_vulns,
            processing_time_ms=1500
        )
        
        # Patch the orchestrator's ai_analyzer directly
        with patch('main.orchestrator') as mock_orchestrator:
            static_analyzer = VulnerabilityAnalyzer()
            mock_bedrock = MagicMock()
            mock_bedrock.available = True
            mock_bedrock.analyze.return_value = mock_bedrock_result
            
            orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
            mock_orchestrator.analyze_contract = orchestrator.analyze_contract
            mock_orchestrator.ai_analyzer = mock_bedrock
            
            response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
            
            assert response.status_code == 200
            data = response.json()
            
            # Should use hybrid analysis
            assert data["analysis_method"] == "hybrid"
            assert data["ai_available"] is True
            
            # Should have vulnerabilities from both analyzers
            vulnerabilities = data["vulnerabilities"]
            assert len(vulnerabilities) > 1  # Static + AI vulnerabilities
            
            # Check for AI-generated vulnerability
            ai_vulns = [v for v in vulnerabilities if "AI detected" in v["description"]]
            assert len(ai_vulns) > 0
            
            # Verify remediation details are included
            ai_vuln_with_remediation = next(
                (v for v in vulnerabilities if "remediation" in v), None
            )
            if ai_vuln_with_remediation:
                remediation = ai_vuln_with_remediation["remediation"]
                assert "explanation" in remediation
                assert "code_example" in remediation
    
    def test_deduplication_works_correctly(self):
        """Test that duplicate vulnerabilities are properly merged."""
        # Create mock AI analyzer that returns duplicate vulnerability
        mock_ai_vulns = [
            Vulnerability(
                type="Re-entrancy Attack",  # Same type as static analyzer
                severity="Critical",        # Higher severity
                line=10,                   # Same line
                description="AI detected re-entrancy vulnerability with detailed analysis",
                recommendation="Use ReentrancyGuard from OpenZeppelin",
                confidence=0.95,           # Higher confidence
                source="ai"
            )
        ]
        
        mock_bedrock_result = BedrockAnalysisResult(
            success=True,
            vulnerabilities=mock_ai_vulns,
            processing_time_ms=1200
        )
        
        with patch('app.services.bedrock_analyzer.BedrockAnalyzer') as mock_bedrock_class:
            mock_bedrock = MagicMock()
            mock_bedrock.available = True
            mock_bedrock.analyze.return_value = mock_bedrock_result
            mock_bedrock_class.return_value = mock_bedrock
            
            from main import get_orchestrator
            with patch('main.get_orchestrator') as mock_get_orchestrator:
                static_analyzer = VulnerabilityAnalyzer()
                orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
                mock_get_orchestrator.return_value = orchestrator
                
                response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
                
                assert response.status_code == 200
                data = response.json()
                
                # Check that duplicates were merged
                vulnerabilities = data["vulnerabilities"]
                reentrancy_vulns = [v for v in vulnerabilities if "Re-entrancy" in v["type"]]
                
                # Should have only one re-entrancy vulnerability (merged)
                assert len(reentrancy_vulns) == 1
                
                # Should use higher severity and confidence from AI
                reentrancy_vuln = reentrancy_vulns[0]
                assert reentrancy_vuln["severity"] == "Critical"
                assert reentrancy_vuln["confidence"] >= 90  # Should use higher confidence
    
    def test_response_format_matches_specification(self):
        """Test that API response format matches the specification."""
        response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
        
        assert response.status_code == 200
        data = response.json()
        
        # Required fields from specification
        required_fields = [
            "analysis_id", "risk_score", "vulnerabilities", "summary",
            "analysis_method", "ai_available", "processing_time_ms"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Verify field types
        assert isinstance(data["analysis_id"], str)
        assert isinstance(data["risk_score"], int)
        assert isinstance(data["vulnerabilities"], list)
        assert isinstance(data["summary"], str)
        assert isinstance(data["analysis_method"], str)
        assert isinstance(data["ai_available"], bool)
        assert isinstance(data["processing_time_ms"], int)
        
        # Verify analysis_method values
        assert data["analysis_method"] in ["static", "hybrid"]
        
        # Verify vulnerability structure
        for vuln in data["vulnerabilities"]:
            required_vuln_fields = ["type", "line", "severity", "confidence", "description", "recommendation"]
            for field in required_vuln_fields:
                assert field in vuln, f"Missing vulnerability field: {field}"

class TestDegradedModeScenarios:
    """Test degraded mode scenarios when AI analysis is unavailable."""
    
    @patch.dict(os.environ, {"ENABLE_AI_ANALYSIS": "false"})
    def test_ai_analysis_disabled_by_configuration(self):
        """Test analysis when AI is disabled by configuration."""
        response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
        
        assert response.status_code == 200
        data = response.json()
        
        # Should use static analysis only
        assert data["analysis_method"] == "static"
        assert data["ai_available"] is False
        
        # Should still detect vulnerabilities
        assert len(data["vulnerabilities"]) > 0
        assert data["risk_score"] > 0
        
        # Should have reasonable processing time
        assert data["processing_time_ms"] >= 0  # Allow 0ms for fast tests
    
    def test_aws_credentials_not_configured(self):
        """Test analysis without AWS credentials configured."""
        with patch('app.services.bedrock_analyzer.BedrockAnalyzer') as mock_bedrock_class:
            # Mock unavailable AI analyzer
            mock_bedrock = MagicMock()
            mock_bedrock.available = False
            mock_bedrock_class.return_value = mock_bedrock
            
            from main import get_orchestrator
            with patch('main.get_orchestrator') as mock_get_orchestrator:
                static_analyzer = VulnerabilityAnalyzer()
                orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
                mock_get_orchestrator.return_value = orchestrator
                
                response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
                
                assert response.status_code == 200
                data = response.json()
                
                # Should fall back to static analysis
                assert data["analysis_method"] == "static"
                assert data["ai_available"] is False
                
                # Should still work and detect vulnerabilities
                assert len(data["vulnerabilities"]) > 0
                assert data["risk_score"] > 0
    
    def test_bedrock_api_unavailable(self):
        """Test analysis when Bedrock API is unavailable."""
        from app.models.contract import BedrockAnalysisResult
        
        # Mock AI analyzer that fails
        mock_bedrock_result = BedrockAnalysisResult(
            success=False,
            vulnerabilities=[],
            error_message="Bedrock API unavailable",
            processing_time_ms=5000
        )
        
        # Patch the orchestrator directly
        with patch('main.orchestrator') as mock_orchestrator:
            static_analyzer = VulnerabilityAnalyzer()
            mock_bedrock = MagicMock()
            mock_bedrock.available = True  # Available but fails during analysis
            mock_bedrock.analyze.return_value = mock_bedrock_result
            
            orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
            mock_orchestrator.analyze_contract = orchestrator.analyze_contract
            mock_orchestrator.ai_analyzer = mock_bedrock
            
            response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
            
            assert response.status_code == 200
            data = response.json()
            
            # Should fall back to static analysis
            assert data["analysis_method"] == "static"
            assert data["ai_available"] is True  # Was available but failed
            
            # Should still detect vulnerabilities from static analysis
            assert len(data["vulnerabilities"]) > 0
            assert data["risk_score"] > 0
    
    def test_static_analysis_continues_working(self):
        """Test that static analysis continues to work in all degraded scenarios."""
        scenarios = [
            # AI disabled
            {"ENABLE_AI_ANALYSIS": "false"},
            # AI required but unavailable (should still work for this test)
            {"AI_ANALYSIS_REQUIRED": "false", "ENABLE_AI_ANALYSIS": "true"}
        ]
        
        for env_vars in scenarios:
            with patch.dict(os.environ, env_vars):
                with patch('app.services.bedrock_analyzer.BedrockAnalyzer') as mock_bedrock_class:
                    # Mock unavailable AI analyzer
                    mock_bedrock = MagicMock()
                    mock_bedrock.available = False
                    mock_bedrock_class.return_value = mock_bedrock
                    
                    from main import get_orchestrator
                    with patch('main.get_orchestrator') as mock_get_orchestrator:
                        static_analyzer = VulnerabilityAnalyzer()
                        orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
                        mock_get_orchestrator.return_value = orchestrator
                        
                        response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
                        
                        assert response.status_code == 200
                        data = response.json()
                        
                        # Static analysis should always work
                        assert len(data["vulnerabilities"]) > 0
                        assert data["risk_score"] > 0
                        assert data["analysis_method"] == "static"
                        
                        # Should detect expected vulnerability types
                        vuln_types = [v["type"] for v in data["vulnerabilities"]]
                        assert any("Re-entrancy" in vtype for vtype in vuln_types)
    
    def test_appropriate_status_fields_are_set(self):
        """Test that appropriate status fields are set in degraded mode."""
        with patch('app.services.bedrock_analyzer.BedrockAnalyzer') as mock_bedrock_class:
            # Test scenario 1: AI not available
            mock_bedrock = MagicMock()
            mock_bedrock.available = False
            mock_bedrock_class.return_value = mock_bedrock
            
            from main import get_orchestrator
            with patch('main.get_orchestrator') as mock_get_orchestrator:
                static_analyzer = VulnerabilityAnalyzer()
                orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
                mock_get_orchestrator.return_value = orchestrator
                
                response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
                
                assert response.status_code == 200
                data = response.json()
                
                # Verify status fields
                assert data["analysis_method"] == "static"
                assert data["ai_available"] is False
                assert isinstance(data["processing_time_ms"], int)
                assert data["processing_time_ms"] >= 0  # Allow 0ms for fast tests
        
        # Test scenario 2: AI available but fails
        from app.models.contract import BedrockAnalysisResult
        mock_bedrock_result = BedrockAnalysisResult(
            success=False,
            vulnerabilities=[],
            error_message="API timeout",
            processing_time_ms=25000
        )
        
        # Patch the orchestrator directly for this test
        with patch('main.orchestrator') as mock_orchestrator:
            static_analyzer = VulnerabilityAnalyzer()
            mock_bedrock = MagicMock()
            mock_bedrock.available = True
            mock_bedrock.analyze.return_value = mock_bedrock_result
            
            orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
            mock_orchestrator.analyze_contract = orchestrator.analyze_contract
            mock_orchestrator.ai_analyzer = mock_bedrock
            
            response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify status fields for failed AI analysis
            assert data["analysis_method"] == "static"
            assert data["ai_available"] is True  # Was available but failed
            assert isinstance(data["processing_time_ms"], int)
            assert data["processing_time_ms"] >= 0  # Allow 0ms for fast tests
    
    def test_analysis_completes_within_30_seconds(self):
        """Test that analysis completes within 30 seconds regardless of AI availability (Requirement 4.4)."""
        import time
        
        # Test with AI unavailable - should complete quickly
        with patch('app.services.bedrock_analyzer.BedrockAnalyzer') as mock_bedrock_class:
            mock_bedrock = MagicMock()
            mock_bedrock.available = False
            mock_bedrock_class.return_value = mock_bedrock
            
            from main import get_orchestrator
            with patch('main.get_orchestrator') as mock_get_orchestrator:
                static_analyzer = VulnerabilityAnalyzer()
                orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
                mock_get_orchestrator.return_value = orchestrator
                
                start_time = time.time()
                response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
                end_time = time.time()
                
                assert response.status_code == 200
                assert (end_time - start_time) < 30.0  # Should complete within 30 seconds
                
                data = response.json()
                assert data["analysis_method"] == "static"
                assert data["processing_time_ms"] < 30000  # Should be much faster than 30 seconds
        
        # Test with AI timeout - should still complete within 30 seconds
        from app.models.contract import BedrockAnalysisResult
        mock_bedrock_result = BedrockAnalysisResult(
            success=False,
            vulnerabilities=[],
            error_message="Request timed out after 25 seconds",
            processing_time_ms=25000  # Simulated 25-second timeout
        )
        
        with patch('main.orchestrator') as mock_orchestrator:
            static_analyzer = VulnerabilityAnalyzer()
            mock_bedrock = MagicMock()
            mock_bedrock.available = True
            mock_bedrock.analyze.return_value = mock_bedrock_result
            
            orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
            mock_orchestrator.analyze_contract = orchestrator.analyze_contract
            mock_orchestrator.ai_analyzer = mock_bedrock
            
            start_time = time.time()
            response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 30.0  # Should complete within 30 seconds
            
            data = response.json()
            assert data["analysis_method"] == "static"  # Should fall back to static
            assert data["ai_available"] is True  # AI was available but timed out
    
    def test_error_logging_in_degraded_mode(self):
        """Test that errors are properly logged when AI analysis fails (Requirement 4.2)."""
        from app.models.contract import BedrockAnalysisResult
        import logging
        
        # Capture log messages
        with patch('app.services.analysis_orchestrator.logger') as mock_logger:
            mock_bedrock_result = BedrockAnalysisResult(
                success=False,
                vulnerabilities=[],
                error_message="Bedrock service temporarily unavailable",
                processing_time_ms=1000
            )
            
            with patch('main.orchestrator') as mock_orchestrator:
                static_analyzer = VulnerabilityAnalyzer()
                mock_bedrock = MagicMock()
                mock_bedrock.available = True
                mock_bedrock.analyze.return_value = mock_bedrock_result
                
                orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
                mock_orchestrator.analyze_contract = orchestrator.analyze_contract
                mock_orchestrator.ai_analyzer = mock_bedrock
                
                response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
                
                assert response.status_code == 200
                data = response.json()
                assert data["analysis_method"] == "static"
                
                # Verify error was logged
                mock_logger.warning.assert_called()
                log_calls = [call.args[0] for call in mock_logger.warning.call_args_list]
                assert any("AI analysis failed" in call for call in log_calls)
    
    def test_status_field_indicates_ai_unavailable(self):
        """Test that status field indicates AI analysis was unavailable (Requirement 4.3)."""
        # Test multiple scenarios where AI is unavailable
        scenarios = [
            # Scenario 1: AI disabled by configuration
            {"env": {"ENABLE_AI_ANALYSIS": "false"}, "ai_available": False},
            # Scenario 2: AWS credentials not configured
            {"mock_unavailable": True, "ai_available": False},
        ]
        
        for scenario in scenarios:
            if "env" in scenario:
                with patch.dict(os.environ, scenario["env"]):
                    response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
            else:
                with patch('app.services.bedrock_analyzer.BedrockAnalyzer') as mock_bedrock_class:
                    mock_bedrock = MagicMock()
                    mock_bedrock.available = False
                    mock_bedrock_class.return_value = mock_bedrock
                    
                    from main import get_orchestrator
                    with patch('main.get_orchestrator') as mock_get_orchestrator:
                        static_analyzer = VulnerabilityAnalyzer()
                        orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
                        mock_get_orchestrator.return_value = orchestrator
                        
                        response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify status fields indicate AI was unavailable
            assert data["analysis_method"] == "static"
            assert data["ai_available"] == scenario["ai_available"]
            
            # Verify static analysis still works
            assert len(data["vulnerabilities"]) > 0
            assert data["risk_score"] > 0
            assert isinstance(data["processing_time_ms"], int)
    
    @patch.dict(os.environ, {"AI_ANALYSIS_REQUIRED": "true", "ENABLE_AI_ANALYSIS": "true"})
    def test_required_ai_analysis_unavailable_fails_request(self):
        """Test that request fails when AI analysis is required but unavailable."""
        with patch('app.services.bedrock_analyzer.BedrockAnalyzer') as mock_bedrock_class:
            # Mock unavailable AI analyzer
            mock_bedrock = MagicMock()
            mock_bedrock.available = False
            mock_bedrock_class.return_value = mock_bedrock
            
            from main import get_orchestrator
            with patch('main.get_orchestrator') as mock_get_orchestrator:
                static_analyzer = VulnerabilityAnalyzer()
                orchestrator = AnalysisOrchestrator(static_analyzer, mock_bedrock)
                mock_get_orchestrator.return_value = orchestrator
                
                response = client.post("/api/v1/analyze", json={"code": VULNERABLE_CONTRACT})
                
                # Should fail with 503 when AI is required but unavailable
                assert response.status_code == 503
                data = response.json()
                assert "AI analysis is required but not available" in data["detail"]