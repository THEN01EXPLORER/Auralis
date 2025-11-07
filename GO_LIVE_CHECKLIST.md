# 🚀 GO LIVE CHECKLIST - Follow These Steps Now

## ✅ TASK 1: Deploy Frontend to AWS Amplify (5 minutes)

### Step-by-Step:

1. **Open AWS Amplify Console**
   - URL: https://console.aws.amazon.com/amplify/
   - Sign in with your AWS account

2. **Create New App**
   - Click "New app" → "Host web app"
   - Select "Deploy without Git provider"

3. **Configure App**
   - App name: `Auralis`
   - Environment name: `production`

4. **Upload Build Folder**
   - Drag and drop the ENTIRE `frontend/build/` folder
   - (The folder is at: `d:\1ST DH\Auralis\frontend\build\`)

5. **Deploy**
   - Click "Save and deploy"
   - Wait 2-3 minutes

6. **Copy Your Live URL**
   - You'll get: `https://production.XXXXX.amplifyapp.com`
   - **SAVE THIS URL!**

### Expected Result:
- ✅ Frontend is live
- ⚠️ Backend calls will fail (this is normal - we fix in Task 3)

---

## ✅ TASK 2: Deploy Backend to AWS Lambda (10 minutes)

### Option A: Create Lambda Package (Recommended)

**Step 1: Create Deployment Package**
```bash
cd backend
python lambda_package.py
```

This creates `auralis_lambda.zip`

**Step 2: Create Lambda Function**
1. Go to: https://console.aws.amazon.com/lambda/
2. Click "Create function"
3. Choose "Author from scratch"
4. Function name: `auralis-backend`
5. Runtime: Python 3.11
6. Click "Create function"

**Step 3: Upload Code**
1. In the "Code" tab, click "Upload from" → ".zip file"
2. Upload `auralis_lambda.zip`
3. Click "Save"

**Step 4: Configure Handler**
1. Go to "Runtime settings"
2. Click "Edit"
3. Handler: `app.main.handler`
4. Click "Save"

**Step 5: Add Permissions**
1. Go to "Configuration" → "Permissions"
2. Click the role name (opens IAM)
3. Click "Add permissions" → "Attach policies"
4. Search and add: `AmazonBedrockFullAccess`
5. Click "Add permissions"

**Step 6: Create API Gateway**
1. Go to: https://console.aws.amazon.com/apigateway/
2. Click "Create API" → "REST API" (not private)
3. API name: `auralis-api`
4. Click "Create API"

**Step 7: Create Resource and Method**
1. Click "Actions" → "Create Resource"
2. Resource name: `{proxy+}` (enable proxy)
3. Click "Create Resource"
4. Select the resource, click "Actions" → "Create Method" → "ANY"
5. Integration type: Lambda Function
6. Lambda Function: `auralis-backend`
7. Click "Save" → "OK"

**Step 8: Enable CORS**
1. Select the resource
2. Click "Actions" → "Enable CORS"
3. Click "Enable CORS and replace existing CORS headers"

**Step 9: Deploy API**
1. Click "Actions" → "Deploy API"
2. Deployment stage: "New Stage"
3. Stage name: `prod`
4. Click "Deploy"

**Step 10: Copy API URL**
- You'll see: `https://XXXXXX.execute-api.us-east-1.amazonaws.com/prod`
- **SAVE THIS URL!**

### Option B: Use Render.com (Easier Alternative)

1. Go to: https://render.com
2. Sign up (free)
3. Click "New +" → "Web Service"
4. Connect GitHub: `THEN01EXPLORER/Auralis`
5. Root Directory: `backend`
6. Name: `auralis-backend`
7. Runtime: Python 3
8. Build: `pip install -r requirements.txt`
9. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
10. Click "Create Web Service"
11. Copy URL: `https://auralis-backend.onrender.com`

---

## ✅ TASK 3: Connect Frontend to Backend (5 minutes)

### Step 1: Update API URL

Open `frontend/src/services/api.js` and change:

**FROM:**
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

**TO:**
```javascript
const API_BASE_URL = 'https://YOUR-API-URL-HERE';
```

Replace `YOUR-API-URL-HERE` with:
- Lambda: `https://XXXXXX.execute-api.us-east-1.amazonaws.com/prod`
- Render: `https://auralis-backend.onrender.com`

### Step 2: Rebuild Frontend
```bash
cd frontend
npm run build
```

### Step 3: Redeploy to Amplify
1. Go back to AWS Amplify Console
2. Find your `Auralis` app
3. Drag and drop the NEW `frontend/build/` folder
4. Wait 2 minutes for deployment

### Step 4: Test Your Live App
- Open your Amplify URL
- Paste a contract
- Click "Analyze"
- ✅ Should work end-to-end!

---

## 📋 Deployment Checklist

- [ ] Task 1: Frontend deployed to Amplify
- [ ] Task 1: Live frontend URL obtained
- [ ] Task 2: Backend deployed (Lambda or Render)
- [ ] Task 2: Live backend URL obtained
- [ ] Task 3: Updated api.js with backend URL
- [ ] Task 3: Rebuilt frontend
- [ ] Task 3: Redeployed frontend to Amplify
- [ ] Test: Empty state loads
- [ ] Test: Analysis works end-to-end
- [ ] Test: Error state works

---

## 🎯 Victory Condition

When you can share your Amplify URL and anyone can:
1. Load the app
2. Paste a contract
3. Click analyze
4. See results

**YOU'RE LIVE! 🎉**

---

## Quick Reference

**Frontend Build Location:** `d:\1ST DH\Auralis\frontend\build\`

**AWS Consoles:**
- Amplify: https://console.aws.amazon.com/amplify/
- Lambda: https://console.aws.amazon.com/lambda/
- API Gateway: https://console.aws.amazon.com/apigateway/

**Alternative Backend:** https://render.com

---

## Next Steps After Deployment

1. Update README.md with live URL
2. Update HACKATHON_JOURNAL.md
3. Take screenshots of live app
4. Commit and push changes
5. Prepare demo video

**Start with Task 1 NOW! Open AWS Amplify Console and upload your build folder!** 🚀
