from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.contract import AnalyzeRequest, AnalyzeResponse
from app.services.analyzer import VulnerabilityAnalyzer
import uuid

app = FastAPI(title="Auralis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = VulnerabilityAnalyzer()

@app.get("/")
def root():
    return {"message": "Auralis Smart Contract Security Auditor API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze_contract(request: AnalyzeRequest):
    vulnerabilities = analyzer.analyze(request.contract_code)
    risk_score = analyzer.calculate_risk_score(vulnerabilities)
    
    return AnalyzeResponse(
        analysis_id=str(uuid.uuid4()),
        vulnerabilities=vulnerabilities,
        risk_score=risk_score,
        summary=f"Found {len(vulnerabilities)} vulnerabilities with risk score {risk_score}/100"
    )
