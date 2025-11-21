# Auralis Frontend-Backend Connection Verification

## ✅ Connection Status: VERIFIED AND FIXED

This document details all connections between frontend and backend components and confirms they are properly configured.

---

## 🔌 API Endpoint Connections

### Frontend Service: `frontend/src/services/api.js`

#### Base URL Configuration
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

**Environment Files:**
- Development: `frontend/.env` → `http://localhost:8000`
- Production: `frontend/.env.production` → API Gateway URL
- Docker: `docker-compose.yml` → `http://localhost:8000`

#### API Methods → Backend Endpoints

| Frontend Method | HTTP Method | Backend Endpoint | Status |
|----------------|-------------|------------------|--------|
| `analyzeContract()` | POST | `/api/v1/analyze` | ✅ Connected |
| `analyzeRepo()` | POST | `/api/v1/analyze_repo` | ✅ Connected |
| `healthCheck()` | GET | `/health` | ✅ Connected |

---

## 📦 Request/Response Format

### Single Contract Analysis

**Frontend Request** (`frontend/src/services/api.js`):
```javascript
axios.post(`${API_BASE_URL}/api/v1/analyze`, {
  code: contractCode  // ← Sends as "code"
})
```

**Backend Expects** (`backend/main.py`):
```python
class ContractRequest(BaseModel):
    code: str  # ← Expects "code"
```

✅ **Status**: Field names match perfectly!

### Repository Analysis

**Frontend Request**:
```javascript
axios.post(`${API_BASE_URL}/api/v1/analyze_repo`, {
  github_url: githubUrl  // ← Sends as "github_url"
})
```

**Backend Expects**:
```python
class RepoRequest(BaseModel):
    github_url: str  # ← Expects "github_url"
```

✅ **Status**: Field names match perfectly!

---

## 🔄 Data Flow

### Complete Analysis Flow

```
User Input (Code)
    ↓
CodeEditor Component (frontend/src/components/CodeEditor.js)
    ↓ [onAnalyze callback]
Home Page (frontend/src/pages/Home.js)
    ↓ [handleAnalyze function]
API Service (frontend/src/services/api.js)
    ↓ [axios.post with { code: contractCode }]
Backend API (backend/main.py)
    ↓ [POST /api/v1/analyze]
Analysis Orchestrator (backend/app/services/analysis_orchestrator.py)
    ↓ [coordinates static + AI analysis]
Static Analyzer (backend/app/services/analyzer.py)
    + [parallel]
AI Analyzer (backend/app/services/bedrock_analyzer.py)
    ↓
Vulnerability Merger (backend/app/services/vulnerability_merger.py)
    ↓ [combines results]
Risk Score Calculator (backend/app/utils/risk_calculator.py)
    ↓
Response (AnalysisResult)
    ↓ [JSON response]
Home Page (frontend/src/pages/Home.js)
    ↓ [setReport(result)]
VulnerabilityReport Component (frontend/src/components/VulnerabilityReport.js)
    ↓ [renders results]
User sees results!
```

---

## 🎨 Frontend Component Structure

```
frontend/src/
├── App.js                          → Main app, router setup
├── index.js                        → React entry point
├── pages/
│   └── Home.js                     → Main page, orchestrates analysis flow
├── components/
│   ├── CodeEditor.js              → Code input (sends to Home)
│   ├── VulnerabilityReport.js     → Results display (receives from Home)
│   ├── RiskMeter.js               → Risk score visualization
│   ├── ErrorBoundary.js           → Error handling wrapper
│   └── LoadingSpinner.js          → Loading state
├── services/
│   └── api.js                     → API communication layer
└── styles/
    └── *.css                       → Component styles
```

**Connection Flow:**
1. `index.js` → renders `App.js`
2. `App.js` → routes to `Home.js`
3. `Home.js` → uses `CodeEditor` + `VulnerabilityReport` + `api.js`
4. All imports verified ✅

---

## 🔧 Backend Service Structure

```
backend/
├── main.py                         → FastAPI app, all endpoints
├── app/
│   ├── models/
│   │   └── contract.py            → Pydantic models (used by main.py)
│   ├── services/
│   │   ├── analyzer.py            → Static analysis (used by main.py)
│   │   ├── bedrock_analyzer.py    → AI analysis (used by main.py)
│   │   ├── analysis_orchestrator.py → Coordinates analysis (used by main.py)
│   │   ├── vulnerability_merger.py  → Merges results (used by orchestrator)
│   │   ├── dread_scorer.py        → DREAD scoring (used by main.py)
│   │   └── pdf_report_generator.py → PDF generation (used by main.py)
│   └── utils/
│       └── risk_calculator.py      → Risk calculations (used by main.py)
└── requirements.txt                → All dependencies
```

