# 🛡️ Auralis MVP - Crawl Phase

**Branch**: `feature/mvp-ide-prbot`

This is the Hackathon MVP (Crawl phase) implementation of Auralis, featuring the core components for smart contract security auditing.

## 🎯 MVP Components

### 1. VS Code Extension (`vscode-extension/`)
Full-featured IDE plugin with:
- ✅ **Real-time inline diagnostics** - Squiggly lines + hover popups
- ✅ **Vulnerability tree view** - Sidebar with grouped issues by severity
- ✅ **Interactive control flow graph** - Visual function call graph
- ✅ **One-click AI fixes** - Apply remediation suggestions instantly
- ✅ **Auto-analyze on save** - Continuous security monitoring

### 2. GitHub PR Bot (`.github/workflows/auralis-pr-bot.yml`)
Automated PR security review:
- ✅ **Inline PR comments** - Vulnerabilities shown directly in code review
- ✅ **GitHub Suggestions** - One-click fix suggestions in PR
- ✅ **Summary comment** - Aggregate security report
- ✅ **Slither integration** - Fallback to Slither if API unavailable

### 3. Slither Integration (`backend/app/services/slither_service.py`)
Static analysis pipeline:
- ✅ **Slither wrapper** - Converts Slither output to Auralis format
- ✅ **Installation scripts** - `tools/install_slither.sh` and `.bat`
- ✅ **CI/CD ready** - Works in GitHub Actions
- ✅ **Hybrid analysis** - Combines with AI for better results

### 4. DREAD Risk Scoring (`backend/app/services/dread_scorer.py`)
Professional risk assessment:
- ✅ **DREAD matrix** - Damage, Reproducibility, Exploitability, Affected users, Discoverability
- ✅ **Vulnerability-specific scores** - Pre-configured for common issues
- ✅ **Aggregate metrics** - Overall risk assessment
- ✅ **API endpoint** - `/api/v1/dread_score`

### 5. PDF Report Generator (`backend/app/services/pdf_report_generator.py`)
One-click audit reports:
- ✅ **Professional formatting** - Executive summary + detailed findings
- ✅ **DREAD matrix table** - Visual risk breakdown
- ✅ **Color-coded severity** - Easy-to-read vulnerability list
- ✅ **API endpoint** - `/api/v1/generate_report`

### 6. Multi-Chain Adapter Interface (`backend/app/adapters/chain_adapter.py`)
Future-proof architecture:
- ✅ **Ethereum/Solidity** - Fully implemented
- 🔄 **Solana/Rust** - Interface ready (post-MVP)
- 🔄 **Move (Aptos/Sui)** - Interface ready (post-MVP)
- ✅ **Auto-detection** - Identifies blockchain from code

## 🚀 Quick Start

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Install Slither (optional but recommended)
bash ../tools/install_slither.sh  # Linux/Mac
# or
..\tools\install_slither.bat      # Windows

# Start the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### VS Code Extension Setup

```bash
cd vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Package extension
npm run package

# Install in VS Code
# Extensions → ... → Install from VSIX → select auralis-vscode-0.1.0.vsix
```

### Configure VS Code

Open VS Code settings (Ctrl+,) and add:

```json
{
  "auralis.apiEndpoint": "http://localhost:8000",
  "auralis.enableRealTimeAnalysis": true,
  "auralis.enableSlither": false
}
```

## 📖 Usage Examples

### 1. Analyze Contract in VS Code

1. Open a `.sol` file
2. Save the file (auto-analysis triggers)
3. View vulnerabilities in:
   - Problems panel (Ctrl+Shift+M)
   - Auralis sidebar
   - Inline squiggly lines

### 2. Generate PDF Report

```bash
curl -X POST http://localhost:8000/api/v1/generate_report \
  -H "Content-Type: application/json" \
  -d @contract.json \
  --output audit_report.pdf
```

### 3. Calculate DREAD Scores

```bash
curl -X POST http://localhost:8000/api/v1/dread_score \
  -H "Content-Type: application/json" \
  -d '{"code": "contract Test { ... }"}' \
  | jq .
```

### 4. Test GitHub PR Bot

1. Create a PR with `.sol` file changes
2. Bot automatically comments with vulnerabilities
3. Click "Apply suggestion" to fix issues

## 🧪 Testing

### Run All Tests

```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# VS Code extension tests
cd vscode-extension
npm test

# Integration tests
# (Requires backend running on port 8000)
curl http://localhost:8000/health
```

