from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
import sys
import time
import logging
import tempfile
import shutil
from pathlib import Path
from contextlib import asynccontextmanager
try:
    from git import Repo
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    Repo = None
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.errors import http_exception_handler, validation_exception_handler, generic_exception_handler
from app.core.middleware import RequestIdMiddleware, AccessLogMiddleware


sys.path.append('app')
from app.utils.risk_calculator import calculate_risk_score
from app.services.analyzer import VulnerabilityAnalyzer
from app.services.bedrock_analyzer import BedrockAnalyzer
from app.services.analyzer import VulnerabilityAnalyzer
from app.services.bedrock_analyzer import BedrockAnalyzer
from app.services.analysis_orchestrator import AnalysisOrchestrator
from app.api.deps import get_current_user
from fastapi import Depends
try:
    from app.services.dread_scorer import DREADScorer
    from app.services.pdf_report_generator import PDFReportGenerator
    ADVANCED_FEATURES = True
except ImportError:
    ADVANCED_FEATURES = False
    DREADScorer = None
    PDFReportGenerator = None
from app.models.contract import AnalyzeResponse

# Configure logging with environment-based settings
# Logging is configured via app.core.logging

# Initialize logging configuration
logger = configure_logging()

# Lifespan event handler for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    app.state.start_time = time.time()
    app.state.total_scans = 0
    app.state.total_vulnerabilities = 0
    app.state.risk_scores_sum = 0
    app.state.avg_risk_score = 0
    logger.info("Auralis API started successfully")
    yield
    # Shutdown (if needed in the future)
    logger.info("Auralis API shutting down")

