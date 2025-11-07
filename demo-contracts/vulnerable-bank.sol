// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title VulnerableBank
 * @dev INTENTIONALLY VULNERABLE - For demonstration purposes only
 * 
 * This contract contains multiple security vulnerabilities:
 * 1. Reentrancy attack in withdraw()
 * 2. No access control on critical functions
 * 3. Unchecked external call
 */

contract VulnerableBank {
    mapping(address => uint) public balances;
    
    event Deposit(address indexed user, uint amount);
    event Withdrawal(address indexed user, uint amount);
    
    /**
     * @dev Deposit ETH into the contract
     */
    function deposit() public payable {
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }
    
    /**
     * @dev Withdraw ETH from the contract
     * VULNERABLE: Reentrancy attack possible!
     * The balance is updated AFTER the external call
     */
    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // VULNERABILITY: External call before state update
        (bool success, ) = msg.sender.call{value: amount}("");
        
        // State update happens after external call - DANGEROUS!
        balances[msg.sender] -= amount;
        
        emit Withdrawal(msg.sender, amount);
    }
    
    /**
     * @dev Get contract balance
     */
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}
