import React, { useState, useRef, useEffect } from 'react';
import '../styles/CodeEditor.css';

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

  const textareaRef = useRef(null);

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

  return (
    <div className="code-editor">
      <div className="editor-header">
        <h3>📝 Smart Contract Code</h3>
        <button onClick={handleAnalyze} className="analyze-btn">
          🔍 Analyze Contract
        </button>
      </div>
      <textarea
        ref={textareaRef}
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="code-textarea"
        spellCheck="false"
        placeholder="Paste your Solidity contract code here..."
        aria-label="Smart contract code editor"
        aria-describedby="code-editor-description"
      />
      <div id="code-editor-description" className="sr-only">
        Enter your Solidity smart contract code for security analysis
      </div>
    </div>
  );
}

export default CodeEditor;
