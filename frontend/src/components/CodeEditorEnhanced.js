import React, { useState } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { javascript } from '@codemirror/lang-javascript';
import '../styles/CodeEditor.css';

function CodeEditorEnhanced({ onAnalyze, vulnerabilities = [] }) {
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

  return (
    <div className="code-editor">
      <div className="editor-header">
        <h3>Smart Contract Code</h3>
        <button onClick={() => onAnalyze(code)} className="analyze-btn">
          Analyze Contract
        </button>
      </div>
      <CodeMirror
        value={code}
        height="400px"
        theme="dark"
        extensions={[javascript()]}
        onChange={(value) => setCode(value)}
        className="code-mirror"
      />
    </div>
  );
}

export default CodeEditorEnhanced;
