# Auralis VS Code Extension

AI-powered smart contract security auditor with real-time inline diagnostics and vulnerability visualization.

## Features

### 🔍 Real-Time Inline Diagnostics
- Squiggly-line alerts for vulnerabilities as you code
- Hover popups with detailed descriptions
- One-click AI-powered fixes

### 🌳 Vulnerability Tree View
- Sidebar showing all issues grouped by file and severity
- Quick navigation to vulnerable code
- Risk score overview

### 📊 Interactive Control Flow Graph
- Visual representation of function calls and dependencies
- Clickable nodes to jump to code
- Identify complex execution paths

### 🤖 AI-Powered Analysis
- Hybrid static + AI analysis using AWS Bedrock
- Context-aware vulnerability detection
- Smart remediation suggestions

## Installation

### Prerequisites
- VS Code 1.80.0 or higher
- Node.js 18+ and npm
- Auralis backend running (see backend setup)

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/your-org/auralis.git
cd auralis/vscode-extension
```

2. Install dependencies:
```bash
npm install
```

3. Compile the extension:
```bash
npm run compile
```

4. Package the extension:
```bash
npm run package
```

5. Install the `.vsix` file in VS Code:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Click "..." menu → "Install from VSIX"
   - Select `auralis-vscode-0.1.0.vsix`

## Configuration

Open VS Code settings and configure Auralis:

```json
{
  "auralis.apiEndpoint": "http://localhost:8000",
  "auralis.enableRealTimeAnalysis": true,
  "auralis.enableSlither": false
}
```

### Settings

- `auralis.apiEndpoint`: URL of the Auralis backend API
- `auralis.enableRealTimeAnalysis`: Auto-analyze on file save
- `auralis.enableSlither`: Enable Slither integration (requires Slither installed)

## Usage

### Analyze Current Contract

1. Open a `.sol` file
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Auralis: Analyze Contract"
4. View results in the Problems panel and Vulnerability Tree

### View Vulnerability Tree

1. Click the Auralis icon in the sidebar
2. Expand files to see vulnerabilities grouped by severity
3. Click on a vulnerability to jump to the code

### Show Control Flow Graph

1. Open a `.sol` file
2. Press `Ctrl+Shift+P`
3. Type "Auralis: Show Control Flow Graph"
4. Interactive graph opens in a new panel

### Apply AI Fix

1. Hover over a vulnerability (squiggly line)
2. Click "Quick Fix" or press `Ctrl+.`
3. Select "Auralis: Apply AI Fix"
4. Review and save the changes

## Commands

- `Auralis: Analyze Contract` - Analyze the current Solidity file
- `Auralis: Show Vulnerability Tree` - Open the vulnerability sidebar
- `Auralis: Show Control Flow Graph` - Display interactive control flow
- `Auralis: Apply AI Fix` - Apply suggested fix for a vulnerability

## Development

### Run in Development Mode

1. Open the extension folder in VS Code
2. Press `F5` to launch Extension Development Host
3. Test the extension in the new window

### Watch Mode

```bash
npm run watch
```

### Run Tests

```bash
npm test
```

## Troubleshooting

### Extension Not Activating

- Ensure you have a `.sol` file open
- Check the Output panel (View → Output → Auralis)

### Cannot Connect to API

- Verify the backend is running: `curl http://localhost:8000/health`
- Check `auralis.apiEndpoint` setting
- Review firewall/network settings

### No Vulnerabilities Detected

- Ensure the file contains valid Solidity code
- Check if the backend is properly configured
- Review backend logs for errors

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](../LICENSE)

## Support

- GitHub Issues: https://github.com/your-org/auralis/issues
- Documentation: https://github.com/your-org/auralis/docs

---

**Powered by Auralis 🛡️**
