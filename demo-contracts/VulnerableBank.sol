// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title VulnerableBank
 * @dev INTENTIONALLY VULNERABLE CONTRACT FOR DEMO PURPOSES
 * DO NOT USE IN PRODUCTION
 * 
 * This contract contains multiple security vulnerabilities for demonstration:
 * - Reentrancy attack vulnerability
 * - Missing access control
 * - Unchecked external call
 * - State changes after external calls
 */
contract VulnerableBank {
    mapping(address => uint256) public balances;
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    /**
     * @dev Deposit funds into the bank
     */
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    /**
     * @dev Withdraw funds - VULNERABLE TO REENTRANCY
     * The external call happens before state update
     */
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // VULNERABILITY: External call before state change
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        // VULNERABILITY: State change after external call
        balances[msg.sender] -= amount;
    }
    
    /**
     * @dev Emergency withdrawal - MISSING ACCESS CONTROL
     * Anyone can call this function!
     */
    function emergencyWithdraw() public {
        // VULNERABILITY: No access control check
        payable(msg.sender).transfer(address(this).balance);
    }
    
    /**
     * @dev Get contract balance
     */
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
    
    /**
     * @dev Get user balance
     */
    function getUserBalance(address user) public view returns (uint256) {
        return balances[user];
    }
}
