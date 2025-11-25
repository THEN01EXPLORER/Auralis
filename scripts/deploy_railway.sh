#!/usr/bin/env bash
set -euo pipefail

# deploy_railway.sh
# Deploy Auralis backend to Railway.app (No credit card required!)
# Prerequisites:
# - Railway account (free tier: https://railway.app/)
# - Railway CLI installed

BACKEND_DIR="backend"

echo "Deploying Auralis backend to Railway.app..."

# Check if railway CLI is installed
if ! command -v railway >/dev/null 2>&1; then
  echo "Railway CLI not found. Installing..."
  npm install -g @railway/cli
fi

cd "$BACKEND_DIR"

# Login to Railway
if ! railway whoami >/dev/null 2>&1; then
  echo "Logging into Railway..."
  railway login
fi

# Initialize project
echo "Initializing Railway project..."
railway init

# Set environment variables
echo "Setting environment variables..."
railway variables set ENABLE_AI_ANALYSIS=false
railway variables set AI_ANALYSIS_REQUIRED=false
railway variables set AWS_REGION=us-east-1
railway variables set BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
railway variables set LOG_LEVEL=INFO
railway variables set PORT=8080

# Deploy
echo "Deploying to Railway..."
railway up

# Get deployment URL
echo ""
echo "✅ Backend deployed to Railway!"
echo ""
echo "Get your backend URL:"
echo "  railway domain"
echo ""
echo "Or view in dashboard:"
echo "  railway open"
echo ""
echo "Next steps:"
echo "1. Get your Railway URL: railway domain"
echo "2. Update REACT_APP_API_URL in Vercel to your Railway URL"
echo "3. Test: curl https://your-app.railway.app/health"
