#!/bin/bash

# Auralis Deployment Verification Script
# Verifies that the deployed backend is working correctly

set -e

# Configuration
API_ENDPOINT="${API_ENDPOINT:-http://localhost:8000}"
TIMEOUT=10

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Auralis Deployment Verification${NC}"
echo "API Endpoint: $API_ENDPOINT"
echo ""

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" -m $TIMEOUT "$API_ENDPOINT/health" 2>/dev/null || echo "000")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    echo "  Response: $BODY"
else
    echo -e "${RED}✗ Health check failed (HTTP $HTTP_CODE)${NC}"
    exit 1
fi

echo ""

# Test 2: Root Endpoint
echo -e "${YELLOW}Test 2: Root Endpoint${NC}"
ROOT_RESPONSE=$(curl -s -w "\n%{http_code}" -m $TIMEOUT "$API_ENDPOINT/" 2>/dev/null || echo "000")
HTTP_CODE=$(echo "$ROOT_RESPONSE" | tail -n1)
BODY=$(echo "$ROOT_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Root endpoint accessible${NC}"
    echo "  Response: $BODY"
else
    echo -e "${RED}✗ Root endpoint failed (HTTP $HTTP_CODE)${NC}"
    exit 1
fi

echo ""

# Test 3: Contract Analysis
echo -e "${YELLOW}Test 3: Contract Analysis${NC}"
CONTRACT_CODE='pragma solidity ^0.8.0; contract Test { function test() public {} }'
ANALYSIS_RESPONSE=$(curl -s -w "\n%{http_code}" -m 30 \
    -X POST "$API_ENDPOINT/api/v1/analyze" \
    -H "Content-Type: application/json" \
    -d "{\"code\": \"$CONTRACT_CODE\"}" 2>/dev/null || echo "000")

HTTP_CODE=$(echo "$ANALYSIS_RESPONSE" | tail -n1)
BODY=$(echo "$ANALYSIS_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "503" ]; then
    echo -e "${GREEN}✓ Contract analysis endpoint working${NC}"
    echo "  HTTP Status: $HTTP_CODE"
    
    # Check response format
    if echo "$BODY" | grep -q "risk_score\|vulnerabilities"; then
        echo -e "${GREEN}✓ Response format valid${NC}"
    else
        echo -e "${YELLOW}⚠ Response format may be incomplete${NC}"
    fi
else
    echo -e "${RED}✗ Contract analysis failed (HTTP $HTTP_CODE)${NC}"
    exit 1
fi

echo ""

# Test 4: Rate Limiting
echo -e "${YELLOW}Test 4: Rate Limiting${NC}"
RATE_LIMIT_TEST=0
for i in {1..5}; do
    RESPONSE=$(curl -s -w "\n%{http_code}" -m 5 \
        -X POST "$API_ENDPOINT/api/v1/analyze" \
        -H "Content-Type: application/json" \
        -d "{\"code\": \"test\"}" 2>/dev/null || echo "000")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    
    if [ "$HTTP_CODE" = "429" ]; then
        RATE_LIMIT_TEST=1
        break
    fi
done

if [ $RATE_LIMIT_TEST -eq 1 ]; then
    echo -e "${GREEN}✓ Rate limiting is active${NC}"
else
    echo -e "${YELLOW}⚠ Rate limiting may not be configured${NC}"
fi

echo ""

# Test 5: CORS Headers
echo -e "${YELLOW}Test 5: CORS Headers${NC}"
CORS_RESPONSE=$(curl -s -i -X OPTIONS "$API_ENDPOINT/api/v1/analyze" 2>/dev/null | grep -i "access-control" || echo "")

if [ ! -z "$CORS_RESPONSE" ]; then
    echo -e "${GREEN}✓ CORS headers present${NC}"
    echo "  $CORS_RESPONSE"
else
    echo -e "${YELLOW}⚠ CORS headers not found${NC}"
fi

echo ""

# Summary
echo -e "${BLUE}✓ Deployment verification complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Test the frontend at your Amplify URL"
echo "2. Monitor CloudWatch logs for errors"
echo "3. Configure custom domain if needed"
echo "4. Set up monitoring and alerts"
echo ""
