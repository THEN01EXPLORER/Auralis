# AI-Powered Analysis Integration - Design Document

## Overview

This design integrates AWS Bedrock AI analysis into the existing Auralis vulnerability detection pipeline. The system will use a hybrid approach combining pattern-based static analysis with AI-powered semantic analysis to provide comprehensive smart contract security audits.

## Architecture

### Current Flow
```
User Request → FastAPI Endpoint → Static Pattern Matching → Response
```

### New Hybrid Flow
```
User Request → FastAPI Endpoint → Static Analyzer → AI Analyzer → Merge Results → Response
                                        ↓              ↓
                                   Vulnerabilities  Vulnerabilities
                                        ↓              ↓
                                        └──────┬───────┘
                                               ↓
                                      Deduplication Logic
                                               ↓
                                        Unified Response
```

## Components and Interfaces

### 1. Analysis Orchestrator (New)

**Purpose:** Coordinates the execution of both analyzers and merges results.

**Location:** `backend/app/services/analysis_orchestrator.py`

**Interface:**
```python
class AnalysisOrchestrator:
    def __init__(self, static_analyzer: VulnerabilityAnalyzer, ai_analyzer: BedrockAnalyzer):
        self.static_analyzer = static_analyzer
        self.ai_analyzer = ai_analyzer
    
    async def analyze_contract(self, contract_code: str) -> AnalysisResult:
        """
        Orchestrates hybrid analysis combining static and AI analysis.
        
        Returns:
            AnalysisResult with merged vulnerabilities and metadata
        """
        pass
```

### 2. Bedrock Analyzer (Refactored)

**Purpose:** Wraps AWS Bedrock API calls with proper error handling.

**Location:** `backend/app/services/bedrock_analyzer.py`

**Interface:**
```python
class BedrockAnalyzer:
    def __init__(self, region: str = 'us-east-1', timeout: int = 25):
        self.region = region
        self.timeout = timeout
        self.available = self._check_availability()
    
    def analyze(self, contract_code: str, static_results: List[Vulnerability] = None) -> BedrockAnalysisResult:
        """
        Analyzes contract using AWS Bedrock Claude 3.
        
        Args:
            contract_code: Solidity contract source code
            static_results: Optional static analysis results for context
            
        Returns:
            BedrockAnalysisResult with vulnerabilities or error info
        """
        pass
    
    def _check_availability(self) -> bool:
        """Checks if AWS credentials are configured"""
        pass
```

### 3. Vulnerability Merger (New)

**Purpose:** Intelligently merges duplicate vulnerabilities from multiple sources.

**Location:** `backend/app/services/vulnerability_merger.py`

**Interface:**
```python
class VulnerabilityMerger:
    @staticmethod
    def merge(static_vulns: List[Vulnerability], ai_vulns: List[Vulnerability]) -> List[Vulnerability]:
        """
        Merges vulnerabilities from static and AI analysis.
        
        Deduplication logic:
        - Same type + same line = merge
        - Take highest severity
        - Take highest confidence
        - Combine descriptions
        
        Returns:
            Deduplicated list of vulnerabilities
        """
        pass
    
    @staticmethod
    def _is_duplicate(v1: Vulnerability, v2: Vulnerability) -> bool:
        """Determines if two vulnerabilities are duplicates"""
        pass
    
    @staticmethod
    def _merge_two(v1: Vulnerability, v2: Vulnerability) -> Vulnerability:
        """Merges two duplicate vulnerabilities"""
        pass
```

### 4. Updated API Endpoint

**Location:** `backend/main.py` or `backend/app/api/analyze.py`

**Changes:**
- Replace direct static analysis with orchestrator call
- Add analysis_method field to response
- Add error handling for AI failures

## Data Models

### Enhanced Vulnerability Model

```python
class Vulnerability(BaseModel):
    type: str
    severity: str  # Critical, High, Medium, Low
    line: int
    description: str
    recommendation: str
    confidence: float = 0.85
    source: str = "static"  # NEW: "static", "ai", or "hybrid"
    remediation: Optional[RemediationDetails] = None  # NEW

class RemediationDetails(BaseModel):
    explanation: str
    code_example: Optional[str] = None
```

### Analysis Result Model

```python
class AnalysisResult(BaseModel):
    analysis_id: str
    vulnerabilities: List[Vulnerability]
    risk_score: int
    summary: str
    analysis_method: str  # NEW: "static", "ai", or "hybrid"
    ai_available: bool  # NEW: indicates if AI was attempted
    processing_time_ms: int  # NEW: performance metric
```

### Bedrock Analysis Result

