# Auralis Deployment Guide

Complete step-by-step instructions for deploying Auralis to AWS.

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured with credentials
- Node.js 16+ and npm
- Python 3.8+
- Git

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AWS Cloud                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AWS Amplify (Frontend)                              │  │
│  │  - React SPA                                         │  │
│  │  - CloudFront CDN                                    │  │
│  │  - Auto-deploy from GitHub                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Gateway                                         │  │
│  │  - Rate limiting                                     │  │
│  │  - CORS configuration                               │  │
│  │  - Request/Response transformation                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AWS Lambda (Backend)                                │  │
│  │  - FastAPI application                              │  │
│  │  - Hybrid analysis engine                           │  │
│  │  - CloudWatch logging                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AWS Bedrock                                         │  │
│  │  - Claude 3 Sonnet model                            │  │
│  │  - AI-powered vulnerability analysis                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Step 1: Prepare AWS Account

### 1.1 Create IAM Role for Lambda

```bash
# Create trust policy
cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create role
aws iam create-role \
  --role-name auralis-lambda-role \
  --assume-role-policy-document file://trust-policy.json

# Attach policies
aws iam attach-role-policy \
  --role-name auralis-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Create and attach custom policy for Bedrock
cat > bedrock-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["bedrock:InvokeModel"],
      "Resource": "arn:aws:bedrock:*:*:foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    }
  ]
}
EOF

aws iam put-role-policy \
  --role-name auralis-lambda-role \
  --policy-name auralis-bedrock-policy \
  --policy-document file://bedrock-policy.json
```

### 1.2 Enable AWS Bedrock

1. Go to AWS Bedrock console
2. Click "Get started"
3. Request access to Claude 3 Sonnet model
4. Wait for approval (usually instant)

## Step 2: Deploy Backend to Lambda

### 2.1 Build Deployment Package

```bash
# Make deployment script executable
chmod +x deploy-backend.sh

# Run deployment script
./deploy-backend.sh
```

This creates `lambda_deployment/auralis-backend-deployment.zip`

### 2.2 Create Lambda Function

```bash
# Get your AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create Lambda function
aws lambda create-function \
  --function-name auralis-api \
  --runtime python3.11 \
  --role arn:aws:iam::${ACCOUNT_ID}:role/auralis-lambda-role \
  --handler lambda_handler.handler \
  --zip-file fileb://lambda_deployment/auralis-backend-deployment.zip \
  --timeout 30 \
  --memory-size 1024 \
  --environment Variables="{
    AWS_REGION=us-east-1,
    ENABLE_AI_ANALYSIS=true,
    BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0,
    LOG_LEVEL=INFO
  }"
```

### 2.3 Create API Gateway

```bash
# Create REST API
API_ID=$(aws apigateway create-rest-api \
  --name auralis-api \
  --description "Auralis Smart Contract Security Auditor" \
  --query 'id' \
  --output text)

echo "API ID: $API_ID"

# Get root resource
ROOT_ID=$(aws apigateway get-resources \
  --rest-api-id $API_ID \
  --query 'items[0].id' \
  --output text)

# Create proxy resource
PROXY_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_ID \
  --path-part '{proxy+}' \
  --query 'id' \
  --output text)

# Create ANY method
aws apigateway put-method \
  --rest-api-id $API_ID \
  --resource-id $PROXY_ID \
  --http-method ANY \
  --authorization-type NONE

# Create Lambda integration
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $PROXY_ID \
  --http-method ANY \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:${ACCOUNT_ID}:function:auralis-api/invocations

# Grant API Gateway permission to invoke Lambda
aws lambda add-permission \
  --function-name auralis-api \
  --statement-id apigateway-access \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com

# Deploy API
DEPLOYMENT_ID=$(aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod \
  --query 'id' \
  --output text)

echo "API Endpoint: https://${API_ID}.execute-api.us-east-1.amazonaws.com/prod"
```

## Step 3: Deploy Frontend to Amplify

### 3.1 Connect GitHub Repository

1. Go to AWS Amplify Console
2. Click "New app" → "Host web app"
3. Select GitHub and authorize
4. Select your Auralis repository
5. Click "Next"

### 3.2 Configure Build Settings

