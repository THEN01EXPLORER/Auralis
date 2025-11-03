# 🚀 GUARDIANAI AUDIT - DAY 1 QUICK START

## Prerequisites
- Python 3.8+
- Node.js 16+
- Amazon Q installed in IDE
- Git

---

## 🏃 Quick Start (5 Minutes)

### Step 1: Backend Setup
```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 2: Frontend Setup
```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Expected Output:**
```
Compiled successfully!
Local: http://localhost:3000
```

### Step 3: Test the Application
1. Open browser: `http://localhost:3000`
2. Paste sample contract (see below)
3. Click "Analyze Contract"
4. View vulnerability report

---

## 📝 Sample Test Contract

```solidity
pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint) public balances;
    
    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount);
        msg.sender.call{value: amount}("");
        balances[msg.sender] -= amount;
    }
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function transfer(address to, uint amount) public {
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

**Expected Detections:**
- ✅ Re-entrancy Attack (Line 7)
- ✅ Access Control Violation (Lines 6, 11, 16)
- ✅ Integer Overflow (Line 17)
- ✅ Unchecked Return Value (Line 7)

---

## 🧪 Run Automated Tests

```bash
# Make sure backend is running first
python test_day1.py
```

**Expected Output:**
```
🏆 GUARDIANAI AUDIT - DAY 1 TEST SUITE
✅ PASS - Health Check
✅ PASS - Analyze Endpoint
✅ PASS - CORS Configuration
🎯 Score: 3/3 tests passed
🎉 ALL TESTS PASSED - DAY 1 COMPLETE!
```

---

## 📸 Evidence Collection Checklist

### Screenshots to Capture
- [ ] Amazon Q in IDE (active)
- [ ] Project structure in file explorer
- [ ] Backend code (main.py)
- [ ] Backend code (analyzer.py)
- [ ] Frontend code (Home.js)
- [ ] Backend running in terminal
- [ ] Frontend running in terminal
- [ ] Application in browser (empty state)
- [ ] Application with sample contract
- [ ] Vulnerability report displayed
- [ ] Test script results
- [ ] Git commit history

**Save to:** `screenshots/day1/`

---

## 🔧 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend won't start
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
```

### CORS errors
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Frontend should be on port 3000

### Port already in use
```bash
# Backend (change port)
uvicorn app.main:app --reload --port 8001

# Frontend (change port)
PORT=3001 npm start
```

---

## 📊 Day 1 Deliverables

### Code
- ✅ FastAPI backend with 2 endpoints
- ✅ React frontend with 2 components
- ✅ Vulnerability analyzer (4 detection types)
- ✅ AWS Bedrock integration (ready)

### Documentation
- ✅ DAY1_EXECUTION.md
- ✅ QUICKSTART_DAY1.md
- ✅ Test script

### Evidence
- ✅ 9+ screenshots
- ✅ Working demo

---

## 🎯 Next Steps (Day 2)

1. **AWS Bedrock Testing**
   - Configure AWS credentials
   - Test Claude 3 Sonnet
   - Validate AI responses

2. **Enhanced Features**
   - Syntax highlighting
   - Line highlighting
   - Confidence scores

3. **More Evidence**
   - 10+ additional screenshots
   - Screen recording
   - Amazon Q usage documentation

---

## 💡 Tips

- Keep both terminals open (backend + frontend)
- Use Amazon Q for code assistance
- Take screenshots as you work
- Commit code frequently
- Test after each change

---

## 🆘 Need Help?

1. Check `HACKATHON_JOURNAL.md` for detailed notes
2. Review `TEST_GUIDE.md` for testing strategies
3. See `DEPLOYMENT_GUIDE.md` for AWS setup

---

**Day 1 Status:** ✅ COMPLETE  
**MVP Status:** ✅ FUNCTIONAL  
**Ready for Day 2:** ✅ YES

🏆 Great work! Let's continue building tomorrow!
