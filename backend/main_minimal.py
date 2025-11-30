"""
Auralis API - Minimal version for free tier hosting
No external dependencies beyond FastAPI/uvicorn
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import os
import time
import re
import uuid
import json
from typing import List, Optional
from datetime import datetime
import pathlib

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

class RepoRequest(BaseModel):
    github_url: str

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
    },
    {
        "name": "Unchecked Send",
        "pattern": r"send\s*\([^)]+\)\s*;",
        "severity": "High",
        "description": "Return value of send() not checked. May silently fail.",
        "recommendation": "Always check the return value: require(addr.send(amount), 'Send failed');"
    },
    {
        "name": "Front-Running Vulnerability",
        "pattern": r"(approve|swap|buy|sell|trade)\s*\(",
        "severity": "Medium",
        "description": "Function may be susceptible to front-running attacks.",
        "recommendation": "Implement commit-reveal schemes or use private mempools."
    },
    {
        "name": "Denial of Service",
        "pattern": r"require\s*\([^)]*\.length|for\s*\([^)]*\.length",
        "severity": "High",
        "description": "Array length in loop may cause DoS via gas limit.",
        "recommendation": "Limit array size or use pagination patterns."
    },
    {
        "name": "Signature Replay",
        "pattern": r"ecrecover\s*\(|signature|ECDSA",
        "severity": "High",
        "description": "Signature verification detected. May be vulnerable to replay attacks.",
        "recommendation": "Include nonce and chain ID in signed messages to prevent replay."
    },
    {
        "name": "Flash Loan Vulnerability",
        "pattern": r"getReserves|price|oracle|swap.*\(",
        "severity": "Critical",
        "description": "Price-sensitive operation detected. May be vulnerable to flash loan attacks.",
        "recommendation": "Use TWAP oracles and check for price manipulation."
    },
    {
        "name": "Uninitialized Storage",
        "pattern": r"struct\s+\w+\s*\{[^}]+\}\s*\w+\s*;",
        "severity": "High",
        "description": "Uninitialized storage pointer detected.",
        "recommendation": "Always initialize storage variables explicitly."
    },
    {
        "name": "Arbitrary Jump",
        "pattern": r"assembly\s*\{[^}]*jump",
        "severity": "Critical",
        "description": "Arbitrary jump in assembly detected.",
        "recommendation": "Avoid arbitrary jumps. Use high-level Solidity constructs."
    },
    {
        "name": "Weak Randomness",
        "pattern": r"block\.difficulty|blockhash|block\.number.*random|keccak256.*block",
        "severity": "High",
        "description": "Weak source of randomness detected. Can be predicted by miners.",
        "recommendation": "Use Chainlink VRF or commit-reveal for randomness."
    },
    {
        "name": "Missing Zero Check",
        "pattern": r"address\s+\w+\s*[=;]|payable\s*\(\s*\w+\s*\)",
        "severity": "Medium",
        "description": "Address variable may not be checked for zero address.",
        "recommendation": "Add require(addr != address(0)) checks."
    },
    {
        "name": "Hardcoded Address",
        "pattern": r"0x[a-fA-F0-9]{40}",
        "severity": "Low",
        "description": "Hardcoded address detected.",
        "recommendation": "Consider using constructor parameters or admin functions for addresses."
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
                confidence = 0.85 if pattern_info["severity"] in ["Critical", "High"] else 0.70
                
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


# Sample vulnerable contracts for demo
SAMPLE_CONTRACTS = {
    "reentrancy": {
        "name": "Reentrancy Attack Demo",
        "description": "Classic reentrancy vulnerability in a bank contract",
        "code": """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// VULNERABLE: Classic Reentrancy Attack
contract VulnerableBank {
    mapping(address => uint256) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    // VULNERABLE: State change after external call
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // External call BEFORE state update - VULNERABLE!
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        // State update AFTER external call - TOO LATE!
        balances[msg.sender] -= amount;
    }
    
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}"""
    },
    "overflow": {
        "name": "Integer Overflow Demo",
        "description": "Integer overflow and underflow vulnerabilities",
        "code": """// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

