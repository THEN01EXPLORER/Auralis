# Auralis Testing Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

## Backend Setup & Testing

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Backend Server
```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 3. Test Backend Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"healthy"}`

#### Analyze Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/analyze -H "Content-Type: application/json" -d "{\"contract_code\":\"contract Test { function withdraw() public { msg.sender.call{value: 1}(\\\"\\\"); } }\"}"
```

Expected: JSON response with vulnerabilities detected

### 4. View API Documentation
Open browser: http://localhost:8000/docs

## Frontend Setup & Testing

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Frontend Server
```bash
npm start
```

Expected: Browser opens at http://localhost:3000

### 3. Manual Testing Checklist

#### Test 1: Default Contract Analysis
- Page loads with default vulnerable contract
- Click "Analyze Contract" button
- Verify vulnerabilities appear in right panel
- Check risk score is displayed
- Verify severity badges (Critical, High, Medium, Low)

#### Test 2: Re-entrancy Detection
Expected: "Re-entrancy Attack" vulnerability detected on line with .call

#### Test 3: Access Control Detection
Expected: "Access Control Violation" detected on public functions

## Success Criteria
✅ Backend starts without errors
✅ Frontend loads successfully
✅ Default contract analysis works
✅ All 4 vulnerability types detected
✅ Risk score calculated correctly
✅ UI displays vulnerabilities with proper styling
✅ No console errors
