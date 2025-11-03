# Day 3 Testing Guide - Making It Functional

## ✅ Task 1: Real Risk Score Calculation

### What Changed:
- Backend now analyzes ACTUAL code instead of returning hardcoded vulnerabilities
- Risk score is dynamically calculated based on severity:
  - Critical = 40 points
  - High = 20 points  
  - Medium = 10 points
  - Low = 5 points
  - Total capped at 100

### Test It:
1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm start`
3. Try different contracts:

**Test Case 1: Clean Contract (Score: 0)**
```solidity
pragma solidity ^0.8.0;
contract Safe {
    uint public value;
    function setValue(uint _value) public view {
        // Safe function
    }
}
```
Expected: Risk Score = 0/100

**Test Case 2: One Critical Issue (Score: 40)**
```solidity
contract Test {
    function withdraw() public {
        msg.sender.call{value: 1 ether}("");
    }
}
```
Expected: Risk Score = 40/100 (1 Critical)

**Test Case 3: Multiple Issues (Score: 60+)**
```solidity
contract VulnerableBank {
    mapping(address => uint) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw(uint amount) public {
        (bool success, ) = msg.sender.call{value: amount}("");
        balances[msg.sender] -= amount;
    }
}
```
Expected: Risk Score = 60+ (Critical + High + Medium)

## ✅ Task 2: Line Highlighting

### What Works:
- Click on any line number in vulnerability report
- Code editor automatically scrolls to that line
- Line gets highlighted/selected

### Test It:
1. Analyze the default contract
2. In the right panel, click "Line 14" on Re-entrancy vulnerability
3. Watch the left panel scroll and highlight line 14
4. Click "Line 8" on Access Control vulnerability
5. Watch it jump to line 8

## ✅ Task 3: Remediation "Show Fix" Feature

### What Works:
- Each vulnerability is collapsible
- Click anywhere on vulnerability card to expand
- Shows detailed fix explanation
- Shows code example with proper syntax

### Test It:
1. Analyze any contract with vulnerabilities
2. Click on a vulnerability card (anywhere on it)
3. See it expand with:
   - 💡 Recommendation section
   - 🔧 How to Fix section
   - Code example in dark code block
4. Click again to collapse

## 🎥 OBS Recording Checklist

### Video 1: Dynamic Risk Score (1-2 min)
- [ ] Show current UI with hardcoded score
- [ ] Show backend code before changes
- [ ] Prompt Amazon Q for risk calculation
- [ ] Implement the code
- [ ] Test with different contracts showing different scores
- [ ] Highlight how score changes based on severity

### Video 2: Line Highlighting (1 min)
- [ ] Show vulnerability list
- [ ] Click on line numbers
- [ ] Show editor jumping to each line
- [ ] Demonstrate on 3-4 different vulnerabilities

### Video 3: Remediation Feature (2-3 min) ⭐ STAR FOOTAGE
- [ ] Show app before (collapsed vulnerabilities)
- [ ] Click to expand first vulnerability
- [ ] Show the "How to Fix" section
- [ ] Show the code example
- [ ] Expand 2-3 different vulnerabilities
- [ ] Highlight the professional UI

## Victory Conditions ✅

By end of Day 3, you have:
- [x] Dynamic risk score calculation
- [x] Interactive line highlighting
- [x] Expandable remediation with code examples
- [x] Professional, polished UI
- [x] Full frontend-backend integration

## Next Steps (Day 4)

- AWS Bedrock real AI integration
- Database persistence
- Multi-chain support
- Deployment to production
