"""
Analysis Orchestrator Service

This service coordinates the execution of both static and AI analyzers,
merges their results, and provides a unified analysis response.
"""

import time
import uuid
import logging
from typing import List
from app.models.contract import AnalysisResult, Vulnerability
from app.services.analyzer import VulnerabilityAnalyzer
from app.services.bedrock_analyzer import BedrockAnalyzer
from app.services.vulnerability_merger import VulnerabilityMerger

logger = logging.getLogger(__name__)


class AnalysisOrchestrator:
    """
    Orchestrates hybrid analysis combining static and AI analysis.
    
    This class coordinates the execution of both analyzers, handles failures
    gracefully, merges results, and provides comprehensive analysis metrics.
    """
    
    def __init__(self, static_analyzer: VulnerabilityAnalyzer, ai_analyzer: BedrockAnalyzer):
        """
        Initialize the Analysis Orchestrator.
        
        Args:
            static_analyzer: The static pattern-matching vulnerability analyzer
            ai_analyzer: The AWS Bedrock AI-powered analyzer
        """
        self.static_analyzer = static_analyzer
        self.ai_analyzer = ai_analyzer
        self.merger = VulnerabilityMerger()
    
    async def analyze_contract(self, contract_code: str) -> AnalysisResult:
        """
        Orchestrates hybrid analysis combining static and AI analysis.
        
        This method executes the main orchestration logic:
        1. Runs static analysis first
        2. Attempts AI analysis with static results as context
        3. Merges results when both succeed
        4. Handles failures gracefully
        5. Calculates unified metrics
        
        Args:
            contract_code: The Solidity contract source code to analyze
            
        Returns:
            AnalysisResult with merged vulnerabilities and metadata
        """
        start_time = time.time()
        analysis_id = str(uuid.uuid4())
        
        logger.info(f"Starting hybrid analysis for contract {analysis_id} (code length: {len(contract_code)} chars)")
        
        # Execute static analyzer first and collect results
        static_start_time = time.time()
        logger.info("Executing static analysis...")
        static_vulnerabilities = self.static_analyzer.analyze(contract_code)
        static_duration = int((time.time() - static_start_time) * 1000)
        
        # Log static analysis results with performance metrics
        severity_breakdown = {}
        for vuln in static_vulnerabilities:
            severity_breakdown[vuln.severity] = severity_breakdown.get(vuln.severity, 0) + 1
        
        logger.info(f"Static analysis completed in {static_duration}ms, found {len(static_vulnerabilities)} vulnerabilities")
        if severity_breakdown:
            breakdown_str = ", ".join([f"{count} {severity}" for severity, count in severity_breakdown.items()])
            logger.info(f"Static analysis severity breakdown: {breakdown_str}")
        
        # Initialize result variables
        merged_vulnerabilities = static_vulnerabilities
        analysis_method = "static"
        ai_available = self.ai_analyzer.available
        ai_duration = 0
        merge_duration = 0
        
        # Log AI analyzer availability status for debugging
        if ai_available:
            logger.debug("AI analyzer is available and will be attempted")
        else:
            logger.info("AI analyzer is not available - analysis will use static analysis only")
            logger.debug("AI analyzer unavailability reason: AWS credentials not configured or initialization failed")
        
        # Attempt AI analysis with static results as context
        if ai_available:
            ai_start_time = time.time()
            logger.info(f"Attempting AI analysis with {len(static_vulnerabilities)} static vulnerabilities as context...")
            
            try:
                ai_result = self.ai_analyzer.analyze(contract_code, static_vulnerabilities)
                ai_duration = int((time.time() - ai_start_time) * 1000)
                
                if ai_result.success:
                    # Log AI analysis success with performance metrics
                    ai_severity_breakdown = {}
                    for vuln in ai_result.vulnerabilities:
                        ai_severity_breakdown[vuln.severity] = ai_severity_breakdown.get(vuln.severity, 0) + 1
                    
                    logger.info(f"AI analysis succeeded in {ai_duration}ms, found {len(ai_result.vulnerabilities)} vulnerabilities")
                    if ai_severity_breakdown:
                        ai_breakdown_str = ", ".join([f"{count} {severity}" for severity, count in ai_severity_breakdown.items()])
                        logger.info(f"AI analysis severity breakdown: {ai_breakdown_str}")
                    
                    # Merge results using VulnerabilityMerger when AI succeeds
                    merge_start_time = time.time()
                    merged_vulnerabilities = self.merger.merge(static_vulnerabilities, ai_result.vulnerabilities)
                    merge_duration = int((time.time() - merge_start_time) * 1000)
                    analysis_method = "hybrid"
                    
                    # Calculate deduplication statistics
                    total_before_merge = len(static_vulnerabilities) + len(ai_result.vulnerabilities)
                    duplicates_removed = total_before_merge - len(merged_vulnerabilities)
                    
                    logger.info(f"Vulnerability merge completed in {merge_duration}ms: {total_before_merge} total -> {len(merged_vulnerabilities)} final ({duplicates_removed} duplicates removed)")
                else:
                    logger.warning(f"AI analysis failed after {ai_duration}ms but static analysis succeeded - Error: {ai_result.error_message}")
                    logger.info("Falling back to static analysis results only")
                    # Keep static results and analysis_method as "static"
                    
            except Exception as e:
                ai_duration = int((time.time() - ai_start_time) * 1000)
                
                # Log detailed error information for different exception types
                if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                    logger.error(f"AI analysis timed out after {ai_duration}ms - falling back to static analysis only")
                    logger.debug(f"Timeout error details: {type(e).__name__}: {str(e)}")
                elif "credentials" in str(e).lower() or "unauthorized" in str(e).lower():
                    logger.error(f"AI analysis failed due to credential issues after {ai_duration}ms - falling back to static analysis only")
                    logger.debug(f"Credential error details: {type(e).__name__}: {str(e)}")
                else:
                    logger.error(f"Unexpected error during AI analysis after {ai_duration}ms - {type(e).__name__}: {str(e)}", exc_info=True)
                
                logger.info("Falling back to static analysis results only")
                # Keep static results and analysis_method as "static"
        else:
            logger.info("AI analyzer not available, using static analysis only")
            if not self.ai_analyzer.available:
                logger.debug("AI analyzer unavailable due to: missing AWS credentials or initialization failure")
        
        # Calculate unified risk score from merged vulnerabilities
        risk_score = self._calculate_unified_risk_score(merged_vulnerabilities)
        
        # Track processing time for performance metrics
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Generate summary
        summary = self._generate_summary(merged_vulnerabilities, analysis_method)
        
        # Log comprehensive analysis completion with performance metrics
        logger.info(f"Analysis {analysis_id} completed in {processing_time_ms}ms using {analysis_method} method")
        logger.info(f"Final results: {len(merged_vulnerabilities)} vulnerabilities, risk score: {risk_score}")
        
        # Log performance breakdown if we have timing data
        if analysis_method == "hybrid":
            logger.info(f"Performance breakdown - Static: {static_duration}ms, AI: {ai_duration}ms, Merge: {merge_duration}ms, Total: {processing_time_ms}ms")
            
            # Performance monitoring and alerting
            if processing_time_ms > 25000:  # 25 seconds
                logger.warning(f"Analysis took longer than expected: {processing_time_ms}ms (threshold: 25000ms)")
            if ai_duration > 20000:  # 20 seconds for AI alone
                logger.warning(f"AI analysis was slow: {ai_duration}ms (threshold: 20000ms)")
                
        elif analysis_method == "static":
            logger.info(f"Performance breakdown - Static: {static_duration}ms, Total: {processing_time_ms}ms")
            
            # Performance monitoring for static-only analysis
            if static_duration > 5000:  # 5 seconds for static analysis
                logger.warning(f"Static analysis was slower than expected: {static_duration}ms (threshold: 5000ms)")
        
        # Log performance metrics for monitoring and optimization
        logger.debug(f"Performance metrics - Analysis ID: {analysis_id}, Method: {analysis_method}, "
                    f"Static: {static_duration}ms, AI: {ai_duration}ms, Merge: {merge_duration}ms, "
                    f"Total: {processing_time_ms}ms, Vulnerabilities: {len(merged_vulnerabilities)}, "
                    f"Risk Score: {risk_score}")
        
        return AnalysisResult(
            analysis_id=analysis_id,
            vulnerabilities=merged_vulnerabilities,
            risk_score=risk_score,
            summary=summary,
            analysis_method=analysis_method,
            ai_available=ai_available,
            processing_time_ms=processing_time_ms
        )
    
    def _calculate_unified_risk_score(self, vulnerabilities: List[Vulnerability]) -> int:
        """
        Calculate unified risk score from merged vulnerabilities.
        
        Uses weighted scoring based on severity and confidence levels.
        
        Args:
            vulnerabilities: List of vulnerabilities to score
            
        Returns:
            Risk score between 0 and 100
        """
        if not vulnerabilities:
            return 0
        
        severity_weights = {
            "Critical": 25,
            "High": 15,
            "Medium": 10,
            "Low": 5
        }
        
        total_score = 0
        for vuln in vulnerabilities:
            base_score = severity_weights.get(vuln.severity, 5)
            # Apply confidence weighting
            weighted_score = base_score * vuln.confidence
            total_score += weighted_score
        
        # Cap at 100 and round to integer
        return min(int(total_score), 100)
    
    def _generate_summary(self, vulnerabilities: List[Vulnerability], analysis_method: str) -> str:
        """
        Generate a human-readable summary of the analysis results.
        
        Args:
            vulnerabilities: List of detected vulnerabilities
            analysis_method: Method used for analysis ("static", "ai", or "hybrid")
            
        Returns:
            Summary string describing the analysis results
        """
        if not vulnerabilities:
            return f"No vulnerabilities detected using {analysis_method} analysis."
        
        # Count vulnerabilities by severity
        severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for vuln in vulnerabilities:
            severity_counts[vuln.severity] = severity_counts.get(vuln.severity, 0) + 1
        
        # Build summary parts
        total_count = len(vulnerabilities)
        method_description = {
            "static": "static pattern matching",
            "ai": "AI-powered semantic analysis", 
            "hybrid": "hybrid static and AI analysis"
        }.get(analysis_method, analysis_method)
        
        summary_parts = [f"Found {total_count} vulnerabilities using {method_description}."]
        
        # Add severity breakdown if there are vulnerabilities
        severity_parts = []
        for severity in ["Critical", "High", "Medium", "Low"]:
            count = severity_counts[severity]
            if count > 0:
                severity_parts.append(f"{count} {severity}")
        
        if severity_parts:
            summary_parts.append(f"Breakdown: {', '.join(severity_parts)}.")
        
        return " ".join(summary_parts)