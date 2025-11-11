# 🚀 Deployment Completion Guide

**Complete these steps to get Auralis live!**

---

## ✅ What's Already Done:

- ✅ Lambda function created and tested
- ✅ Backend code deployed
- ✅ Bedrock permissions configured
- ✅ Frontend code updated for API Gateway

---

## 📋 Steps You Need to Complete:

### STEP 1: Finish API Gateway Setup

**Create /analyze_repo endpoint:**

1. Go to API Gateway console
2. Select your `Auralis-API`
3. Click root `/`
4. Click "Create resource"
   - Resource name: `analyze_repo`
   - Enable CORS
5. Select `/analyze_repo`
6. Click "Create method"
   - Method: POST
   - Integration: Lambda function
   - Lambda proxy: ON
   - Function: `Auralis-Backend`
7. Click "Deploy API"
   - Stage: [New Stage]
   - Stage name: `prod`
8. **COPY the Invoke URL!**

**Your Invoke URL will look like:**
```
https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod
```

---

### STEP 2: Update Frontend with Your API URL

**Edit this file:** `frontend/src/services/api.js`

**Find this line (line 4):**
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

**Replace with your API Gateway URL:**
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod';
```

**Example:**
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod';
```

---

### STEP 3: Build Frontend

**In your terminal:**

```bash
cd frontend
npm install
npm run build
```

This creates a `build/` folder with your production-ready app.

---

### STEP 4: Deploy to AWS Amplify

**Option A: Manual Deployment (Fastest)**

1. Go to: https://console.aws.amazon.com/amplify/
2. Click "New app" → "Host web app"
3. Choose "Deploy without Git provider"
4. App name: `Auralis`
5. Environment: `production`
6. Drag and drop the entire `frontend/build` folder
7. Click "Save and deploy"
8. Wait 2-3 minutes
9. **COPY your Amplify URL!**

**Your Amplify URL will look like:**
```
https://production.xxxxxxxxxxxxxx.amplifyapp.com
```

**Option B: GitHub Deployment (Auto-updates)**

1. Push your code to GitHub
2. In Amplify, choose "GitHub"
3. Connect repository
4. Build settings:
   - Build command: `npm run build`
   - Output directory: `build`
5. Deploy

---

### STEP 5: Test Your Live App

**Open your Amplify URL in browser:**

1. **Test Empty State** - Should see welcome screen
2. **Test Single Contract:**
   - Paste a Solidity contract
   - Click "Analyze Contract"
   - Should see results
3. **Test Repo Scanner:**
   - Paste: `https://github.com/OpenZeppelin/openzeppelin-contracts`
   - Click "Analyze Repo"
   - Should see tabbed results

---

### STEP 6: Update README with Live URLs

**Edit:** `README.md`

**Find this line:**
```markdown
**[YOUR_LIVE_AMPLIFY_URL_GOES_HERE]**
```

**Replace with:**
```markdown
**[https://production.xxxxxxxxxxxxxx.amplifyapp.com](https://production.xxxxxxxxxxxxxx.amplifyapp.com)**
```

---

### STEP 7: Commit and Push

```bash
git add .
git commit -m "DEPLOY: Auralis is live on AWS - Updated API URLs and README"
git push origin main
```

---

## 🎯 Final Checklist:

- [ ] API Gateway created with /analyze and /analyze_repo
- [ ] API deployed to `prod` stage
- [ ] Invoke URL copied
- [ ] Frontend api.js updated with API Gateway URL
- [ ] Frontend built (`npm run build`)
- [ ] Amplify app created
- [ ] Build folder uploaded to Amplify
- [ ] Amplify URL copied
- [ ] Live app tested (all 3 features work)
- [ ] README updated with live URL
- [ ] Changes committed and pushed to GitHub

---

## 📝 Save These URLs:

**API Gateway Invoke URL:**
```
https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod
```

**Amplify App URL:**
```
https://production.xxxxxxxxxxxxxx.amplifyapp.com
```

**GitHub Repository:**
```
https://github.com/THEN01EXPLORER/Auralis
```

---

## 🆘 Troubleshooting:

**Frontend shows CORS error:**
- Go to API Gateway
- Select each resource (/analyze, /analyze_repo)
- Enable CORS
- Redeploy API

**API returns 502 Bad Gateway:**
- Check Lambda Proxy integration is enabled
- Redeploy API

**Amplify build fails:**
- Check build logs
- Verify `npm run build` works locally
- Check package.json has correct scripts

---

## 🎉 Once Complete:

You'll have:
- ✅ Live backend API on AWS Lambda
- ✅ Live frontend on AWS Amplify
- ✅ Public URL to share
- ✅ Ready for video recording
- ✅ Ready for submission

---

**Take your time! Complete each step carefully. Once done, you'll have a fully deployed application!** 🚀
