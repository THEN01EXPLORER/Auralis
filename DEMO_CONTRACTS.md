# Demo Smart Contracts for Testing

## Contract 1: Clean & Safe (Risk Score: 0)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SafeContract {
    uint256 public value;
    
    function getValue() public view returns (uint256) {
        return value;
    }
}
```

## Contract 2: Single Critical Issue (Risk Score: 40)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReentrancyVulnerable {
    mapping(address => uint) public balances;
    
    function withdraw() public {
        uint amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        balances[msg.sender] = 0;
    }
}
```

## Contract 3: Multiple Issues (Risk Score: 60+)
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
    
    function adminWithdraw() public {
        payable(msg.sender).transfer(address(this).balance);
    }
}
```

## Contract 4: Maximum Risk (Risk Score: 100)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract HighlyVulnerable {
    mapping(address => uint) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw(uint amount) public {
        (bool success, ) = msg.sender.call{value: amount}("");
        balances[msg.sender] -= amount;
    }
    
    function transfer(address to, uint amount) public {
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
    
    function emergencyWithdraw() public {
        msg.sender.call{value: address(this).balance}("");
    }
}
```

## How to Use

1. Copy any contract above
2. Paste into Auralis code editor
3. Click "Analyze Contract"
4. Watch the risk score change dynamically
5. Click on vulnerabilities to see line highlighting
6. Expand vulnerabilities to see fixes
