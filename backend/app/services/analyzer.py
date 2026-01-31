import re
from typing import List
from app.models.contract import Vulnerability
from app.services.vulnerability_patterns import VULNERABILITY_PATTERNS

class VulnerabilityAnalyzer:
    def analyze(self, contract_code: str) -> List[Vulnerability]:
        vulnerabilities = []
        lines = contract_code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('//') or line.strip().startswith('*'):
                continue
                
            for pattern in VULNERABILITY_PATTERNS:
                for regex in pattern['regex']:
                    # Special handling for more complex logic can stay here or be moved to specialized classes later
                    # For now, we improve the regex matching to be slightly more robust
                    
                    # Access control specific check to filter out false positives
                    if pattern['id'] == 'ACCESS_CONTROL':
                        if 'only' in line or 'require' in line or 'restricted' in line or 'internal' in line or 'private' in line or 'view' in line or 'pure' in line:
                            continue

                    if re.search(regex, line):
                        vulnerabilities.append(Vulnerability(
                            type=pattern['name'],
                            severity=pattern['severity'],
                            line=i,
                            description=pattern['description'],
                            recommendation=pattern['recommendation'],
                            confidence=pattern['confidence']
                        ))
                        # Break inner loop to avoid double reporting same pattern on same line
                        break
        
        return vulnerabilities
    
    def calculate_risk_score(self, vulnerabilities: List[Vulnerability]) -> int:
        severity_scores = {"Critical": 25, "High": 15, "Medium": 10, "Low": 5}
        total = sum(severity_scores.get(v.severity, 0) for v in vulnerabilities)
        return min(total, 100)
