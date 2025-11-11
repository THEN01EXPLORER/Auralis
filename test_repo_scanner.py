"""
Quick test script for the new repo scanner endpoint.
This verifies Day 1 implementation is working correctly.
"""
import requests
import json

# Test the repo scanner with a small public repo
def test_repo_scanner():
    url = "http://localhost:8000/api/v1/analyze_repo"
    
    # Using a small test repo (you can replace with your own)
    payload = {
        "github_url": "https://github.com/yourusername/test-contracts"
    }
    
    print("Testing repo scanner endpoint...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ SUCCESS!")
            print(f"Files analyzed: {result.get('files_analyzed', 0)}")
            print(f"Total vulnerabilities: {result.get('total_vulnerabilities', 0)}")
            print(f"Processing time: {result.get('processing_time_ms', 0)}ms")
            print(f"\nFiles in results:")
            for filename in result.get('results', {}).keys():
                print(f"  - {filename}")
        else:
            print(f"\n✗ FAILED")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n✗ Connection failed. Make sure the backend is running on localhost:8000")
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    test_repo_scanner()
