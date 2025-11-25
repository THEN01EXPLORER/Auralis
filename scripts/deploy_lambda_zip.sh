#!/usr/bin/env bash
set -euo pipefail

# deploy_lambda_zip.sh
# Enhanced deploy script for Auralis backend (zip packaging)
# Features:
# - CLI args and environment overrides
# - Optional Docker-based build for Linux-compatible wheels (--use-docker)
# - Optional API Gateway creation (--create-api)
# - Optional IAM role creation if permissions allow (--create-role)
#
# Usage examples:
#  ROLE_ARN=arn:aws:iam::123456789012:role/auralis-lambda-role ./scripts/deploy_lambda_zip.sh
#  ./scripts/deploy_lambda_zip.sh --use-docker --create-api

FUNCTION_NAME=auralis-backend
ROLE_ARN=""
REGION=us-east-1
TIMEOUT=60
MEMORY=1024
BEDROCK_MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"
ENABLE_AI_ANALYSIS=false
AI_ANALYSIS_REQUIRED=false
AWS_REGION="$REGION"
USE_DOCKER=false
CREATE_API=false
CREATE_ROLE=false
API_NAME="auralis-api"

print_help(){
  cat <<EOF
Usage: $0 [options]

Options:
  -f, --function-name NAME     Lambda function name (default: auralis-backend)
  -r, --role-arn ARN           IAM role ARN for Lambda (required unless --create-role)
  -R, --region REGION          AWS region (default: us-east-1)
  --timeout SECONDS            Lambda timeout in seconds (default: 60)
  --memory MB                  Lambda memory in MB (default: 1024)
  --enable-ai true|false       Enable AI analysis in Lambda env (default: false)
  --ai-required true|false     Treat AI as required (default: false)
  --use-docker                 Use Docker build (lambci image) for manylinux wheels
  --create-api                 Create an HTTP API and wire it to the Lambda
  --create-role                Attempt to create a Lambda IAM role (requires IAM permissions)
  -h, --help                   Show this help

Examples:
  ROLE_ARN=arn:aws:iam::123456789012:role/auralis-lambda-role \
    ./scripts/deploy_lambda_zip.sh --use-docker --create-api

EOF
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    -f|--function-name)
      FUNCTION_NAME="$2"; shift 2;;
    -r|--role-arn)
      ROLE_ARN="$2"; shift 2;;
    -R|--region)
      REGION="$2"; AWS_REGION="$2"; shift 2;;
    --timeout)
      TIMEOUT="$2"; shift 2;;
    --memory)
      MEMORY="$2"; shift 2;;
    --enable-ai)
      ENABLE_AI_ANALYSIS="$2"; shift 2;;
    --ai-required)
      AI_ANALYSIS_REQUIRED="$2"; shift 2;;
    --use-docker)
      USE_DOCKER=true; shift;;
    --create-api)
      CREATE_API=true; shift;;
    --create-role)
      CREATE_ROLE=true; shift;;
    -h|--help)
      print_help; exit 0;;
    *)
      echo "Unknown option: $1"; print_help; exit 1;;
  esac
done

echo "Deploying Lambda: $FUNCTION_NAME (region: $REGION)"

if [ "$CREATE_ROLE" = true ] && [ -z "$ROLE_ARN" ]; then
  echo "Attempting to create IAM role: auralis-lambda-role"
  cat > /tmp/auralis_lambda_trust.json <<'TRUST'
{ "Version": "2012-10-17", "Statement": [{ "Effect": "Allow", "Principal": { "Service": "lambda.amazonaws.com" }, "Action": "sts:AssumeRole" }] }
TRUST
  aws iam create-role --role-name auralis-lambda-role --assume-role-policy-document file:///tmp/auralis_lambda_trust.json || true
  aws iam attach-role-policy --role-name auralis-lambda-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole || true
  aws iam attach-role-policy --role-name auralis-lambda-role --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess || true
  ROLE_ARN=$(aws iam get-role --role-name auralis-lambda-role --query 'Role.Arn' --output text)
  echo "Created/using role: $ROLE_ARN"
fi

