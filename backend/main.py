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
    # Analyze the actual code for vulnerabilities
    vulnerabilities = []
    lines = request.code.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Re-entrancy detection
        if '.call{' in line or '.call(' in line:
            vulnerabilities.append({
                "type": "Re-entrancy Attack",
                "line": i,
                "severity": "Critical",
                "confidence": 95,
                "description": "External call detected before state changes. This allows attackers to recursively call back into the contract.",
                "recommendation": "Use Checks-Effects-Interactions pattern or ReentrancyGuard",
                "remediation": {
                    "explanation": "Move state changes before external calls. Update balances first, then transfer funds.",
                    "code_example": "// FIXED\nfunction withdraw(uint amount) public {\n    require(balances[msg.sender] >= amount);\n    balances[msg.sender] -= amount; // State change FIRST\n    (bool success, ) = msg.sender.call{value: amount}(\"\");\n    require(success);\n}"
                }
            })
        
        # Access control detection
        if 'function' in line and 'public' in line and 'onlyOwner' not in line and 'view' not in line and 'pure' not in line:
            vulnerabilities.append({
                "type": "Access Control Violation",
                "line": i,
                "severity": "High",
                "confidence": 85,
                "description": "Public function without access control modifier. Anyone can call this function.",
                "recommendation": "Add onlyOwner or appropriate access control",
                "remediation": {
                    "explanation": "Use OpenZeppelin's Ownable contract to restrict access to sensitive functions.",
                    "code_example": "// FIXED\nimport '@openzeppelin/contracts/access/Ownable.sol';\n\ncontract MyContract is Ownable {\n    function sensitiveFunction() public onlyOwner {\n        // Only owner can execute\n    }\n}"
                }
            })
        
        # Integer overflow detection
        if ('+=' in line or '-=' in line or '*=' in line) and 'unchecked' not in line:
            vulnerabilities.append({
                "type": "Integer Overflow/Underflow",
                "line": i,
                "severity": "Medium",
                "confidence": 80,
                "description": "Arithmetic operation without overflow protection in Solidity < 0.8.0",
                "recommendation": "Use Solidity 0.8+ or SafeMath library",
                "remediation": {
                    "explanation": "Solidity 0.8.0+ has built-in overflow checks. For older versions, use SafeMath.",
                    "code_example": "// FIXED (Solidity 0.8+)\npragma solidity ^0.8.0;\nbalances[msg.sender] += amount; // Safe\n\n// OR use SafeMath for older versions\nusing SafeMath for uint256;\nbalances[msg.sender] = balances[msg.sender].add(amount);"
                }
            })
    
    # Calculate dynamic risk score
    risk_score = calculate_risk_score(vulnerabilities)
    
    return {
        "analysis_id": "test-123",
        "risk_score": risk_score,
        "vulnerabilities": vulnerabilities,
        "summary": f"Found {len(vulnerabilities)} vulnerabilities with risk score {risk_score}/100"
    }
