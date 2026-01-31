import time
from celery import shared_task
from app.services.analysis_orchestrator import AnalysisOrchestrator
from app.services.analyzer import VulnerabilityAnalyzer
from app.services.bedrock_analyzer import BedrockAnalyzer
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# We need to re-initialize orchestrator here because Celery workers are separate processes
# In a real app, this might be a dependency injection or singleton pattern
def get_worker_orchestrator():
    static_analyzer = VulnerabilityAnalyzer()
    ai_analyzer = BedrockAnalyzer(region=settings.AWS_REGION, timeout=settings.BEDROCK_TIMEOUT)
    if not settings.ENABLE_AI_ANALYSIS:
        ai_analyzer.available = False
    return AnalysisOrchestrator(static_analyzer, ai_analyzer)

@shared_task(bind=True, name="scan_repo_task")
def scan_repo_task(self, github_url: str):
    logger.info(f"Starting background repo scan for {github_url}")
    # This is a placeholder for the actual logic which currently resides in main.py
    # In a full refactor, we would move the analyze_repo logic to a service and call it here.
    return {"status": "completed", "github_url": github_url}

@shared_task(bind=True, name="long_analysis_task")
def long_analysis_task(self, code: str):
    logger.info(f"Starting background contract analysis")
    orchestrator = get_worker_orchestrator()
    # Need to run async code in sync task?
    # AnalysisOrchestrator.analyze_contract is async. 
    # Valid strategy: use asgiref.sync.async_to_sync or just run loop
    import asyncio
    
    async def run_analysis():
        return await orchestrator.analyze_contract(code)
    
    result = asyncio.run(run_analysis())
    # Serialize result
    return {
        "risk_score": result.risk_score,
        "vulnerabilities": [v.type for v in result.vulnerabilities]
    }
