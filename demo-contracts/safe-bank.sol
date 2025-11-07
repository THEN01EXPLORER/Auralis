// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title SafeBank
 * @dev SECURE VERSION - Demonstrates proper security practices
 * 
 * This contract fixes the vulnerabilities from VulnerableBank:
 * 1. Uses Checks-Effects-Interactions pattern
 * 2. Includes ReentrancyGuard
 * 3. Proper error handling
 */

contract SafeBank {
    mapping(address => uint) public balances;
    bool private locked;
    
    event Deposit(address indexed user, uint amount);
    event Withdrawal(address indexed user, uint amount);
    
    /**
     * @dev Prevents reentrancy attacks
     */
    modifier nonReentrant() {
        require(!locked, "Reentrant call");
        locked = true;
        _;
        locked = false;
    }
    
    /**
     * @dev Deposit ETH into the contract
     */
    function deposit() public payable {
        require(msg.value > 0, "Must deposit something");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }
    
    /**
     * @dev Withdraw ETH from the contract
     * SECURE: Follows Checks-Effects-Interactions pattern
     */
    function withdraw(uint amount) public nonReentrant {
        // CHECKS: Validate conditions
        require(amount > 0, "Amount must be positive");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // EFFECTS: Update state BEFORE external call
        balances[msg.sender] -= amount;
        
        // INTERACTIONS: External call happens last
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        emit Withdrawal(msg.sender, amount);
    }
    
    /**
     * @dev Get contract balance
     */
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
    
    /**
     * @dev Get user balance
     */
    function getUserBalance(address user) public view returns (uint) {
        return balances[user];
    }
}
