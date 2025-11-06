# Implementation Plan

- [x] 1. Create enhanced data models





  - Create RemediationDetails model in backend/app/models/contract.py
  - Update Vulnerability model to include source field and optional remediation field
  - Create AnalysisResult model with analysis_method, ai_available, and processing_time_ms fields
  - Create BedrockAnalysisResult model for AI analyzer responses
  - _Requirements: 1.5, 5.1, 5.2, 5.3, 5.4_

- [x] 2. Implement Bedrock Analyzer service




  - [x] 2.1 Create BedrockAnalyzer class in backend/app/services/bedrock_analyzer.py


    - Implement __init__ method with region and timeout configuration
    - Implement _check_availability method to verify AWS credentials
    - Set up boto3 bedrock-runtime client with error handling
    - _Requirements: 1.1, 4.1_
  
  - [x] 2.2 Implement analyze method with error handling


    - Build enhanced system prompt that includes static analysis context
    - Construct Bedrock API request payload with contract code
    - Invoke Bedrock model with timeout handling
    - Parse JSON response and convert to BedrockAnalysisResult
    - Handle AWS credential errors, timeouts, and invalid responses
    - _Requirements: 1.2, 1.3, 4.2, 4.4_
-

- [x] 3. Implement Vulnerability Merger service




  - [x] 3.1 Create VulnerabilityMerger class in backend/app/services/vulnerability_merger.py


    - Implement merge method that takes static and AI vulnerability lists
    - Implement _is_duplicate method to detect same type and line number
    - Implement _merge_two method to combine duplicate vulnerabilities
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [x] 3.2 Implement deduplication logic


    - Compare vulnerabilities by type and line number
    - Select highest severity when merging duplicates
    - Select highest confidence score when merging duplicates
    - Combine descriptions from both sources with clear attribution
    - Mark merged vulnerabilities with source="hybrid"
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 4. Implement Analysis Orchestrator service





  - [x] 4.1 Create AnalysisOrchestrator class in backend/app/services/analysis_orchestrator.py


    - Implement __init__ to accept static_analyzer and ai_analyzer dependencies
    - Implement analyze_contract method as main orchestration logic
    - _Requirements: 1.1, 1.4_
  
  - [x] 4.2 Implement hybrid analysis flow


    - Execute static analyzer first and collect results
    - Attempt AI analysis with static results as context
    - Handle AI analyzer failures gracefully with try-except
    - Merge results using VulnerabilityMerger when AI succeeds
    - Calculate unified risk score from merged vulnerabilities
    - Track processing time for performance metrics
    - Set analysis_method field based on which analyzers succeeded
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 4.2, 4.3_

- [x] 5. Update API endpoint to use orchestrator





  - [x] 5.1 Refactor /api/v1/analyze endpoint in backend/main.py


    - Initialize AnalysisOrchestrator with static and AI analyzers
    - Replace direct static analysis call with orchestrator.analyze_contract
    - Update response to include new fields (analysis_method, ai_available, processing_time_ms)
    - Maintain backward compatibility with existing response structure
    - _Requirements: 1.1, 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [x] 5.2 Add configuration and environment variable support


    - Load AWS credentials from environment variables
    - Add ENABLE_AI_ANALYSIS feature flag support
    - Configure Bedrock timeout from environment variable
    - Add logging for AI analysis status and errors
    - _Requirements: 4.1, 4.2_

- [x] 6. Add comprehensive error handling and logging








  - Implement logging for AI analyzer availability check
  - Log warnings when AI analysis fails but static succeeds
  - Log errors with full details for debugging
  - Ensure user-facing error messages don't expose internal details
  - Add performance logging for timing metrics
  - _Requirements: 1.3, 4.2, 4.3, 4.4_

- [x] 7. Write unit tests for new components





-

  - [x] 7.1 Write VulnerabilityMerger tests







    - Test duplicate detection with same type and line
    - Test severity prioritization (Critical > High > Medium > Low)
    - Test confidence score selection (higher value wins)
    - Test description combination
    - Test non-duplicate preservation
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [x] 7.2 Write BedrockAnalyzer tests








    - Mock boto3 client for testing
    - Test successful analysis with valid response
    - Test timeout handling
    - Test AWS credential check
    - Test invalid JSON response handling
    - Test API error handling
    - _Requirements: 1.2, 1.3, 4.1, 4.2_
  -

  - [x] 7.3 Write AnalysisOrchestrator tests







    - Test hybrid analysis with both analyzers succeeding
    - Test static-only fallback when AI fails
    - Test result merging correctness
    - Test timing metrics calculation
    - Test analysis_method field values
    - _Requirements: 1.1, 1.3, 1.4, 1.5_
-

- [x] 8. Integration testing




-

  - [x] 8.1 Test end-to-end analysis flow







    - Test with sample vulnerable contract
    - Verify both analyzers execute
    - Verify deduplication works correctly
    - Verify response format matches specification
    - _Requirements: 1.1, 1.4, 1.5, 5.5_
  
  - [x] 8.2 Test degraded mode scenarios








    - Test without AWS credentials configured
    - Test with Bedrock API unavailable
    - Verify static analysis continues working
    - Verify appropriate status fields are set
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
