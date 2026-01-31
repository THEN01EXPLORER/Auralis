import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError, NoCredentialsError
from app.services.bedrock_analyzer import BedrockAnalyzer
from app.models.contract import Vulnerability, BedrockAnalysisResult, RemediationDetails


class TestBedrockAnalyzer:
    """Test cases for BedrockAnalyzer service."""
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_availability_check_with_valid_credentials(self, mock_boto3):
        """Test AWS credential check with valid credentials."""
        # Mock successful session and credentials
        mock_session = Mock()
        mock_credentials = Mock()
        mock_credentials.access_key = "test_access_key"
        mock_credentials.secret_key = "test_secret_key"
        mock_session.get_credentials.return_value = mock_credentials
        
        mock_boto3.Session.return_value = mock_session
        mock_boto3.client.return_value = Mock()
        
        analyzer = BedrockAnalyzer()
        assert analyzer.available == True
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_availability_check_no_credentials(self, mock_boto3):
        """Test AWS credential check with no credentials."""
        # Mock session with no credentials
        mock_session = Mock()
        mock_session.get_credentials.return_value = None
        
        mock_boto3.Session.return_value = mock_session
        mock_boto3.client.return_value = Mock()
        
        analyzer = BedrockAnalyzer()
        assert analyzer.available == False
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_availability_check_incomplete_credentials(self, mock_boto3):
        """Test AWS credential check with incomplete credentials."""
        # Mock session with incomplete credentials
        mock_session = Mock()
        mock_credentials = Mock()
        mock_credentials.access_key = "test_access_key"
        mock_credentials.secret_key = None  # Missing secret key
        mock_session.get_credentials.return_value = mock_credentials
        
        mock_boto3.Session.return_value = mock_session
        mock_boto3.client.return_value = Mock()
        
        analyzer = BedrockAnalyzer()
        assert analyzer.available == False
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_availability_check_credentials_error(self, mock_boto3):
        """Test AWS credential check with credentials error."""
        mock_boto3.client.side_effect = NoCredentialsError()
        
        analyzer = BedrockAnalyzer()
        assert analyzer.available == False
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_successful_analysis_with_valid_response(self, mock_boto3):
        """Test successful analysis with valid Bedrock response."""
        # Setup mock client
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        # Setup mock session with valid credentials
        mock_session = Mock()
        mock_credentials = Mock()
        mock_credentials.access_key = "test_access_key"
        mock_credentials.secret_key = "test_secret_key"
        mock_session.get_credentials.return_value = mock_credentials
        mock_boto3.Session.return_value = mock_session
        
        # Mock successful Bedrock response
        mock_response_body = {
            "content": [{
                "text": json.dumps([
                    {
                        "type": "Re-entrancy Attack",
                        "severity": "Critical",
                        "line": 42,
                        "description": "AI detected reentrancy vulnerability",
                        "recommendation": "Use checks-effects-interactions pattern",
                        "confidence": 0.95,
                        "remediation": {
                            "explanation": "Implement proper state updates before external calls",
                            "code_example": "require(balances[msg.sender] >= amount);"
                        }
                    }
                ])
            }]
        }
        
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps(mock_response_body).encode()
        mock_client.invoke_model.return_value = mock_response
        
        analyzer = BedrockAnalyzer()
        contract_code = "contract Test { function withdraw() public { msg.sender.call{value: 1 ether}(\"\"); } }"
        
        result = analyzer.analyze(contract_code)
        
        assert result.success == True
        assert len(result.vulnerabilities) == 1
        assert result.vulnerabilities[0].type == "Re-entrancy Attack"
        assert result.vulnerabilities[0].severity == "Critical"
        assert result.vulnerabilities[0].line == 42
        assert result.vulnerabilities[0].confidence == 0.95
        assert result.vulnerabilities[0].source == "ai"
        assert result.vulnerabilities[0].remediation is not None
        assert result.error_message is None
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_analysis_with_unavailable_analyzer(self, mock_boto3):
        """Test analysis when analyzer is not available."""
        # Mock unavailable analyzer
        mock_boto3.client.side_effect = NoCredentialsError()
        
        analyzer = BedrockAnalyzer()
        contract_code = "contract Test {}"
        
        result = analyzer.analyze(contract_code)
        
        assert result.success == False
        assert len(result.vulnerabilities) == 0
        assert "not available" in result.error_message
        assert result.processing_time_ms >= 0
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_client_error_handling(self, mock_boto3):
        """Test handling of AWS ClientError."""
        # Setup mock client
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        # Setup mock session with valid credentials
        mock_session = Mock()
        mock_credentials = Mock()
        mock_credentials.access_key = "test_access_key"
        mock_credentials.secret_key = "test_secret_key"
        mock_session.get_credentials.return_value = mock_credentials
        mock_boto3.Session.return_value = mock_session
        
        # Mock ClientError
        error_response = {
            'Error': {
                'Code': 'ThrottlingException',
                'Message': 'Request was throttled'
            }
        }
        mock_client.invoke_model.side_effect = ClientError(error_response, 'InvokeModel')
        
        analyzer = BedrockAnalyzer()
        contract_code = "contract Test {}"
        
        result = analyzer.analyze(contract_code)
        
        assert result.success == False
        assert len(result.vulnerabilities) == 0
        assert "high demand" in result.error_message  # Throttling-specific message
        assert result.processing_time_ms >= 0
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_invalid_json_response_handling(self, mock_boto3):
        """Test handling of invalid JSON response from Bedrock."""
        # Setup mock client
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        # Setup mock session with valid credentials
        mock_session = Mock()
        mock_credentials = Mock()
        mock_credentials.access_key = "test_access_key"
        mock_credentials.secret_key = "test_secret_key"
        mock_session.get_credentials.return_value = mock_credentials
        mock_boto3.Session.return_value = mock_session
        
        # Mock response with invalid JSON
        mock_response_body = {
            "content": [{
                "text": "This is not valid JSON for vulnerability analysis"
            }]
        }
        
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps(mock_response_body).encode()
        mock_client.invoke_model.return_value = mock_response
        
        analyzer = BedrockAnalyzer()
        contract_code = "contract Test {}"
        
        result = analyzer.analyze(contract_code)
        
        assert result.success == True  # Should still succeed but with empty vulnerabilities
        assert len(result.vulnerabilities) == 0  # No valid vulnerabilities parsed
        assert result.error_message is None
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_empty_response_handling(self, mock_boto3):
        """Test handling of empty response from Bedrock."""
        # Setup mock client
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        # Setup mock session with valid credentials
        mock_session = Mock()
        mock_credentials = Mock()
        mock_credentials.access_key = "test_access_key"
        mock_credentials.secret_key = "test_secret_key"
        mock_session.get_credentials.return_value = mock_credentials
        mock_boto3.Session.return_value = mock_session
        
        # Mock empty response
        mock_response_body = {}
        
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps(mock_response_body).encode()
        mock_client.invoke_model.return_value = mock_response
        
        analyzer = BedrockAnalyzer()
        contract_code = "contract Test {}"
        
        result = analyzer.analyze(contract_code)
        
        assert result.success == False
        assert len(result.vulnerabilities) == 0
        assert "temporarily unavailable" in result.error_message
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_timeout_handling(self, mock_boto3):
        """Test timeout handling during Bedrock API call."""
        # Setup mock client
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        # Setup mock session with valid credentials
        mock_session = Mock()
        mock_credentials = Mock()
        mock_credentials.access_key = "test_access_key"
        mock_credentials.secret_key = "test_secret_key"
        mock_session.get_credentials.return_value = mock_credentials
        mock_boto3.Session.return_value = mock_session
        
        # Mock timeout exception
        mock_client.invoke_model.side_effect = Exception("Request timed out")
        
        analyzer = BedrockAnalyzer()
        contract_code = "contract Test {}"
        
        result = analyzer.analyze(contract_code)
        
        assert result.success == False
        assert len(result.vulnerabilities) == 0
        assert "timed out" in result.error_message
        assert result.processing_time_ms >= 0
    
    @patch('app.services.bedrock_analyzer.boto3')
    def test_system_prompt_with_static_context(self, mock_boto3):
        """Test that system prompt includes static analysis context when provided."""
        # Setup mock client
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        # Setup mock session with valid credentials
        mock_session = Mock()
        mock_credentials = Mock()
        mock_credentials.access_key = "test_access_key"
        mock_credentials.secret_key = "test_secret_key"
        mock_session.get_credentials.return_value = mock_credentials
        mock_boto3.Session.return_value = mock_session
        
        # Mock successful response
        mock_response_body = {
            "content": [{
                "text": "[]"  # Empty vulnerability array
            }]
        }
        
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps(mock_response_body).encode()
        mock_client.invoke_model.return_value = mock_response
        
        analyzer = BedrockAnalyzer()
        contract_code = "contract Test {}"
        
        # Create static vulnerabilities for context
        static_vulns = [
            Vulnerability(
                type="Access Control",
                severity="High",
                line=25,
                description="Missing access control",
                recommendation="Add access control",
                confidence=0.8,
                source="static"
            )
        ]
        
        result = analyzer.analyze(contract_code, static_vulns)
        
        # Verify the invoke_model was called
        assert mock_client.invoke_model.called
        
        # Get the call arguments to verify system prompt includes context
        call_args = mock_client.invoke_model.call_args
        request_body = json.loads(call_args[1]['body'])
        system_prompt = request_body['system']
        
        # Verify static context is included in system prompt
        assert "Static analysis has already identified" in system_prompt
        assert "Access Control" in system_prompt
        assert "line 25" in system_prompt
        
        assert result.success == True
    
    def test_parse_bedrock_response_with_valid_json(self):
        """Test parsing of valid JSON response from Bedrock."""
        analyzer = BedrockAnalyzer()
        
        response_text = json.dumps([
            {
                "type": "Integer Overflow",
                "severity": "Medium",
                "line": 15,
                "description": "Potential integer overflow",
                "recommendation": "Use SafeMath library",
                "confidence": 0.85,
                "remediation": {
                    "explanation": "Use SafeMath to prevent overflow",
                    "code_example": "using SafeMath for uint256;"
                }
            }
        ])
        
        vulnerabilities = analyzer._parse_bedrock_response(response_text)
        
        assert len(vulnerabilities) == 1
        assert vulnerabilities[0].type == "Integer Overflow"
        assert vulnerabilities[0].severity == "Medium"
        assert vulnerabilities[0].line == 15
        assert vulnerabilities[0].confidence == 0.85
        assert vulnerabilities[0].source == "ai"
        assert vulnerabilities[0].remediation is not None
        assert vulnerabilities[0].remediation.explanation == "Use SafeMath to prevent overflow"
    
    def test_parse_bedrock_response_with_invalid_json(self):
        """Test parsing of invalid JSON response from Bedrock."""
        analyzer = BedrockAnalyzer()
        
        response_text = "This is not valid JSON"
        
        vulnerabilities = analyzer._parse_bedrock_response(response_text)
        
        assert len(vulnerabilities) == 0
    
    def test_parse_bedrock_response_with_missing_fields(self):
        """Test parsing response with missing required fields."""
        analyzer = BedrockAnalyzer()
        
        response_text = json.dumps([
            {
                "type": "Test Vulnerability",
                # Missing severity, line, etc.
            }
        ])
        
        vulnerabilities = analyzer._parse_bedrock_response(response_text)
        
        # Should handle missing fields gracefully
        assert len(vulnerabilities) == 1
        assert vulnerabilities[0].type == "Test Vulnerability"
        assert vulnerabilities[0].severity == "Medium"  # Default value
        assert vulnerabilities[0].line == 0  # Default value