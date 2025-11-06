import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from app.services.analysis_orchestrator import AnalysisOrchestrator
from app.services.analyzer import VulnerabilityAnalyzer
from app.services.bedrock_analyzer import BedrockAnalyzer
from app.models.contract import Vulnerability, BedrockAnalysisResult, AnalysisResult


class TestAnalysisOrchestrator:
    """Test cases for AnalysisOrchestrator service."""
    
    @pytest.fixture
    def mock_static_analyzer(self):
        """Create a mock static analyzer."""
        analyzer = Mock(spec=VulnerabilityAnalyzer)
        return analyzer
    
    @pytest.fixture
    def mock_ai_analyzer(self):
        """Create a mock AI analyzer."""
        analyzer = Mock(spec=BedrockAnalyzer)
        return analyzer
    
    @pytest.fixture
    def orchestrator(self, mock_static_analyzer, mock_ai_analyzer):
        """Create an orchestrator with mocked dependencies."""
        return AnalysisOrchestrator(mock_static_analyzer, mock_ai_analyzer)
    
    @pytest.mark.asyncio
    async def test_hybrid_analysis_both_analyzers_succeed(self, orchestrator, mock_static_analyzer, mock_ai_analyzer):
        """Test hybrid analysis when both analyzers succeed."""
        # Setup static analyzer mock
        static_vulns = [
            Vulnerability(
                type="Re-entrancy Attack",
                severity="High",
                line=42,
                description="Static reentrancy detection",
                recommendation="Use checks-effects-interactions",
                confidence=0.8,
                source="static"
            )
        ]
        mock_static_analyzer.analyze.return_value = static_vulns
        
        # Setup AI analyzer mock
        ai_vulns = [
            Vulnerability(
                type="Business Logic Flaw",
                severity="Critical",
                line=25,
                description="AI detected business logic issue",
                recommendation="Review business logic",
                confidence=0.9,
                source="ai"
            )
        ]
        ai_result = BedrockAnalysisResult(
            success=True,
            vulnerabilities=ai_vulns,
            error_message=None,
            processing_time_ms=1500
        )
        mock_ai_analyzer.available = True
        mock_ai_analyzer.analyze.return_value = ai_result
        
        contract_code = "contract Test { function test() public {} }"
        result = await orchestrator.analyze_contract(contract_code)
        
        # Verify result structure
        assert isinstance(result, AnalysisResult)
        assert result.analysis_method == "hybrid"
        assert result.ai_available == True
        assert len(result.vulnerabilities) == 2  # Both static and AI vulnerabilities
        assert result.risk_score > 0
        assert result.processing_time_ms >= 0
        assert "hybrid" in result.summary
        
        # Verify both analyzers were called
        mock_static_analyzer.analyze.assert_called_once_with(contract_code)
        mock_ai_analyzer.analyze.assert_called_once_with(contract_code, static_vulns)
    
    @pytest.mark.asyncio
    async def test_static_only_fallback_when_ai_fails(self, orchestrator, mock_static_analyzer, mock_ai_analyzer):
        """Test static-only fallback when AI analysis fails."""
        # Setup static analyzer mock
        static_vulns = [
            Vulnerability(
                type="Access Control",
                severity="Medium",
                line=30,
                description="Missing access control",
                recommendation="Add access control checks",
                confidence=0.7,
                source="static"
            )
        ]
        mock_static_analyzer.analyze.return_value = static_vulns
        
        # Setup AI analyzer to fail
        ai_result = BedrockAnalysisResult(
            success=False,
            vulnerabilities=[],
            error_message="AI service temporarily unavailable",
            processing_time_ms=500
        )
        mock_ai_analyzer.available = True
        mock_ai_analyzer.analyze.return_value = ai_result
        
        contract_code = "contract Test { function test() public {} }"
        result = await orchestrator.analyze_contract(contract_code)
        
        # Verify fallback to static analysis
        assert result.analysis_method == "static"
        assert result.ai_available == True
        assert len(result.vulnerabilities) == 1
        assert result.vulnerabilities[0].type == "Access Control"
        assert "static" in result.summary
        
        # Verify both analyzers were attempted
        mock_static_analyzer.analyze.assert_called_once_with(contract_code)
        mock_ai_analyzer.analyze.assert_called_once_with(contract_code, static_vulns)
    
    @pytest.mark.asyncio
    async def test_static_only_when_ai_unavailable(self, orchestrator, mock_static_analyzer, mock_ai_analyzer):
        """Test static-only analysis when AI analyzer is unavailable."""
        # Setup static analyzer mock
        static_vulns = [
            Vulnerability(
                type="Timestamp Dependence",
                severity="Low",
                line=15,
                description="Uses block.timestamp",
                recommendation="Use block.number instead",
                confidence=0.6,
                source="static"
            )
        ]
        mock_static_analyzer.analyze.return_value = static_vulns
        
        # Setup AI analyzer as unavailable
        mock_ai_analyzer.available = False
        
        contract_code = "contract Test { function test() public {} }"
        result = await orchestrator.analyze_contract(contract_code)
        
        # Verify static-only analysis
        assert result.analysis_method == "static"
        assert result.ai_available == False
        assert len(result.vulnerabilities) == 1
        assert result.vulnerabilities[0].type == "Timestamp Dependence"
        
        # Verify only static analyzer was called
        mock_static_analyzer.analyze.assert_called_once_with(contract_code)
        mock_ai_analyzer.analyze.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_result_merging_correctness(self, orchestrator, mock_static_analyzer, mock_ai_analyzer):
        """Test that result merging works correctly with duplicates."""
        # Setup static analyzer with duplicate vulnerability
        static_vulns = [
            Vulnerability(
                type="Re-entrancy Attack",
                severity="High",
                line=42,
                description="Static reentrancy detection",
                recommendation="Static recommendation",
                confidence=0.8,
                source="static"
            ),
            Vulnerability(
                type="Access Control",
                severity="Medium",
                line=25,
                description="Static access control",
                recommendation="Static access recommendation",
                confidence=0.7,
                source="static"
            )
        ]
        mock_static_analyzer.analyze.return_value = static_vulns
        
        # Setup AI analyzer with one duplicate and one unique
        ai_vulns = [
            Vulnerability(
                type="Re-entrancy Attack",  # Duplicate with static
                severity="Critical",  # Higher severity
                line=42,
                description="AI reentrancy detection",
                recommendation="AI recommendation",
                confidence=0.9,  # Higher confidence
                source="ai"
            ),
            Vulnerability(
                type="Business Logic Flaw",  # Unique AI vulnerability
                severity="High",
                line=60,
                description="AI business logic detection",
                recommendation="AI business recommendation",
                confidence=0.85,
                source="ai"
            )
        ]
        ai_result = BedrockAnalysisResult(
            success=True,
            vulnerabilities=ai_vulns,
            error_message=None,
            processing_time_ms=2000
        )
        mock_ai_analyzer.available = True
        mock_ai_analyzer.analyze.return_value = ai_result
        
        contract_code = "contract Test { function test() public {} }"
        result = await orchestrator.analyze_contract(contract_code)
        
        # Verify merging results
        assert result.analysis_method == "hybrid"
        assert len(result.vulnerabilities) == 3  # 1 merged + 1 unique static + 1 unique AI
        
        # Find the merged vulnerability
        merged_vuln = next((v for v in result.vulnerabilities if v.source == "hybrid"), None)
        assert merged_vuln is not None
        assert merged_vuln.type == "Re-entrancy Attack"
        assert merged_vuln.severity == "Critical"  # AI had higher severity
        assert merged_vuln.confidence == 0.9  # AI had higher confidence
        
        # Verify unique vulnerabilities are preserved
        types = [v.type for v in result.vulnerabilities]
        assert "Access Control" in types
        assert "Business Logic Flaw" in types
    
    @pytest.mark.asyncio
    async def test_timing_metrics_calculation(self, orchestrator, mock_static_analyzer, mock_ai_analyzer):
        """Test that timing metrics are calculated correctly."""
        # Setup static analyzer mock
        mock_static_analyzer.analyze.return_value = []
        
        # Setup AI analyzer mock
        ai_result = BedrockAnalysisResult(
            success=True,
            vulnerabilities=[],
            error_message=None,
            processing_time_ms=1000
        )
        mock_ai_analyzer.available = True
        mock_ai_analyzer.analyze.return_value = ai_result
        
        contract_code = "contract Test {}"
        result = await orchestrator.analyze_contract(contract_code)
        
        # Verify timing metrics
        assert result.processing_time_ms >= 0
        assert isinstance(result.processing_time_ms, int)
    
    @pytest.mark.asyncio
    async def test_analysis_method_field_values(self, orchestrator, mock_static_analyzer, mock_ai_analyzer):
        """Test that analysis_method field is set correctly in different scenarios."""
        mock_static_analyzer.analyze.return_value = []
        
        # Test hybrid method
        ai_result = BedrockAnalysisResult(success=True, vulnerabilities=[], error_message=None, processing_time_ms=1000)
        mock_ai_analyzer.available = True
        mock_ai_analyzer.analyze.return_value = ai_result
        
        result = await orchestrator.analyze_contract("contract Test {}")
        assert result.analysis_method == "hybrid"
        
        # Test static method when AI fails
        ai_result = BedrockAnalysisResult(success=False, vulnerabilities=[], error_message="Failed", processing_time_ms=500)
        mock_ai_analyzer.analyze.return_value = ai_result
        
        result = await orchestrator.analyze_contract("contract Test {}")
        assert result.analysis_method == "static"
        
        # Test static method when AI unavailable
        mock_ai_analyzer.available = False
        
        result = await orchestrator.analyze_contract("contract Test {}")
        assert result.analysis_method == "static"
    
    @pytest.mark.asyncio
    async def test_ai_analyzer_exception_handling(self, orchestrator, mock_static_analyzer, mock_ai_analyzer):
        """Test handling of exceptions from AI analyzer."""
        # Setup static analyzer mock
        static_vulns = [
            Vulnerability(
                type="Test Vulnerability",
                severity="Medium",
                line=10,
                description="Test description",
                recommendation="Test recommendation",
                confidence=0.8,
                source="static"
            )
        ]
        mock_static_analyzer.analyze.return_value = static_vulns
        
        # Setup AI analyzer to raise exception
        mock_ai_analyzer.available = True
        mock_ai_analyzer.analyze.side_effect = Exception("Unexpected AI error")
        
        contract_code = "contract Test {}"
        result = await orchestrator.analyze_contract(contract_code)
        
        # Verify graceful handling
        assert result.analysis_method == "static"
        assert result.ai_available == True
        assert len(result.vulnerabilities) == 1
        assert result.vulnerabilities[0].type == "Test Vulnerability"
    
    def test_unified_risk_score_calculation(self, orchestrator):
        """Test unified risk score calculation."""
        # Test empty vulnerabilities
        score = orchestrator._calculate_unified_risk_score([])
        assert score == 0
        
        # Test single critical vulnerability
        critical_vuln = Vulnerability(
            type="Critical Issue",
            severity="Critical",
            line=1,
            description="Test",
            recommendation="Test",
            confidence=1.0,
            source="static"
        )
        score = orchestrator._calculate_unified_risk_score([critical_vuln])
        assert score == 25  # Critical = 25 points * 1.0 confidence
        
        # Test multiple vulnerabilities
        vulnerabilities = [
            Vulnerability(type="Critical", severity="Critical", line=1, description="", recommendation="", confidence=1.0, source="static"),
            Vulnerability(type="High", severity="High", line=2, description="", recommendation="", confidence=0.8, source="ai"),
            Vulnerability(type="Medium", severity="Medium", line=3, description="", recommendation="", confidence=0.6, source="hybrid")
        ]
        score = orchestrator._calculate_unified_risk_score(vulnerabilities)
        expected = 25 * 1.0 + 15 * 0.8 + 10 * 0.6  # 25 + 12 + 6 = 43
        assert score == int(expected)
        
        # Test score capping at 100
        many_critical = [
            Vulnerability(type=f"Critical{i}", severity="Critical", line=i, description="", recommendation="", confidence=1.0, source="static")
            for i in range(10)  # 10 critical vulnerabilities = 250 points
        ]
        score = orchestrator._calculate_unified_risk_score(many_critical)
        assert score == 100  # Should be capped at 100
    
    def test_summary_generation(self, orchestrator):
        """Test summary generation for different scenarios."""
        # Test no vulnerabilities
        summary = orchestrator._generate_summary([], "static")
        assert "No vulnerabilities detected" in summary
        assert "static" in summary
        
        # Test single vulnerability
        vulnerabilities = [
            Vulnerability(
                type="Test",
                severity="High",
                line=1,
                description="",
                recommendation="",
                confidence=0.8,
                source="static"
            )
        ]
        summary = orchestrator._generate_summary(vulnerabilities, "hybrid")
        assert "Found 1 vulnerabilities" in summary
        assert "hybrid" in summary
        assert "1 High" in summary
        
        # Test multiple vulnerabilities with different severities
        vulnerabilities = [
            Vulnerability(type="Critical", severity="Critical", line=1, description="", recommendation="", confidence=1.0, source="static"),
            Vulnerability(type="High1", severity="High", line=2, description="", recommendation="", confidence=0.8, source="ai"),
            Vulnerability(type="High2", severity="High", line=3, description="", recommendation="", confidence=0.9, source="hybrid"),
            Vulnerability(type="Medium", severity="Medium", line=4, description="", recommendation="", confidence=0.7, source="static")
        ]
        summary = orchestrator._generate_summary(vulnerabilities, "hybrid")
        assert "Found 4 vulnerabilities" in summary
        assert "1 Critical" in summary
        assert "2 High" in summary
        assert "1 Medium" in summary