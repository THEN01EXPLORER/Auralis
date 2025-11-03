# AWS Deployment Guide

## Prerequisites
- AWS Account
- AWS CLI installed and configured
- AWS SAM CLI installed
- Node.js and npm

## Backend Deployment (AWS Lambda + API Gateway)

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Build with SAM
```bash
sam build
```

### Step 3: Deploy to AWS
```bash
sam deploy --guided
```

Follow the prompts:
- Stack Name: `auralis-backend`
- AWS Region: `us-east-1` (or your preferred region)
- Confirm changes: `Y`
- Allow SAM CLI IAM role creation: `Y`
- Disable rollback: `N`
- Save arguments to config: `Y`

### Step 4: Get API URL
After deployment, SAM will output:
```
Outputs:
AuralisApi: https://[id].execute-api.us-east-1.amazonaws.com/Prod/
```

Copy this URL for frontend configuration.

## Frontend Deployment (AWS Amplify)

### Step 1: Update API URL
Edit `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'https://[your-api-id].execute-api.us-east-1.amazonaws.com/Prod';
```

### Step 2: Build Frontend
```bash
cd frontend
npm install
npm run build
```

### Step 3: Deploy to Amplify

#### Option A: Amplify Console (Drag & Drop)
1. Go to AWS Amplify Console
2. Click "Host web app"
3. Choose "Deploy without Git provider"
4. Drag and drop the `build` folder
5. Click "Save and deploy"

#### Option B: Amplify CLI
```bash
npm install -g @aws-amplify/cli
amplify init
amplify add hosting
amplify publish
```

### Step 4: Get Website URL
Amplify will provide a URL like:
```
https://[branch].[app-id].amplifyapp.com
```

## Testing Deployment

1. Open the Amplify URL in browser
2. Paste a smart contract
3. Click "Analyze Contract"
4. Verify vulnerabilities are detected
5. Check risk score calculation
6. Test line highlighting
7. Expand remediation sections

## Troubleshooting

### Backend Issues
- **CORS errors**: Check CORS settings in main.py
- **Timeout**: Increase Lambda timeout in template.yaml
- **Import errors**: Verify all dependencies in requirements.txt

### Frontend Issues
- **API connection failed**: Verify API URL in api.js
- **Build errors**: Run `npm install` again
- **Blank page**: Check browser console for errors

## Cost Optimization

### Lambda
- Free tier: 1M requests/month
- Pay per execution after free tier

### Amplify
- Free tier: 1000 build minutes/month
- 15 GB served/month free

### API Gateway
- Free tier: 1M API calls/month

## Security Considerations

1. Enable AWS WAF for API Gateway
2. Set up CloudWatch alarms
3. Use AWS Secrets Manager for sensitive data
4. Enable CloudTrail logging
5. Implement rate limiting

## Monitoring

### CloudWatch Logs
```bash
aws logs tail /aws/lambda/auralis-backend --follow
```

### API Gateway Metrics
- Check AWS Console → API Gateway → Stages → Prod → Logs/Tracing

### Amplify Logs
- Check AWS Console → Amplify → App → Hosting → Build logs

## Updating Deployment

### Backend Updates
```bash
cd backend
sam build
sam deploy
```

### Frontend Updates
```bash
cd frontend
npm run build
# Re-upload build folder to Amplify Console
```

## Rollback

### Backend
```bash
aws cloudformation delete-stack --stack-name auralis-backend
```

### Frontend
- Delete app from Amplify Console

## Success Checklist

- [ ] Backend deployed to Lambda
- [ ] API Gateway URL obtained
- [ ] Frontend updated with API URL
- [ ] Frontend built successfully
- [ ] Frontend deployed to Amplify
- [ ] Public URL obtained
- [ ] Full end-to-end test passed
- [ ] URLs documented in HACKATHON_JOURNAL.md
- [ ] Changes committed to GitHub
