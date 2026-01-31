import React, { useState, useRef, useEffect, useCallback } from 'react';
import '../styles/CodeEditor.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Sample contracts for quick demo
const SAMPLE_CONTRACTS = {
  reentrancy: {
    name: "🔓 Reentrancy Attack",
    code: `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// VULNERABLE: Classic Reentrancy Attack
contract VulnerableBank {
    mapping(address => uint256) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    // VULNERABLE: State change after external call
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // External call BEFORE state update - VULNERABLE!
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        // State update AFTER external call - TOO LATE!
        balances[msg.sender] -= amount;
    }
}`
  },
  access: {
    name: "🔑 Access Control",
    code: `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// VULNERABLE: Multiple access control issues
contract VulnerableVault {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    // VULNERABLE: tx.origin instead of msg.sender
    modifier onlyOwner() {
        require(tx.origin == owner, "Not owner");
        _;
    }
    
    // VULNERABLE: No access control!
    function withdrawAll() public {
        payable(msg.sender).transfer(address(this).balance);
    }
    
    // VULNERABLE: Unprotected selfdestruct
    function destroy() public {
        selfdestruct(payable(owner));
    }
    
    // VULNERABLE: Anyone can change owner
    function changeOwner(address newOwner) public {
        owner = newOwner;
    }
}`
  },
  flashloan: {
    name: "⚡ Flash Loan",
    code: `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IUniswapPair {
    function getReserves() external view returns (uint112, uint112, uint32);
}

// VULNERABLE: Flash loan attack vector
contract VulnerableLending {
    IUniswapPair public pair;
    mapping(address => uint256) public borrowed;
    
    // VULNERABLE: Spot price from DEX can be manipulated
    function getPrice() public view returns (uint256) {
        (uint112 reserve0, uint112 reserve1,) = pair.getReserves();
        return (reserve1 * 1e18) / reserve0;
    }
    
    // VULNERABLE: Uses manipulable spot price
    function borrow(uint256 collateralAmount) public {
        uint256 price = getPrice();
        uint256 borrowAmount = (collateralAmount * price) / 1e18;
        borrowed[msg.sender] += borrowAmount;
    }
}`
  },
  randomness: {
    name: "🎲 Weak Randomness",
    code: `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// VULNERABLE: Predictable randomness
contract VulnerableLottery {
    address[] public players;
    
    function buyTicket() public payable {
        players.push(msg.sender);
    }
    
    // VULNERABLE: Miner can predict/manipulate
    function pickWinner() public {
        uint256 random = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.difficulty,
            block.number
        )));
        
        uint256 winnerIndex = random % players.length;
        payable(players[winnerIndex]).transfer(address(this).balance);
    }
}`
  }
};

function CodeEditor({ onAnalyze, highlightLine }) {
  const [code, setCode] = useState(`// SPDX-License-Identifier: MIT
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
}`);

  const [showSamples, setShowSamples] = useState(false);
  const [copied, setCopied] = useState(false);
  const textareaRef = useRef(null);

  // Keyboard shortcut: Ctrl+Enter to analyze
  const handleKeyDown = useCallback((e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      onAnalyze(code);
    }
  }, [code, onAnalyze]);

  useEffect(() => {
    if (highlightLine && textareaRef.current) {
      const lines = code.split('\n');
      let charCount = 0;
      
      for (let i = 0; i < highlightLine - 1; i++) {
        charCount += lines[i].length + 1;
      }
      
      const lineStart = charCount;
      const lineEnd = charCount + (lines[highlightLine - 1]?.length || 0);
      
      textareaRef.current.focus();
      textareaRef.current.setSelectionRange(lineStart, lineEnd);
      textareaRef.current.scrollTop = (highlightLine - 5) * 20;
    }
  }, [highlightLine, code]);

  const handleAnalyze = () => {
    onAnalyze(code);
  };

  const loadSample = (sampleKey) => {
    setCode(SAMPLE_CONTRACTS[sampleKey].code);
    setShowSamples(false);
  };

  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const clearCode = () => {
    setCode('');
    textareaRef.current?.focus();
  };

  return (
    <div className="code-editor">
      <div className="editor-header">
        <h3>📝 Smart Contract Code</h3>
        <div className="editor-actions">
          <div className="sample-dropdown">
            <button 
              className="sample-btn"
              onClick={() => setShowSamples(!showSamples)}
              title="Load sample vulnerable contract"
            >
              📋 Samples
            </button>
            {showSamples && (
              <div className="sample-menu">
                {Object.entries(SAMPLE_CONTRACTS).map(([key, sample]) => (
                  <button 
                    key={key}
                    className="sample-item"
                    onClick={() => loadSample(key)}
                  >
                    {sample.name}
                  </button>
                ))}
              </div>
            )}
          </div>
          <button onClick={copyCode} className="icon-btn" title="Copy code">
            {copied ? '✅' : '📋'}
          </button>
          <button onClick={clearCode} className="icon-btn" title="Clear editor">
            🗑️
          </button>
          <button onClick={handleAnalyze} className="analyze-btn">
            🔍 Analyze <span className="shortcut">Ctrl+Enter</span>
          </button>
        </div>
      </div>
      <textarea
        ref={textareaRef}
        value={code}
        onChange={(e) => setCode(e.target.value)}
        onKeyDown={handleKeyDown}
        className="code-textarea"
        spellCheck="false"
        placeholder="Paste your Solidity contract code here..."
        aria-label="Smart contract code editor"
        aria-describedby="code-editor-description"
      />
      <div className="editor-footer">
        <span className="line-count">{code.split('\n').length} lines</span>
        <span className="char-count">{code.length} characters</span>
        <span className="hint">💡 Tip: Press Ctrl+Enter to analyze</span>
      </div>
      <div id="code-editor-description" className="sr-only">
        Enter your Solidity smart contract code for security analysis
      </div>
    </div>
  );
}

export default CodeEditor;
