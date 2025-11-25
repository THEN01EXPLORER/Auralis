#!/usr/bin/env bash
set -euo pipefail

# deploy_vercel.sh
# Deploy Auralis frontend to Vercel
# Prerequisites:
# - Node.js and npm installed
# - Vercel account (free tier)
# - Vercel CLI installed: npm i -g vercel

FRONTEND_DIR="frontend"
BACKEND_URL=${REACT_APP_API_URL:-""}

echo "Deploying Auralis frontend to Vercel..."

if ! command -v vercel >/dev/null 2>&1; then
  echo "Vercel CLI not found. Installing..."
  npm install -g vercel
fi

cd "$FRONTEND_DIR"

echo "Installing dependencies..."
npm install

echo "Building production bundle..."
npm run build

echo "Logging into Vercel (follow prompts)..."
vercel login

if [ -n "$BACKEND_URL" ]; then
  echo "Setting REACT_APP_API_URL=$BACKEND_URL"
  vercel env add REACT_APP_API_URL production <<< "$BACKEND_URL"
fi

echo "Deploying to production..."
vercel --prod

echo ""
echo "✅ Frontend deployed to Vercel!"
echo ""
echo "Next steps:"
echo "1. Note the production URL from the output above"
echo "2. Set REACT_APP_API_URL environment variable in Vercel dashboard:"
echo "   Go to: Project Settings > Environment Variables"
echo "   Add: REACT_APP_API_URL = <your-backend-url>"
echo "3. Redeploy or trigger a new build after setting the env var"
echo ""
echo "To update the deployment:"
echo "  cd $FRONTEND_DIR && vercel --prod"
