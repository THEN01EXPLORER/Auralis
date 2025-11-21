# Auralis API Documentation

Complete API reference for the Auralis smart contract security auditor.

## Base URL

```
Production: https://your-api-endpoint.execute-api.us-east-1.amazonaws.com/prod
Development: http://localhost:8000
```

## Authentication

Currently, Auralis API does not require authentication. Rate limiting is applied per IP address.

## Rate Limiting

- **Analyze Contract**: 60 requests/minute
- **Analyze Repository**: 10 requests/minute
- **DREAD Score**: 60 requests/minute
- **Generate Report**: 30 requests/minute
- **Health Check**: Unlimited

Rate limit headers:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Unix timestamp when limit resets
- `Retry-After`: Seconds to wait before retrying (on 429 response)

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "ok"
}
```

**Status Code**: 200

---

### 2. Root Endpoint

Get API information.

**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "Auralis API",
  "status": "running"
}
```

**Status Code**: 200

---

### 3. Analyze Contract

Analyze a single smart contract for vulnerabilities.

**Endpoint**: `POST /api/v1/analyze`

**Rate Limit**: 60 requests/minute

**Request Body**:
```json
{
  "code": "pragma solidity ^0.8.0;\ncontract Test { ... }"
}
```

**Response** (200 OK):
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "risk_score": 75,
  "vulnerabilities": [
    {
      "type": "Re-entrancy Attack",
      "line": 14,
      "severity": "Critical",
      "confidence": 95,
      "description": "External call detected before state changes...",
      "recommendation": "Use Checks-Effects-Interactions pattern",
      "remediation": {
        "explanation": "Reorder operations to prevent re-entrancy...",
        "code_example": "// Fixed code example..."
      }
    }
  ],
  "summary": "Contract has 1 critical vulnerability",
  "analysis_method": "hybrid",
  "ai_available": true,
  "processing_time_ms": 2500
}
```

**Response** (503 Service Unavailable):
```json
{
  "detail": "AI analysis is required but not available..."
}
```

**Response** (429 Too Many Requests):
```json
{
  "error": "Rate limit exceeded",
  "detail": "Too many requests. Please try again later.",
  "retry_after": 60
}
```

**Parameters**:
- `code` (string, required): Solidity contract source code

**Response Fields**:
- `analysis_id` (string): Unique identifier for this analysis
- `risk_score` (integer): Overall risk score (0-100)
- `vulnerabilities` (array): List of detected vulnerabilities
- `summary` (string): Human-readable summary
- `analysis_method` (string): "static", "ai", or "hybrid"
- `ai_available` (boolean): Whether AI analysis was used
- `processing_time_ms` (integer): Time taken in milliseconds

---

### 4. Analyze Repository

Analyze all Solidity files in a GitHub repository.

**Endpoint**: `POST /api/v1/analyze_repo`

**Rate Limit**: 10 requests/minute

**Request Body**:
```json
{
  "github_url": "https://github.com/username/repository"
}
```

**Response** (200 OK):
```json
{
  "repository_url": "https://github.com/username/repository",
  "files_analyzed": 3,
  "total_vulnerabilities": 5,
  "processing_time_ms": 15000,
  "results": {
    "contracts/Token.sol": {
      "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
      "risk_score": 85,
      "vulnerabilities": [...],
      "summary": "...",
      "analysis_method": "hybrid",
      "ai_available": true,
      "processing_time_ms": 5000
    },
    "contracts/Staking.sol": {
      "analysis_id": "550e8400-e29b-41d4-a716-446655440001",
      "risk_score": 45,
      "vulnerabilities": [...],
      "summary": "...",
      "analysis_method": "hybrid",
      "ai_available": true,
      "processing_time_ms": 4500
    }
  }
}
```

**Response** (400 Bad Request):
```json
{
  "detail": "Failed to clone repository. Please check the URL..."
}
```

**Response** (404 Not Found):
```json
{
  "detail": "No Solidity (.sol) files found in the repository"
}
```

**Parameters**:
- `github_url` (string, required): GitHub repository URL

**Response Fields**:
- `repository_url` (string): The analyzed repository URL
- `files_analyzed` (integer): Number of Solidity files found
- `total_vulnerabilities` (integer): Total vulnerabilities across all files
- `processing_time_ms` (integer): Total time taken
- `results` (object): Analysis results keyed by filename

---

### 5. Calculate DREAD Score

Calculate DREAD risk scores for a contract.

**Endpoint**: `POST /api/v1/dread_score`

**Rate Limit**: 60 requests/minute

**Request Body**:
```json
{
  "code": "pragma solidity ^0.8.0;\ncontract Test { ... }"
}
```

**Response** (200 OK):
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "risk_score": 75,
  "dread_scores": {
    "damage_potential": 8,
    "reproducibility": 7,
    "exploitability": 6,
    "affected_users": 9,
    "discoverability": 5,
    "overall": 7
  },
  "vulnerabilities_count": 3
}
```

