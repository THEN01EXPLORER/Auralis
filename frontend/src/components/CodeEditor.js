import React, { useState } from 'react';
import '../styles/CodeEditor.css';

function CodeEditor({ onAnalyze }) {
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

  const handleAnalyze = () => {
    onAnalyze(code);
  };

  return (
    <div className="code-editor">
      <div className="editor-header">
        <h3>Smart Contract Code</h3>
        <button onClick={handleAnalyze} className="analyze-btn">
          Analyze Contract
        </button>
      </div>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="code-textarea"
        spellCheck="false"
      />
    </div>
  );
}

export default CodeEditor;
