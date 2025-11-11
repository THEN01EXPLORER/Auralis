# 🚀 AWS Deployment Guide - Days 13-14

**Goal:** Deploy Auralis to AWS with a live, public URL

---

## DAY 13: Deploy Backend to AWS Lambda

### Step 1: Create Lambda Deployment Package

**In your terminal:**

```bash
cd backend
python lambda_package.py
```

This will create `auralis_lambda.zip` (approximately 50-100 MB).

**What it does:**
- Installs all dependencies from requirements.txt
- Packages the app/ directory
- Creates a Lambda-compatible zip file

---

### Step 2: Create Lambda Function

**Go to AWS Console:**

1. **Open AWS Lambda Console:**
   - URL: https://console.aws.amazon.com/lambda/
   - Or search "Lambda" in AWS Console

2. **Create Function:**
   - Click "Create function"
   - Choose "Author from scratch"
   - Function name: `Auralis-Backend`
   - Runtime: **Python 3.11**
   - Architecture: x86_64
   - Click "Create function"

3. **Upload Deployment Package:**
   - In the "Code" tab
   - Click "Upload from" → ".zip file"
   - Select `auralis_lambda.zip`
   - Click "Save"
   - **Wait for upload to complete** (may take 1-2 minutes)

4. **Configure Handler:**
   - In "Runtime settings" section
   - Click "Edit"
   - Handler: `main.handler`
   - Click "Save"

5. **Configure Timeout:**
   - Go to "Configuration" tab → "General configuration"
   - Click "Edit"
   - Timeout: **5 minutes** (300 seconds)
   - Memory: **512 MB** (or higher if needed)
   - Click "Save"

6. **Configure Environment Variables:**
   - Go to "Configuration" tab → "Environment variables"
   - Click "Edit" → "Add environment variable"
   - Add these variables:
     ```
     AWS_REGION = us-east-1
     ENABLE_AI_ANALYSIS = true
     BEDROCK_MODEL_ID = anthropic.claude-3-sonnet-20240229-v1:0
     LOG_LEVEL = INFO
     ```
   - Click "Save"

---

### Step 3: Add Bedrock Permissions

**Configure IAM Role:**

1. **Go to Configuration → Permissions**
2. Click on the **Role name** (e.g., `Auralis-Backend-role-xxxxx`)
3. This opens the IAM Console
4. Click "Add permissions" → "Attach policies"
5. Search for: `AmazonBedrockFullAccess`
6. Check the box next to it
7. Click "Add permissions"

**Alternative: Create Custom Policy (More Secure)**

If you want minimal permissions:

