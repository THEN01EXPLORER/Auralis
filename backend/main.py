from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ContractRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/audit")
def audit(request: ContractRequest):
    return {
        "risk_score": 85,
        "vulnerabilities": [
            {
                "type": "Re-entrancy",
                "line_number": 22,
                "severity": "High",
                "description": "A mock re-entrancy vulnerability was detected."
            }
        ]
    }
