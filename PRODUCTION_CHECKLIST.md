# 🚀 Production Deployment Checklist

Your code is now production-ready! Follow this checklist before deploying.

## ✅ Code Status
- ✅ No syntax errors
- ✅ No console.log statements in frontend
- ✅ Environment variables configured
- ✅ CORS properly configured
- ✅ Error handling in place
- ✅ Logging configured
- ✅ API endpoints use /api/v1 prefix

## 📋 Pre-Deployment Steps

### 1. Backend Configuration
```bash
cd backend

# Create production environment file
cp .env.example .env.production

# Edit .env.production with your AWS credentials
# Required variables:
# - AWS_REGION
# - AWS_ACCESS_KEY_ID (or use IAM role)
# - AWS_SECRET_ACCESS_KEY (or use IAM role)
```

### 2. Frontend Configuration
```bash
cd frontend

# Update .env.production with your API URL
# Replace: https://your-api-id.execute-api.us-east-1.amazonaws.com/Prod
# With your actual API Gateway URL
```

### 3. Security Settings

**Update CORS in production:**
```bash
# In backend/.env.production, replace:
ALLOWED_ORIGINS=*

# With your actual frontend domain:
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 🌐 Deployment Options

### Option 1: AWS (Recommended)

**Backend: AWS Lambda + API Gateway**
```bash
cd backend
pip install -r requirements.txt -t package/
cd package && zip -r ../auralis-lambda.zip . && cd ..
zip -g auralis-lambda.zip main.py app/

# Upload to Lambda via AWS Console or CLI
aws lambda update-function-code \
  --function-name auralis-backend \
  --zip-file fileb://auralis-lambda.zip
```

**Frontend: AWS Amplify**
```bash
cd frontend
npm install
npm run build

# Upload build/ folder to Amplify Console
```

### Option 2: Heroku

```bash
# Install Heroku CLI
# Login: heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set AWS_REGION=us-east-1
heroku config:set ENABLE_AI_ANALYSIS=true
heroku config:set AWS_ACCESS_KEY_ID=your-key
heroku config:set AWS_SECRET_ACCESS_KEY=your-secret

# Deploy
git push heroku main
```

### Option 3: VPS (DigitalOcean, Linode, etc.)

```bash
# On your server:
git clone your-repo
cd your-repo

# Backend
cd backend
pip install -r requirements.txt
gunicorn -c gunicorn.conf.py main:app

# Frontend
cd frontend
npm install
npm run build
# Serve build/ folder with nginx or serve
```

### Option 4: Docker

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🔒 Security Checklist

- [ ] AWS credentials configured (use IAM roles in production)
- [ ] CORS restricted to your domain (not *)
- [ ] Environment variables set (not hardcoded)
- [ ] HTTPS enabled
- [ ] API rate limiting configured (optional)
- [ ] Secrets stored securely (AWS Secrets Manager, etc.)

## 🧪 Testing Before Go-Live

```bash
# Test backend health
curl https://your-api-url/health

# Test analysis endpoint
curl -X POST https://your-api-url/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"contract Test{}"}'

# Test frontend
# Open your frontend URL in browser
# Try analyzing a contract
# Try analyzing a repository
```

## 📊 Monitoring

After deployment, monitor:
- [ ] CloudWatch Logs (AWS)
- [ ] Error rates
- [ ] Response times
- [ ] AWS Bedrock usage/costs

## 🆘 Troubleshooting

**Backend won't start:**
- Check environment variables are set
- Verify AWS credentials
- Check logs for errors

**Frontend can't connect:**
- Verify API URL in .env.production
- Check CORS settings
- Verify API Gateway is deployed

**AI analysis not working:**
- Check AWS Bedrock permissions
- Verify model ID is correct
- Check AWS region matches

## 🎉 You're Ready!

Your code is production-ready. Choose your deployment option and follow the steps above.

**Need help?** Check DEPLOYMENT.md for detailed instructions.
