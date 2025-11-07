# 🚀 Deploy Auralis to Production - Step by Step

## Prerequisites Check

Before deploying, ensure you have:
- ✅ AWS CLI installed and configured (`aws configure`)
- ✅ AWS SAM CLI installed (`sam --version`)
- ✅ Valid AWS credentials with permissions for Lambda, API Gateway, and Bedrock

---

## Part 1: Deploy Backend to AWS Lambda

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Build the Lambda Package
```bash
sam build
```

**Expected Output:** "Build Succeeded"

### Step 3: Deploy to AWS
```bash
sam deploy --guided
```

**Answer the prompts:**
- Stack Name: `auralis-backend`
- AWS Region: `us-east-1` (or your preferred region)
- Confirm changes before deploy: `Y`
- Allow SAM CLI IAM role creation: `Y`
- Disable rollback: `N`
- AuralisFunction may not have authorization defined: `Y`
- Save arguments to configuration file: `Y`
- SAM configuration file: `samconfig.toml`
- SAM configuration environment: `default`

### Step 4: Get Your API URL
After deployment completes, look for the **Outputs** section:
```
Outputs
-----------------------------------------------------------------
Key                 AuralisApi
Description         API Gateway endpoint URL for Prod stage
Value               https://XXXXXXXXXX.execute-api.us-east-1.amazonaws.com/Prod/
-----------------------------------------------------------------
```

**COPY THIS URL!** You'll need it for the frontend.

### Step 5: Test the Backend
```bash
curl https://YOUR-API-URL/health
```

Should return: `{"status":"healthy"}`

---

## Part 2: Deploy Frontend to AWS Amplify

### Step 1: Update API URL in Frontend

Open `frontend/src/services/api.js` and update:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://YOUR-API-URL-HERE/Prod';
```

Replace `YOUR-API-URL-HERE` with the URL from Step 4 above.

### Step 2: Build the Frontend
```bash
cd frontend
npm run build
```

**Expected Output:** Creates a `build/` folder

### Step 3: Deploy to AWS Amplify

**Option A: Using AWS Amplify Console (Easiest)**

1. Go to AWS Amplify Console: https://console.aws.amazon.com/amplify/
2. Click "New app" → "Host web app"
3. Choose "Deploy without Git provider"
4. App name: `auralis`
5. Environment name: `production`
6. Drag and drop the entire `build/` folder
7. Click "Save and deploy"

**Option B: Using Amplify CLI**

```bash
npm install -g @aws-amplify/cli
amplify configure
amplify init
amplify add hosting
amplify publish
```

### Step 4: Get Your Live URL

Amplify will provide a URL like:
```
https://production.XXXXXXXXXX.amplifyapp.com
```

**This is your live Auralis URL!** 🎉

---

## Part 3: Test the Live Application

1. Open your Amplify URL in a browser
2. Test all three states:
   - ✅ Empty State (on first load)
   - ✅ Success State (paste contract and analyze)
   - ✅ Error State (if backend has issues)

---

## Part 4: Update Documentation

### Update README.md
Add the live demo link:
```markdown
## 🌐 Live Demo

**Try Auralis now:** https://your-amplify-url.amplifyapp.com

**API Endpoint:** https://your-api-url.execute-api.us-east-1.amazonaws.com/Prod/
```

### Update HACKATHON_JOURNAL.md
Add entry:
```markdown
## DAY 8 (NOV 8): AURALIS IS LIVE 🚀

**Status:** DEPLOYED TO PRODUCTION

Successfully deployed Auralis to AWS:
- Backend: AWS Lambda + API Gateway
- Frontend: AWS Amplify
- Live URL: https://your-amplify-url.amplifyapp.com

The application is now publicly accessible and ready for judging.
```

---

## Troubleshooting

### Backend Issues

**Problem:** SAM build fails
**Solution:** 
```bash
pip install -r requirements.txt
sam build --use-container
```

**Problem:** Lambda timeout
**Solution:** Already increased to 60s in template.yaml

**Problem:** CORS errors
**Solution:** Already set to allow all origins in main.py

### Frontend Issues

**Problem:** API calls fail
**Solution:** Check API URL in api.js includes `/Prod` at the end

**Problem:** Build fails
**Solution:**
```bash
rm -rf node_modules
npm install
npm run build
```

---

## Quick Redeploy Commands

### Update Backend:
```bash
cd backend
sam build
sam deploy
```

### Update Frontend:
```bash
cd frontend
npm run build
# Then re-upload build/ folder to Amplify Console
```

---

## Cost Estimate

**AWS Lambda:**
- Free tier: 1M requests/month
- Your usage: ~0 cost during hackathon

**API Gateway:**
- Free tier: 1M requests/month
- Your usage: ~0 cost during hackathon

**AWS Amplify:**
- Free tier: 1000 build minutes/month
- Your usage: ~0 cost during hackathon

**Total Expected Cost: $0** (within free tier)

---

## Success Checklist

- [ ] Backend deployed to Lambda
- [ ] API Gateway URL obtained
- [ ] Frontend updated with API URL
- [ ] Frontend built successfully
- [ ] Frontend deployed to Amplify
- [ ] Live URL obtained
- [ ] All three UI states tested
- [ ] Documentation updated
- [ ] Changes committed to GitHub

---

## 🎉 Victory Condition

When you can share a link like `https://auralis.amplifyapp.com` and anyone in the world can use your app, **YOU'VE WON!**

That's what separates a project from a product. Let's make it happen! 🚀