### Run Demo Workflow

```bash
# Trigger GitHub Actions workflow
git push origin feature/mvp-ide-prbot

# Or manually trigger
# GitHub → Actions → Auralis MVP Demo → Run workflow
```

## 📦 Deliverables Checklist

- [x] VS Code extension with inline diagnostics
- [x] Vulnerability tree view sidebar
- [x] Interactive control flow graph
- [x] GitHub Action PR bot
- [x] Inline PR comments with suggestions
- [x] Slither integration + install scripts
- [x] DREAD risk scoring system
- [x] PDF report generator
- [x] Multi-chain adapter interface
- [x] API endpoints for all features
- [x] Demo workflow (CI/CD)
- [ ] Demo video (60s)
- [ ] Demo PR with screenshots
- [ ] Unit tests for extension
- [ ] End-to-end tests

## 🎬 Demo Video Script (60s)

**[0-10s] Hook**
"Smart contract hacks cost billions. Traditional tools miss complex vulnerabilities."

**[10-25s] VS Code Extension**
- Open vulnerable contract
- Show inline diagnostics appearing
- Hover over vulnerability
- Click "Apply Fix"
- Show vulnerability tree

**[25-40s] GitHub PR Bot**
- Open PR with vulnerable code
- Show bot comment with findings
- Click "Apply suggestion"
- Show inline comments

**[40-50s] PDF Report**
- Click "Generate Report"
- Show professional PDF with DREAD matrix
- Highlight risk scores

**[50-60s] Close**
"Auralis: AI-powered security for Web3. Built with AWS Bedrock."

## 🔧 Configuration

### Environment Variables

```bash
# Backend
export AURALIS_API_URL=http://localhost:8000
export AWS_REGION=us-east-1
export ENABLE_AI_ANALYSIS=true
export BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

# GitHub Actions
AURALIS_API_URL=https://your-api.com
GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
```

### VS Code Settings

```json
{
  "auralis.apiEndpoint": "http://localhost:8000",
  "auralis.enableRealTimeAnalysis": true,
  "auralis.enableSlither": false
}
```

## 🐛 Troubleshooting

### VS Code Extension Not Working

1. Check backend is running: `curl http://localhost:8000/health`
2. Verify settings: `auralis.apiEndpoint`
3. Check Output panel: View → Output → Auralis
4. Reload window: Ctrl+Shift+P → "Reload Window"

### GitHub Action Failing

1. Check `AURALIS_API_URL` secret is set
2. Verify Slither installation in workflow
3. Check changed files contain `.sol` files
4. Review workflow logs in Actions tab

### PDF Generation Error

```bash
# Install reportlab
pip install reportlab

# Test PDF generation
python -c "from app.services.pdf_report_generator import PDFReportGenerator; print(PDFReportGenerator().available)"
```

### Slither Not Found

```bash
# Install Slither
pip install slither-analyzer

# Verify installation
slither --version

# Install Solidity compiler
pip install solc-select
solc-select install 0.8.20
solc-select use 0.8.20
```

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    VS Code Extension                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Inline     │  │ Vulnerability│  │ Control Flow │  │
│  │ Diagnostics  │  │     Tree     │  │    Graph     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP API
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Analysis   │  │    DREAD     │  │     PDF      │  │
│  │ Orchestrator │  │    Scorer    │  │  Generator   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Slither    │  │   Bedrock    │  │ Multi-Chain  │  │
│  │   Service    │  │   Analyzer   │  │   Adapters   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  GitHub Actions Bot                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  PR Comment  │  │    Inline    │  │  Suggestion  │  │
│  │   Summary    │  │   Comments   │  │    Fixes     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Post-MVP Roadmap (Walk Phase)

- [ ] AI-powered fuzz test generation
- [ ] LiveOps monitoring dashboard
- [ ] Warden community platform
- [ ] Formal verification integration
- [ ] Solana/Rust analysis
- [ ] Move (Aptos/Sui) analysis
- [ ] Multi-agent collaboration system

## 📝 License

See [LICENSE](./LICENSE)

## 🙏 Acknowledgments

- AWS Bedrock for AI analysis
- Slither for static analysis
- VS Code Extension API
- GitHub Actions

---

**Built for AWS Global Vibe Hackathon 🚀**

*Powered by AWS Bedrock | Accelerated by Amazon Q & Kiro IDE*
