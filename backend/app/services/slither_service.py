"""
Slither Integration Service
Runs Slither static analysis and converts results to Auralis format
"""

import subprocess
import json
import tempfile
import os
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SlitherService:
    """Service for running Slither analysis and converting results"""
    
    def __init__(self):
        self.available = self._check_slither_available()
    
    def _check_slither_available(self) -> bool:
        """Check if Slither is installed and available"""
        try:
            result = subprocess.run(
                ['slither', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            logger.warning(f"Slither not available: {str(e)}")
            return False
    
    def analyze_contract(self, code: str, filename: str = "contract.sol") -> Optional[Dict]:
        """
        Analyze a smart contract using Slither
        
        Args:
            code: Solidity source code
            filename: Name for the temporary file
            
        Returns:
            Dictionary with Slither analysis results in Auralis format
        """
        if not self.available:
            logger.warning("Slither is not available")
            return None
        
        # Create temporary file
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / filename
            temp_file.write_text(code, encoding='utf-8')
            
            try:
                # Run Slither with JSON output
                result = subprocess.run(
                    ['slither', str(temp_file), '--json', '-'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Slither returns non-zero even on success if vulnerabilities found
                if result.stdout:
                    slither_data = json.loads(result.stdout)
                    return self._convert_to_auralis_format(slither_data)
                else:
                    logger.error(f"Slither analysis failed: {result.stderr}")
                    return None
                    
            except subprocess.TimeoutExpired:
                logger.error("Slither analysis timed out")
                return None
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Slither output: {str(e)}")
                return None
            except Exception as e:
                logger.error(f"Slither analysis error: {str(e)}")
                return None
    
    def _convert_to_auralis_format(self, slither_data: Dict) -> Dict:
        """Convert Slither JSON output to Auralis vulnerability format"""
        vulnerabilities = []
        
        # Extract detectors from Slither results
        detectors = slither_data.get('results', {}).get('detectors', [])
        
        for detector in detectors:
            # Map Slither impact to Auralis severity
            impact = detector.get('impact', 'Informational')
            severity = self._map_severity(impact)
            
            # Extract line number from source mapping
            line_number = self._extract_line_number(detector)
            
            # Map Slither confidence to percentage
            confidence = self._map_confidence(detector.get('confidence', 'Medium'))
            
            vuln = {
                'type': detector.get('check', 'Unknown'),
                'line': line_number,
                'severity': severity,
                'confidence': confidence,
                'description': detector.get('description', ''),
                'recommendation': self._generate_recommendation(detector),
                'source': 'slither',
                'slither_impact': impact,
                'slither_confidence': detector.get('confidence', 'Medium')
            }
            
            vulnerabilities.append(vuln)
        
        # Calculate risk score based on vulnerabilities
        risk_score = self._calculate_risk_score(vulnerabilities)
        
        return {
            'vulnerabilities': vulnerabilities,
            'risk_score': risk_score,
            'analysis_method': 'slither',
            'slither_version': slither_data.get('success', True)
        }
    
    def _map_severity(self, slither_impact: str) -> str:
        """Map Slither impact levels to Auralis severity levels"""
        mapping = {
            'High': 'High',
            'Medium': 'Medium',
            'Low': 'Low',
            'Informational': 'Low',
            'Optimization': 'Low'
        }
        return mapping.get(slither_impact, 'Medium')
    
    def _map_confidence(self, slither_confidence: str) -> int:
        """Map Slither confidence to percentage"""
        mapping = {
            'High': 90,
            'Medium': 70,
            'Low': 50
        }
        return mapping.get(slither_confidence, 70)
    
    def _extract_line_number(self, detector: Dict) -> int:
        """Extract line number from Slither detector result"""
        try:
            # Try to get line from first element
            elements = detector.get('elements', [])
            if elements:
                source_mapping = elements[0].get('source_mapping', {})
                lines = source_mapping.get('lines', [])
                if lines:
                    return lines[0]
            
            # Fallback to first_markdown_element
            first_element = detector.get('first_markdown_element', {})
            if first_element:
                source_mapping = first_element.get('source_mapping', {})
                lines = source_mapping.get('lines', [])
                if lines:
                    return lines[0]
        except Exception:
            pass
        
        return 0
    
    def _generate_recommendation(self, detector: Dict) -> str:
        """Generate recommendation based on Slither detector type"""
        check = detector.get('check', '')
        
        recommendations = {
            'reentrancy-eth': 'Use the Checks-Effects-Interactions pattern and consider using ReentrancyGuard',
            'arbitrary-send-eth': 'Restrict who can call this function or use pull payment pattern',
            'unprotected-upgrade': 'Add access control to upgrade functions',
            'suicidal': 'Add access control to selfdestruct function',
            'controlled-delegatecall': 'Avoid delegatecall to user-controlled addresses',
            'timestamp': 'Avoid using block.timestamp for critical logic',
            'weak-prng': 'Use Chainlink VRF or similar for random number generation'
        }
        
        return recommendations.get(check, 'Review and fix this issue according to best practices')
    
    def _calculate_risk_score(self, vulnerabilities: List[Dict]) -> int:
        """Calculate overall risk score from vulnerabilities"""
        if not vulnerabilities:
            return 0
        
        severity_weights = {
            'Critical': 25,
            'High': 20,
            'Medium': 10,
            'Low': 5
        }
        
        total_score = sum(
            severity_weights.get(v['severity'], 5) 
            for v in vulnerabilities
        )
        
        return min(total_score, 100)