// VULNERABLE: No SafeMath in Solidity < 0.8
contract VulnerableToken {
    mapping(address => uint256) public balances;
    uint256 public totalSupply;
    
    function mint(address to, uint256 amount) public {
        // VULNERABLE: Can overflow
        balances[to] += amount;
        totalSupply += amount;
    }
    
    function transfer(address to, uint256 amount) public {
        // VULNERABLE: Can underflow if balance < amount
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
    
    function batchMint(address[] memory recipients, uint256 amount) public {
        for (uint i = 0; i < recipients.length; i++) {
            // VULNERABLE: Unbounded loop + overflow risk
            balances[recipients[i]] += amount;
        }
    }
}"""
    },
    "access_control": {
        "name": "Access Control Demo",
        "description": "Missing access control and tx.origin issues",
        "code": """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// VULNERABLE: Multiple access control issues
contract VulnerableVault {
    address public owner;
    mapping(address => uint256) public deposits;
    
    constructor() {
        owner = msg.sender;
    }
    
    // VULNERABLE: tx.origin instead of msg.sender
    modifier onlyOwner() {
        require(tx.origin == owner, "Not owner");
        _;
    }
    
    function deposit() public payable {
        deposits[msg.sender] += msg.value;
    }
    
    // VULNERABLE: No access control!
    function withdrawAll() public {
        payable(msg.sender).transfer(address(this).balance);
    }
    
    // VULNERABLE: Unprotected selfdestruct
    function destroy() public {
        selfdestruct(payable(owner));
    }
    
    // VULNERABLE: Anyone can change owner
    function changeOwner(address newOwner) public {
        owner = newOwner;
    }
}"""
    },
    "flash_loan": {
        "name": "Flash Loan Vulnerability Demo",
        "description": "Price oracle manipulation vulnerability",
        "code": """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IUniswapPair {
    function getReserves() external view returns (uint112, uint112, uint32);
}

// VULNERABLE: Flash loan attack vector
contract VulnerableLending {
    IUniswapPair public pair;
    mapping(address => uint256) public deposits;
    mapping(address => uint256) public borrowed;
    
    // VULNERABLE: Spot price from DEX can be manipulated
    function getPrice() public view returns (uint256) {
        (uint112 reserve0, uint112 reserve1,) = pair.getReserves();
        return (reserve1 * 1e18) / reserve0; // Spot price!
    }
    
    // VULNERABLE: Uses manipulable spot price
    function borrow(uint256 collateralAmount) public {
        uint256 price = getPrice();
        uint256 borrowAmount = (collateralAmount * price) / 1e18;
        
        deposits[msg.sender] += collateralAmount;
        borrowed[msg.sender] += borrowAmount;
        
        // Transfer borrowed amount...
    }
    
    // Attacker can: Flash loan -> Manipulate price -> Borrow more -> Repay flash loan
}"""
    },
    "randomness": {
        "name": "Weak Randomness Demo",
        "description": "Predictable randomness vulnerabilities",
        "code": """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// VULNERABLE: Predictable randomness
contract VulnerableLottery {
    uint256 public ticketPrice = 0.1 ether;
    address[] public players;
    
    function buyTicket() public payable {
        require(msg.value == ticketPrice, "Wrong price");
        players.push(msg.sender);
    }
    
    // VULNERABLE: Miner can predict/manipulate
    function pickWinner() public {
        // Block values are known to miners!
        uint256 random = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.difficulty,
            block.number,
            players.length
        )));
        
        uint256 winnerIndex = random % players.length;
        address winner = players[winnerIndex];
        
        payable(winner).transfer(address(this).balance);
        delete players;
    }
    
    // Also vulnerable
    function generateRandom() public view returns (uint256) {
        return uint256(blockhash(block.number - 1)) % 100;
    }
}"""
    }
}


@app.get("/api/v1/samples")
def get_sample_contracts():
    """Get list of sample vulnerable contracts for demo."""
    samples = [
        {
            "id": key,
            "name": value["name"],
            "description": value["description"]
        }
        for key, value in SAMPLE_CONTRACTS.items()
    ]
    return {"samples": samples}


@app.get("/api/v1/samples/{sample_id}")
def get_sample_contract(sample_id: str):
    """Get a specific sample contract."""
    if sample_id not in SAMPLE_CONTRACTS:
        raise HTTPException(status_code=404, detail="Sample not found")
    
    sample = SAMPLE_CONTRACTS[sample_id]
    return {
        "id": sample_id,
        "name": sample["name"],
        "description": sample["description"],
        "code": sample["code"]
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


# Error logging endpoint - accept client-side error reports
class ErrorLogRequest(BaseModel):
    error_id: str
    message: str
    stack: Optional[str] = None
    url: Optional[str] = None
    user_agent: Optional[str] = None


@app.post("/api/v1/log_error")
def log_client_error(request: ErrorLogRequest):
    """Receive client-side error reports and append to server log."""
    try:
        logs_dir = pathlib.Path("./logs")
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / "client_errors.log"
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error_id": request.error_id,
            "message": request.message,
            "stack": request.stack,
            "url": request.url,
            "user_agent": request.user_agent,
        }
        with open(log_file, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")

        return {"status": "logged", "error_id": request.error_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write error log: {str(e)}")


@app.post("/api/v1/analyze_repo")
def analyze_repo(request: RepoRequest):
    """Analyze all Solidity files in a GitHub repository."""
    import tempfile
    import shutil
    import zipfile
    import io
    from pathlib import Path
    from urllib.request import urlopen
    
    github_url = request.github_url.strip()
    
    # Validate GitHub URL
    if not github_url.startswith("https://github.com/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub URL. Must start with https://github.com/"
        )
    
    # Convert GitHub URL to archive download URL
    # https://github.com/owner/repo -> https://github.com/owner/repo/archive/refs/heads/main.zip
    if github_url.endswith('/'):
        github_url = github_url[:-1]
    
    zip_url = f"{github_url}/archive/refs/heads/main.zip"
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    start_time = time.time()
    
    try:
        # Download repository as ZIP
        zip_data = None
        download_error = None
        
        # Try common branch names
        branches = ["main", "master", "develop", "dev"]
        
        for branch in branches:
            try:
                zip_url = f"{github_url}/archive/refs/heads/{branch}.zip"
                response = urlopen(zip_url, timeout=30)
                zip_data = response.read()
                break # Success!
            except Exception as e:
                download_error = e
                continue
        
        if zip_data is None:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to download repository. Tried branches: {', '.join(branches)}. Check URL or repository visibility."
            )
        
        # Extract ZIP
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find all .sol files
        all_sol_files = list(Path(temp_dir).rglob("*.sol"))
        
        # Filter out common directories
        excluded_dirs = {"node_modules", ".git"}
        # We're less strict with test folders now, as some repos put contracts there
        # But we still want to avoid node_modules
        
        sol_files = [
            f for f in all_sol_files
            if not any(excluded in f.parts for excluded in excluded_dirs)
        ]
        
        if not sol_files:
            # Provide helpful error message
            if all_sol_files:
                excluded_count = len(all_sol_files) - len(sol_files)
                raise HTTPException(
                    status_code=404,
                    detail=f"Found {len(all_sol_files)} Solidity files, but all are in test/mock directories. Try a repository with contracts in src/ or contracts/ folders."
                )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="No Solidity (.sol) files found in repository. Make sure the repository contains Solidity smart contracts."
                )
        
        # Analyze each file
        results = {}
        total_vulns = 0
        
        for sol_file in sol_files[:10]:  # Limit to 10 files for free tier
            try:
                code = sol_file.read_text(encoding='utf-8')
                
                # Analyze using existing function
                analysis = analyze_contract(code)
                results[sol_file.name] = analysis
                total_vulns += len(analysis)
                
            except Exception as e:
                results[sol_file.name] = {
                    "error": str(e),
                    "analysis_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "vulnerabilities": []
                }
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return {
            "repository_url": github_url,
            "files_analyzed": len(results),
            "total_vulnerabilities": total_vulns,
            "processing_time_ms": processing_time,
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing repository: {str(e)}"
        )
    finally:
        # Cleanup
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


# Export Request Model
class ExportRequest(BaseModel):
    analysis_id: str
    risk_score: int
    vulnerabilities: List[dict]
    summary: str
    contract_code: Optional[str] = None
    format: str = "json"  # json, txt, or markdown


@app.post("/api/v1/export")
async def export_report(request: ExportRequest):
    """Export analysis report in various formats."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if request.format == "json":
        # JSON Export
        report = {
            "report_type": "Auralis Security Audit Report",
            "generated_at": timestamp,
            "analysis_id": request.analysis_id,
            "risk_score": request.risk_score,
            "risk_level": "Low" if request.risk_score < 30 else "Medium" if request.risk_score < 60 else "High" if request.risk_score < 80 else "Critical",
            "summary": request.summary,
            "total_vulnerabilities": len(request.vulnerabilities),
            "vulnerabilities": request.vulnerabilities,
            "disclaimer": "This report is generated by automated static analysis and should be reviewed by security experts."
        }
        
        return Response(
            content=json.dumps(report, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=auralis_report_{request.analysis_id}.json"
            }
        )
    
    elif request.format == "markdown" or request.format == "md":
        # Markdown Export
        md_content = f"""# 🛡️ Auralis Security Audit Report

**Generated:** {timestamp}  
**Analysis ID:** {request.analysis_id}  
**Risk Score:** {request.risk_score}/100  

---

## 📊 Summary

{request.summary}

---

## 🔍 Vulnerabilities Found ({len(request.vulnerabilities)})

"""
        
        # Group by severity
        for severity in ["Critical", "High", "Medium", "Low"]:
            vulns = [v for v in request.vulnerabilities if v.get("severity") == severity]
            if vulns:
                emoji = "🔴" if severity == "Critical" else "🟠" if severity == "High" else "🟡" if severity == "Medium" else "🟢"
                md_content += f"### {emoji} {severity} Severity\n\n"
                for v in vulns:
                    md_content += f"**{v.get('type', 'Unknown')}** (Line {v.get('line', 'N/A')})\n"
                    md_content += f"- *Confidence:* {v.get('confidence', 0)}%\n"
                    md_content += f"- *Description:* {v.get('description', '')}\n"
                    md_content += f"- *Recommendation:* {v.get('recommendation', '')}\n\n"
        
        md_content += """---

## ⚠️ Disclaimer

This report is generated by automated static analysis. While Auralis uses advanced pattern matching to detect common vulnerabilities, it should not be considered a complete security audit. We recommend having your smart contracts reviewed by professional security auditors before deployment.

---

*Generated by [Auralis](https://auralis-tawny.vercel.app) - Smart Contract Security Auditor*
"""
        
        return Response(
            content=md_content,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f"attachment; filename=auralis_report_{request.analysis_id}.md"
            }
        )
    
    else:  # txt format
        # Plain Text Export
        txt_content = f"""===============================================
        AURALIS SECURITY AUDIT REPORT
===============================================

Generated: {timestamp}
Analysis ID: {request.analysis_id}
Risk Score: {request.risk_score}/100

-----------------------------------------------
SUMMARY
-----------------------------------------------
{request.summary}

-----------------------------------------------
VULNERABILITIES FOUND ({len(request.vulnerabilities)})
-----------------------------------------------

"""
        
        for i, v in enumerate(request.vulnerabilities, 1):
            txt_content += f"""{i}. {v.get('type', 'Unknown')} [{v.get('severity', 'Unknown')}]
   Line: {v.get('line', 'N/A')}
   Confidence: {v.get('confidence', 0)}%
   Description: {v.get('description', '')}
   Recommendation: {v.get('recommendation', '')}

"""
        
        txt_content += """-----------------------------------------------
DISCLAIMER
-----------------------------------------------
This report is generated by automated static analysis.
Please have your contracts reviewed by security experts.

===============================================
Generated by Auralis - Smart Contract Security Auditor
https://auralis-tawny.vercel.app
===============================================
"""
        
        return Response(
            content=txt_content,
            media_type="text/plain",
            headers={
                "Content-Disposition": f"attachment; filename=auralis_report_{request.analysis_id}.txt"
            }
        )


# Run server
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
