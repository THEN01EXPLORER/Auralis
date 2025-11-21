# 🎯 Auralis Demo Instructions

Quick setup for demonstrating Auralis features.

## Quick Start (5 minutes)

### 1. Start Backend
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Verify: http://localhost:8000/health

### 2. Start Frontend
```bash
cd frontend
npm install
npm start
```
Opens: http://localhost:3000

## Demo Flow

### Feature 1: Single Contract Analysis
1. Open Auralis in browser
2. Paste contract from `demo-contracts/VulnerableBank.sol`
3. Click "Analyze Contract"
4. Show vulnerabilities with risk scores
5. Click "Show Fix" to reveal remediation code

### Feature 2: Repository Scanner
1. Scroll to "Analyze GitHub Repository"
2. Paste a GitHub URL with Solidity contracts
3. Click "Analyze Repo"
4. Show tabbed results for multiple files
5. Click through tabs to show individual reports

### Feature 3: AI-Powered Analysis
- Point out "Source" badges (Static/AI/Hybrid)
- Show confidence scores (e.g., 95%)
- Highlight AI-generated remediation explanations

## Demo Repositories

### Option 1: Create Your Own (Recommended)
Create a small repo with 2-3 contracts:
```
https://github.com/yourusername/test-contracts
```

### Option 2: Use Public Repos
- OpenZeppelin: `https://github.com/OpenZeppelin/openzeppelin-contracts`
- Ethernaut: `https://github.com/OpenZeppelin/ethernaut`

## Troubleshooting
- Backend not responding? Check port 8000 is free
- Frontend errors? Clear browser cache
- No vulnerabilities? Use demo-contracts/VulnerableBank.sol

## Demo Checklist
- [ ] Backend running
- [ ] Frontend loaded
- [ ] Demo contract ready
- [ ] GitHub URL ready
- [ ] All features tested

For video recording instructions, see VIDEO_GUIDE.md.
