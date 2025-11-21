#!/bin/bash

# Auralis Frontend Deployment Script for AWS Amplify
# This script builds and prepares the React frontend for deployment

set -e

echo "🚀 Starting Auralis Frontend Deployment..."

# Configuration
AMPLIFY_APP_ID="${AMPLIFY_APP_ID:-}"
AWS_REGION="${AWS_REGION:-us-east-1}"
ENVIRONMENT="${ENVIRONMENT:-production}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"

# Navigate to frontend directory
cd frontend

echo -e "${YELLOW}Installing dependencies...${NC}"
npm install --quiet

echo -e "${YELLOW}Building production bundle...${NC}"
npm run build

# Check build output
if [ ! -d "build" ]; then
    echo -e "${RED}❌ Build failed - no build directory created${NC}"
    exit 1
fi

BUILD_SIZE=$(du -sh build | cut -f1)
echo -e "${GREEN}✓ Build complete: $BUILD_SIZE${NC}"

# Create amplify.yml if it doesn't exist
if [ ! -f "amplify.yml" ]; then
    echo -e "${YELLOW}Creating amplify.yml configuration...${NC}"
    cat > amplify.yml << 'EOF'
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
  env:
    REACT_APP_API_URL: $API_URL
    REACT_APP_ENABLE_ANALYTICS: 'true'
EOF
fi

echo -e "${YELLOW}Build artifacts:${NC}"
echo "  Location: frontend/build"
echo "  Size: $BUILD_SIZE"
echo "  Files: $(find build -type f | wc -l)"

cd ..

echo -e "${GREEN}✓ Frontend build complete!${NC}"
echo ""
echo "Deployment options:"
echo ""
echo "Option 1: Deploy via AWS Amplify Console (Recommended)"
echo "  1. Go to https://console.aws.amazon.com/amplify"
echo "  2. Create a new app and connect your GitHub repository"
echo "  3. Configure build settings (use amplify.yml)"
echo "  4. Deploy"
echo ""
echo "Option 2: Deploy via AWS CLI"
if [ ! -z "$AMPLIFY_APP_ID" ]; then
    echo "  aws amplify start-deployment --app-id $AMPLIFY_APP_ID --branch-name main --region $AWS_REGION"
else
    echo "  Set AMPLIFY_APP_ID environment variable first"
fi
echo ""
echo "Option 3: Deploy to S3 + CloudFront"
echo "  aws s3 sync frontend/build s3://your-bucket-name/"
echo ""
