# 🚀 Auralis Installation Guide

Complete setup instructions for the Auralis MVP.

## Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18 or higher
- **VS Code**: 1.80.0 or higher
- **Git**: For cloning the repository
- **AWS Account**: (Optional) For AI analysis with Bedrock

## Quick Install (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/your-org/auralis.git
cd auralis
git checkout feature/mvp-ide-prbot
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Optional: Install Slither
bash ../tools/install_slither.sh  # Linux/Mac
# or
..\tools\install_slither.bat      # Windows

# Start backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Verify: Open http://localhost:8000/health

### 3. VS Code Extension Setup

```bash
cd vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Package extension
npm run package
```

### 4. Install Extension in VS Code

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Click "..." menu → "Install from VSIX"
4. Select `vscode-extension/auralis-vscode-0.1.0.vsix`
5. Reload VS Code

### 5. Configure VS Code

Open Settings (Ctrl+,) and add:

```json
{
  "auralis.apiEndpoint": "http://localhost:8000",
  "auralis.enableRealTimeAnalysis": true,
  "auralis.enableSlither": false
}
```

## Detailed Installation

### Backend Configuration

#### Environment Variables

Create `backend/.env`:

```bash
# API Configuration
AURALIS_API_URL=http://localhost:8000
LOG_LEVEL=INFO

# AWS Bedrock (Optional)
AWS_REGION=us-east-1
ENABLE_AI_ANALYSIS=true
AI_ANALYSIS_REQUIRED=false
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_TIMEOUT=25

# AWS Credentials (if not using IAM role)
# AWS_ACCESS_KEY_ID=your_key
# AWS_SECRET_ACCESS_KEY=your_secret
```

#### Install Optional Dependencies

```bash
# For PDF generation
pip install reportlab

# For Slither integration
pip install slither-analyzer solc-select

# For development
pip install pytest pytest-asyncio black flake8
```

### VS Code Extension Development

#### Run in Development Mode

1. Open `vscode-extension` folder in VS Code
2. Press F5 to launch Extension Development Host
3. Test in the new VS Code window

#### Watch Mode

```bash
cd vscode-extension
npm run watch
```

This auto-compiles TypeScript on file changes.

### GitHub Actions Setup

#### Configure Repository Secrets

1. Go to GitHub repo → Settings → Secrets
2. Add secrets:
   - `AURALIS_API_URL`: Your deployed API endpoint
   - `GITHUB_TOKEN`: (Automatically provided)

#### Enable GitHub Actions

1. Go to Actions tab
2. Enable workflows if disabled
3. Workflows will run on PR creation

## Verification

### Test Backend

```bash
# Health check
curl http://localhost:8000/health

# Analyze contract
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "contract Test { function test() public {} }"}'

# Generate PDF report
curl -X POST http://localhost:8000/api/v1/generate_report \
  -H "Content-Type: application/json" \
  -d '{"code": "contract Test { function test() public {} }"}' \
  --output test_report.pdf

# Calculate DREAD scores
curl -X POST http://localhost:8000/api/v1/dread_score \
  -H "Content-Type: application/json" \
  -d '{"code": "contract Test { function test() public {} }"}'
```

### Test VS Code Extension

1. Open a `.sol` file in VS Code
2. Save the file (Ctrl+S)
3. Check for:
   - Squiggly lines on vulnerabilities
   - Auralis icon in sidebar
   - Problems panel entries

### Test GitHub Action

1. Create a test branch
2. Add/modify a `.sol` file
3. Create a PR
4. Check for Auralis bot comment

## Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
pip install -r requirements.txt
```

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill the process or use different port
python -m uvicorn main:app --port 8001
```

### VS Code Extension Not Working

**Issue**: Extension not activating

**Solution**:
1. Check you have a `.sol` file open
2. Reload VS Code: Ctrl+Shift+P → "Reload Window"
3. Check Output panel: View → Output → Auralis

**Issue**: Cannot connect to API

**Solution**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `auralis.apiEndpoint` setting
3. Check firewall/antivirus settings

### Slither Installation Issues

**Error**: `slither: command not found`

**Solution**:
```bash
pip install slither-analyzer
slither --version
```

**Error**: `solc not found`

**Solution**:
```bash
pip install solc-select
solc-select install 0.8.20
solc-select use 0.8.20
```

### PDF Generation Fails

**Error**: `reportlab not installed`

**Solution**:
```bash
pip install reportlab
```

### GitHub Action Fails

**Issue**: Workflow not triggering

**Solution**:
1. Ensure workflow file is on base branch
2. Check GitHub Actions are enabled
3. Verify PR contains `.sol` file changes

**Issue**: Slither not found in CI

**Solution**: Workflow installs Slither automatically. Check workflow logs for errors.

## Platform-Specific Notes

### Windows

- Use `venv\Scripts\activate` instead of `source venv/bin/activate`
- Use `python` instead of `python3`
- Use backslashes in paths: `..\tools\install_slither.bat`
- May need to run PowerShell as Administrator

### macOS

- May need to install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```
- Use Homebrew for Python if needed:
  ```bash
  brew install python@3.10
  ```

### Linux

- May need to install build tools:
  ```bash
  sudo apt-get install build-essential python3-dev
  ```

## Uninstallation

### Remove VS Code Extension

1. Extensions → Auralis → Uninstall
2. Reload VS Code

### Remove Backend

```bash
cd backend
deactivate  # Exit virtual environment
cd ..
rm -rf backend/venv
```

### Remove GitHub Action

Delete `.github/workflows/auralis-pr-bot.yml`

## Next Steps

- Read [MVP_README.md](./MVP_README.md) for usage examples
- Follow [DEMO_INSTRUCTIONS.md](./DEMO_INSTRUCTIONS.md) for demo setup
- Check [HACKATHON_JOURNAL.md](./HACKATHON_JOURNAL.md) for development log

## Support

- **Issues**: https://github.com/your-org/auralis/issues
- **Docs**: https://github.com/your-org/auralis/docs
- **Discord**: (Coming soon)

---

**Installation complete! Start securing your smart contracts with Auralis 🛡️**
