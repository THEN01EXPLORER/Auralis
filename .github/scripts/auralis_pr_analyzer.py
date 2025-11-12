#!/usr/bin/env python3
"""
Auralis PR Analyzer Script
Analyzes changed Solidity files in a PR and generates results for GitHub Actions
"""

import os
import sys
import json
import requests
from pathlib import Path

def read_changed_files():
    """Read the list of changed .sol files"""
    changed_files_path = Path('changed_files.txt')
    if not changed_files_path.exists():
        return []
    
    with open(changed_files_path, 'r') as f:
        files = [line.strip() for line in f if line.strip()]
    
    return files

def analyze_file(api_url, file_path):
    """Analyze a single Solidity file using Auralis API"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        response = requests.post(
            f"{api_url}/api/v1/analyze",
            json={"code": code},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            result['filename'] = file_path
            return result
        else:
            print(f"Error analyzing {file_path}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Exception analyzing {file_path}: {str(e)}")
        return None

def run_slither(file_path):
    """Run Slither analysis on a file and convert to Auralis format"""
    try:
        import subprocess
        result = subprocess.run(
            ['slither', file_path, '--json', '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 or result.stdout:
            slither_data = json.loads(result.stdout)
            return convert_slither_to_auralis(slither_data)
        
    except Exception as e:
        print(f"Slither analysis failed for {file_path}: {str(e)}")
    
    return None

def convert_slither_to_auralis(slither_data):
    """Convert Slither output to Auralis format"""
    vulnerabilities = []
    
    for detector in slither_data.get('results', {}).get('detectors', []):
        vuln = {
            'type': detector.get('check', 'Unknown'),
            'line': detector.get('first_markdown_element', {}).get('source_mapping', {}).get('lines', [0])[0],
            'severity': detector.get('impact', 'Low').capitalize(),
            'confidence': 80,
            'description': detector.get('description', ''),
            'recommendation': detector.get('recommendation', 'Review this issue'),
            'source': 'slither'
        }
        vulnerabilities.append(vuln)
    
    return vulnerabilities

def main():
    api_url = os.getenv('AURALIS_API_URL', 'http://localhost:8000')
    changed_files = read_changed_files()
    
    results = {
        'files': [],
        'analysis_method': 'hybrid',
        'total_vulnerabilities': 0
    }
    
    for file_path in changed_files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        print(f"Analyzing {file_path}...")
        
        # Try Auralis API first
        file_result = analyze_file(api_url, file_path)
        
        # Fallback to Slither if API fails
        if not file_result:
            print(f"API analysis failed, trying Slither...")
            slither_vulns = run_slither(file_path)
            if slither_vulns:
                file_result = {
                    'filename': file_path,
                    'risk_score': min(len(slither_vulns) * 15, 100),
                    'vulnerabilities': slither_vulns,
                    'analysis_method': 'slither'
                }
        
        if file_result:
            results['files'].append(file_result)
            results['total_vulnerabilities'] += len(file_result.get('vulnerabilities', []))
    
    # Write results to file for GitHub Actions
    with open('auralis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAnalysis complete: {len(results['files'])} files, {results['total_vulnerabilities']} vulnerabilities")
    
    # Exit with error code if critical vulnerabilities found
    critical_count = sum(
        1 for file in results['files'] 
        for vuln in file.get('vulnerabilities', []) 
        if vuln.get('severity') in ['Critical', 'High']
    )
    
    if critical_count > 0:
        print(f"⚠️  Found {critical_count} critical/high severity vulnerabilities")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == '__main__':
    main()
