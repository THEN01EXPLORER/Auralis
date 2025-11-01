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
                    recommendation="Use Checks-Effects-Interactions pattern or ReentrancyGuard"
                ))
            
            # Integer overflow detection
            if re.search(r'\+\+|\-\-|[\+\-\*](?!\s*=)', line) and 'unchecked' not in line:
                vulnerabilities.append(Vulnerability(
                    type="Integer Overflow/Underflow",
                    severity="High",
                    line=i,
                    description="Unchecked arithmetic operation detected",
                    recommendation="Use SafeMath library or Solidity 0.8+ built-in checks"
                ))
            
            # Access control detection
            if 'function' in line and 'public' in line and 'onlyOwner' not in line:
                vulnerabilities.append(Vulnerability(
                    type="Access Control Violation",
                    severity="Medium",
                    line=i,
                    description="Public function without access control modifier",
                    recommendation="Add appropriate access control modifiers (onlyOwner, onlyAdmin)"
                ))
            
            # Unchecked return values
            if '.transfer(' in line or '.send(' in line:
                vulnerabilities.append(Vulnerability(
                    type="Unchecked Return Value",
                    severity="Medium",
                    line=i,
                    description="Low-level call without checking return value",
                    recommendation="Check return value or use transfer() with require()"
                ))
        
        return vulnerabilities
    
    def calculate_risk_score(self, vulnerabilities: List[Vulnerability]) -> int:
        severity_scores = {"Critical": 25, "High": 15, "Medium": 10, "Low": 5}
        total = sum(severity_scores.get(v.severity, 0) for v in vulnerabilities)
        return min(total, 100)
