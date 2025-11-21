# Auralis Quick Reference

Fast lookup for common tasks and commands.

## 🚀 Quick Start

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

### Run Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Deploy Backend to Lambda

```bash
chmod +x deploy-backend.sh
./deploy-backend.sh
```

### Deploy Frontend to Amplify

```bash
chmod +x deploy-frontend.sh
./deploy-frontend.sh
```

### Verify Deployment

```bash
chmod +x scripts/verify-deployment.sh
API_ENDPOINT=https://your-endpoint scripts/verify-deployment.sh
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**:
```env
AWS_REGION=us-east-1
ENABLE_AI_ANALYSIS=true
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
LOG_LEVEL=INFO
RATE_LIMIT_PER_MINUTE=60
ALLOWED_ORIGINS=http://localhost:3000
```

**Frontend (.env)**:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENABLE_ANALYTICS=true
```

## 📡 API Endpoints

### Analyze Contract
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "pragma solidity ^0.8.0; contract Test {}"}'
```

### Analyze Repository
```bash
curl -X POST http://localhost:8000/api/v1/analyze_repo \
  -H "Content-Type: application/json" \
  -d '{"github_url": "https://github.com/user/repo"}'
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 🐛 Debugging

### Check Logs

```bash
# Backend
tail -f backend.log

# AWS Lambda
aws logs tail /aws/lambda/auralis-api --follow

# Browser console
# Press F12
```

### Test Endpoints

```bash
# Health
curl http://localhost:8000/health

# Analyze
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "test"}'
```

## 📊 Monitoring

### CloudWatch Logs

```bash
# View logs
aws logs tail /aws/lambda/auralis-api --follow

# Get metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=auralis-api \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average
```

## 🔐 AWS Setup

### Create IAM Role

```bash
aws iam create-role \
  --role-name auralis-lambda-role \
  --assume-role-policy-document file://trust-policy.json
```

### Create Lambda Function

```bash
aws lambda create-function \
  --function-name auralis-api \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT_ID:role/auralis-lambda-role \
  --handler lambda_handler.handler \
  --zip-file fileb://lambda_deployment/auralis-backend-deployment.zip
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| DEPLOYMENT_GUIDE.md | Step-by-step AWS deployment |
| API_DOCUMENTATION.md | Complete API reference |
| TROUBLESHOOTING.md | Common issues and solutions |
| AURALIS_COMPLETION_SUMMARY.md | Project completion status |

## 🧪 Testing

### Run All Tests

```bash
# Backend
cd backend
pytest tests/ -v --cov

# Frontend
cd frontend
npm test
```

### Run Specific Test

```bash
# Backend
pytest tests/test_rate_limiting.py -v

# Frontend
npm test -- ErrorBoundary.test.js
```

## 🎯 Common Tasks

### Update Lambda Function

```bash
aws lambda update-function-code \
  --function-name auralis-api \
  --zip-file fileb://lambda_deployment/auralis-backend-deployment.zip
```

### Update Environment Variables

```bash
aws lambda update-function-configuration \
  --function-name auralis-api \
  --environment Variables="{KEY=value}"
```

### View Lambda Logs

```bash
aws logs tail /aws/lambda/auralis-api --follow
```

### Increase Lambda Timeout

```bash
aws lambda update-function-configuration \
  --function-name auralis-api \
  --timeout 60
```

### Increase Lambda Memory

```bash
aws lambda update-function-configuration \
  --function-name auralis-api \
  --memory-size 2048
```

## 🚨 Troubleshooting

### Port Already in Use

```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Module Not Found

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### CORS Error

```bash
# Update ALLOWED_ORIGINS
export ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
```

### Rate Limited

```bash
# Wait 60 seconds or increase limit
export RATE_LIMIT_PER_MINUTE=120
```

## 📈 Performance

### Expected Times

| Operation | Time |
|-----------|------|
| Health check | <100ms |
| Simple contract | 2-5s |
| Complex contract | 5-15s |
| Repository (3 files) | 15-30s |
| PDF generation | 2-5s |

### Optimize

```bash
# Increase Lambda memory (more CPU)
aws lambda update-function-configuration \
  --function-name auralis-api \
  --memory-size 2048

# Increase timeout
aws lambda update-function-configuration \
  --function-name auralis-api \
  --timeout 60
```

## 💰 Cost Estimation

| Service | Cost |
|---------|------|
| Lambda | $0.20 per 1M requests |
| Bedrock | $0.003 per 1K input tokens |
| API Gateway | $3.50 per 1M requests |
| Amplify | $0.01 per GB served |
| CloudWatch | $5-10/month |
| **Total** | **~$50-100/month** |

## 🔗 Useful Links

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS Amplify Documentation](https://docs.aws.amazon.com/amplify/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## 📞 Support

1. Check TROUBLESHOOTING.md
2. Review CloudWatch logs
3. Check API_DOCUMENTATION.md
4. Review code comments
5. Check test files for examples

## ⚡ Pro Tips

1. **Use AWS CLI aliases** for faster commands
2. **Monitor costs** with CloudWatch alarms
3. **Cache results** to reduce API calls
4. **Use provisioned concurrency** for consistent performance
5. **Set up auto-scaling** for high traffic
6. **Enable X-Ray** for detailed tracing
7. **Use Lambda layers** for shared dependencies

## 🎓 Learning Resources

- DEPLOYMENT_GUIDE.md - Learn AWS deployment
- API_DOCUMENTATION.md - Learn API usage
- TROUBLESHOOTING.md - Learn debugging
- Test files - Learn testing patterns
- Code comments - Learn implementation

---

**Last Updated**: November 17, 2025
**Version**: 1.0.0
