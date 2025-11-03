from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
sys.path.append('app')
from app.utils.risk_calculator import calculate_risk_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def analyze(request: ContractRequest):
    vulnerabilities = [
        {
            "type": "Re-entrancy Attack",
            "line": 14,
            "severity": "Critical",
            "confidence": 95,
            "description": "External call before state changes detected",
            "recommendation": "Use ReentrancyGuard from OpenZeppelin",
            "remediation": {
                "explanation": "Implement the Checks-Effects-Interactions pattern: check conditions, update state, then make external calls.",
                "code_example": "// FIXED VERSION\nfunction withdraw(uint amount) public {\n    require(balances[msg.sender] >= amount);\n    balances[msg.sender] -= amount; // Update state first\n    (bool success, ) = msg.sender.call{value: amount}(\"\");\n    require(success);\n}"
            }
        },
        {
            "type": "Access Control Violation",
            "line": 8,
            "severity": "Medium",
            "confidence": 90,
            "description": "Public function without access control",
            "recommendation": "Add onlyOwner modifier",
            "remediation": {
                "explanation": "Add access control using OpenZeppelin's Ownable contract.",
                "code_example": "// FIXED VERSION\nimport \"@openzeppelin/contracts/access/Ownable.sol\";\n\ncontract MyContract is Ownable {\n    function sensitiveFunction() public onlyOwner {\n        // Only owner can call this\n    }\n}"
            }
        }
    ]
    
    risk_score = calculate_risk_score(vulnerabilities)
    
    return {
        "analysis_id": "test-123",
        "risk_score": risk_score,
        "vulnerabilities": vulnerabilities,
        "summary": f"Found {len(vulnerabilities)} vulnerabilities with risk score {risk_score}/100"
    }
