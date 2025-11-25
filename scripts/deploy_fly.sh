#!/usr/bin/env bash
set -euo pipefail

# deploy_fly.sh
# Deploy Auralis backend to Fly.io
# Prerequisites:
# - Fly.io account (free tier: https://fly.io/signup)
# - flyctl CLI installed (see below)

BACKEND_DIR="backend"
APP_NAME="auralis-backend"
REGION="syd"  # Change to your preferred region (run: flyctl platform regions)

echo "Deploying Auralis backend to Fly.io..."

# Check if flyctl is installed
if ! command -v flyctl >/dev/null 2>&1; then
  echo "flyctl not found. Installing..."
  echo "Please follow the installation instructions at: https://fly.io/docs/hands-on/install-flyctl/"
  echo ""
  echo "Quick install:"
  echo "  macOS/Linux: curl -L https://fly.io/install.sh | sh"
  echo "  Windows: iwr https://fly.io/install.ps1 -useb | iex"
  echo ""
  exit 1
fi

cd "$BACKEND_DIR"

# Check if already logged in
if ! flyctl auth whoami >/dev/null 2>&1; then
  echo "Logging into Fly.io..."
  flyctl auth login
fi

# Check if app exists
if ! flyctl apps list | grep -q "$APP_NAME"; then
  echo "Creating new Fly.io app: $APP_NAME"
  flyctl launch --name "$APP_NAME" --region "$REGION" --no-deploy
else
  echo "App $APP_NAME already exists, updating..."
fi

# Set environment variables (secrets)
echo "Setting environment variables..."
flyctl secrets set \
  ENABLE_AI_ANALYSIS=false \
  AI_ANALYSIS_REQUIRED=false \
  AWS_REGION=us-east-1 \
  BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0 \
  LOG_LEVEL=INFO

# Deploy
echo "Deploying to Fly.io..."
flyctl deploy

# Get the app URL
APP_URL=$(flyctl info --json | grep -o '"Hostname":"[^"]*"' | cut -d'"' -f4)
if [ -z "$APP_URL" ]; then
  APP_URL="$APP_NAME.fly.dev"
fi

echo ""
echo "✅ Backend deployed to Fly.io!"
echo ""
echo "Backend URL: https://$APP_URL"
echo ""
echo "Next steps:"
echo "1. Test your backend:"
echo "   curl https://$APP_URL/health"
echo ""
echo "2. Update frontend REACT_APP_API_URL:"
echo "   Go to Vercel dashboard → Your project → Settings → Environment Variables"
echo "   Update REACT_APP_API_URL to: https://$APP_URL"
echo "   Then redeploy the frontend"
echo ""
echo "3. View logs:"
echo "   flyctl logs"
echo ""
echo "To update the deployment:"
echo "  cd $BACKEND_DIR && flyctl deploy"
