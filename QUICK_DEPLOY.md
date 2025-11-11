# 🚀 Quick Deploy Reference

## ✅ Step 1: Lambda Package Created!

**File:** `backend/auralis_lambda.zip`
**Size:** 22.61 MB
**Location:** In your `backend/` folder

---

## 📤 Step 2: Upload to AWS Lambda

### Create Lambda Function:

1. **Go to:** https://console.aws.amazon.com/lambda/

2. **Click:** "Create function"

3. **Configure:**
   - Function name: `Auralis-Backend`
   - Runtime: **Python 3.11**
   - Architecture: x86_64
   - Click "Create function"

4. **Upload ZIP:**
   - In "Code" tab
   - Click "Upload from" → ".zip file"
   - Select `backend/auralis_lambda.zip`
   - Click "Save"
   - **Wait 1-2 minutes for upload**

5. **Set Handler:**
   - In "Runtime settings" section
   - Click "Edit"
   - Handler: **`app.main.handler`** ← IMPORTANT!
   - Click "Save"

6. **Set Timeout:**
   - Go to "Configuration" → "General configuration"
   - Click "Edit"
   - Timeout: **300 seconds** (5 minutes)
   - Memory: **512 MB**
   - Click "Save"

7. **Add Environment Variables:**
   - Go to "Configuration" → "Environment variables"
   - Click "Edit" → "Add environment variable"
   - Add:
     ```
     AWS_REGION = us-east-1
     ENABLE_AI_ANALYSIS = true
     BEDROCK_MODEL_ID = anthropic.claude-3-sonnet-20240229-v1:0
     LOG_LEVEL = INFO
     ```
   - Click "Save"

8. **Add Bedrock Permissions:**
   - Go to "Configuration" → "Permissions"
   - Click the Role name (opens IAM)
   - Click "Add permissions" → "Attach policies"
   - Search: `AmazonBedrockFullAccess`
   - Check the box
   - Click "Add permissions"

---

## 🧪 Step 3: Test Lambda

1. Click "Test" tab
2. Click "Create new event"
3. Event name: `TestAnalyze`
4. Paste this JSON:
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
7. Should see success response!

---

## 🌐 Step 4: Create API Gateway (Tomorrow - Day 14)

After Lambda is working, you'll:
1. Create REST API in API Gateway
2. Create `/analyze` and `/analyze_repo` endpoints
3. Connect to Lambda
4. Enable CORS
5. Deploy to `prod` stage
6. Get your API URL

---

## 📝 Important Notes

**Handler Path:** `app.main.handler` (NOT `main.handler`)

**Why?** The zip contains:
```
auralis_lambda.zip/
├── app/
│   └── main.py  ← Your FastAPI app with handler
├── fastapi/
├── boto3/
└── ... (other dependencies)
```

**Timeout:** Must be 5 minutes because:
- Repository cloning takes time
- AI analysis can be slow
- Multiple files need processing

**Memory:** 512 MB minimum because:
- GitPython needs memory for cloning
- AI model responses can be large
- Multiple concurrent analyses

---

## ❌ Common Errors & Fixes

**Error:** "Unable to import module 'app.main'"
**Fix:** Verify handler is `app.main.handler`

**Error:** "Task timed out after 3.00 seconds"
**Fix:** Increase timeout to 300 seconds

**Error:** "AccessDeniedException: User is not authorized to perform: bedrock:InvokeModel"
**Fix:** Attach AmazonBedrockFullAccess policy to Lambda role

**Error:** "No module named 'mangum'"
**Fix:** Re-create zip with `python lambda_package.py`

---

## ✅ Checklist

Before moving to Day 14:
- [ ] Lambda function created
- [ ] auralis_lambda.zip uploaded
- [ ] Handler set to `app.main.handler`
- [ ] Timeout set to 300 seconds
- [ ] Memory set to 512 MB
- [ ] Environment variables added
- [ ] Bedrock permissions attached
- [ ] Test event passes successfully

---

## 🎯 Next Steps

Once Lambda test passes:
1. Open `AWS_DEPLOYMENT_STEPS.md`
2. Go to "DAY 14: Deploy API Gateway & Frontend"
3. Follow steps to create API Gateway
4. Deploy frontend to Amplify
5. Get your live URL!

---

**You're doing great! Lambda is the hardest part. After this, it's smooth sailing!** 🚀
