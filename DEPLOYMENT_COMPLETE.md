# 🚀 AWS DEPLOYMENT GUIDE - COMPLETE

## Lambda Deployment (Backend)

### serverless.yml
```yaml
service: guardianai-audit

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  environment:
    AWS_BEDROCK_REGION: us-east-1

functions:
  api:
    handler: lambda_handler.handler
    events:
      - httpApi:
          path: /{proxy+}
          method: ANY
    timeout: 30
    memorySize: 512

plugins:
  - serverless-python-requirements
```

### Deploy Commands
```bash
# Install serverless
npm install -g serverless

# Deploy
cd backend
serverless deploy

# Get API URL
serverless info
```

## Amplify Deployment (Frontend)

### amplify.yml
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
    baseDirectory: build
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

### Deploy Steps
1. Push code to GitHub
2. Connect to AWS Amplify
3. Select repository
4. Configure build settings
5. Deploy

## Environment Variables

### Backend (.env)
```
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL=anthropic.claude-3-sonnet-20240229-v1:0
CORS_ORIGINS=https://your-amplify-url.amplifyapp.com
```

### Frontend (.env)
```
REACT_APP_API_URL=https://your-api-gateway-url.amazonaws.com
```

## Quick Deploy Script

```bash
#!/bin/bash

# Backend
cd backend
serverless deploy
BACKEND_URL=$(serverless info --verbose | grep "endpoint:" | awk '{print $2}')

# Frontend
cd ../frontend
echo "REACT_APP_API_URL=$BACKEND_URL" > .env
npm run build

# Amplify (manual step)
echo "Deploy frontend/build to Amplify"
echo "Backend URL: $BACKEND_URL"
```

## Post-Deployment Checklist

- [ ] Backend API accessible
- [ ] Frontend loads
- [ ] CORS configured
- [ ] Bedrock permissions set
- [ ] Environment variables set
- [ ] SSL certificate active
- [ ] Custom domain (optional)
- [ ] Monitoring enabled

## Testing Production

```bash
# Test backend
curl https://your-api.amazonaws.com/health

# Test analysis
curl -X POST https://your-api.amazonaws.com/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"contract_code": "test"}'
```

**Deployment ready! Follow steps above to go live.**
