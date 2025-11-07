# 🚀 Simple Deployment (No SAM CLI Required)

## Option 1: Deploy Frontend Only (Recommended - 5 min)

Your frontend is already built! Just upload it.

### AWS Amplify Console Upload:

1. **Open:** https://console.aws.amazon.com/amplify/
2. **Click:** "New app" → "Host web app" → "Deploy without Git"
3. **Upload:** Drag `frontend/build/` folder
4. **Done:** Get live URL in 2 minutes

**Backend:** Keep running locally for now (localhost:8000)

---

## Option 2: Deploy Backend to Render (Free - 10 min)

### Step 1: Create Account
- Go to: https://render.com
- Sign up (free tier available)

### Step 2: New Web Service
- Click "New +" → "Web Service"
- Connect GitHub: `THEN01EXPLORER/Auralis`
- Root Directory: `backend`
- Name: `auralis-backend`
- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Deploy
- Click "Create Web Service"
- Wait 5 minutes
- Get URL: `https://auralis-backend.onrender.com`

### Step 4: Update Frontend
Edit `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'https://auralis-backend.onrender.com';
```

Rebuild and redeploy frontend:
```bash
cd frontend
npm run build
# Upload new build/ to Amplify
```

---

## Option 3: Manual Lambda Package (Advanced)

### Create Deployment Package:
```bash
cd backend
python lambda_package.py
```

### Upload to AWS Lambda:
1. Go to: https://console.aws.amazon.com/lambda/
2. Create function: `auralis-api`
3. Runtime: Python 3.11
4. Upload: `auralis_lambda.zip`
5. Handler: `app.main.handler`
6. Add API Gateway trigger
7. Copy API Gateway URL

---

## Recommended Path for Hackathon

**Phase 1 (Now - 5 min):**
- Deploy frontend to Amplify
- Keep backend on localhost
- Record demo video with localhost

**Phase 2 (Later - 10 min):**
- Deploy backend to Render (easiest)
- Update frontend API URL
- Redeploy frontend

**Result:** Live demo URL without SAM CLI!

---

## Quick Commands

### Build Frontend:
```bash
cd frontend
npm run build
```

### Test Locally:
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm start
```

### Create Lambda Package:
```bash
cd backend
python lambda_package.py
```

---

## What You Have Right Now

✅ Frontend built (`frontend/build/`)
✅ Backend running locally
✅ All features working
✅ Ready to deploy

**Just upload `frontend/build/` to Amplify and you're live!** 🎉