if [ -z "$ROLE_ARN" ]; then
  echo "ERROR: ROLE_ARN not provided. Export ROLE_ARN or pass --role-arn, or run with --create-role" >&2
fi

rm -rf build_package deployment.zip
mkdir -p build_package

build_with_docker(){
  echo "Building dependencies inside Docker (lambci image) for compatibility..."
  if ! command -v docker >/dev/null 2>&1; then
    echo "Docker not found. Install Docker or run without --use-docker."; exit 1
  fi

  # Use lambci build image to install manylinux compatible wheels
  docker run --rm -v "$PWD/backend":/var/task -w /var/task lambci/lambda:build-python3.11 /bin/sh -c \
    "python -m pip install --upgrade pip setuptools wheel && pip install -r requirements.txt -t /var/task/build_package"
}

build_locally(){
  echo "Installing dependencies locally into build_package..."
  python -m pip install --upgrade pip setuptools wheel
  python -m pip install -r backend/requirements.txt -t build_package || true
}

echo "Copying backend source files..."
cp -r backend/*.py build_package/ || true
cp -r backend/app build_package/app || true

if [ "$USE_DOCKER" = true ]; then
  build_with_docker
else
  build_locally
fi

pushd build_package >/dev/null
zip -r9 ../deployment.zip . >/dev/null
popd >/dev/null

if [ -n "$(aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" 2>/dev/null || true)" ]; then
  echo "Updating existing function code: $FUNCTION_NAME"
  aws lambda update-function-code --function-name "$FUNCTION_NAME" --zip-file fileb://deployment.zip --region "$REGION"
else
  if [ -z "$ROLE_ARN" ]; then
    echo "ERROR: Cannot create Lambda without ROLE_ARN."; exit 1
  fi
  echo "Creating function: $FUNCTION_NAME"
  aws lambda create-function \
    --function-name "$FUNCTION_NAME" \
    --runtime python3.11 \
    --handler main.handler \
    --role "$ROLE_ARN" \
    --zip-file fileb://deployment.zip \
    --timeout $TIMEOUT \
    --memory-size $MEMORY \
    --region "$REGION"
fi

echo "Updating function configuration (env vars)..."
aws lambda update-function-configuration --function-name "$FUNCTION_NAME" --region "$REGION" \
  --environment "Variables={ENABLE_AI_ANALYSIS=$ENABLE_AI_ANALYSIS,AI_ANALYSIS_REQUIRED=$AI_ANALYSIS_REQUIRED,AWS_REGION=$AWS_REGION,BEDROCK_MODEL_ID=$BEDROCK_MODEL_ID,LOG_LEVEL=INFO}"

rm -rf build_package deployment.zip

echo "Lambda $FUNCTION_NAME deployed/updated in region $REGION."

if [ "$CREATE_API" = true ]; then
  echo "Creating HTTP API and wiring to Lambda..."
  ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
  API_ID=$(aws apigatewayv2 create-api --name "$API_NAME" --protocol-type HTTP --query ApiId --output text --region "$REGION")
  INTEGRATION_ID=$(aws apigatewayv2 create-integration --api-id $API_ID --integration-type AWS_PROXY --integration-uri "arn:aws:lambda:$REGION:$ACCOUNT_ID:function:$FUNCTION_NAME" --payload-format-version "2.0" --query IntegrationId --output text --region "$REGION")
  aws apigatewayv2 create-route --api-id $API_ID --route-key "ANY /{proxy+}" --target "integrations/$INTEGRATION_ID" --region "$REGION"
  aws apigatewayv2 create-stage --api-id $API_ID --stage-name prod --auto-deploy --region "$REGION"
  aws lambda add-permission --function-name $FUNCTION_NAME --statement-id apigw-invoke-$API_ID --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:$REGION:$ACCOUNT_ID:$API_ID/*/*/*" || true
  API_URL="https://${API_ID}.execute-api.${REGION}.amazonaws.com/prod"
  echo "API URL: $API_URL"
  echo "Set this as REACT_APP_API_URL in Amplify or your frontend environment." 
fi

echo "Next steps: (1) create API Gateway if not already, (2) add REACT_APP_API_URL to Amplify, (3) test endpoints."