```python
class BedrockAnalysisResult(BaseModel):
    success: bool
    vulnerabilities: List[Vulnerability]
    error_message: Optional[str] = None
    processing_time_ms: int
```

## Error Handling

### AI Analyzer Failures

1. **AWS Credentials Missing**
   - Detection: Check for boto3 client initialization failure
   - Action: Set `ai_available = False`, use static analysis only
   - Log: Warning level

2. **Bedrock API Timeout**
   - Detection: Request exceeds 25 second timeout
   - Action: Return static results with warning
   - Log: Error level with request details

3. **Bedrock API Error**
   - Detection: HTTP error or invalid response
   - Action: Return static results with error message
   - Log: Error level with full exception

4. **Invalid JSON Response**
   - Detection: JSON parsing fails on Bedrock response
   - Action: Return static results, log raw response
   - Log: Error level

### Graceful Degradation Strategy

```python
try:
    ai_result = await bedrock_analyzer.analyze(code, static_vulns)
    if ai_result.success:
        merged_vulns = merger.merge(static_vulns, ai_result.vulnerabilities)
        analysis_method = "hybrid"
    else:
        merged_vulns = static_vulns
        analysis_method = "static"
        logger.warning(f"AI analysis failed: {ai_result.error_message}")
except Exception as e:
    logger.error(f"Unexpected AI analysis error: {e}")
    merged_vulns = static_vulns
    analysis_method = "static"
```

## Testing Strategy

### Unit Tests

1. **VulnerabilityMerger Tests**
   - Test duplicate detection (same type + line)
   - Test severity prioritization
   - Test confidence score selection
   - Test description combination
   - Test non-duplicate preservation

2. **BedrockAnalyzer Tests**
   - Test successful analysis
   - Test timeout handling
   - Test credential check
   - Test invalid JSON response
   - Mock boto3 client

3. **AnalysisOrchestrator Tests**
   - Test hybrid analysis flow
   - Test static-only fallback
   - Test result merging
   - Test timing metrics

### Integration Tests

1. **End-to-End Analysis**
   - Test with real contract code
   - Verify both analyzers run
   - Verify deduplication works
   - Verify response format

2. **Degraded Mode**
   - Test without AWS credentials
   - Test with Bedrock unavailable
   - Verify static analysis still works

### Manual Testing

1. Upload sample vulnerable contract
2. Verify hybrid analysis runs
3. Check for duplicate vulnerabilities
4. Verify AI-enhanced descriptions
5. Test with AWS credentials disabled
6. Verify graceful degradation

## Performance Considerations

### Timing Targets

- Static Analysis: < 1 second
- AI Analysis: < 25 seconds
- Total Request: < 30 seconds
- Timeout: 30 seconds

### Optimization Strategies

1. **Parallel Execution** (Future Enhancement)
   - Run static and AI analysis concurrently
   - Reduces total time to max(static, ai) instead of sum

2. **Caching** (Future Enhancement)
   - Cache AI results for identical contracts
   - Use contract hash as cache key

3. **Request Batching** (Future Enhancement)
   - Batch multiple contracts in single Bedrock request
   - Reduces API call overhead

## Configuration

### Environment Variables

```env
# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_TIMEOUT=25

# Feature Flags
ENABLE_AI_ANALYSIS=true
AI_ANALYSIS_REQUIRED=false  # If true, fail request when AI unavailable
```

### Bedrock Prompt Engineering

The AI analyzer will use an enhanced system prompt that:
- Provides context from static analysis results
- Requests specific JSON format
- Focuses on semantic vulnerabilities
- Includes remediation guidance
- Specifies confidence scoring

## Migration Plan

### Phase 1: Implementation
1. Create new service classes
2. Implement merger logic
3. Add unit tests
4. Update API endpoint

### Phase 2: Testing
1. Test with AWS credentials
2. Test without AWS credentials
3. Verify backward compatibility
4. Performance testing

### Phase 3: Deployment
1. Deploy to staging
2. Monitor error rates
3. Verify AI analysis working
4. Deploy to production

## Security Considerations

1. **AWS Credentials**: Store in environment variables, never commit
2. **Input Validation**: Sanitize contract code before sending to Bedrock
3. **Rate Limiting**: Implement to prevent Bedrock API abuse
4. **Cost Control**: Monitor Bedrock token usage
5. **Error Messages**: Don't expose internal errors to users

## Backward Compatibility

- Existing `/api/v1/analyze` endpoint maintains same response structure
- New fields are additive (analysis_method, ai_available)
- Frontend can ignore new fields if not needed
- Static-only mode produces identical results to current implementation
