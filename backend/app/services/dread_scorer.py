"""
DREAD Risk Assessment System
Calculates DREAD scores for vulnerabilities:
- Damage: How bad would an attack be?
- Reproducibility: How easy is it to reproduce?
- Exploitability: How much work is it to launch the attack?
- Affected users: How many users will be impacted?
- Discoverability: How easy is it to discover the threat?
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class DREADScore:
    damage: int  # 0-10
    reproducibility: int  # 0-10
    exploitability: int  # 0-10
    affected_users: int  # 0-10
    discoverability: int  # 0-10
    
    @property
    def total(self) -> int:
        """Calculate total DREAD score (0-50)"""
        return (self.damage + self.reproducibility + self.exploitability + 
                self.affected_users + self.discoverability)
    
    @property
    def average(self) -> float:
        """Calculate average DREAD score (0-10)"""
        return self.total / 5
    
    @property
    def risk_level(self) -> str:
        """Determine risk level based on average score"""
        avg = self.average
        if avg >= 8:
            return "Critical"
        elif avg >= 6:
            return "High"
        elif avg >= 4:
            return "Medium"
        else:
            return "Low"

class DREADScorer:
    """Calculate DREAD scores for smart contract vulnerabilities"""
    
    # Vulnerability type to DREAD mapping
    VULNERABILITY_DREAD_MAP = {
        'Re-entrancy Attack': DREADScore(10, 8, 7, 10, 6),
        'Reentrancy': DREADScore(10, 8, 7, 10, 6),
        'Integer Overflow': DREADScore(9, 9, 6, 9, 7),
        'Integer Underflow': DREADScore(9, 9, 6, 9, 7),
        'Unchecked External Call': DREADScore(8, 7, 6, 8, 8),
        'Access Control Violation': DREADScore(9, 8, 5, 10, 7),
        'Unprotected Ether Withdrawal': DREADScore(10, 9, 6, 10, 8),
        'Timestamp Dependence': DREADScore(6, 8, 7, 7, 6),
        'Delegatecall to Untrusted Callee': DREADScore(10, 7, 6, 10, 5),
        'Uninitialized Storage Pointer': DREADScore(8, 6, 5, 8, 4),
        'Denial of Service': DREADScore(7, 7, 6, 9, 6),
        'Front-Running': DREADScore(7, 8, 7, 8, 5),
        'Weak Randomness': DREADScore(8, 9, 7, 9, 6),
        'Selfdestruct': DREADScore(10, 8, 5, 10, 7),
        'Arbitrary Jump': DREADScore(9, 5, 4, 9, 3),
        'Gas Limit': DREADScore(5, 7, 6, 6, 7),
        'Transaction Order Dependence': DREADScore(6, 7, 7, 7, 5),
    }
    
    # Default DREAD scores by severity
    DEFAULT_SCORES = {
        'Critical': DREADScore(10, 8, 7, 10, 7),
        'High': DREADScore(8, 7, 6, 8, 6),
        'Medium': DREADScore(6, 6, 5, 6, 5),
        'Low': DREADScore(4, 5, 4, 4, 4),
    }
    
    def calculate_dread(self, vulnerability: Dict) -> DREADScore:
        """
        Calculate DREAD score for a vulnerability
        
        Args:
            vulnerability: Dict with 'type' and 'severity' keys
            
        Returns:
            DREADScore object
        """
        vuln_type = vulnerability.get('type', '')
        severity = vulnerability.get('severity', 'Medium')
        
        # Try to find exact match for vulnerability type
        for key, score in self.VULNERABILITY_DREAD_MAP.items():
            if key.lower() in vuln_type.lower():
                return score
        
        # Fallback to severity-based default
        return self.DEFAULT_SCORES.get(severity, self.DEFAULT_SCORES['Medium'])
    
    def calculate_aggregate_dread(self, vulnerabilities: List[Dict]) -> Dict:
        """
        Calculate aggregate DREAD metrics for multiple vulnerabilities
        
        Returns:
            Dict with aggregate statistics
        """
        if not vulnerabilities:
            return {
                'average_damage': 0,
                'average_reproducibility': 0,
                'average_exploitability': 0,
                'average_affected_users': 0,
                'average_discoverability': 0,
                'average_total': 0,
                'max_risk_level': 'Low',
                'vulnerability_count': 0
            }
        
        scores = [self.calculate_dread(v) for v in vulnerabilities]
        
        count = len(scores)
        
        return {
            'average_damage': sum(s.damage for s in scores) / count,
            'average_reproducibility': sum(s.reproducibility for s in scores) / count,
            'average_exploitability': sum(s.exploitability for s in scores) / count,
            'average_affected_users': sum(s.affected_users for s in scores) / count,
            'average_discoverability': sum(s.discoverability for s in scores) / count,
            'average_total': sum(s.total for s in scores) / count,
            'max_risk_level': max((s.risk_level for s in scores), 
                                 key=lambda x: ['Low', 'Medium', 'High', 'Critical'].index(x)),
            'vulnerability_count': count,
            'individual_scores': [
                {
                    'type': v.get('type'),
                    'line': v.get('line'),
                    'dread': {
                        'damage': s.damage,
                        'reproducibility': s.reproducibility,
                        'exploitability': s.exploitability,
                        'affected_users': s.affected_users,
                        'discoverability': s.discoverability,
                        'total': s.total,
                        'average': s.average,
                        'risk_level': s.risk_level
                    }
                }
                for v, s in zip(vulnerabilities, scores)
            ]
        }
