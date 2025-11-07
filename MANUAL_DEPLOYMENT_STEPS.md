# 📦 Manual Deployment Steps (No CLI Tools Required)

## Fastest Path: Manual Upload to AWS Amplify

### Step 1: Build Frontend Locally

```bash
cd frontend
npm run build
```

This creates a `build/` folder with your production-ready app.

### Step 2: Deploy to AWS Amplify Console

1. **Open AWS Amplify Console**
   - Go to: https://console.aws.amazon.com/amplify/
   - Sign in with your AWS account

2. **Create New App**
   - Click "New app" → "Host web app"
   - Select "Deploy without Git provider"

3. **Upload Build Folder**
   - App name: `auralis`
   - Environment name: `production`
   - Drag and drop the entire `build/` folder
   - Click "Save and deploy"

4. **Get Your Live URL**
   - Wait 2-3 minutes for deployment
   - You'll get: `https://production.XXXXX.amplifyapp.com`

### Step 3: Test Your Live App

Open the URL and verify all three states work:
- Empty state (first load)
- Success state (analyze a contract)
- Error state (backend offline)

---

## Backend Options (Choose One)

### Option A: Keep Backend Local (For Demo)
- Run backend locally during demo
- Use ngrok to expose: `ngrok http 8000`
- Update frontend API URL to ngrok URL

### Option B: Manual Lambda Deployment
1. Zip the backend folder
2. Upload to AWS Lambda console
3. Configure API Gateway manually

### Option C: Use GitHub + Amplify Auto-Deploy
1. Push code to GitHub (already done)
2. In Amplify, connect to GitHub repo
3. Auto-deploys on every push

---

## What You Can Do RIGHT NOW

```bash
cd frontend
npm run build
```

Then manually upload `build/` folder to AWS Amplify Console.

**Result: Live frontend in 5 minutes!** 🚀
