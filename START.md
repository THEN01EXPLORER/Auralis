# Quick Start Guide

## Start Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```

## Test the Application
1. Open http://localhost:3000
2. Click "Analyze Contract" button
3. View vulnerabilities in the right panel

## What You Should See
- **Left Panel**: Code editor with sample vulnerable contract
- **Right Panel**: Analysis report with:
  - Risk Score
  - 4 Vulnerabilities detected:
    - Re-entrancy Attack (Critical)
    - Integer Overflow/Underflow (High)
    - Access Control Violation (Medium)
    - Unchecked Return Value (Medium)

## API Documentation
http://localhost:8000/docs
