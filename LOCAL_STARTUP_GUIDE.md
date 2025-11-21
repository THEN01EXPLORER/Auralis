# 🚀 Auralis Local Startup Guide

## ✅ Services Running

### Backend (FastAPI)
- **Status**: ✅ Running
- **URL**: http://localhost:8000
- **Process**: Python FastAPI with Uvicorn
- **Port**: 8000

**Available Endpoints**:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/analyze` - Analyze contract
- `POST /api/v1/analyze_repo` - Analyze repository
- `POST /api/v1/dread_score` - Calculate DREAD score
- `POST /api/v1/generate_report` - Generate PDF report

### Frontend (React)
- **Status**: ✅ Running
- **URL**: http://localhost:3000
- **Process**: React development server
- **Port**: 3000

---

## 🌐 Access the Application

### Open in Browser
```
Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

---

## 🧪 Test the Application

### Test Backend Health
```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{"status": "ok"}
```

### Test Contract Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "pragma solidity ^0.8.0; contract Test { function test() public {} }"}'
```

### Test Frontend
1. Open http://localhost:3000 in your browser
2. Paste a Solidity contract in the code editor
3. Click "Analyze Contract"
4. View the results

---

## 📊 Features Available

### ✅ Working Features
- Contract analysis with static analyzer
- Repository scanning
- DREAD risk scoring
- PDF report generation
- Rate limiting (60 req/min)
- Error handling
- Loading states
- Responsive UI

### ⚠️ Limited Features (No AWS Credentials)
- AI-powered analysis (requires AWS Bedrock credentials)
- Will fall back to static analysis only

---

## 🔧 Configuration

### Backend Environment Variables
Located in `backend/.env` or set via environment:

```env
AWS_REGION=us-east-1
ENABLE_AI_ANALYSIS=true
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
LOG_LEVEL=INFO
RATE_LIMIT_PER_MINUTE=60
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend Environment Variables
Located in `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENABLE_ANALYTICS=true
```

---

## 📝 Sample Contracts to Test

### Simple Contract
```solidity
pragma solidity ^0.8.0;

contract SimpleToken {
    mapping(address => uint256) public balances;
    
    function transfer(address to, uint256 amount) public {
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

### Vulnerable Contract (Re-entrancy)
```solidity
pragma solidity ^0.8.0;

contract Vulnerable {
    mapping(address => uint256) public balances;
    
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount);
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        balances[msg.sender] -= amount;
    }
}
```

### Complex Contract
```solidity
pragma solidity ^0.8.0;

contract ComplexToken {
    string public name = "Test Token";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    
    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowance;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    constructor(uint256 initialSupply) {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balances[msg.sender] = totalSupply;
    }
    
    function transfer(address to, uint256 value) public returns (bool) {
        require(to != address(0));
        require(balances[msg.sender] >= value);
        balances[msg.sender] -= value;
        balances[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
}
```

---

## 🐛 Troubleshooting

### Backend Not Responding
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not running, start it manually
python backend/main.py
```

### Frontend Not Loading
```bash
# Check if frontend is running
# Open http://localhost:3000 in browser

# If not running, start it manually
npm start --prefix frontend
```

### CORS Errors
- Make sure `ALLOWED_ORIGINS` includes `http://localhost:3000`
- Check browser console for specific error

### Rate Limit Exceeded
- Wait 60 seconds for rate limit to reset
- Or increase `RATE_LIMIT_PER_MINUTE` in environment

### AI Analysis Not Working
- AWS credentials not configured (expected for local testing)
- Static analysis will still work
- To enable AI: Configure AWS credentials and set `ENABLE_AI_ANALYSIS=true`

---

## 📊 Monitoring

### View Backend Logs
```bash
# Logs are printed to console
# Check the terminal running the backend
```

### View Frontend Logs
```bash
# Open browser console (F12)
# Check Network tab for API calls
```

### Check API Response Times
```bash
# Use curl with verbose output
curl -v http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "test"}'
```

---

## 🧪 Run Tests

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Test Coverage
```bash
cd backend
pytest tests/ --cov
```

---

## 🔄 Restart Services

### Restart Backend
```bash
# Stop the process (Ctrl+C in terminal)
# Then restart
python backend/main.py
```

### Restart Frontend
```bash
# Stop the process (Ctrl+C in terminal)
# Then restart
npm start --prefix frontend
```

---

## 📈 Performance

### Expected Performance
- Frontend load time: <2 seconds
- API response time: <500ms
- Contract analysis: 2-5 seconds (static only)
- Repository scan: 15-30 seconds (3 files)

### Monitor Performance
```bash
# Check response times
curl -w "Time: %{time_total}s\n" http://localhost:8000/health
```

---

## 🔐 Security Notes

### Local Development
- CORS is configured for localhost:3000
- Rate limiting is active (60 req/min)
- No authentication required (local only)
- AWS credentials not needed for static analysis

### Before Production
- Configure AWS credentials for AI analysis
- Update ALLOWED_ORIGINS for production domain
- Enable HTTPS
- Set up proper authentication
- Configure rate limiting appropriately

---

## 📚 Documentation

For more information, see:
- `DEPLOYMENT_GUIDE.md` - Production deployment
- `API_DOCUMENTATION.md` - API reference
- `TROUBLESHOOTING.md` - Common issues
- `QUICK_REFERENCE.md` - Quick commands

---

## 🎯 Next Steps

1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:3000
3. Test the application with sample contracts
4. Review the code and documentation
5. Deploy to AWS when ready

---

## 💡 Tips

- Use the API docs at http://localhost:8000/docs for interactive testing
- Try different contract examples to see analysis results
- Check browser console (F12) for frontend errors
- Check terminal for backend logs
- Use curl or Postman to test API endpoints directly

---

## 🆘 Need Help?

1. Check TROUBLESHOOTING.md for common issues
2. Review API_DOCUMENTATION.md for endpoint details
3. Check code comments for implementation details
4. Review test files for usage examples

---

**Status**: ✅ **RUNNING LOCALLY**
**Backend**: http://localhost:8000
**Frontend**: http://localhost:3000
**Last Updated**: November 17, 2025