**All imports in main.py verified:**
```python
from app.utils.risk_calculator import calculate_risk_score  ✅
from app.services.analyzer import VulnerabilityAnalyzer     ✅
from app.services.bedrock_analyzer import BedrockAnalyzer   ✅
from app.services.analysis_orchestrator import ...          ✅
from app.services.dread_scorer import DREADScorer           ✅
from app.services.pdf_report_generator import ...           ✅
from app.models.contract import AnalyzeResponse             ✅
```

---

## 🐳 Docker Integration

### docker-compose.yml

```yaml
services:
  backend:
    ports: ["8000:8000"]
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - ENABLE_AI_ANALYSIS=${ENABLE_AI_ANALYSIS:-true}
      # ... other env vars
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    
  frontend:
    ports: ["3000:80"]
    environment:
      - REACT_APP_API_URL=http://localhost:8000  ✅ Points to backend
    depends_on:
      - backend  ✅ Waits for backend to start
```

**Connection:** Frontend container configured to connect to backend at `localhost:8000` ✅

---

## 🔒 CORS Configuration

**Backend** (`backend/main.py`):
```python
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ['*'] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Status:** ✅ Allows all origins by default for development
**Production Note:** Set `ALLOWED_ORIGINS` environment variable to restrict

---

## 📋 Issues Found and Fixed

### ✅ Issue 1: Duplicate main.py Files
- **Problem**: Two main.py files (`backend/main.py` and `backend/app/main.py`)
- **Impact**: Confusion about which file is the actual entry point
- **Fix**: Moved `backend/app/main.py` to `backend/app/main.py.backup`
- **Result**: Clear single entry point at `backend/main.py`

### ✅ Issue 2: Missing psutil Dependency
- **Problem**: `backend/main.py` imports psutil but it wasn't in requirements.txt
- **Impact**: Runtime error when trying to log system resources
- **Fix**: Added `psutil==5.9.6` to `backend/requirements.txt`
- **Result**: All dependencies satisfied

### ✅ Issue 3: Incorrect Lambda Handler Import
- **Problem**: `backend/lambda_handler.py` imported from `app.main` (old location)
- **Impact**: Lambda deployment would fail
- **Fix**: Changed import to `from main import app`
- **Result**: Lambda handler correctly imports from main entry point

### ✅ Issue 4: Empty app/__init__.py
- **Problem**: No documentation about the app directory structure
- **Fix**: Added comments explaining the structure
- **Result**: Clear understanding that app/ is for modules, not main app

---

## 🧪 Testing the Connection

### Quick Health Check
```bash
# Start backend
cd backend
python -m uvicorn main:app --reload

# In another terminal, test the connection
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

### Test Frontend → Backend Connection
```bash
# Start both services
docker-compose up

# Frontend: http://localhost:3000
# Backend:  http://localhost:8000

# Paste code in frontend and click "Analyze"
# Should see results displayed
```

### Test Individual Endpoints
```bash
# Test analyze endpoint
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"pragma solidity ^0.8.0; contract Test {}"}'

# Test repo endpoint
curl -X POST http://localhost:8000/api/v1/analyze_repo \
  -H "Content-Type: application/json" \
  -d '{"github_url":"https://github.com/user/repo"}'
```

---

## 🎯 Connection Checklist

- [✅] Frontend API service correctly configured
- [✅] Backend endpoints match frontend calls
- [✅] Request/response field names match
- [✅] CORS properly configured
- [✅] Environment variables set up
- [✅] Docker Compose connections work
- [✅] All backend imports resolve correctly
- [✅] All frontend imports resolve correctly
- [✅] No duplicate/conflicting files
- [✅] All dependencies in requirements.txt
- [✅] Lambda handlers correctly reference main.py

---

## 🚀 Ready to Deploy

All connections verified and working! The application is ready for:
- ✅ Local development
- ✅ Docker deployment
- ✅ AWS Lambda deployment
- ✅ Production deployment

For deployment instructions, see:
- `DEPLOYMENT_GUIDE.md`
- `QUICK_START.md`
- `LOCAL_STARTUP_GUIDE.md`