1. Click "Add permissions" → "Create inline policy"
2. Choose JSON tab
3. Paste:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
        }
    ]
}
```
4. Name it: `BedrockInvokePolicy`
5. Click "Create policy"

---

### Step 4: Test Lambda Function

**Create Test Event:**

1. In Lambda console, click "Test" tab
2. Click "Create new event"
3. Event name: `TestAnalyze`
4. Event JSON:
```json
{
    "httpMethod": "POST",
    "path": "/api/v1/analyze",
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "{\"code\": \"pragma solidity ^0.8.0; contract Test { function test() public {} }\"}"
}
```
5. Click "Save"
6. Click "Test"
7. Check response - should see analysis results

**If test fails:**
- Check CloudWatch Logs (link in test results)
- Verify handler is set to `main.handler`
- Verify Bedrock permissions are attached
- Check environment variables

---

## DAY 14: Deploy API Gateway & Frontend

### Step 1: Create API Gateway

**Go to API Gateway Console:**

1. **Open API Gateway:**
   - URL: https://console.aws.amazon.com/apigateway/
   - Or search "API Gateway" in AWS Console

2. **Create API:**
   - Click "Create API"
   - Choose "REST API" (not Private or HTTP API)
   - Click "Build"
   - API name: `Auralis-API`
   - Description: "Auralis Smart Contract Security API"
   - Endpoint Type: Regional
   - Click "Create API"

---

### Step 2: Create /analyze Endpoint

**Create Resource:**

1. Click "Actions" → "Create Resource"
2. Resource Name: `analyze`
3. Resource Path: `/analyze`
4. Enable CORS: ✅ Check this box
5. Click "Create Resource"

**Create POST Method:**

1. With `/analyze` selected, click "Actions" → "Create Method"
2. Select "POST" from dropdown
3. Click the checkmark ✓
4. Configure:
   - Integration type: **Lambda Function**
   - Use Lambda Proxy integration: ✅ **Check this box** (IMPORTANT!)
   - Lambda Region: us-east-1 (or your region)
   - Lambda Function: `Auralis-Backend`
   - Click "Save"
5. Click "OK" to give API Gateway permission to invoke Lambda

---

### Step 3: Create /analyze_repo Endpoint

**Create Resource:**

1. Click root `/` in the tree
2. Click "Actions" → "Create Resource"
3. Resource Name: `analyze_repo`
4. Resource Path: `/analyze_repo`
5. Enable CORS: ✅ Check this box
6. Click "Create Resource"

**Create POST Method:**

1. With `/analyze_repo` selected, click "Actions" → "Create Method"
2. Select "POST" from dropdown
3. Click the checkmark ✓
4. Configure:
   - Integration type: **Lambda Function**
   - Use Lambda Proxy integration: ✅ **Check this box** (IMPORTANT!)
   - Lambda Region: us-east-1 (or your region)
   - Lambda Function: `Auralis-Backend`
   - Click "Save"
5. Click "OK" to give API Gateway permission

---

### Step 4: Enable CORS (Important!)

**For /analyze:**

1. Select `/analyze` resource
2. Click "Actions" → "Enable CORS"
3. Keep default settings:
   - Access-Control-Allow-Origin: `'*'`
   - Access-Control-Allow-Headers: `'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'`
4. Click "Enable CORS and replace existing CORS headers"
5. Click "Yes, replace existing values"

**For /analyze_repo:**

1. Select `/analyze_repo` resource
2. Click "Actions" → "Enable CORS"
3. Keep default settings
4. Click "Enable CORS and replace existing CORS headers"
5. Click "Yes, replace existing values"

---

### Step 5: Deploy API

**Create Deployment:**

1. Click "Actions" → "Deploy API"
2. Deployment stage: **[New Stage]**
3. Stage name: `prod`
4. Stage description: "Production"
5. Click "Deploy"

**Get Your API URL:**

After deployment, you'll see:
```
Invoke URL: https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod
```

**Copy this URL!** You'll need it for the frontend.

**Your endpoints will be:**
- Analyze: `https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/analyze`
- Analyze Repo: `https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/analyze_repo`

---

### Step 6: Test API Gateway

**Test with curl:**

```bash
curl -X POST https://YOUR_API_URL/prod/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "pragma solidity ^0.8.0; contract Test { function test() public {} }"}'
```

Should return analysis results.

---

### Step 7: Update Frontend API URLs

**Edit frontend/src/services/api.js:**

Replace:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

With:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod';
```

**Update endpoint paths:**

Change:
```javascript
const response = await axios.post(`${API_BASE_URL}/api/v1/analyze`, {
```

To:
```javascript
const response = await axios.post(`${API_BASE_URL}/analyze`, {
```

And:
```javascript
const response = await axios.post(`${API_BASE_URL}/api/v1/analyze_repo`, {
```

To:
```javascript
const response = await axios.post(`${API_BASE_URL}/analyze_repo`, {
```

---

### Step 8: Build Frontend

**In frontend directory:**

```bash
cd frontend
npm run build
```

This creates a `build/` folder with optimized production files.

---

### Step 9: Deploy to AWS Amplify

**Option A: Manual Deployment (Fastest)**

1. **Go to AWS Amplify Console:**
   - URL: https://console.aws.amazon.com/amplify/
   - Or search "Amplify" in AWS Console

2. **Create New App:**
   - Click "New app" → "Host web app"
   - Choose "Deploy without Git provider"
   - Click "Continue"

