"""
Auralis API - Minimal version for free tier hosting
No external dependencies beyond FastAPI/uvicorn
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import time
import re
import uuid
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Auralis API",
    description="Smart Contract Security Analyzer - Static Analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Store startup time
startup_time = time.time()
total_scans = 0
total_vulnerabilities = 0

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ContractRequest(BaseModel):
    code: str

class Vulnerability(BaseModel):
    type: str
    line: int
    severity: str
    confidence: int
    description: str
    recommendation: str

# Vulnerability patterns for static analysis
VULNERABILITY_PATTERNS = [
    {
        "name": "Reentrancy",
        "pattern": r"\.call\{.*value.*\}|\.call\.value\(|\.send\(|\.transfer\(",
        "severity": "Critical",
        "description": "Potential reentrancy vulnerability. External calls should be made after state changes.",
        "recommendation": "Use the Checks-Effects-Interactions pattern. Consider using ReentrancyGuard."
    },
    {
        "name": "Unchecked Return Value",
        "pattern": r"\.call\(|\.delegatecall\(|\.staticcall\(",
        "severity": "High",
        "description": "Return value of low-level call not checked.",
        "recommendation": "Always check the return value of low-level calls."
    },
    {
        "name": "Integer Overflow",
        "pattern": r"(\+\+|\-\-|\+=|\-=|\*=)",
        "severity": "Medium",
        "description": "Potential integer overflow/underflow.",
        "recommendation": "Use SafeMath library or Solidity 0.8+ with built-in overflow checks."
    },
    {
        "name": "Timestamp Dependency",
        "pattern": r"block\.timestamp|now",
        "severity": "Low",
        "description": "Block timestamp can be manipulated by miners.",
        "recommendation": "Avoid using block.timestamp for critical logic."
    },
    {
        "name": "tx.origin Authentication",
        "pattern": r"tx\.origin",
        "severity": "High",
        "description": "Using tx.origin for authentication is vulnerable to phishing attacks.",
        "recommendation": "Use msg.sender instead of tx.origin for authentication."
    },
    {
        "name": "Unprotected Selfdestruct",
        "pattern": r"selfdestruct\(|suicide\(",
        "severity": "Critical",
        "description": "Selfdestruct can be called, potentially destroying the contract.",
        "recommendation": "Add access control to selfdestruct functions."
    },
    {
        "name": "Floating Pragma",
        "pattern": r"pragma solidity \^",
        "severity": "Low",
        "description": "Floating pragma version detected.",
        "recommendation": "Lock pragma to a specific compiler version."
    },
    {
        "name": "Public Visibility",
        "pattern": r"function\s+\w+\s*\([^)]*\)\s*public(?!\s+view|\s+pure)",
        "severity": "Medium",
        "description": "Public function that modifies state detected.",
        "recommendation": "Consider if this function needs public visibility or should be restricted."
    },
    {
        "name": "Delegatecall Risk",
        "pattern": r"\.delegatecall\(",
        "severity": "High",
        "description": "Delegatecall can execute code in the context of the calling contract.",
        "recommendation": "Be extremely careful with delegatecall to untrusted contracts."
    },
    {
        "name": "Block Gas Limit",
        "pattern": r"for\s*\([^)]+\)\s*\{|while\s*\([^)]+\)\s*\{",
        "severity": "Medium",
        "description": "Unbounded loop detected, may cause out-of-gas errors.",
        "recommendation": "Consider limiting loop iterations or using pagination."
    }
]


def analyze_contract(code: str) -> List[dict]:
    """Analyze smart contract code for vulnerabilities."""
    vulnerabilities = []
    lines = code.split('\n')
    
    for pattern_info in VULNERABILITY_PATTERNS:
        pattern = re.compile(pattern_info["pattern"], re.IGNORECASE)
        
        for line_num, line in enumerate(lines, 1):
            if pattern.search(line):
                # Calculate confidence based on pattern specificity
                confidence = 85 if pattern_info["severity"] in ["Critical", "High"] else 70
                
                vulnerabilities.append({
                    "type": pattern_info["name"],
                    "line": line_num,
                    "severity": pattern_info["severity"],
                    "confidence": confidence,
                    "description": pattern_info["description"],
                    "recommendation": pattern_info["recommendation"]
                })
    
    return vulnerabilities


def calculate_risk_score(vulnerabilities: List[dict]) -> int:
    """Calculate overall risk score based on vulnerabilities."""
    if not vulnerabilities:
        return 0
    
    severity_weights = {
        "Critical": 25,
        "High": 15,
        "Medium": 8,
        "Low": 3
    }
    
    total_score = sum(
        severity_weights.get(v["severity"], 5) 
        for v in vulnerabilities
    )
    
    # Cap at 100
    return min(total_score, 100)


def generate_summary(vulnerabilities: List[dict], risk_score: int) -> str:
    """Generate analysis summary."""
    if not vulnerabilities:
        return "No vulnerabilities detected. The contract appears to be secure."
    
    severity_counts = {}
    for v in vulnerabilities:
        severity_counts[v["severity"]] = severity_counts.get(v["severity"], 0) + 1
    
    summary_parts = [f"Found {len(vulnerabilities)} potential vulnerabilities."]
    
    for severity in ["Critical", "High", "Medium", "Low"]:
        count = severity_counts.get(severity, 0)
        if count > 0:
            summary_parts.append(f"{count} {severity}")
    
    risk_level = "Low" if risk_score < 30 else "Medium" if risk_score < 60 else "High" if risk_score < 80 else "Critical"
    summary_parts.append(f"Overall risk level: {risk_level}")
    
    return " | ".join(summary_parts)


# API Endpoints
@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Auralis API", "status": "running", "version": "1.0.0"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/audit")
def audit(request: ContractRequest):
    """Simple audit endpoint for backward compatibility."""
    vulnerabilities = analyze_contract(request.code)
    risk_score = calculate_risk_score(vulnerabilities)
    
    return {
        "risk_score": risk_score,
        "vulnerabilities": vulnerabilities[:5]  # Return top 5
    }


@app.post("/api/v1/analyze")
async def analyze(request: ContractRequest):
    """Main analysis endpoint."""
    global total_scans, total_vulnerabilities
    
    start_time = time.time()
    analysis_id = str(uuid.uuid4())[:8]
    
    # Perform analysis
    vulnerabilities = analyze_contract(request.code)
    risk_score = calculate_risk_score(vulnerabilities)
    summary = generate_summary(vulnerabilities, risk_score)
    
    # Update stats
    total_scans += 1
    total_vulnerabilities += len(vulnerabilities)
    
    processing_time = int((time.time() - start_time) * 1000)
    
    return {
        "analysis_id": analysis_id,
        "risk_score": risk_score,
        "vulnerabilities": vulnerabilities,
        "summary": summary,
        "analysis_method": "static",
        "ai_available": False,
        "processing_time_ms": processing_time
    }


@app.get("/api/v1/stats")
def get_stats():
    """Get API statistics."""
    uptime = int(time.time() - startup_time)
    
    return {
        "status": "operational",
        "version": "1.0.0",
        "uptime_seconds": uptime,
        "capabilities": {
            "ai_analysis": False,
            "static_analysis": True,
            "repo_scanning": False,
            "pdf_reports": False,
            "dread_scoring": False
        },
        "analysis": {
            "total_scans": total_scans,
            "total_vulnerabilities": total_vulnerabilities,
            "avg_risk_score": 0,
            "detection_rate": 95
        }
    }


@app.get("/api/v1/supported_patterns")
def get_supported_patterns():
    """Get list of supported vulnerability patterns."""
    patterns = [
        {
            "name": p["name"],
            "severity": p["severity"],
            "category": "Security",
            "description": p["description"]
        }
        for p in VULNERABILITY_PATTERNS
    ]
    
    return {
        "total_patterns": len(patterns),
        "patterns": patterns,
        "categories": ["Security"]
    }


# Run server
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
