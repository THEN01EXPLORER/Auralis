import json
import logging
import boto3
from typing import List, Optional
import time
import pybreaker
from botocore.exceptions import ClientError
from app.models.contract import Vulnerability, RemediationDetails, BedrockAnalysisResult

# Circuit Breaker Configuration
# Open circuit after 5 failures, try to reset after 60 seconds
bedrock_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)


logger = logging.getLogger(__name__)

class BedrockAnalyzer:
    def __init__(self, region: str = 'us-east-1', timeout: int = 25):
        self.region = region
        self.timeout = timeout
        self.bedrock = None
        self.available = False
        self._init_bedrock()

    def _init_bedrock(self):
        try:
            # Check for credentials first
            session = boto3.Session()
            credentials = session.get_credentials()
            if not credentials or not credentials.access_key or not credentials.secret_key:
                logger.warning("Bedrock validation failed: No AWS credentials found")
                self.available = False
                return

            # Configure boto3 with timeout
            config = boto3.session.Config(
                connect_timeout=self.timeout, 
                read_timeout=self.timeout,
                retries={'max_attempts': 1}
            )
            self.bedrock = boto3.client('bedrock-runtime', region_name=self.region, config=config)
            self.available = True
            logger.info(f"Bedrock client initialized successfully in {self.region}")
        except Exception as e:
            logger.warning(f"Failed to initialize Bedrock client: {str(e)}")
            self.available = False

    def analyze(self, contract_code: str, static_vulnerabilities: List[Vulnerability] = None) -> BedrockAnalysisResult:
        start_time = time.time()
        static_vulnerabilities = static_vulnerabilities or []
        
        if not self.available:
            return BedrockAnalysisResult(
                success=False, 
                error_message="Bedrock client not available",
                vulnerabilities=[],
                processing_time_ms=0
            )

        try:
            # Construct a prompt that includes static analysis context
            static_context = "\n".join([f"- {v.type} at line {v.line}" for v in static_vulnerabilities])
            
            system_prompt = f"""You are an expert smart contract security auditor. Analyze the provided Solidity code and identify security vulnerabilities.
            
            Static analysis has already identified the following potential issues:
            {static_context}

            Verify these and find any other logic flaws.

            You MUST return your analysis ONLY in this exact JSON format with no additional text:
            {{
                "vulnerabilities": [
                    {{
                        "type": "Vulnerability Name",
                        "line": <integer>,
                        "severity": "Critical" or "High" or "Medium" or "Low",
                        "description": "Detailed explanation...",
                        "recommendation": "How to fix...",
                        "confidence": <float between 0.0 and 1.0>,
                        "remediation": {{
                            "explanation": "...",
                            "code_example": "..."
                        }}
                    }}
                ]
            }}
            """

            user_message = f"""Analyze this smart contract:
            
            ```solidity
            {contract_code}
            ```
            """

            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.1
            }

            # Wrap the external call with circuit breaker
            # If the circuit is open, this will raise CircuitBreakerError immediately
            @bedrock_breaker
            def invoke_bedrock():
                return self.bedrock.invoke_model(
                    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                    body=json.dumps(payload)
                )

            response = invoke_bedrock()

            response_body = json.loads(response['body'].read())
            
            if 'content' not in response_body or not response_body['content']:
                raise ValueError("Response missing content - service temporarily unavailable")
                
            text_response = response_body['content'][0]['text']
            
            vulnerabilities = self._parse_bedrock_response(text_response)

            processing_time = int((time.time() - start_time) * 1000)
            return BedrockAnalysisResult(
                success=True, 
                vulnerabilities=vulnerabilities,
                processing_time_ms=processing_time
            )

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = str(e)
            if 'Throttling' in error_code:
                error_msg = "Service is experiencing high demand. Please try again later."
            
            logger.error(f"Bedrock AWS error: {error_msg}")
            processing_time = int((time.time() - start_time) * 1000)
            return BedrockAnalysisResult(
                success=False, 
                error_message=error_msg,
                vulnerabilities=[],
                processing_time_ms=processing_time
            )
            
        except pybreaker.CircuitBreakerError:
            logger.error("Bedrock circuit breaker is OPEN - failing fast")
            return BedrockAnalysisResult(
                success=False,
                error_message="AI Service unavailable (Circuit Breaker Open)",
                vulnerabilities=[],
                processing_time_ms=0
            )

        except Exception as e:
            error_msg = str(e)
            if 'temporarily unavailable' in error_msg:
                pass # keep existing message
            else:
                logger.error(f"Bedrock analysis failed: {str(e)}")
                
            processing_time = int((time.time() - start_time) * 1000)
            return BedrockAnalysisResult(
                success=False, 
                error_message=error_msg,
                vulnerabilities=[],
                processing_time_ms=processing_time
            )

    def _parse_bedrock_response(self, text_response: str) -> List[Vulnerability]:
        try:
            # Try to parse raw text first (handles clean JSON)
            try:
                analysis_data = json.loads(text_response)
            except json.JSONDecodeError:
                # Extract JSON from potential wrapper text or markdown
                json_str = text_response
                if "```json" in text_response:
                    json_str = text_response.split("```json")[1].split("```")[0].strip()
                elif "```" in text_response:
                    json_str = text_response.split("```")[1].split("```")[0].strip()
                else:
                    # heuristic to find start/end of JSON structure (dict or list)
                    start_dict = text_response.find("{")
                    start_list = text_response.find("[")
                    
                    start = -1
                    if start_dict != -1 and start_list != -1:
                        start = min(start_dict, start_list)
                    elif start_dict != -1:
                        start = start_dict
                    elif start_list != -1:
                        start = start_list
                        
                    end_dict = text_response.rfind("}")
                    end_list = text_response.rfind("]")
                    
                    end = -1
                    if end_dict != -1 and end_list != -1:
                        end = max(end_dict, end_list)
                    elif end_dict != -1:
                        end = end_dict
                    elif end_list != -1:
                        end = end_list
                        
                    if start != -1 and end != -1:
                        json_str = text_response[start:end+1]

                analysis_data = json.loads(json_str)
            
            # Handle list directly if it returns list instead of dict
            if isinstance(analysis_data, list):
                v_list = analysis_data
            else:
                v_list = analysis_data.get("vulnerabilities", [])
            
            vulnerabilities = []
            for v_data in v_list:
                vulnerabilities.append(Vulnerability(
                    type=v_data.get("type", "Unknown"),
                    severity=v_data.get("severity", "Medium"),
                    line=v_data.get("line", 0),
                    description=v_data.get("description", ""),
                    recommendation=v_data.get("recommendation", ""),
                    confidence=v_data.get("confidence", 0.5),
                    source="ai",
                    remediation=RemediationDetails(**v_data["remediation"]) if v_data.get("remediation") else None
                ))
            return vulnerabilities
        except Exception as e:
            logger.warning(f"Failed to parse Bedrock response: {str(e)}")
            return []
