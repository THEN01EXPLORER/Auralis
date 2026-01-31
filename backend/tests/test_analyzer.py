import pytest
from app.services.analyzer import VulnerabilityAnalyzer

def test_reentrancy_detection():
    analyzer = VulnerabilityAnalyzer()
    code = "msg.sender.call{value: amount}(\"\");"
    vulns = analyzer.analyze(code)
    assert any(v.type == "Re-entrancy Attack" for v in vulns)
    assert any(v.severity == "Critical" for v in vulns)

def test_timestamp_detection():
    analyzer = VulnerabilityAnalyzer()
    code = "require(block.timestamp > deadline);"
    vulns = analyzer.analyze(code)
    assert any(v.type == "Timestamp Dependence" for v in vulns)

def test_delegatecall_detection():
    analyzer = VulnerabilityAnalyzer()
    code = "target.delegatecall(data);"
    vulns = analyzer.analyze(code)
    assert any(v.type == "Delegatecall Injection" for v in vulns)

def test_risk_score_calculation():
    analyzer = VulnerabilityAnalyzer()
    code = """
    function withdraw() public {
        msg.sender.call{value: 1 ether}("");
    }
    """
    vulns = analyzer.analyze(code)
    score = analyzer.calculate_risk_score(vulns)
    assert score > 0
    assert score <= 100

def test_confidence_scores():
    analyzer = VulnerabilityAnalyzer()
    code = "msg.sender.call{value: amount}(\"\");"
    vulns = analyzer.analyze(code)
    assert all(hasattr(v, 'confidence') for v in vulns)
    assert all(0 <= v.confidence <= 1 for v in vulns)
