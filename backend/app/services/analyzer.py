import re
from typing import List
from app.models.contract import Vulnerability

class VulnerabilityAnalyzer:
    def analyze(self, contract_code: str) -> List[Vulnerability]:
        vulnerabilities = []
        lines = contract_code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Re-entrancy detection
            if '.call{' in line or '.call(' in line:
                vulnerabilities.append(Vulnerability(
                    type="Re-entrancy Attack",
                    severity="Critical",
                    line=i,
                    description="External call detected before state changes",
                    recommendation="Use Checks-Effects-Interactions pattern or ReentrancyGuard",
                    confidence=0.95
                ))
            
            # Integer overflow detection
            if re.search(r'\+\+|\-\-|[\+\-\*](?!\s*=)', line) and 'unchecked' not in line:
                vulnerabilities.append(Vulnerability(
                    type="Integer Overflow/Underflow",
                    severity="High",
                    line=i,
                    description="Unchecked arithmetic operation detected",
                    recommendation="Use SafeMath library or Solidity 0.8+ built-in checks",
                    confidence=0.80
                ))
            
            # Access control detection
            if 'function' in line and 'public' in line and 'onlyOwner' not in line:
                vulnerabilities.append(Vulnerability(
                    type="Access Control Violation",
                    severity="Medium",
                    line=i,
                    description="Public function without access control modifier",
                    recommendation="Add appropriate access control modifiers (onlyOwner, onlyAdmin)",
                    confidence=0.75
                ))
            
            # Unchecked return values
            if '.transfer(' in line or '.send(' in line:
                vulnerabilities.append(Vulnerability(
                    type="Unchecked Return Value",
                    severity="Medium",
                    line=i,
                    description="Low-level call without checking return value",
                    recommendation="Check return value or use transfer() with require()",
                    confidence=0.85
                ))
            
            # Timestamp dependence
            if 'block.timestamp' in line or 'now' in line:
                vulnerabilities.append(Vulnerability(
                    type="Timestamp Dependence",
                    severity="Medium",
                    line=i,
                    description="Contract relies on block.timestamp which can be manipulated",
                    recommendation="Avoid using timestamps for critical logic",
                    confidence=0.90
                ))
            
            # Delegatecall injection
            if 'delegatecall' in line:
                vulnerabilities.append(Vulnerability(
                    type="Delegatecall Injection",
                    severity="Critical",
                    line=i,
                    description="Unsafe delegatecall detected - can lead to complete contract takeover",
                    recommendation="Validate delegatecall targets and use library pattern",
                    confidence=0.92
                ))
        
        return vulnerabilities
    
    def calculate_risk_score(self, vulnerabilities: List[Vulnerability]) -> int:
        severity_scores = {"Critical": 25, "High": 15, "Medium": 10, "Low": 5}
        total = sum(severity_scores.get(v.severity, 0) for v in vulnerabilities)
        return min(total, 100)
