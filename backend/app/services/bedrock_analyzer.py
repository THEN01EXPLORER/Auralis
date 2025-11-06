import json
import time
import logging
from typing import List, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from app.models.contract import Vulnerability, BedrockAnalysisResult, RemediationDetails

logger = logging.getLogger(__name__)

class BedrockAnalyzer:
    """
    AWS Bedrock-powered smart contract vulnerability analyzer.
    Uses Claude 3 to perform semantic analysis of smart contracts.
    """
    
    def __init__(self, region: str = 'us-east-1', timeout: int = 25):
        """
        Initialize the Bedrock analyzer.
        
        Args:
            region: AWS region for Bedrock service
            timeout: Request timeout in seconds
        """
        self.region = region
        self.timeout = timeout
        self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        self.client = None
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """
        Check if AWS credentials are configured and Bedrock is accessible.
        
        Returns:
            bool: True if AWS credentials are available, False otherwise
        """
        logger.info(f"Checking AWS Bedrock availability in region: {self.region}")
        
        try:
            # Try to create a boto3 client
            self.client = boto3.client(
                'bedrock-runtime',
                region_name=self.region
            )
            
            # Test credentials by attempting to list models (this doesn't actually call the API)
            # We just check if credentials are configured
            session = boto3.Session()
            credentials = session.get_credentials()
            
            if credentials is None:
                logger.warning("AWS Bedrock availability check failed: No credentials found in environment or AWS config")
                return False
                
            if not credentials.access_key or not credentials.secret_key:
                logger.warning("AWS Bedrock availability check failed: Incomplete credentials (missing access key or secret key)")
                return False
                
            logger.info(f"AWS Bedrock analyzer availability check passed - credentials configured for region {self.region}")
            return True
            
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.warning(f"AWS Bedrock availability check failed: Credentials not properly configured - {type(e).__name__}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"AWS Bedrock availability check failed: Unexpected error during client initialization - {type(e).__name__}: {str(e)}", exc_info=True)
            return False    

    def analyze(self, contract_code: str, static_results: Optional[List[Vulnerability]] = None) -> BedrockAnalysisResult:
        """
        Analyze smart contract using AWS Bedrock Claude 3.
        
        Args:
            contract_code: Solidity contract source code
            static_results: Optional static analysis results for context
            
        Returns:
            BedrockAnalysisResult with vulnerabilities or error info
        """
        start_time = time.time()
        
        if not self.available:
            return BedrockAnalysisResult(
                success=False,
                vulnerabilities=[],
                error_message="AWS Bedrock not available - credentials not configured",
                processing_time_ms=int((time.time() - start_time) * 1000)
            )
        
        try:
            logger.info(f"Starting Bedrock analysis with model {self.model_id}, timeout: {self.timeout}s")
            
            # Build enhanced system prompt with static analysis context
            system_prompt = self._build_system_prompt(static_results)
            
            # Log context information
            context_info = f"with {len(static_results)} static vulnerabilities as context" if static_results else "without static analysis context"
            logger.debug(f"Built system prompt {context_info}")
            
            # Construct the request payload
            request_payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": f"Analyze this Solidity smart contract for security vulnerabilities:\n\n```solidity\n{contract_code}\n```"
                    }
                ]
            }
            
            logger.debug(f"Invoking Bedrock model with payload size: {len(json.dumps(request_payload))} bytes")
            
            # Invoke Bedrock model with timeout handling
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_payload),
                contentType='application/json',
                accept='application/json'
            )
            
            logger.debug("Received response from Bedrock API, parsing content...")
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            
            if 'content' not in response_body or not response_body['content']:
                error_msg = "Empty or malformed response from Bedrock API - missing content field"
                logger.error(f"Bedrock API error: {error_msg}")
                return BedrockAnalysisResult(
                    success=False,
                    vulnerabilities=[],
                    error_message="AI analysis temporarily unavailable",
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            
            # Extract the text content
            content_text = response_body['content'][0]['text']
            logger.debug(f"Extracted content text length: {len(content_text)} characters")
            
            # Parse JSON response and convert to vulnerabilities
            vulnerabilities = self._parse_bedrock_response(content_text)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            logger.info(f"Bedrock analysis completed successfully in {processing_time}ms, found {len(vulnerabilities)} vulnerabilities")
            
            return BedrockAnalysisResult(
                success=True,
                vulnerabilities=vulnerabilities,
                error_message=None,
                processing_time_ms=processing_time
            )
            
        except ClientError as e:
            processing_time = int((time.time() - start_time) * 1000)
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_details = e.response.get('Error', {}).get('Message', str(e))
            
            # Log detailed error information for debugging with context
            logger.error(f"AWS Bedrock API error after {processing_time}ms - Code: {error_code}, Details: {error_details}")
            logger.debug(f"Bedrock API error context - Model: {self.model_id}, Region: {self.region}, "
                        f"Timeout: {self.timeout}s, Contract length: {len(contract_code)} chars", exc_info=True)
            
            # Provide user-friendly error message without exposing internal details
            user_message = "AI analysis temporarily unavailable due to service error"
            if error_code == 'ThrottlingException':
                user_message = "AI analysis temporarily unavailable due to high demand"
                logger.warning(f"Bedrock API throttling detected - consider implementing retry logic or rate limiting")
            elif error_code == 'ValidationException':
                user_message = "AI analysis failed due to invalid request format"
                logger.error(f"Bedrock API validation error - check request payload format and model compatibility")
            elif error_code in ['AccessDeniedException', 'UnauthorizedOperation']:
                user_message = "AI analysis unavailable due to insufficient permissions"
                logger.error(f"Bedrock API access denied - check AWS credentials and IAM permissions for model {self.model_id}")
            elif error_code == 'ModelNotReadyException':
                user_message = "AI analysis temporarily unavailable - model is loading"
                logger.warning(f"Bedrock model {self.model_id} is not ready - may need to wait for model initialization")
            elif error_code == 'ServiceQuotaExceededException':
                user_message = "AI analysis temporarily unavailable due to quota limits"
                logger.error(f"Bedrock service quota exceeded - check AWS service limits and usage")
            else:
                logger.error(f"Unhandled Bedrock API error code: {error_code} - consider adding specific handling")
            
            return BedrockAnalysisResult(
                success=False,
                vulnerabilities=[],
                error_message=user_message,
                processing_time_ms=processing_time
            )
            
        except json.JSONDecodeError as e:
            processing_time = int((time.time() - start_time) * 1000)
            
            # Log detailed parsing error for debugging
            logger.error(f"Failed to parse Bedrock response as JSON after {processing_time}ms - Error: {str(e)}", exc_info=True)
            
            return BedrockAnalysisResult(
                success=False,
                vulnerabilities=[],
                error_message="AI analysis failed due to response format error",
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            
            # Enhanced error logging with specific handling for common issues
            error_type = type(e).__name__
            error_message = str(e)
            
            if "timeout" in error_message.lower() or "timed out" in error_message.lower():
                logger.error(f"Bedrock analysis timed out after {processing_time}ms (configured timeout: {self.timeout}s)")
                logger.warning(f"Consider increasing BEDROCK_TIMEOUT environment variable if timeouts are frequent")
                user_message = "AI analysis timed out - please try again"
            elif "connection" in error_message.lower() or "network" in error_message.lower():
                logger.error(f"Network error during Bedrock analysis after {processing_time}ms - {error_type}: {error_message}")
                logger.debug(f"Network error context - Region: {self.region}, Model: {self.model_id}")
                user_message = "AI analysis temporarily unavailable due to network issues"
            elif "ssl" in error_message.lower() or "certificate" in error_message.lower():
                logger.error(f"SSL/Certificate error during Bedrock analysis - {error_type}: {error_message}")
                logger.debug("SSL error may indicate system certificate issues or network configuration problems")
                user_message = "AI analysis temporarily unavailable due to connection security issues"
            else:
                # Log unexpected errors with full details for debugging
                logger.error(f"Unexpected error during Bedrock analysis after {processing_time}ms - {error_type}: {error_message}", exc_info=True)
                logger.debug(f"Unexpected error context - Model: {self.model_id}, Region: {self.region}, "
                           f"Available: {self.available}, Contract length: {len(contract_code)} chars")
                user_message = "AI analysis temporarily unavailable"
            
            return BedrockAnalysisResult(
                success=False,
                vulnerabilities=[],
                error_message=user_message,
                processing_time_ms=processing_time
            )
    
    def _build_system_prompt(self, static_results: Optional[List[Vulnerability]] = None) -> str:
        """
        Build enhanced system prompt that includes static analysis context.
        
        Args:
            static_results: Optional static analysis results for context
            
        Returns:
            str: System prompt for Claude 3
        """
        base_prompt = """You are an expert smart contract security auditor. Analyze the provided Solidity code for security vulnerabilities.

Focus on semantic vulnerabilities that require deep understanding of the code logic, business rules, and potential attack vectors. Look beyond simple pattern matching.

Key areas to analyze:
1. Business logic flaws
2. Complex re-entrancy scenarios
3. Access control bypasses
4. Economic attacks (MEV, flash loans)
5. State manipulation vulnerabilities
6. Cross-function interactions
7. Edge cases in mathematical operations
8. Governance and upgrade risks

For each vulnerability found, provide:
- type: Brief vulnerability category
- severity: Critical, High, Medium, or Low
- line: Line number where the issue occurs
- description: Detailed explanation of the vulnerability
- recommendation: Specific remediation steps
- confidence: Float between 0.0 and 1.0 indicating confidence level
- remediation: Object with explanation and optional code_example

Return your analysis as a JSON array of vulnerability objects. If no vulnerabilities are found, return an empty array.

Example format:
[
  {
    "type": "Business Logic Flaw",
    "severity": "High",
    "line": 42,
    "description": "The withdraw function allows users to withdraw more than their balance due to incorrect balance checking logic.",
    "recommendation": "Add proper balance validation before allowing withdrawals",
    "confidence": 0.95,
    "remediation": {
      "explanation": "Implement a require statement to check that the withdrawal amount does not exceed the user's balance",
      "code_example": "require(balances[msg.sender] >= amount, 'Insufficient balance');"
    }
  }
]"""

        if static_results:
            static_context = "\n\nStatic analysis has already identified the following issues:\n"
            for vuln in static_results:
                static_context += f"- {vuln.type} at line {vuln.line} ({vuln.severity}): {vuln.description}\n"
            
            static_context += "\nFocus on finding additional semantic vulnerabilities that static analysis might have missed. Avoid duplicating the above findings unless you have significantly different insights."
            
            return base_prompt + static_context
        
        return base_prompt
    
    def _parse_bedrock_response(self, response_text: str) -> List[Vulnerability]:
        """
        Parse JSON response from Bedrock and convert to Vulnerability objects.
        
        Args:
            response_text: Raw text response from Claude 3
            
        Returns:
            List[Vulnerability]: Parsed vulnerabilities
        """
        try:
            # Extract JSON from response (Claude might include explanatory text)
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                logger.warning("No JSON array found in Bedrock response")
                return []
            
            json_text = response_text[json_start:json_end]
            vulnerability_data = json.loads(json_text)
            
            logger.debug(f"Parsing {len(vulnerability_data)} vulnerability objects from Bedrock response")
            
            vulnerabilities = []
            parsing_errors = 0
            
            for i, vuln_dict in enumerate(vulnerability_data):
                try:
                    # Create RemediationDetails if present
                    remediation = None
                    if 'remediation' in vuln_dict and vuln_dict['remediation']:
                        remediation = RemediationDetails(
                            explanation=vuln_dict['remediation'].get('explanation', ''),
                            code_example=vuln_dict['remediation'].get('code_example')
                        )
                    
                    vulnerability = Vulnerability(
                        type=vuln_dict.get('type', 'Unknown'),
                        severity=vuln_dict.get('severity', 'Medium'),
                        line=int(vuln_dict.get('line', 0)),
                        description=vuln_dict.get('description', ''),
                        recommendation=vuln_dict.get('recommendation', ''),
                        confidence=float(vuln_dict.get('confidence', 0.8)),
                        source="ai",
                        remediation=remediation
                    )
                    vulnerabilities.append(vulnerability)
                    
                except (KeyError, ValueError, TypeError) as e:
                    parsing_errors += 1
                    logger.warning(f"Failed to parse vulnerability #{i+1} from Bedrock response - {type(e).__name__}: {str(e)}")
                    logger.debug(f"Problematic vulnerability data: {vuln_dict}")
                    continue
            
            if parsing_errors > 0:
                logger.warning(f"Encountered {parsing_errors} parsing errors out of {len(vulnerability_data)} vulnerabilities")
            
            logger.info(f"Successfully parsed {len(vulnerabilities)} vulnerabilities from Bedrock response")
            return vulnerabilities
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Bedrock response - {type(e).__name__}: {str(e)}")
            logger.debug(f"Raw response text that failed to parse: {response_text[:500]}...")
            return []
        except Exception as e:
            logger.error(f"Unexpected error parsing Bedrock response - {type(e).__name__}: {str(e)}", exc_info=True)
            return []