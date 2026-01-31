def calculate_risk_score(vulnerabilities: list) -> int:
    """
    Calculate risk score based on vulnerability severities.
    
    Scoring:
    - Critical = 40 points
    - High = 20 points
    - Medium = 10 points
    - Low = 5 points
    
    Total capped at 100.
    """
    severity_points = {
        'Critical': 40,
        'High': 20,
        'Medium': 10,
        'Low': 5
    }
    
    total_score = 0
    for vuln in vulnerabilities:
        severity = vuln.get('severity', 'Low')
        total_score += severity_points.get(severity, 0)
    
    return min(total_score, 100)
