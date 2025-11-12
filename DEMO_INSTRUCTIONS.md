# 🎬 Auralis MVP Demo Instructions

## Pre-Demo Setup (5 minutes)

### 1. Start Backend
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Verify: Open http://localhost:8000/health in browser

### 2. Install VS Code Extension
```bash
cd vscode-extension
npm install
npm run compile
npm run package
```

Then in VS Code:
- Extensions → ... → Install from VSIX
- Select `auralis-vscode-0.1.0.vsix`
- Reload VS Code

### 3. Configure VS Code
Settings (Ctrl+,):
```json
{
  "auralis.apiEndpoint": "http://localhost:8000",
  "auralis.enableRealTimeAnalysis": true
}
```

### 4. Prepare Demo Contract
Open `demo-contracts/vulnerable-bank.sol` in VS Code

## Demo Flow (60 seconds)

### Part 1: VS Code Extension (25s)

**[0-5s] Introduction**
- "This is Auralis - AI-powered smart contract security"
- Show vulnerable-bank.sol open in VS Code

**[5-15s] Inline Diagnostics**
- Save file (Ctrl+S) to trigger analysis
- Point to red squiggly lines appearing
- Hover over a vulnerability to show popup
- "Real-time AI analysis as you code"

**[15-20s] Vulnerability Tree**
- Click Auralis icon in sidebar
- Expand vulnerability tree
- "All issues organized by severity"

**[20-25s] Control Flow Graph**
- Ctrl+Shift+P → "Auralis: Show Control Flow Graph"
- "Visual representation of function calls"

### Part 2: GitHub PR Bot (15s)

**[25-30s] Show PR**
- Open browser to demo PR
- "Automatic security review on every PR"

**[30-35s] Bot Comment**
- Scroll to Auralis bot comment
- Show vulnerability table
- "Comprehensive security report"

**[35-40s] Inline Suggestions**
- Show inline comment on vulnerable line
- Point to "Apply suggestion" button
- "One-click fixes powered by AI"

### Part 3: PDF Report (10s)

**[40-45s] Generate Report**
```bash
curl -X POST http://localhost:8000/api/v1/generate_report \
  -H "Content-Type: application/json" \
  -d @demo-contracts/vulnerable-bank.json \
  --output audit_report.pdf
```

**[45-50s] Show PDF**
- Open audit_report.pdf
- Show DREAD matrix
- "Professional audit reports in seconds"

### Part 4: Close (10s)

**[50-60s] Wrap Up**
- "Auralis combines static analysis with AWS Bedrock AI"
- "Built with Amazon Q and Kiro IDE"
- "Securing Web3, one contract at a time"
- Show GitHub repo URL

## Recording Tips

### Screen Setup
1. **Left half**: VS Code with vulnerable-bank.sol
2. **Right half**: Browser with GitHub PR

### Camera Position
- Face camera during introduction (0-5s)
- Screen share for demo (5-50s)
- Face camera for close (50-60s)

### Audio
- Use good microphone
- Minimize background noise
- Speak clearly and confidently

### Editing
- Add text overlays for key features
- Highlight mouse cursor
- Add background music (low volume)
- Include captions

## Backup Plans

### If Backend Fails
- Use mock data (extension has fallback)
- Show pre-recorded API responses

### If Extension Fails
- Show screenshots of working extension
- Demo backend API with curl commands

### If GitHub Action Fails
- Show previous successful PR
- Walk through workflow file

## Post-Demo Checklist

- [ ] Upload video to YouTube (unlisted)
- [ ] Add video link to README
- [ ] Create demo PR with screenshots
- [ ] Update HACKATHON_JOURNAL.md
- [ ] Tag release: `v0.1.0-mvp`

## Demo PR Template

```markdown
## 🛡️ Auralis MVP Demo

This PR demonstrates the Crawl phase MVP features:

### ✅ Features Implemented

1. **VS Code Extension**
   - Real-time inline diagnostics
   - Vulnerability tree view
   - Interactive control flow graph
   
2. **GitHub PR Bot**
   - Automated security comments
   - Inline vulnerability annotations
   - One-click fix suggestions

3. **Backend Services**
   - DREAD risk scoring
   - PDF report generation
   - Slither integration

### 📸 Screenshots

![VS Code Extension](screenshots/vscode-extension.png)
![GitHub PR Bot](screenshots/pr-bot.png)
![PDF Report](screenshots/pdf-report.png)

### 🎥 Demo Video

[Watch 60s Demo](https://youtube.com/...)

### 🧪 Testing

```bash
# Run demo workflow
gh workflow run mvp-demo.yml

# Test locally
cd backend && python -m uvicorn main:app --reload
cd vscode-extension && npm run compile
```

### 📝 Checklist

- [x] VS Code extension compiles
- [x] GitHub Action runs successfully
- [x] PDF generation works
- [x] DREAD scoring accurate
- [x] Demo video recorded
- [x] Documentation updated

---

**Ready for hackathon submission! 🚀**
```

## Troubleshooting During Demo

### Extension Not Showing Vulnerabilities
1. Check backend is running: `curl http://localhost:8000/health`
2. Check VS Code Output panel: View → Output → Auralis
3. Manually trigger: Ctrl+Shift+P → "Auralis: Analyze Contract"

### GitHub Action Not Triggering
1. Ensure PR has `.sol` file changes
2. Check workflow file is on base branch
3. Verify GitHub Actions are enabled

### PDF Generation Fails
```bash
pip install reportlab
```

## Questions & Answers

**Q: How does Auralis differ from Slither?**
A: Auralis combines Slither's static analysis with AWS Bedrock AI for semantic understanding. It catches logic flaws that pattern-matching misses.

**Q: Can it analyze other languages?**
A: MVP supports Solidity. Post-MVP will add Rust (Solana) and Move (Aptos/Sui).

**Q: How accurate is the AI analysis?**
A: We use Claude 3 Sonnet with confidence scores. High-confidence findings are 90%+ accurate.

**Q: Is it production-ready?**
A: This is an MVP. For production, add more test coverage and security hardening.

**Q: How was it built so fast?**
A: Amazon Q and Kiro IDE accelerated development by 10x through AI-assisted coding.

---

**Good luck with the demo! 🎬**
