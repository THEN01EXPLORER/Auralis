from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import time
import logging
sys.path.append('app')
from app.utils.risk_calculator import calculate_risk_score
from app.services.analyzer import VulnerabilityAnalyzer
from app.services.bedrock_analyzer import BedrockAnalyzer
from app.services.analysis_orchestrator import AnalysisOrchestrator
from app.models.contract import AnalyzeResponse

# Configure logging with environment-based settings
def configure_logging():
    """Configure logging with environment-based settings for comprehensive error handling and debugging."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_format = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = os.getenv('LOG_FILE', None)
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level, logging.INFO)
    
    # Configure basic logging
    handlers = []
    
    # Console handler (always present)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)
    
    # File handler (optional)
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(numeric_level)
            file_formatter = logging.Formatter(log_format)
            file_handler.setFormatter(file_formatter)
            handlers.append(file_handler)
        except Exception as e:
            print(f"Warning: Could not create log file {log_file}: {e}")
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=handlers,
        force=True  # Override any existing configuration
    )
    
    # Log configuration details
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured - Level: {log_level}, Format: {log_format}")
    if log_file:
        logger.info(f"Log file: {log_file}")
    
    return logger

# Initialize logging configuration
logger = configure_logging()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers and orchestrator
def get_orchestrator():
    """Initialize and return the analysis orchestrator with configuration."""
    # Load configuration from environment variables
    enable_ai_analysis = os.getenv('ENABLE_AI_ANALYSIS', 'true').lower() == 'true'
    ai_analysis_required = os.getenv('AI_ANALYSIS_REQUIRED', 'false').lower() == 'true'
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    bedrock_timeout = int(os.getenv('BEDROCK_TIMEOUT', '25'))
    bedrock_model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
    
    # Log configuration
    logger.info("=== Auralis Analysis Configuration ===")
    logger.info(f"AI Analysis Enabled: {enable_ai_analysis}")
    logger.info(f"AI Analysis Required: {ai_analysis_required}")
    logger.info(f"AWS Region: {aws_region}")
    logger.info(f"Bedrock Timeout: {bedrock_timeout}s")
    logger.info(f"Bedrock Model: {bedrock_model_id}")
    
    # Initialize static analyzer
    static_analyzer = VulnerabilityAnalyzer()
    logger.info("Static analyzer initialized")
    
    # Initialize AI analyzer if enabled
    ai_analyzer = None
    if enable_ai_analysis:
        ai_analyzer = BedrockAnalyzer(region=aws_region, timeout=bedrock_timeout)
        if ai_analyzer.available:
            logger.info("AI analyzer initialized and available")
        else:
            logger.warning("AI analyzer initialized but not available (check AWS credentials)")
            if ai_analysis_required:
                logger.error("AI analysis is required but not available - service may fail")
    else:
        # Create a disabled AI analyzer
        ai_analyzer = BedrockAnalyzer(region=aws_region, timeout=bedrock_timeout)
        ai_analyzer.available = False
        logger.info("AI analysis disabled by configuration")
    
    return AnalysisOrchestrator(static_analyzer, ai_analyzer)

# Global orchestrator instance
orchestrator = get_orchestrator()

class ContractRequest(BaseModel):
    code: str

@app.get("/")
def root():
    return {"message": "Auralis API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/audit")
def audit(request: ContractRequest):
    return {
        "risk_score": 85,
        "vulnerabilities": [
            {
                "type": "Re-entrancy Attack",
                "line_number": 14,
                "severity": "High",
                "description": "External call detected before state changes.",
                "recommendation": "Use Checks-Effects-Interactions pattern"
            },
            {
                "type": "Access Control Violation",
                "line_number": 8,
                "severity": "Medium",
                "description": "Public function without access control.",
                "recommendation": "Add onlyOwner modifier"
            }
        ]
    }

@app.post("/api/v1/analyze")
async def analyze(request: ContractRequest):
    """
    Analyze smart contract for vulnerabilities using hybrid static and AI analysis.
    
    This endpoint uses the AnalysisOrchestrator to coordinate both static pattern-matching
    and AI-powered semantic analysis, providing comprehensive vulnerability detection.
    """
    try:
        request_start_time = time.time()
        logger.info(f"Starting contract analysis request (code length: {len(request.code)} characters)")
        
        # Log AI analyzer status and configuration
        ai_analysis_required = os.getenv('AI_ANALYSIS_REQUIRED', 'false').lower() == 'true'
        enable_ai_analysis = os.getenv('ENABLE_AI_ANALYSIS', 'true').lower() == 'true'
        
        logger.info(f"Analysis configuration - AI enabled: {enable_ai_analysis}, AI required: {ai_analysis_required}, AI available: {orchestrator.ai_analyzer.available}")
        
        if orchestrator.ai_analyzer.available:
            logger.info("AI analyzer is available for this request")
        else:
            logger.warning("AI analyzer is not available for this request")
            if ai_analysis_required:
                logger.error("AI analysis is required but not available - failing request with 503 status")
                raise HTTPException(
                    status_code=503, 
                    detail="AI analysis is required but not available. Please check AWS configuration."
                )
        
        # Use orchestrator to perform hybrid analysis
        analysis_result = await orchestrator.analyze_contract(request.code)
        
        # Log analysis results with detailed status
        if analysis_result.analysis_method == "hybrid":
            logger.info("Successfully completed hybrid analysis (static + AI)")
        elif analysis_result.analysis_method == "static":
            if orchestrator.ai_analyzer.available:
                logger.warning("AI analysis failed but static analysis succeeded - falling back to static analysis only")
            else:
                logger.info("Completed static analysis only (AI analyzer not available)")
        
        # Convert vulnerabilities to the expected format for backward compatibility
        vulnerabilities_dict = []
        for vuln in analysis_result.vulnerabilities:
            vuln_dict = {
                "type": vuln.type,
                "line": vuln.line,
                "severity": vuln.severity,
                "confidence": int(vuln.confidence * 100),  # Convert to percentage for backward compatibility
                "description": vuln.description,
                "recommendation": vuln.recommendation
            }
            
            # Add remediation if available
            if vuln.remediation:
                vuln_dict["remediation"] = {
                    "explanation": vuln.remediation.explanation,
                    "code_example": vuln.remediation.code_example
                }
            
            vulnerabilities_dict.append(vuln_dict)
        
        # Build response with new fields while maintaining backward compatibility
        response = {
            "analysis_id": analysis_result.analysis_id,
            "risk_score": analysis_result.risk_score,
            "vulnerabilities": vulnerabilities_dict,
            "summary": analysis_result.summary,
            # New fields for enhanced functionality
            "analysis_method": analysis_result.analysis_method,
            "ai_available": analysis_result.ai_available,
            "processing_time_ms": analysis_result.processing_time_ms
        }
        
        # Log comprehensive performance metrics and results
        total_request_time = int((time.time() - request_start_time) * 1000)
        logger.info(f"Request completed successfully - Method: {analysis_result.analysis_method}, "
                   f"Vulnerabilities: {len(analysis_result.vulnerabilities)}, "
                   f"Risk Score: {analysis_result.risk_score}, "
                   f"Analysis Time: {analysis_result.processing_time_ms}ms, "
                   f"Total Request Time: {total_request_time}ms")
        
        # Log vulnerability breakdown by severity for monitoring
        severity_counts = {}
        for vuln in analysis_result.vulnerabilities:
            severity_counts[vuln.severity] = severity_counts.get(vuln.severity, 0) + 1
        
        if severity_counts:
            severity_summary = ", ".join([f"{count} {severity}" for severity, count in severity_counts.items()])
            logger.info(f"Vulnerability severity breakdown: {severity_summary}")
        
        return response
        
    except HTTPException as e:
        # Log HTTP exceptions with context before re-raising
        total_request_time = int((time.time() - request_start_time) * 1000)
        logger.warning(f"Request failed with HTTP {e.status_code} after {total_request_time}ms: {e.detail}")
        
        # Log additional context for debugging
        if e.status_code == 503:
            logger.debug("Service unavailable - likely due to AI analysis being required but not available")
        elif e.status_code >= 400 and e.status_code < 500:
            logger.debug(f"Client error {e.status_code} - check request format and configuration")
        
        raise
    except Exception as e:
        # Log unexpected errors with comprehensive context for debugging
        total_request_time = int((time.time() - request_start_time) * 1000)
        error_type = type(e).__name__
        error_message = str(e)
        
        logger.error(f"Unexpected analysis error after {total_request_time}ms - {error_type}: {error_message}", exc_info=True)
        
        # Log additional context that might help with debugging
        logger.debug(f"Error context - Contract length: {len(request.code)} chars, "
                    f"AI available: {orchestrator.ai_analyzer.available}, "
                    f"Request time: {total_request_time}ms")
        
        # Log system resource information if available
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent
            cpu_percent = psutil.cpu_percent()
            logger.debug(f"System resources at error - Memory: {memory_percent}%, CPU: {cpu_percent}%")
        except ImportError:
            logger.debug("System resource monitoring not available (psutil not installed)")
        except Exception:
            logger.debug("Could not retrieve system resource information")
        
        raise HTTPException(status_code=500, detail="Internal server error during analysis")