1. Select branch (main)
2. Click "Edit" on build settings
3. Paste the following build configuration:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm install
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/build
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
  env:
    REACT_APP_API_URL: https://YOUR_API_ENDPOINT
```

Replace `YOUR_API_ENDPOINT` with your Lambda API Gateway URL.

### 3.3 Deploy

1. Click "Save and deploy"
2. Wait for deployment to complete
3. Your frontend will be available at the Amplify URL

## Step 4: Configure Environment Variables

### 4.1 Lambda Environment Variables

```bash
aws lambda update-function-configuration \
  --function-name auralis-api \
  --environment Variables="{
    AWS_REGION=us-east-1,
    ENABLE_AI_ANALYSIS=true,
    AI_ANALYSIS_REQUIRED=false,
    BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0,
    BEDROCK_TIMEOUT=25,
    LOG_LEVEL=INFO,
    LOG_FORMAT=json,
    RATE_LIMIT_PER_MINUTE=60,
    ALLOWED_ORIGINS=https://YOUR_AMPLIFY_URL.amplifyapp.com
  }"
```

### 4.2 Amplify Environment Variables

In Amplify Console:
1. Go to App settings → Environment variables
2. Add `REACT_APP_API_URL` with your Lambda API endpoint
3. Redeploy

## Step 5: Verify Deployment

```bash
# Make verification script executable
chmod +x scripts/verify-deployment.sh

# Run verification
API_ENDPOINT=https://YOUR_API_ENDPOINT scripts/verify-deployment.sh
```

## Step 6: Set Up Monitoring

### 6.1 CloudWatch Logs

```bash
# Create log group
aws logs create-log-group --log-group-name /aws/lambda/auralis-api

# Set retention
aws logs put-retention-policy \
  --log-group-name /aws/lambda/auralis-api \
  --retention-in-days 30
```

### 6.2 CloudWatch Alarms

```bash
# High error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name auralis-high-error-rate \
  --alarm-description "Alert when Lambda error rate is high" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --dimensions Name=FunctionName,Value=auralis-api
```

## Step 7: Custom Domain (Optional)

### 7.1 Set Up Custom Domain in Amplify

1. Go to Amplify Console
2. App settings → Domain management
3. Add domain
4. Follow DNS configuration steps

### 7.2 Update CORS Settings

```bash
aws lambda update-function-configuration \
  --function-name auralis-api \
  --environment Variables="{
    ALLOWED_ORIGINS=https://your-custom-domain.com
  }"
```

## Troubleshooting

### Lambda Function Timeout

If analysis takes too long:
1. Increase Lambda timeout (max 15 minutes)
2. Increase memory (more CPU)
3. Optimize Bedrock prompts

```bash
aws lambda update-function-configuration \
  --function-name auralis-api \
  --timeout 60 \
  --memory-size 2048
```

### CORS Errors

Check CORS configuration:
```bash
aws lambda get-function-configuration --function-name auralis-api | grep ALLOWED_ORIGINS
```

### Bedrock Access Denied

Verify IAM policy:
```bash
aws iam get-role-policy \
  --role-name auralis-lambda-role \
  --policy-name auralis-bedrock-policy
```

### High Costs

Monitor Lambda invocations and Bedrock usage:
```bash
# Get Lambda metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=auralis-api \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## Cost Estimation

### Monthly Costs (Estimated)

- **Lambda**: $0.20 per 1M requests + compute time
- **Bedrock**: $0.003 per 1K input tokens + $0.015 per 1K output tokens
- **API Gateway**: $3.50 per 1M requests
- **Amplify**: $0.01 per GB served
- **CloudWatch**: ~$5-10 for logs

**Total**: ~$50-100/month for moderate usage

## Rollback Procedure

If something goes wrong:

```bash
# Rollback Lambda to previous version
aws lambda update-function-code \
  --function-name auralis-api \
  --zip-file fileb://previous-deployment.zip

# Rollback Amplify
# Go to Amplify Console → Deployments → Select previous deployment → Redeploy
```

## Next Steps

1. Monitor CloudWatch logs
2. Set up alerts for errors
3. Configure auto-scaling if needed
4. Plan for disaster recovery
5. Set up CI/CD pipeline for automated deployments

## Support

For issues or questions:
1. Check CloudWatch logs
2. Review AWS documentation
3. Check Auralis GitHub issues
4. Contact AWS support (if applicable)