**Parameters**:
- `code` (string, required): Solidity contract source code

**Response Fields**:
- `analysis_id` (string): Unique identifier for this analysis
- `risk_score` (integer): Overall risk score
- `dread_scores` (object): DREAD scoring breakdown
- `vulnerabilities_count` (integer): Number of vulnerabilities found

**DREAD Scoring**:
- **Damage Potential** (1-10): How much damage if exploited
- **Reproducibility** (1-10): How easy to reproduce
- **Exploitability** (1-10): How easy to exploit
- **Affected Users** (1-10): How many users affected
- **Discoverability** (1-10): How easy to discover
- **Overall**: Average of all scores

---

### 6. Generate Report

Generate a PDF audit report for a contract.

**Endpoint**: `POST /api/v1/generate_report`

**Rate Limit**: 30 requests/minute

**Request Body**:
```json
{
  "code": "pragma solidity ^0.8.0;\ncontract Test { ... }"
}
```

**Response** (200 OK):
```
[Binary PDF content]
```

**Headers**:
- `Content-Type`: application/pdf
- `Content-Disposition`: attachment; filename="auralis_audit_[id].pdf"

**Response** (503 Service Unavailable):
```json
{
  "detail": "PDF generation not available. Install reportlab..."
}
```

**Parameters**:
- `code` (string, required): Solidity contract source code

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request format or missing required fields"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "detail": "Too many requests. Please try again later.",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error during analysis"
}
```

### 503 Service Unavailable
```json
{
  "detail": "AI analysis is required but not available"
}
```

## Vulnerability Object

```json
{
  "type": "Re-entrancy Attack",
  "line": 14,
  "severity": "Critical",
  "confidence": 95,
  "description": "External call detected before state changes...",
  "recommendation": "Use Checks-Effects-Interactions pattern",
  "source": "hybrid",
  "remediation": {
    "explanation": "Reorder operations to prevent re-entrancy...",
    "code_example": "// Fixed code example..."
  }
}
```

**Fields**:
- `type` (string): Vulnerability type
- `line` (integer): Line number in source code
- `severity` (string): "Critical", "High", "Medium", or "Low"
- `confidence` (integer): Confidence score (0-100)
- `description` (string): Detailed description
- `recommendation` (string): How to fix
- `source` (string): "static", "ai", or "hybrid"
- `remediation` (object, optional): Code fix example

## Severity Levels

| Level | Description | CVSS Score |
|-------|-------------|-----------|
| Critical | Immediate exploitation risk | 9.0-10.0 |
| High | Significant security impact | 7.0-8.9 |
| Medium | Moderate security impact | 4.0-6.9 |
| Low | Minor security impact | 0.1-3.9 |

## Examples

### Example 1: Analyze a Simple Contract

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "pragma solidity ^0.8.0;\ncontract Test {\n  function test() public {}\n}"
  }'
```

### Example 2: Analyze a Repository

```bash
curl -X POST http://localhost:8000/api/v1/analyze_repo \
  -H "Content-Type: application/json" \
  -d '{
    "github_url": "https://github.com/OpenZeppelin/openzeppelin-contracts"
  }'
```

### Example 3: Handle Rate Limiting

```bash
# Check rate limit headers
curl -i -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "..."}'

# Response headers include:
# X-RateLimit-Limit: 60
# X-RateLimit-Remaining: 59
# X-RateLimit-Reset: 1704067200
```

### Example 4: Generate PDF Report

```bash
curl -X POST http://localhost:8000/api/v1/generate_report \
  -H "Content-Type: application/json" \
  -d '{"code": "..."}' \
  --output report.pdf
```

## Best Practices

1. **Batch Requests**: Analyze multiple contracts in sequence to avoid rate limits
2. **Cache Results**: Store analysis results to avoid re-analyzing the same code
3. **Handle Errors**: Implement retry logic with exponential backoff
4. **Monitor Usage**: Track API calls to stay within rate limits
5. **Use Compression**: Enable gzip compression for large requests
6. **Timeout Handling**: Set appropriate timeouts (30+ seconds for analysis)

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Hybrid analysis (static + AI)
- Repository scanning
- DREAD scoring
- PDF report generation
- Rate limiting
- Error handling

## Support

For API issues or questions:
1. Check this documentation
2. Review error messages
3. Check CloudWatch logs
4. Open an issue on GitHub
