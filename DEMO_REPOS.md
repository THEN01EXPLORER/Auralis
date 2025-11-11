# 📦 Demo Repository URLs for Video

**Purpose:** List of public GitHub repositories with Solidity contracts for testing the repo scanner feature in the demo video.

---

## Recommended Demo Repos

### Option 1: Small, Simple Repos (Best for Demo)

**1. OpenZeppelin Contracts (Specific Folder)**
```
https://github.com/OpenZeppelin/openzeppelin-contracts
```
- **Pros:** Well-known, professional, many contracts
- **Cons:** Large repo, may take longer to clone
- **Best for:** Showing credibility

**2. Simple DeFi Examples**
```
https://github.com/scaffold-eth/scaffold-eth-examples
```
- **Pros:** Educational, clear contract names
- **Cons:** May have many non-Solidity files
- **Best for:** Showing real-world use case

**3. Your Own Test Repo (Recommended)**
Create a small test repo with 2-3 contracts:
```
https://github.com/yourusername/test-contracts
```
- **Pros:** Full control, fast, predictable results
- **Cons:** Need to create it first
- **Best for:** Controlled demo environment

---

## Creating Your Own Demo Repo

### Quick Setup (5 minutes)

1. **Create new GitHub repo:**
   - Name: `auralis-demo-contracts`
   - Description: "Sample vulnerable contracts for Auralis demo"
   - Public
   - Add README

2. **Add 3 contracts:**

**contracts/VulnerableBank.sol** (copy from demo-contracts/)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint256) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount);
        (bool success, ) = msg.sender.call{value: amount}("");
        balances[msg.sender] -= amount;
    }
}
```

**contracts/UnsafeToken.sol**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UnsafeToken {
    mapping(address => uint256) public balances;
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function mint(address to, uint256 amount) public {
        // VULNERABILITY: No access control
        balances[to] += amount;
    }
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

**contracts/TimeLock.sol**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeLock {
    mapping(address => uint256) public lockTime;
    mapping(address => uint256) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
        lockTime[msg.sender] = block.timestamp + 1 weeks;
    }
    
    function withdraw() public {
        // VULNERABILITY: Timestamp dependence
        require(block.timestamp >= lockTime[msg.sender]);
        require(balances[msg.sender] > 0);
        
        uint256 amount = balances[msg.sender];
        balances[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
```

3. **Commit and push:**
```bash
git add .
git commit -m "Add demo contracts"
git push
```

4. **Use in demo:**
```
https://github.com/yourusername/auralis-demo-contracts
```

---

## Demo Script for Repo Scanner

### What to Say
> "And here's where it gets even better. Let me show you the repository scanner. I'll paste a GitHub URL—this is a repo with three different Solidity contracts."

### What to Do
1. Scroll down to "Analyze GitHub Repository" section
2. Paste your demo repo URL
3. Click "Analyze Repo"
4. Wait for loading (2-3 seconds)
5. Show the results:
   - Point to "3 files analyzed"
   - Point to "X total vulnerabilities"
   - Click first tab: "VulnerableBank.sol"
   - Show its vulnerabilities
   - Click second tab: "UnsafeToken.sol"
   - Show its vulnerabilities
   - Click third tab: "TimeLock.sol"
   - Show its vulnerabilities

### What to Say (continued)
> "See these tabs? Each one is a different file. VulnerableBank has a reentrancy issue. UnsafeToken has missing access control. TimeLock has timestamp dependence. Three contracts analyzed in seconds. This is how you audit an entire project at once."

---

## Backup Repos (If Primary Fails)

### Public Vulnerable Contract Collections

**1. Damn Vulnerable DeFi**
```
https://github.com/tinchoabbate/damn-vulnerable-defi
```
- Intentionally vulnerable contracts for learning
- Well-documented
- May have many files

**2. Ethernaut Challenges**
```
https://github.com/OpenZeppelin/ethernaut
```
- Security challenges with vulnerable contracts
- Educational
- Good variety of vulnerabilities

**3. SWC Registry Examples**
```
https://github.com/SmartContractSecurity/SWC-registry
```
- Smart contract weakness classification
- Each weakness has example contract
- Very educational

---

## Testing Your Demo Repo

Before recording, test your demo repo:

1. **Start backend:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Test repo scanner:**
   - Open http://localhost:3000
   - Paste your demo repo URL
   - Click "Analyze Repo"
   - Verify it works correctly
   - Check that all files appear in tabs
   - Verify vulnerabilities are detected

4. **Time the analysis:**
   - Should complete in 10-30 seconds
   - If longer, consider using smaller repo

5. **Note the results:**
   - How many files?
   - How many total vulnerabilities?
   - Which files have the most issues?
   - Use this info in your narration

---

## Troubleshooting

**Problem:** Repo takes too long to clone
**Solution:** Use smaller repo or specific branch/folder

**Problem:** No .sol files found
**Solution:** Verify repo has Solidity contracts in root or contracts/ folder

**Problem:** Analysis fails for some files
**Solution:** This is okay! Show the error handling in the UI

**Problem:** Too many files (10+)
**Solution:** Use smaller repo or create your own with 2-3 contracts

---

## Demo Repo Checklist

Before recording:
- [ ] Demo repo created and pushed to GitHub
- [ ] Repo is public (not private)
- [ ] Contains 2-3 Solidity contracts
- [ ] Contracts have intentional vulnerabilities
- [ ] Tested with Auralis locally
- [ ] Analysis completes in under 30 seconds
- [ ] All files appear in tabs
- [ ] Vulnerabilities are detected
- [ ] URL copied and ready to paste

---

## Alternative: Use Local Git Server (Advanced)

If you want full control without GitHub dependency:

1. Install local Git server (Gitea, GitLab)
2. Create local repo with contracts
3. Use local URL in demo
4. Pros: No internet dependency, full control
5. Cons: More setup, less impressive (not "real" GitHub)

**Recommendation:** Use real GitHub repo for authenticity

---

**Your demo repo is the "wow" moment. Make it count!** 🚀
