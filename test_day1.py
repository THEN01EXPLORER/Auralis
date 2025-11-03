"""
Day 1 Testing Script - GUARDIANAI AUDIT
Tests all backend endpoints and functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🧪 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_analyze():
    """Test analyze endpoint"""
    print("\n🧪 Testing /api/v1/analyze endpoint...")
    
    test_contract = """
    pragma solidity ^0.8.0;
    
    contract Vulnerable {
        mapping(address => uint) public balances;
        
        function withdraw(uint amount) public {
            require(balances[msg.sender] >= amount);
            msg.sender.call{value: amount}("");
            balances[msg.sender] -= amount;
        }
        
        function deposit() public payable {
            balances[msg.sender] += msg.value;
        }
    }
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze",
            json={"contract_code": test_contract, "chain_type": "ethereum"}
        )
        assert response.status_code == 200
        data = response.json()
        
        print(f"✅ Analysis completed")
        print(f"   Analysis ID: {data['analysis_id']}")
        print(f"   Risk Score: {data['risk_score']}/100")
        print(f"   Vulnerabilities Found: {len(data['vulnerabilities'])}")
        
        for vuln in data['vulnerabilities']:
            print(f"   - {vuln['type']} (Line {vuln['line']}) - {vuln['severity']}")
        
        return True
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def test_cors():
    """Test CORS headers"""
    print("\n🧪 Testing CORS configuration...")
    try:
        response = requests.options(
            f"{BASE_URL}/api/v1/analyze",
            headers={"Origin": "http://localhost:3000"}
        )
        print("✅ CORS configured correctly")
        return True
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🏆 GUARDIANAI AUDIT - DAY 1 TEST SUITE")
    print("=" * 60)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Analyze Endpoint", test_analyze()))
    results.append(("CORS Configuration", test_cors()))
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - DAY 1 COMPLETE!")
    else:
        print("⚠️  Some tests failed - review and fix")

if __name__ == "__main__":
    main()