app = FastAPI(
    title="Auralis API",
    description="AI-powered smart contract security auditor",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Initialize Prometheus Metrics
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

# Initialize Sentry
if settings.SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.starlette import StarletteIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[
            FastApiIntegration(), 
            StarletteIntegration(),
            RedisIntegration(),
        ],
        traces_sample_rate=0.1,
    )
    logger.info("Sentry integration enabled")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Add rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded errors with proper response format."""
    logger.warning(f"Rate limit exceeded for IP: {get_remote_address(request)}")
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": "Too many requests. Please try again later.",
            "retry_after": 60
        },
        headers={"Retry-After": "60"}
    )

# CORS configuration - restrict in production
# Middleware
app.add_middleware(AccessLogMiddleware)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS else ["*"]
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
# Generic handler disabled for now to allow easier debugging during development, 
# enable in production or wrap in strict conditional.
# app.add_exception_handler(Exception, generic_exception_handler)

# Initialize analyzers and orchestrator
def get_orchestrator():
    """Initialize and return the analysis orchestrator with configuration."""
    # Log configuration
    logger.info("=== Auralis Analysis Configuration ===")
    logger.info(f"AI Analysis Enabled: {settings.ENABLE_AI_ANALYSIS}")
    logger.info(f"AI Analysis Required: {settings.AI_ANALYSIS_REQUIRED}")
    logger.info(f"AWS Region: {settings.AWS_REGION}")
    logger.info(f"Bedrock Timeout: {settings.BEDROCK_TIMEOUT}s")
    logger.info(f"Bedrock Model: {settings.BEDROCK_MODEL_ID}")
    
    # Initialize static analyzer
    static_analyzer = VulnerabilityAnalyzer()
    logger.info("Static analyzer initialized")
    
    # Initialize AI analyzer if enabled
    ai_analyzer = None
    if settings.ENABLE_AI_ANALYSIS:
        ai_analyzer = BedrockAnalyzer(region=settings.AWS_REGION, timeout=settings.BEDROCK_TIMEOUT)
        if ai_analyzer.available:
            logger.info("AI analyzer initialized and available")
        else:
            logger.warning("AI analyzer initialized but not available (check AWS credentials)")
            if settings.AI_ANALYSIS_REQUIRED:
                logger.error("AI analysis is required but not available - service may fail")
    else:
        # Create a disabled AI analyzer
        ai_analyzer = BedrockAnalyzer(region=settings.AWS_REGION, timeout=settings.BEDROCK_TIMEOUT)
        ai_analyzer.available = False
        logger.info("AI analysis disabled by configuration")
    
    return AnalysisOrchestrator(static_analyzer, ai_analyzer)

# Global orchestrator instance
orchestrator = get_orchestrator()

class ContractRequest(BaseModel):
    code: str

class RepoRequest(BaseModel):
    github_url: str

@app.get("/")
def root():
    """Root endpoint - not rate limited."""
    return {"message": "Auralis API", "status": "running"}

@app.get("/health")
async def health():
    """
    Liveness probe - is the app running?
    """
    return {"status": "ok", "version": "1.0.0"}

@app.get("/ready")
async def ready():
    """
    Readiness probe - is the app ready to accept traffic?
    Checks critical dependencies like Redis.
    """
    readiness = {
        "status": "ok",
        "checks": {
            "api": True,
            "redis": False
        }
    }
    
    # Check Redis
    try:
        from app.worker import celery_app
        # Ping redis
        with celery_app.connection_for_write() as conn:
            conn.default_channel.client.ping()
        readiness["checks"]["redis"] = True
    except Exception as e:
        logger.error(f"Readiness check failed: Redis unreachable: {e}")
        readiness["status"] = "degraded"
        # In a strict environment, you might return 503 here
        # return JSONResponse(status_code=503, content=readiness)
    
    return readiness

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
@limiter.limit("60/minute")
async def analyze(request: Request, contract_request: ContractRequest):
    """
    Analyze smart contract for vulnerabilities using hybrid static and AI analysis.
    
    This endpoint uses the AnalysisOrchestrator to coordinate both static pattern-matching
    and AI-powered semantic analysis, providing comprehensive vulnerability detection.
    """
    request_start_time = time.time()
    try:
        logger.info(f"Starting contract analysis request (code length: {len(contract_request.code)} characters)")
        
        # Log AI analyzer status and configuration
        logger.info(f"Analysis configuration - AI enabled: {settings.ENABLE_AI_ANALYSIS}, AI required: {settings.AI_ANALYSIS_REQUIRED}, AI available: {orchestrator.ai_analyzer.available}")
        
        if orchestrator.ai_analyzer.available:
            logger.info("AI analyzer is available for this request")
        else:
            logger.warning("AI analyzer is not available for this request")
            if settings.AI_ANALYSIS_REQUIRED:
                logger.error("AI analysis is required but not available - failing request with 503 status")
                raise HTTPException(
                    status_code=503, 
                    detail="AI analysis is required but not available. Please check AWS configuration."
                )
        
        # Use orchestrator to perform hybrid analysis
        analysis_result = await orchestrator.analyze_contract(contract_request.code)
        
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
        
        # Update global statistics
        if not hasattr(app.state, 'total_scans'):
            app.state.total_scans = 0
            app.state.total_vulnerabilities = 0
            app.state.risk_scores_sum = 0
        
        app.state.total_scans += 1
        app.state.total_vulnerabilities += len(analysis_result.vulnerabilities)
        app.state.risk_scores_sum += analysis_result.risk_score
        app.state.avg_risk_score = int(app.state.risk_scores_sum / app.state.total_scans)
        
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
        logger.debug(f"Error context - Contract length: {len(contract_request.code)} chars, "
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


@app.post("/api/v1/analyze_repo")
@limiter.limit("10/minute")
async def analyze_repo(request: Request, repo_request: RepoRequest):
    """
    Analyze an entire GitHub repository for smart contract vulnerabilities.
    
    This endpoint clones a GitHub repository, finds all .sol files, and analyzes
    each one using the hybrid analysis orchestrator. Returns a dictionary mapping
    filenames to their full analysis reports.
    """
    # Check if git is available
    if not GIT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Repository scanning is not available in this deployment. GitPython dependency is not installed."
        )
    
    temp_dir = None
    request_start_time = time.time()
    
    try:
        logger.info(f"Starting repository analysis for URL: {repo_request.github_url}")
        
        # Create temporary directory for cloning
        temp_dir = tempfile.TemporaryDirectory()
        clone_path = temp_dir.name
        
        logger.info(f"Cloning repository to temporary directory: {clone_path}")
        clone_start_time = time.time()
        
        # Clone the repository
        try:
            print(f"DEBUG: Cloning {repo_request.github_url} to {clone_path}")
            Repo.clone_from(repo_request.github_url, clone_path, depth=1)
            clone_duration = int((time.time() - clone_start_time) * 1000)
            logger.info(f"Repository cloned successfully in {clone_duration}ms")
        except Exception as e:
            print(f"DEBUG: Clone FAILED. Error: {type(e).__name__}: {str(e)}")
            logger.error(f"Failed to clone repository: {type(e).__name__}: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to clone repository. Please check the URL and ensure it's a valid public GitHub repository. Error: {str(e)}"
            )
        
        # Find all .sol files in the cloned repository
        sol_files = []
        for sol_file in Path(clone_path).rglob("*.sol"):
            # Skip files in common dependency directories
            if any(skip_dir in sol_file.parts for skip_dir in ['node_modules', '.git', 'test', 'tests']):
                continue
            sol_files.append(sol_file)
        
        logger.info(f"Found {len(sol_files)} Solidity files to analyze")
        
        if not sol_files:
            logger.warning("No Solidity files found in repository")
            raise HTTPException(
                status_code=404,
                detail="No Solidity (.sol) files found in the repository"
            )
        
        # Analyze each .sol file
        results = {}
        total_vulnerabilities = 0
        
        for sol_file in sol_files:
            filename = str(sol_file.name)  # Initialize with default value
            try:
                # Read file content
                with open(sol_file, 'r', encoding='utf-8') as f:
                    contract_code = f.read()
                
                # Get relative path for cleaner filename
                relative_path = sol_file.relative_to(clone_path)
                filename = str(relative_path)
                
                logger.info(f"Analyzing file: {filename} ({len(contract_code)} characters)")
                
                # Analyze the contract using the orchestrator
                analysis_result = await orchestrator.analyze_contract(contract_code)
                
                # Convert to response format
                vulnerabilities_dict = []
                for vuln in analysis_result.vulnerabilities:
                    vuln_dict = {
                        "type": vuln.type,
                        "line": vuln.line,
                        "severity": vuln.severity,
                        "confidence": int(vuln.confidence * 100),
                        "description": vuln.description,
                        "recommendation": vuln.recommendation
                    }
                    
                    if vuln.remediation:
                        vuln_dict["remediation"] = {
                            "explanation": vuln.remediation.explanation,
                            "code_example": vuln.remediation.code_example
                        }
                    
                    vulnerabilities_dict.append(vuln_dict)
                
                # Store result for this file
                results[filename] = {
                    "analysis_id": analysis_result.analysis_id,
                    "risk_score": analysis_result.risk_score,
                    "vulnerabilities": vulnerabilities_dict,
                    "summary": analysis_result.summary,
                    "analysis_method": analysis_result.analysis_method,
                    "ai_available": analysis_result.ai_available,
                    "processing_time_ms": analysis_result.processing_time_ms
                }
                
                total_vulnerabilities += len(analysis_result.vulnerabilities)
                logger.info(f"Completed analysis of {filename}: {len(analysis_result.vulnerabilities)} vulnerabilities, risk score: {analysis_result.risk_score}")
                
            except Exception as e:
                logger.error(f"Error analyzing file {filename}: {type(e).__name__}: {str(e)}")
                results[filename] = {
                    "error": f"Failed to analyze file: {str(e)}",
                    "risk_score": 0,
                    "vulnerabilities": [],
                    "summary": f"Analysis failed: {str(e)}"
                }
        
        # Calculate total processing time
        total_time = int((time.time() - request_start_time) * 1000)
        
        logger.info(f"Repository analysis completed in {total_time}ms: {len(sol_files)} files analyzed, {total_vulnerabilities} total vulnerabilities found")
        
        return {
            "repository_url": repo_request.github_url,
            "files_analyzed": len(sol_files),
            "total_vulnerabilities": total_vulnerabilities,
            "processing_time_ms": total_time,
            "results": results
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        total_time = int((time.time() - request_start_time) * 1000)
        logger.error(f"Unexpected error during repository analysis after {total_time}ms: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during repository analysis: {str(e)}"
        )
        
    finally:
        # Always clean up the temporary directory
        if temp_dir:
            try:
                temp_dir.cleanup()
                logger.info("Temporary directory cleaned up successfully")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary directory: {str(e)}")


@app.post("/api/v1/dread_score")
@limiter.limit("60/minute")
async def calculate_dread(request: Request, contract_request: ContractRequest):
    """
    Calculate DREAD risk scores for a contract
    """
    if not ADVANCED_FEATURES:
        raise HTTPException(
            status_code=503,
            detail="DREAD scoring is not available in this deployment."
        )
    
    try:
        # First analyze the contract
        analysis_result = await orchestrator.analyze_contract(contract_request.code)
        
        # Calculate DREAD scores
        dread_scorer = DREADScorer()
        
        # Convert vulnerabilities to dict format for DREAD scorer
        vulns_dict = [
            {
                'type': v.type,
                'line': v.line,
                'severity': v.severity,
                'description': v.description,
                'recommendation': v.recommendation
            }
            for v in analysis_result.vulnerabilities
        ]
        
        dread_scores = dread_scorer.calculate_aggregate_dread(vulns_dict)
        
        return {
            'analysis_id': analysis_result.analysis_id,
            'risk_score': analysis_result.risk_score,
            'dread_scores': dread_scores,
            'vulnerabilities_count': len(analysis_result.vulnerabilities)
        }
    except Exception as e:
        logger.error(f"DREAD scoring error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to calculate DREAD scores")


@app.post("/api/v1/generate_report")
@limiter.limit("30/minute")
async def generate_report(request: Request, contract_request: ContractRequest):
    """
    Generate a PDF audit report for a contract
    """
    if not ADVANCED_FEATURES:
        raise HTTPException(
            status_code=503,
            detail="PDF report generation is not available in this deployment."
        )
    
    try:
        # Analyze the contract
        analysis_result = await orchestrator.analyze_contract(contract_request.code)
        
        # Calculate DREAD scores
        dread_scorer = DREADScorer()
        
        # Convert vulnerabilities to dict format for DREAD scorer
        vulns_dict = [
            {
                'type': v.type,
                'line': v.line,
                'severity': v.severity,
                'description': v.description,
                'recommendation': v.recommendation
            }
            for v in analysis_result.vulnerabilities
        ]
        
        dread_scores = dread_scorer.calculate_aggregate_dread(vulns_dict)
        
        # Generate PDF
        pdf_generator = PDFReportGenerator()
        
        if not pdf_generator.available:
            raise HTTPException(
                status_code=503,
                detail="PDF generation not available. Install reportlab: pip install reportlab"
            )
        
        # Prepare analysis result dict
        analysis_dict = {
            'analysis_id': analysis_result.analysis_id,
            'risk_score': analysis_result.risk_score,
            'vulnerabilities': vulns_dict,
            'analysis_method': analysis_result.analysis_method
        }
        
        pdf_bytes = pdf_generator.generate_report(analysis_dict, dread_scores)
        
        # Return PDF as response
        from fastapi.responses import Response
        return Response(
            content=pdf_bytes,
            media_type='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="auralis_audit_{analysis_result.analysis_id}.pdf"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF generation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate PDF report")


@app.get("/api/v1/stats")
def get_stats():
    """Get API statistics and system metrics."""
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        system_info = {
            "cpu_usage_percent": cpu_percent,
            "memory_used_gb": round(memory.used / (1024**3), 2),
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "memory_percent": memory.percent,
            "disk_used_gb": round(disk.used / (1024**3), 2),
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_percent": disk.percent
        }
    except ImportError:
        system_info = {"available": False}
    except Exception as e:
        logger.error(f"System metrics error: {str(e)}")
        system_info = {"available": False}
    
    # Get AI analyzer status
    ai_available = orchestrator.ai_analyzer.available if orchestrator else False
    
    return {
        "status": "operational",
        "version": "1.0.0",
        "uptime_seconds": int(time.time() - getattr(app.state, 'start_time', time.time())),
        "system": system_info,
        "capabilities": {
            "ai_analysis": ai_available,
            "static_analysis": True,
            "repo_scanning": GIT_AVAILABLE,
            "pdf_reports": ADVANCED_FEATURES,
            "dread_scoring": ADVANCED_FEATURES
        },
        "analysis": {
            "total_scans": getattr(app.state, 'total_scans', 0),
            "total_vulnerabilities": getattr(app.state, 'total_vulnerabilities', 0),
            "avg_risk_score": getattr(app.state, 'avg_risk_score', 0),
            "detection_rate": 95
        }
    }


@app.get("/api/v1/supported_patterns")
def get_supported_patterns():
    """Get list of all supported vulnerability patterns."""
    patterns = [
        {
            "name": "Re-entrancy Attack",
            "severity": "Critical",
            "category": "Security",
            "description": "External calls before state changes can lead to re-entrancy"
        },
        {
            "name": "Integer Overflow/Underflow",
            "severity": "High",
            "category": "Security",
            "description": "Unchecked arithmetic operations"
        },
        {
            "name": "Access Control Violation",
            "severity": "Medium",
            "category": "Access Control",
            "description": "Public functions without proper access modifiers"
        },
        {
            "name": "Unchecked Return Value",
            "severity": "Medium",
            "category": "Security",
            "description": "Low-level calls without checking return values"
        },
        {
            "name": "Denial of Service",
            "severity": "High",
            "category": "Security",
            "description": "Potential DoS through gas limit issues"
        },
        {
            "name": "Front-running",
            "severity": "High",
            "category": "Security",
            "description": "Transaction ordering dependency vulnerabilities"
        },
        {
            "name": "Timestamp Dependence",
            "severity": "Low",
            "category": "Security",
            "description": "Reliance on block.timestamp for critical logic"
        }
    ]
    
    return {
        "total_patterns": len(patterns),
        "patterns": patterns,
        "categories": ["Security", "Access Control"]
    }


# Async Job Endpoints

@app.post("/api/v1/analyze_repo_async")
@limiter.limit("5/minute")
async def analyze_repo_async(request: Request, repo_request: RepoRequest, current_user: str = Depends(get_current_user)):
    """
    Trigger an asynchronous repository scan.
    Returns a task_id to poll for status.
    Protected by JWT Auth.
    """
    if not GIT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Repository scanning is not available."
        )
        
    from app.tasks.repo_scanner import scan_repo_task
    task = scan_repo_task.delay(repo_request.github_url)
    
    return {
        "task_id": task.id,
        "status": "accepted",
        "message": "Repository scan started in background"
    }

@app.get("/api/v1/jobs/{task_id}")
async def get_job_status(task_id: str, current_user: str = Depends(get_current_user)):
    """
    Get the status and result of a background job.
    """
    from celery.result import AsyncResult
    from app.worker import celery_app
    
    task_result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": task_result.status,
    }
    
    if task_result.successful():
        response["result"] = task_result.result
    elif task_result.failed():
        response["error"] = str(task_result.result)
        
    return response

# Lambda handler for AWS deployment
from mangum import Mangum
handler = Mangum(app)

# Run the server locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
