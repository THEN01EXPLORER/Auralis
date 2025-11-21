# 🔑 How to Get AWS Access Keys

## Step-by-Step Guide

### Option 1: Create New IAM User (Recommended for Development)

#### Step 1: Go to IAM Console
1. Log in to AWS Console: https://console.aws.amazon.com/
2. Search for "IAM" in the top search bar
3. Click on "IAM" (Identity and Access Management)

#### Step 2: Create New User
1. Click **"Users"** in the left sidebar
2. Click **"Create user"** button (top right)
3. Enter username: `auralis-app` (or any name you prefer)
4. Click **"Next"**

#### Step 3: Set Permissions
1. Select **"Attach policies directly"**
2. Search and check these policies:
   - ✅ `AmazonBedrockFullAccess` (for AI analysis)
   - ✅ `AWSLambdaFullAccess` (if deploying to Lambda)
3. Click **"Next"**
4. Click **"Create user"**

#### Step 4: Create Access Key
1. Click on the user you just created (`auralis-app`)
2. Go to **"Security credentials"** tab
3. Scroll down to **"Access keys"** section
4. Click **"Create access key"**
5. Select use case: **"Application running outside AWS"**
6. Click **"Next"**
7. (Optional) Add description: "Auralis app credentials"
8. Click **"Create access key"**

#### Step 5: Save Your Keys ⚠️ IMPORTANT
You'll see:
```
Access key ID: AKIAIOSFODNN7EXAMPLE
Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**⚠️ CRITICAL:** 
- Copy both keys immediately
- Save them in a secure location
- You can only see the secret key ONCE
- If you lose it, you'll need to create a new key

#### Step 6: Add to Your Project
Open `backend/.env.production` and add:
```bash
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
```

---

### Option 2: Use Existing IAM User

If you already have an IAM user:

#### Step 1: Go to IAM Console
1. AWS Console → IAM → Users
2. Click on your existing user

#### Step 2: Check Permissions
1. Go to **"Permissions"** tab
2. Verify you have: `AmazonBedrockFullAccess`
3. If not, click **"Add permissions"** → **"Attach policies directly"**
4. Search and add `AmazonBedrockFullAccess`

#### Step 3: Create Access Key
1. Go to **"Security credentials"** tab
2. Scroll to **"Access keys"**
3. Click **"Create access key"**
4. Follow steps 5-6 from Option 1 above

---

### Option 3: Use Root Account Keys (⚠️ NOT RECOMMENDED)

**Warning:** Using root account keys is a security risk. Only use for testing.

1. Click your account name (top right)
2. Click **"Security credentials"**
3. Scroll to **"Access keys"**
4. Click **"Create access key"**
5. Confirm the warning
6. Save the keys

**⚠️ For production, always use IAM users, not root account!**

---

## 🔒 Security Best Practices

### DO:
✅ Create separate IAM users for different applications
✅ Use minimal required permissions (principle of least privilege)
✅ Rotate access keys regularly (every 90 days)
✅ Store keys securely (never commit to Git)
✅ Use environment variables for keys
✅ Delete unused access keys

### DON'T:
❌ Share access keys with others
❌ Commit keys to GitHub/Git
❌ Use root account keys in production
❌ Give more permissions than needed
❌ Store keys in plain text files
❌ Email or message keys

---

## 🧪 Testing Your Keys

After setting up, test if they work:

```bash
# Install AWS CLI (if not installed)
pip install awscli

# Configure AWS CLI
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Enter region: us-east-1
# Enter output format: json

# Test Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

If you see a list of models, your keys work! ✅

---

## 🚨 What If I Lost My Secret Key?

**You cannot recover a lost secret key.**

You must:
1. Go to IAM → Users → Your User → Security credentials
2. Find the old access key
3. Click **"Actions"** → **"Deactivate"** (or Delete)
4. Create a new access key (follow steps above)
5. Update your `.env.production` file with new keys

---

## 💰 Cost Considerations

### AWS Bedrock Pricing (as of 2024):
- **Claude 3 Sonnet:**
  - Input: ~$3 per 1M tokens
  - Output: ~$15 per 1M tokens
- **Free tier:** No free tier for Bedrock
- **Typical analysis:** ~1000-5000 tokens per contract

### Estimated Costs:
- **100 analyses/month:** ~$1-5
- **1000 analyses/month:** ~$10-50
- **10000 analyses/month:** ~$100-500

**Tip:** Set up billing alerts in AWS Console!

---

## 🔐 Alternative: Use IAM Roles (For AWS Deployments)

If deploying to AWS Lambda or EC2, you can use IAM roles instead of access keys:

### For Lambda:
1. Create Lambda function
2. Attach IAM role with `AmazonBedrockFullAccess`
3. No need for access keys in code!

### For EC2:
1. Create EC2 instance
2. Attach IAM role with `AmazonBedrockFullAccess`
3. No need for access keys in code!

**This is more secure than using access keys!**

---

## 📋 Quick Checklist

- [ ] Created IAM user (or using existing)
- [ ] Attached `AmazonBedrockFullAccess` policy
- [ ] Created access key
- [ ] Saved Access Key ID
- [ ] Saved Secret Access Key
- [ ] Added keys to `backend/.env.production`
- [ ] Tested keys work
- [ ] Set up billing alerts (optional)

---

## 🆘 Troubleshooting

### Error: "Access Denied"
- Check IAM user has `AmazonBedrockFullAccess` policy
- Verify keys are correct (no extra spaces)
- Check region is correct (us-east-1)

### Error: "Invalid Access Key"
- Keys might be deactivated
- Check in IAM → Users → Security credentials
- Create new keys if needed

### Error: "Bedrock not available in region"
- Bedrock is only available in certain regions
- Use: us-east-1, us-west-2, or eu-west-1
- Update AWS_REGION in .env.production

---

## 📞 Need More Help?

- AWS IAM Documentation: https://docs.aws.amazon.com/IAM/
- AWS Bedrock Documentation: https://docs.aws.amazon.com/bedrock/
- AWS Support: https://console.aws.amazon.com/support/

---

**Once you have your keys, add them to `backend/.env.production` and you're ready to go!** 🚀
