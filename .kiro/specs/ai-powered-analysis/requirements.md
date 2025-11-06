# Requirements Document

## Introduction

This feature enhances the Auralis smart contract security auditor by integrating AWS Bedrock AI-powered analysis alongside the existing pattern-matching vulnerability detection. The System shall combine static analysis results with AI-generated insights to provide comprehensive security audits with deeper semantic understanding of smart contract vulnerabilities.

## Glossary

- **Auralis**: The smart contract security auditing platform
- **Static Analyzer**: The pattern-matching vulnerability detection system currently implemented
- **AI Analyzer**: AWS Bedrock Claude 3 model for semantic vulnerability analysis
- **Hybrid Analysis**: Combined results from both Static Analyzer and AI Analyzer
- **Risk Score**: Numerical value (0-100) indicating overall contract security risk
- **Vulnerability**: A security issue detected in smart contract code

## Requirements

### Requirement 1: AI Analysis Integration

**User Story:** As a security auditor, I want the system to use AI-powered analysis in addition to pattern matching, so that I can detect complex vulnerabilities that require semantic understanding.

#### Acceptance Criteria

1. WHEN the user submits a contract for analysis, THE Auralis SHALL invoke the AI Analyzer after the Static Analyzer completes
2. WHEN the AI Analyzer is invoked, THE Auralis SHALL pass the contract code and Static Analyzer results as context
3. IF the AI Analyzer fails or times out, THEN THE Auralis SHALL return the Static Analyzer results with a warning message
4. THE Auralis SHALL merge vulnerabilities from both the Static Analyzer and AI Analyzer into a single response
5. THE Auralis SHALL calculate a unified Risk Score based on all detected vulnerabilities

### Requirement 2: Duplicate Vulnerability Handling

**User Story:** As a security auditor, I want duplicate vulnerabilities to be merged intelligently, so that I don't see the same issue reported twice.

#### Acceptance Criteria

1. WHEN both analyzers detect the same vulnerability type on the same line, THE Auralis SHALL merge them into a single vulnerability entry
2. WHEN merging duplicate vulnerabilities, THE Auralis SHALL combine the descriptions and recommendations from both sources
3. THE Auralis SHALL use the higher confidence score when duplicates are merged
4. THE Auralis SHALL preserve the highest severity level when duplicates are merged

### Requirement 3: AI-Enhanced Vulnerability Details

**User Story:** As a security auditor, I want AI-generated vulnerabilities to include detailed explanations and remediation guidance, so that I can better understand and fix security issues.

#### Acceptance Criteria

1. WHEN the AI Analyzer detects a vulnerability, THE Auralis SHALL include a detailed description field
2. WHEN the AI Analyzer detects a vulnerability, THE Auralis SHALL include a recommendation field
3. WHERE the AI Analyzer provides remediation code examples, THE Auralis SHALL include them in the response
4. THE Auralis SHALL ensure all AI-generated vulnerabilities include line numbers, severity, and confidence scores

### Requirement 4: Graceful Degradation

**User Story:** As a system administrator, I want the analysis to continue working even if AWS Bedrock is unavailable, so that users always receive some level of security analysis.

#### Acceptance Criteria

1. IF AWS credentials are not configured, THEN THE Auralis SHALL use only the Static Analyzer
2. IF the AI Analyzer request fails, THEN THE Auralis SHALL log the error and return Static Analyzer results
3. WHEN operating in degraded mode, THE Auralis SHALL include a status field indicating AI analysis was unavailable
4. THE Auralis SHALL complete analysis requests within 30 seconds regardless of AI Analyzer availability

### Requirement 5: Response Format Consistency

**User Story:** As a frontend developer, I want the API response format to remain consistent whether AI analysis is used or not, so that the UI doesn't break.

#### Acceptance Criteria

1. THE Auralis SHALL return responses in the existing AnalyzeResponse format
2. THE Auralis SHALL include an additional analysis_method field indicating which analyzers were used
3. WHEN both analyzers are used, THE Auralis SHALL set analysis_method to "hybrid"
4. WHEN only Static Analyzer is used, THE Auralis SHALL set analysis_method to "static"
5. THE Auralis SHALL maintain backward compatibility with existing frontend code
