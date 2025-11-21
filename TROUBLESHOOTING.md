# Auralis Troubleshooting Guide

Common issues and solutions for Auralis deployment and usage.

## Table of Contents

1. [Backend Issues](#backend-issues)
2. [Frontend Issues](#frontend-issues)
3. [AWS Deployment Issues](#aws-deployment-issues)
4. [Analysis Issues](#analysis-issues)
5. [Performance Issues](#performance-issues)

---

## Backend Issues

### Issue: "ModuleNotFoundError: No module named 'app'"

**Cause**: Python path not configured correctly

**Solution**:
```bash
# Ensure you're in the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run with correct path
python main.py
```

### Issue: "AWS credentials not found"

**Cause**: AWS credentials not configured

**Solution**:
```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
```

### Issue: "Bedrock model not found"

**Cause**: Model ID incorrect or Bedrock not enabled

**Solution**:
1. Verify model ID in environment variables
2. Check Bedrock is enabled in your AWS region
3. Request access to Claude 3 Sonnet model
4. Wait for approval (usually instant)

```bash
# Check available models
aws bedrock list-foundation-models --region us-east-1
```

### Issue: "Port 8000 already in use"

**Cause**: Another process using the port

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn main:app --port 8001
```

### Issue: "CORS error when calling from frontend"

**Cause**: CORS not configured correctly

**Solution**:
```bash
# Update ALLOWED_ORIGINS environment variable
export ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com

# Or in .env file
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
```

### Issue: "Rate limit exceeded (429)"

**Cause**: Too many requests from same IP

**Solution**:
```bash
# Wait for rate limit to reset (60 seconds)
# Or increase rate limit in environment
export RATE_LIMIT_PER_MINUTE=120

# Check current rate limit
curl -i http://localhost:8000/health
# Look for X-RateLimit-* headers
```

---

## Frontend Issues

### Issue: "Cannot find module 'react-router-dom'"

**Cause**: Dependencies not installed

**Solution**:
```bash
cd frontend
npm install
npm start
```

### Issue: "API endpoint not responding"

**Cause**: Backend not running or wrong URL

**Solution**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Check API URL in frontend code
3. Check CORS configuration
4. Check firewall/network settings

### Issue: "Blank page or white screen"

**Cause**: JavaScript error or build issue

**Solution**:
```bash
# Check browser console for errors (F12)
# Clear cache and rebuild
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Issue: "Code editor not working"

**Cause**: CodeMirror library not loaded

**Solution**:
```bash
# Reinstall dependencies
npm install

# Check browser console for errors
# Verify @uiw/react-codemirror is installed
npm list @uiw/react-codemirror
```

### Issue: "Results not displaying"

**Cause**: API response format mismatch

**Solution**:
1. Check API response in browser Network tab
2. Verify response matches expected format
3. Check for API errors (4xx, 5xx status codes)
4. Check browser console for JavaScript errors

---

## AWS Deployment Issues

### Issue: "Lambda function timeout"

**Cause**: Analysis taking too long

**Solution**:
```bash
# Increase timeout (max 15 minutes)
aws lambda update-function-configuration \
  --function-name auralis-api \
  --timeout 60

# Increase memory (more CPU)
aws lambda update-function-configuration \
  --function-name auralis-api \
  --memory-size 2048
```

### Issue: "Lambda cold start too slow"

**Cause**: First invocation takes time to initialize

**Solution**:
1. Increase memory allocation (improves CPU)
2. Use Lambda provisioned concurrency
3. Optimize dependencies (remove unused packages)
4. Use Lambda layers for common dependencies

```bash
# Increase memory
aws lambda update-function-configuration \
  --function-name auralis-api \
  --memory-size 2048
```

### Issue: "API Gateway 502 Bad Gateway"

**Cause**: Lambda function error or timeout

**Solution**:
1. Check CloudWatch logs
2. Check Lambda function configuration
3. Verify IAM permissions
4. Test Lambda directly

```bash
# Check logs
aws logs tail /aws/lambda/auralis-api --follow

# Test Lambda
aws lambda invoke \
  --function-name auralis-api \
  --payload '{"body": "{\"code\": \"test\"}"}' \
  response.json
```

### Issue: "Amplify deployment failed"

**Cause**: Build error or configuration issue

**Solution**:
1. Check Amplify build logs
2. Verify amplify.yml configuration
3. Check environment variables
4. Verify GitHub permissions

```bash
# Check build logs in Amplify Console
# Or redeploy manually
git push origin main
```

### Issue: "CORS errors in production"

**Cause**: ALLOWED_ORIGINS not configured for production domain

**Solution**:
```bash
# Update Lambda environment variable
aws lambda update-function-configuration \
  --function-name auralis-api \
  --environment Variables="{
    ALLOWED_ORIGINS=https://your-amplify-url.amplifyapp.com
  }"
```

### Issue: "High AWS costs"

**Cause**: Excessive Lambda invocations or Bedrock usage

**Solution**:
1. Monitor CloudWatch metrics
2. Implement caching
3. Optimize Bedrock prompts
4. Set up cost alerts

```bash
# Set up cost alert
aws budgets create-budget \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --budget file://budget.json
```

---

## Analysis Issues

### Issue: "No vulnerabilities detected"

**Cause**: Contract is secure or analysis not working

**Solution**:
1. Test with known vulnerable contract
2. Check analysis method (static vs hybrid)
3. Verify AI analysis is enabled
4. Check CloudWatch logs for errors

```bash
# Test with vulnerable contract
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "pragma solidity ^0.8.0; contract Test { function test() public payable { msg.sender.call{value: msg.value}(\"\"); } }"
  }'
```

### Issue: "False positives in results"

**Cause**: Static analyzer too aggressive

**Solution**:
1. Review vulnerability descriptions
2. Check confidence scores
3. Use AI analysis for context
4. Report false positives

### Issue: "Repository analysis fails"

**Cause**: Invalid GitHub URL or access issues

**Solution**:
1. Verify GitHub URL is correct
2. Check repository is public
3. Check network connectivity
4. Check file size limits

```bash
# Test GitHub access
git clone https://github.com/username/repo --depth 1
```

### Issue: "Analysis takes too long"

**Cause**: Large contract or slow AI response

**Solution**:
1. Increase Lambda timeout
2. Increase Lambda memory
3. Optimize contract code
4. Use static analysis only

```bash
# Disable AI analysis for faster results
export ENABLE_AI_ANALYSIS=false
```

---

## Performance Issues

### Issue: "Slow API response times"

**Cause**: Lambda cold start or slow analysis

**Solution**:
1. Increase Lambda memory
2. Use provisioned concurrency
3. Optimize code
4. Check CloudWatch metrics

```bash
# Check performance metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=auralis-api \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average,Maximum
```

### Issue: "Frontend loads slowly"

**Cause**: Large bundle size or slow network

**Solution**:
```bash
# Analyze bundle size
cd frontend
npm run build
npm install -g serve
serve -s build

# Check bundle size
npm run build -- --analyze
```

### Issue: "Database queries slow"

**Cause**: Missing indexes or inefficient queries

**Solution**:
1. Add database indexes
2. Optimize queries
3. Use caching
4. Monitor query performance

---

## Debugging Tips

### Enable Debug Logging

```bash
# Backend
export LOG_LEVEL=DEBUG
python main.py

# Frontend
export REACT_APP_DEBUG=true
npm start
```

### Check Logs

```bash
# Backend logs
tail -f backend.log

# AWS Lambda logs
aws logs tail /aws/lambda/auralis-api --follow

# Browser console
# Press F12 in browser
```

### Test Endpoints

```bash
# Test health
curl http://localhost:8000/health

# Test analyze
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "pragma solidity ^0.8.0; contract Test {}"}'

# Test with verbose output
curl -v http://localhost:8000/health
```

### Monitor Resources

```bash
# CPU and memory usage
top

# Network connections
netstat -an | grep 8000

# Disk usage
df -h
```

---

## Getting Help

1. **Check Logs**: Always check logs first
2. **Search Issues**: Look for similar issues on GitHub
3. **Read Documentation**: Check README and API docs
4. **Test Locally**: Reproduce issue locally first
5. **Provide Details**: Include logs, error messages, and steps to reproduce

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "ModuleNotFoundError" | Missing dependency | `pip install -r requirements.txt` |
| "Connection refused" | Service not running | Start backend/frontend |
| "CORS error" | Wrong origin | Update ALLOWED_ORIGINS |
| "Rate limit exceeded" | Too many requests | Wait or increase limit |
| "Bedrock error" | AWS issue | Check credentials and permissions |
| "Timeout" | Analysis too slow | Increase timeout or memory |
| "Out of memory" | Insufficient resources | Increase Lambda memory |

---

## Performance Benchmarks

Expected performance on standard configuration:

| Operation | Time | Notes |
|-----------|------|-------|
| Health check | <100ms | No analysis |
| Simple contract | 2-5s | Static only |
| Complex contract | 5-15s | With AI analysis |
| Repository (3 files) | 15-30s | Parallel processing |
| PDF generation | 2-5s | After analysis |

---

## Still Having Issues?

1. Check this guide again
2. Review CloudWatch logs
3. Check GitHub issues
4. Open a new issue with:
   - Error message
   - Steps to reproduce
   - Logs/screenshots
   - Environment details
