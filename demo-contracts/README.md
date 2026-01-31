# Demo Contracts for Auralis

This folder contains sample smart contracts for demonstrating Auralis capabilities.

## Contracts

### 1. vulnerable-bank.sol
**Purpose:** Demonstrates vulnerability detection

**Vulnerabilities:**
- ✗ Reentrancy attack in `withdraw()`
- ✗ No access control
- ✗ Unchecked external call
- ✗ State update after external call

**Use Case:** Show how Auralis detects and explains vulnerabilities

---

### 2. safe-bank.sol
**Purpose:** Demonstrates secure coding practices

**Security Features:**
- ✓ Checks-Effects-Interactions pattern
- ✓ ReentrancyGuard modifier
- ✓ Proper error handling
- ✓ State updates before external calls

**Use Case:** Show the "after" version with fixes applied

---

## Usage in Demo Video

### Step 1: Show Vulnerable Contract
1. Paste `vulnerable-bank.sol` into Auralis
2. Click "Analyze"
3. Show detected vulnerabilities
4. Highlight source badges (Static/AI/Hybrid)
5. Show confidence scores

### Step 2: Show Remediation
1. Click "Show Fix" on reentrancy vulnerability
2. Show explanation
3. Show code example
4. Compare with `safe-bank.sol`

### Step 3: Verify Fix
1. Paste `safe-bank.sol` into Auralis
2. Click "Analyze"
3. Show zero or minimal vulnerabilities
4. Demonstrate the improvement

---

## Quick Copy-Paste (for video)

**Vulnerable Version (use this in demo):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount);
        (bool success, ) = msg.sender.call{value: amount}("");
        balances[msg.sender] -= amount;
    }
}
```

---

## Expected Auralis Output

### For vulnerable-bank.sol:
- **Risk Score:** 75-85/100
- **Vulnerabilities Found:** 3-5
- **Severity:** High (Reentrancy)
- **Source:** Hybrid (detected by both static and AI)
- **Confidence:** 95%+

### For safe-bank.sol:
- **Risk Score:** 15-25/100
- **Vulnerabilities Found:** 0-1
- **Severity:** Low/Info
- **Source:** Static
- **Confidence:** Varies

---

## Tips for Demo

1. **Start with vulnerable:** Show the problem first
2. **Highlight hybrid detection:** Emphasize AI + Static working together
3. **Show Fix feature:** This is your "wow" moment
4. **Compare before/after:** Show the improvement
5. **Keep it simple:** Don't get lost in technical details

---

## Additional Test Cases

If you want to show more capabilities:

**Integer Overflow:**
```solidity
function unsafeAdd(uint a, uint b) public pure returns (uint) {
    return a + b;  // No overflow check
}
```

**Access Control:**
```solidity
function withdraw() public {
    // Anyone can withdraw!
    payable(msg.sender).transfer(address(this).balance);
}
```

**Unchecked Call:**
```solidity
function send(address to) public {
    to.call{value: 1 ether}("");  // Return value not checked
}
```

---

**These contracts are ready for your demo video!** 🎬
