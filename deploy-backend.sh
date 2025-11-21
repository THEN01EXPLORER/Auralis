#!/bin/bash

# Auralis Backend Deployment Script for AWS Lambda
# This script packages the FastAPI backend for deployment to AWS Lambda

set -e

echo "🚀 Starting Auralis Backend Deployment..."

# Configuration
LAMBDA_FUNCTION_NAME="${LAMBDA_FUNCTION_NAME:-auralis-api}"
AWS_REGION="${AWS_REGION:-us-east-1}"
DEPLOYMENT_BUCKET="${DEPLOYMENT_BUCKET:-auralis-deployments}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI is not installed${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

if ! command -v zip &> /dev/null; then
    echo -e "${RED}❌ zip is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"

# Create deployment directory
DEPLOY_DIR="lambda_deployment"
if [ -d "$DEPLOY_DIR" ]; then
    echo "Cleaning up previous deployment..."
    rm -rf "$DEPLOY_DIR"
fi

mkdir -p "$DEPLOY_DIR/package"
cd "$DEPLOY_DIR/package"

echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r ../../backend/requirements.txt -t . --quiet

echo -e "${YELLOW}Copying application code...${NC}"
cp -r ../../backend/app .
cp ../../backend/main.py .
cp ../../backend/config.py .
cp ../../backend/database.py .
cp ../../backend/dependencies.py .
cp ../../backend/schemas.py .
cp ../../backend/models.py .
cp ../../backend/tasks.py .
cp ../../backend/celery_app.py .

# Create Lambda handler wrapper if it doesn't exist
if [ ! -f "lambda_handler.py" ]; then
    echo -e "${YELLOW}Creating Lambda handler wrapper...${NC}"
    cat > lambda_handler.py << 'EOF'
from mangum import Mangum
from main import app

handler = Mangum(app)
EOF
fi

echo -e "${YELLOW}Creating deployment package...${NC}"
cd ..
zip -r auralis-backend-deployment.zip package/ -q

cd ..

# Get file size
FILE_SIZE=$(du -h "$DEPLOY_DIR/auralis-backend-deployment.zip" | cut -f1)
echo -e "${GREEN}✓ Deployment package created: $FILE_SIZE${NC}"

# Upload to S3 if bucket is specified
if [ ! -z "$DEPLOYMENT_BUCKET" ]; then
    echo -e "${YELLOW}Uploading to S3...${NC}"
    aws s3 cp "$DEPLOY_DIR/auralis-backend-deployment.zip" \
        "s3://$DEPLOYMENT_BUCKET/auralis-backend-$(date +%Y%m%d-%H%M%S).zip" \
        --region "$AWS_REGION" || echo -e "${YELLOW}⚠ S3 upload skipped (bucket may not exist)${NC}"
fi

# Update Lambda function if it exists
echo -e "${YELLOW}Checking for existing Lambda function...${NC}"
if aws lambda get-function --function-name "$LAMBDA_FUNCTION_NAME" --region "$AWS_REGION" &> /dev/null; then
    echo -e "${YELLOW}Updating Lambda function code...${NC}"
    aws lambda update-function-code \
        --function-name "$LAMBDA_FUNCTION_NAME" \
        --zip-file "fileb://$DEPLOY_DIR/auralis-backend-deployment.zip" \
        --region "$AWS_REGION" > /dev/null
    echo -e "${GREEN}✓ Lambda function updated${NC}"
else
    echo -e "${YELLOW}⚠ Lambda function '$LAMBDA_FUNCTION_NAME' not found${NC}"
    echo "To create the function, use:"
    echo "  aws lambda create-function --function-name $LAMBDA_FUNCTION_NAME \\"
    echo "    --runtime python3.11 --role <IAM_ROLE_ARN> \\"
    echo "    --handler lambda_handler.handler \\"
    echo "    --zip-file fileb://$DEPLOY_DIR/auralis-backend-deployment.zip \\"
    echo "    --timeout 30 --memory-size 1024 \\"
    echo "    --region $AWS_REGION"
fi

echo -e "${GREEN}✓ Backend deployment complete!${NC}"
echo ""
echo "Deployment package: $DEPLOY_DIR/auralis-backend-deployment.zip"
echo "Size: $FILE_SIZE"
echo ""
echo "Next steps:"
echo "1. Configure environment variables in Lambda console"
echo "2. Set up API Gateway trigger"
echo "3. Test the endpoint"
echo ""
