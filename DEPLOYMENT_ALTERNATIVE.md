# 🚀 Alternative Deployment Options (No SAM CLI Required)

## Option 1: Deploy Frontend Only (Fastest - 5 minutes)

Since SAM CLI is not installed, let's get your frontend live first using free hosting.

### Deploy to Vercel (Recommended - Easiest)

**Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

**Step 2: Deploy Frontend**
```bash
cd frontend
vercel
```

Follow prompts:
- Set up and deploy? `Y`
- Which scope? (your account)
- Link to existing project? `N`
- Project name: `auralis`
- Directory: `./`
- Override settings? `N`

**You'll get a live URL instantly!** (e.g., `https://auralis.vercel.app`)

**Step 3: Update API URL**

For now, keep using localhost backend or deploy backend separately.

---

## Option 2: Deploy Backend to Railway (No SAM Required)

### Step 1: Create Railway Account
Go to https://railway.app and sign up (free tier available)

### Step 2: Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Connect your Auralis repository
- Select the `backend` folder

### Step 3: Configure
Add environment variables in Railway dashboard:
- `PORT`: `8000`
- `USE_BEDROCK`: `false`

### Step 4: Get URL
Railway will give you a URL like: `https://auralis-backend.railway.app`

---

## Option 3: Deploy Backend to Render (Free Tier)

### Step 1: Create Render Account
Go to https://render.com and sign up

### Step 2: New Web Service
- Click "New +" → "Web Service"
- Connect GitHub repository
- Select `backend` folder
- Name: `auralis-backend`
- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Get URL
Render provides: `https://auralis-backend.onrender.com`

---

## Option 4: Install SAM CLI (For AWS Lambda)

### Windows Installation:
```bash
# Download SAM CLI installer
# Visit: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

# Or use Chocolatey:
choco install aws-sam-cli

# Or use MSI installer from AWS
```

### After Installation:
```bash
sam --version
cd backend
sam build
sam deploy --guided
```

---

## Recommended Quick Path

**For immediate demo:**
1. Deploy frontend to Vercel (5 min)
2. Keep backend on localhost for testing
3. Record demo video with localhost
4. Deploy backend to Railway/Render later (10 min)

**For full AWS deployment:**
1. Install SAM CLI
2. Follow DEPLOY_NOW.md guide
3. Deploy both to AWS

---

## Quick Frontend Deployment (Right Now)

```bash
# Install Vercel
npm install -g vercel

# Deploy
cd frontend
vercel --prod

# Done! You'll get a live URL
```

**This gets you 50% deployed in 5 minutes!**

---

## Update After Deployment

Once you have a live backend URL, update `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.com';
```

Then redeploy frontend:
```bash
cd frontend
vercel --prod
```

---

## Which Option Should You Choose?

**Need it live NOW:** Vercel (frontend only)
**Want full AWS:** Install SAM CLI first
**Want easiest backend:** Railway or Render
**Want best for hackathon:** Vercel + Railway (both free, fast)

Choose based on your timeline and requirements!