3. **Upload Build:**
   - App name: `Auralis`
   - Environment name: `production`
   - Drag and drop the entire `frontend/build` folder
   - Or click "Choose files" and select the build folder
   - Click "Save and deploy"

4. **Wait for Deployment:**
   - Takes 2-3 minutes
   - Watch the progress bar

5. **Get Your URL:**
   - After deployment completes, you'll see:
   ```
   https://production.xxxxxxxxxxxxxx.amplifyapp.com
   ```
   - **This is your live Auralis URL!**

**Option B: GitHub Deployment (Automatic Updates)**

1. Push your code to GitHub
2. In Amplify Console, choose "GitHub"
3. Connect your repository
4. Configure build settings:
   - Build command: `npm run build`
   - Build output directory: `build`
5. Deploy

---

### Step 10: Test Live Application

**Open your Amplify URL in browser:**

1. **Test Empty State:**
   - Should see welcome screen

2. **Test Single Contract Analysis:**
   - Paste a Solidity contract
   - Click "Analyze Contract"
   - Should see results

3. **Test Repository Scanner:**
   - Paste a GitHub URL (e.g., `https://github.com/OpenZeppelin/openzeppelin-contracts`)
   - Click "Analyze Repo"
   - Should see tabbed results

**If something doesn't work:**
- Check browser console for errors
- Verify API Gateway URL is correct in api.js
- Check API Gateway CORS settings
- Check Lambda CloudWatch logs

---

## Troubleshooting

### Lambda Issues

**Problem:** Function times out
**Solution:** Increase timeout to 5 minutes in Configuration

**Problem:** "Module not found" error
**Solution:** Verify handler is `main.handler`, not `app.main.handler`

**Problem:** Bedrock access denied
**Solution:** Verify IAM role has Bedrock permissions

### API Gateway Issues

**Problem:** CORS errors in browser
**Solution:** Enable CORS on both resources, redeploy API

**Problem:** 502 Bad Gateway
**Solution:** Check Lambda Proxy integration is enabled

**Problem:** 403 Forbidden
**Solution:** Verify API is deployed to `prod` stage

### Frontend Issues

**Problem:** API calls fail
**Solution:** Verify API_BASE_URL is correct, includes `/prod`

**Problem:** Build fails
**Solution:** Run `npm install` first, check for errors

---

## Deployment Checklist

### Backend (Lambda)
- [ ] auralis_lambda.zip created
- [ ] Lambda function created (Python 3.11)
- [ ] Handler set to `main.handler`
- [ ] Timeout set to 5 minutes
- [ ] Memory set to 512 MB+
- [ ] Environment variables configured
- [ ] Bedrock permissions attached
- [ ] Test event passes

### API Gateway
- [ ] REST API created
- [ ] /analyze resource created
- [ ] /analyze POST method created with Lambda Proxy
- [ ] /analyze_repo resource created
- [ ] /analyze_repo POST method created with Lambda Proxy
- [ ] CORS enabled on both resources
- [ ] API deployed to `prod` stage
- [ ] Invoke URL copied

### Frontend
- [ ] api.js updated with API Gateway URL
- [ ] Endpoint paths updated (removed /api/v1)
- [ ] npm run build completed successfully
- [ ] Amplify app created
- [ ] Build folder uploaded
- [ ] Deployment successful
- [ ] Live URL obtained

### Testing
- [ ] Lambda test event passes
- [ ] API Gateway curl test works
- [ ] Frontend loads in browser
- [ ] Single contract analysis works
- [ ] Repository scanner works
- [ ] No CORS errors in console

---

## Final URLs

**Backend API:**
```
https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod
```

**Frontend App:**
```
https://production.xxxxxxxxxxxxxx.amplifyapp.com
```

**Save these URLs for your README and submission!**

---

## Next Steps

After deployment:
1. Update README.md with live demo URL
2. Test all features on live site
3. Take screenshots for documentation
4. Proceed to Day 15: Finalize Documentation

---

**Deployment complete! Auralis is now live on AWS!** 🎉
