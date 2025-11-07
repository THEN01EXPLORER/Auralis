# ✅ DEPLOYMENT PACKAGE READY!

## What's Ready:

### ✅ Frontend Build
**Location:** `frontend/build/`
**Size:** 68.41 kB (optimized)
**Status:** Ready to upload

### ✅ Backend Lambda Package
**Location:** `backend/auralis_lambda.zip`
**Size:** 21.85 MB
**Status:** Ready to upload

---

## MANUAL DEPLOYMENT STEPS

### TASK 1: Deploy Frontend (5 minutes)

1. **Open AWS Amplify Console**
   - URL: https://console.aws.amazon.com/amplify/
   
2. **Create App**
   - Click "New app" → "Host web app"
   - Choose "Deploy without Git provider"
   
3. **Upload**
   - App name: `Auralis`
   - Drag `frontend/build/` folder
   - Click "Save and deploy"
   
4. **Save URL**
   - Copy: `https://production.XXXXX.amplifyapp.com`

---

### TASK 2: Deploy Backend (10 minutes)

#### Step 1: Create Lambda Function
1. Go to: https://console.aws.amazon.com/lambda/
2. Click "Create function"
3. Choose "Author from scratch"
4. Function name: `auralis-backend`
5. Runtime: Python 3.11
6. Click "Create function"

#### Step 2: Upload Code
1. In "Code" tab, click "Upload from" → ".zip file"
2. Upload `backend/auralis_lambda.zip`
3. Click "Save"

#### Step 3: Configure Handler
1. Go to "Runtime settings"
2. Click "Edit"
3. Handler: `app.main.handler`
4. Click "Save"

#### Step 4: Add Permissions
1. Go to "Configuration" → "Permissions"
2. Click the role name
3. Click "Add permissions" → "Attach policies"
4. Add: `AmazonBedrockFullAccess`
5. Click "Add permissions"

#### Step 5: Increase Timeout
1. Go to "Configuration" → "General configuration"
2. Click "Edit"
3. Timeout: 60 seconds
4. Memory: 1024 MB
5. Click "Save"

#### Step 6: Create API Gateway
1. Go to: https://console.aws.amazon.com/apigateway/
2. Click "Create API" → "REST API" (Build)
3. API name: `auralis-api`
4. Click "Create API"

#### Step 7: Configure API
1. Click "Actions" → "Create Resource"
2. Check "Configure as proxy resource"
3. Resource name: `{proxy+}`
4. Click "Create Resource"

5. Select `{proxy+}`, click "Actions" → "Create Method" → "ANY"
6. Integration type: Lambda Function
7. Use Lambda Proxy integration: ✓
8. Lambda Function: `auralis-backend`
9. Click "Save" → "OK"

#### Step 8: Enable CORS
1. Select `{proxy+}` resource
2. Click "Actions" → "Enable CORS"
3. Click "Enable CORS and replace existing CORS headers"
4. Click "Yes, replace existing values"

#### Step 9: Deploy API
1. Click "Actions" → "Deploy API"
2. Deployment stage: "[New Stage]"
3. Stage name: `prod`
4. Click "Deploy"

#### Step 10: Save API URL
- Copy: `https://XXXXXX.execute-api.us-east-1.amazonaws.com/prod`

---

### TASK 3: Connect Frontend to Backend (5 minutes)

#### Step 1: Update API URL
Edit `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = 'https://YOUR-API-GATEWAY-URL/prod';
```

Replace with your API Gateway URL from Task 2, Step 10.

#### Step 2: Rebuild Frontend
```bash
cd frontend
npm run build
```

#### Step 3: Redeploy to Amplify
1. Go back to AWS Amplify Console
2. Find your `Auralis` app
3. Drag new `frontend/build/` folder
4. Wait 2 minutes

#### Step 4: Test
- Open your Amplify URL
- Paste a contract
- Click "Analyze"
- Should work end-to-end!

---

## Alternative: Use Render for Backend (Easier)

If Lambda is too complex, use Render.com:

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

Then update `frontend/src/services/api.js` with this URL and rebuild.

---

## Files Ready for Upload:

- ✅ `frontend/build/` → AWS Amplify
- ✅ `backend/auralis_lambda.zip` → AWS Lambda

---

## After Deployment:

### Update Documentation
```bash
# Update README.md with live URL
# Update HACKATHON_JOURNAL.md
git add .
git commit -m "docs: Add live deployment URLs"
git push
```

### Take Screenshots
- Empty state
- Success state with analysis
- Show Fix expanded
- Error state

---

## You're Ready to Deploy!

Follow the steps above in order. Each task takes 5-10 minutes.

**Total time: 20 minutes to fully live!** 🚀
