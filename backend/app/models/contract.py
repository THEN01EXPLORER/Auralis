from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    contract_code: str
    chain_type: Optional[str] = "ethereum"

class RemediationDetails(BaseModel):
    explanation: str
    code_example: Optional[str] = None

class Vulnerability(BaseModel):
    type: str
    severity: str
    line: int
    description: str
    recommendation: str
    confidence: float = 0.85
    source: str = "static"  # "static", "ai", or "hybrid"
    remediation: Optional[RemediationDetails] = None

class AnalysisResult(BaseModel):
    analysis_id: str
    vulnerabilities: List[Vulnerability]
    risk_score: int
    summary: str
    analysis_method: str  # "static", "ai", or "hybrid"
    ai_available: bool
    processing_time_ms: int

class BedrockAnalysisResult(BaseModel):
    success: bool
    vulnerabilities: List[Vulnerability]
    error_message: Optional[str] = None
    processing_time_ms: int

class AnalyzeResponse(BaseModel):
    analysis_id: str
    vulnerabilities: List[Vulnerability]
    risk_score: int
    summary: str
