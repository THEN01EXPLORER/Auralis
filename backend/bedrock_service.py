import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def analyze_contract(code: str) -> dict:
    system_prompt = """You are an expert smart contract security auditor. Analyze the provided Solidity code and identify all security vulnerabilities.

You MUST return your analysis ONLY in this exact JSON format with no additional text:
{
    "risk_score": <integer from 0-100>,
    "vulnerabilities": [
        {
            "type": "Vulnerability Name",
            "line_number": <integer>,
            "severity": "High" or "Medium" or "Low",
            "description": "Detailed explanation of the vulnerability and why it is a risk."
        }
    ]
}

Focus on critical vulnerabilities like:
- Re-entrancy attacks
- Integer overflow/underflow
- Access control issues
- Unchecked external calls
- Front-running vulnerabilities
- Timestamp dependence
- Gas limit issues

Return ONLY valid JSON, no markdown, no explanations outside the JSON."""

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": f"Analyze this smart contract:\n\n{code}"
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps(payload)
    )

    response_body = json.loads(response['body'].read())
    text_response = response_body['content'][0]['text']
    
    # Parse JSON from response
    analysis = json.loads(text_response)
    return analysis
