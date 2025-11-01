# AWS Lambda Deployment Guide

## Prerequisites
- AWS Account with Bedrock access
- AWS CLI configured
- Serverless Framework installed

## Step 1: Install Serverless Framework
```bash
npm install -g serverless
```

## Step 2: Configure AWS Credentials
```bash
aws configure
```

## Step 3: Deploy Backend
```bash
cd backend
serverless deploy
```

## Step 4: Update Frontend API URL
After deployment, update frontend/src/services/api.js with the API Gateway URL

## Step 5: Test Deployment
```bash
curl https://your-api-gateway-url/health
```

## Environment Variables
Set USE_BEDROCK=true in Lambda environment
