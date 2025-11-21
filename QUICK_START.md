# 🚀 Auralis - Quick Start Guide

## ✅ Your Application is Running!

**Backend:** http://localhost:8000  
**Frontend:** http://localhost:3000  
**API Documentation:** http://localhost:8000/docs

---

## 🎯 How to Use Auralis

### 1. Analyze a Single Smart Contract

1. Open http://localhost:3000 in your browser
2. Paste your Solidity code into the editor
3. Click **"Analyze Contract"**
4. View vulnerabilities with risk scores and AI-powered recommendations

### 2. Analyze a GitHub Repository

1. Enter a GitHub repository URL (e.g., `https://github.com/user/repo`)
2. Click **"Analyze Repo"**
3. View results for all Solidity files in the repository

---

## 🛠️ Running the Application

### Start Both Servers (Git Bash)
```bash
bash run_auralis.sh
```

### Start Manually

**Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm start
```

---

## 🔧 Configuration

### AWS Credentials (Optional - for AI Analysis)

The app works without AWS credentials using static analysis only. To enable AI-powered analysis:

1. Edit `backend/.env.production`
2. Add your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_REGION=us-east-1
   ```

### Current Status
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ⚠️ AI Analysis: Disabled (no AWS credentials)
- ✅ Static Analysis: Enabled

---

## 🧪 Test the Application

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test Analysis Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"contract Test { function withdraw() public { msg.sender.call.value(1 ether)(); } }"}'
```

---

## 📊 Features

- **Hybrid Analysis:** Static pattern-matching + AI semantic analysis
- **Repository Scanner:** Analyze entire GitHub repos
- **Smart Remediation:** AI-generated fix recommendations
- **Risk Scoring:** Comprehensive vulnerability assessment
- **Professional UI:** Clean, modern interface

---

## 🛑 Stop the Servers

Press `Ctrl+C` in the terminal where you ran `run_auralis.sh`

Or manually:
```bash
# Find and kill processes
pkill -f "uvicorn main:app"
pkill -f "react-scripts start"
```

---

## 📚 Additional Documentation

- **README.md** - Full project documentation
- **DEPLOYMENT_GUIDE.md** - Production deployment instructions
- **TEST_GUIDE.md** - Testing documentation
- **VIDEO_SCRIPT.md** - Demo video script

---

## 🆘 Troubleshooting

**Port already in use:**
```bash
# Kill process on port 8000
npx kill-port 8000

# Kill process on port 3000
npx kill-port 3000
```

**Backend won't start:**
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `cd backend && pip install -r requirements.txt`

**Frontend won't start:**
- Check Node version: `node --version` (need 16+)
- Install dependencies: `cd frontend && npm install`

---

## 🎉 You're All Set!

Your Auralis smart contract security auditor is ready to use. Open http://localhost:3000 and start analyzing contracts!
