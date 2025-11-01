from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    contract_code: str
    chain_type: Optional[str] = "ethereum"

class Vulnerability(BaseModel):
    type: str
    severity: str
    line: int
    description: str
    recommendation: str

class AnalyzeResponse(BaseModel):
    analysis_id: str
    vulnerabilities: List[Vulnerability]
    risk_score: int
    summary: str
