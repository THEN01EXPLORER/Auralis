# 🚀 Auralis Deployment Guide

Quick guide to deploy Auralis to AWS.

## Prerequisites
- AWS Account with Bedrock access
- AWS CLI configured
- Node.js 16+ and Python 3.8+

## Backend Deployment (AWS Lambda)

### 1. Package Lambda Function
```bash
cd backend
pip install -r requirements.txt -t package/
cd package && zip -r ../auralis-lambda.zip . && cd ..
zip -g auralis-lambda.zip main.py app/
```

### 2. Create Lambda Function
```bash
aws lambda create-function \
  --function-name auralis-backend \
  --runtime python3.11 \
  --handler main.handler \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --zip-file fileb://auralis-lambda.zip \
  --timeout 300 \
  --memory-size 512
```

### 3. Configure Environment Variables
```bash
aws lambda update-function-configuration \
  --function-name auralis-backend \
  --environment Variables="{AWS_REGION=us-east-1,ENABLE_AI_ANALYSIS=true,BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0}"
```

### 4. Add Bedrock Permissions
Attach `AmazonBedrockFullAccess` policy to Lambda execution role.

## API Gateway Setup

### 1. Create REST API
```bash
aws apigateway create-rest-api --name auralis-api
```

### 2. Create Resources and Methods
- Create `/analyze` resource with POST method
- Create `/analyze_repo` resource with POST method
- Enable CORS on both
- Deploy to `prod` stage

## Frontend Deployment (AWS Amplify)

### 1. Build Frontend
```bash
cd frontend
npm install
npm run build
```

### 2. Deploy to Amplify
1. Go to AWS Amplify Console
2. Click "New app" → "Host web app"
3. Choose "Deploy without Git"
4. Upload `build/` folder
5. Deploy

## Testing
```bash
# Test backend
curl https://YOUR_API_URL/prod/analyze -X POST -H "Content-Type: application/json" -d '{"code":"contract Test{}"}'

# Test frontend
# Open Amplify URL in browser
```

## Troubleshooting
- **Lambda timeout**: Increase to 300 seconds
- **CORS errors**: Enable CORS in API Gateway
- **Bedrock access denied**: Check IAM permissions

For detailed instructions, see AWS documentation.
