# 🛡️ Auralis

> An AI-powered security auditor for smart contracts, built for the AWS Global Vibe Hackathon 2025.

[![Amazon Kiro](https://img.shields.io/badge/Built%20with-Amazon%20Kiro-FF9900?logo=amazon-aws)](https://kiro.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)](https://reactjs.org/)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel)](https://vercel.com/)
[![Render](https://img.shields.io/badge/Backend-Render-46E3B7?logo=render)](https://render.com/)

---

## 🌐 Live Demo

🔗 **Frontend:** [https://auralis-tawny.vercel.app](https://auralis-tawny.vercel.app)

🔗 **Backend API:** [https://auralis-1-doxn.onrender.com](https://auralis-1-doxn.onrender.com)

---

## 🎯 What is Auralis?

Auralis is a smart contract security auditor that uses pattern-based static analysis to detect vulnerabilities in Solidity code. Built for the AWS Global Vibe Hackathon 2025 using **Amazon Kiro IDE**.

**The Problem:** Billions of dollars are lost annually to smart contract exploits. Traditional audits are slow, expensive, and often miss critical vulnerabilities.

**The Solution:** Auralis provides instant security analysis with 20 vulnerability detection patterns, exportable reports, and actionable remediation suggestions.

---

## ✨ Features

### 🔍 20 Vulnerability Detection Patterns
Detects critical smart contract vulnerabilities including reentrancy, integer overflow, front-running, flash loan attacks, and more.

### 📦 GitHub Repository Scanner
Analyze an entire GitHub repository with one click. Auralis clones the repo, finds all Solidity files, and provides a comprehensive security report for each contract.

### 📤 Export Reports
Download analysis results in multiple formats:
- **JSON** - For programmatic use
- **Markdown** - For documentation
- **Plain Text** - For quick sharing

### 🎨 Professional UI
- **Dark/Light Mode** - Toggle between themes
- **Sample Contracts** - Pre-loaded vulnerable contracts for testing
- **Keyboard Shortcuts** - Ctrl+Enter to analyze
- **Severity Badges** - Color-coded vulnerability levels

---

## 🏗️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------||
| **Frontend** | React 18.2 | Modern UI with code editor |
| **Backend** | FastAPI + Python | High-performance async API |
| **Static Analysis** | Custom Pattern Matcher | 20 vulnerability detection patterns |
| **Frontend Hosting** | Vercel | Fast, global CDN deployment |
| **Backend Hosting** | Render.com | Managed Python server |
| **AI Development** | Amazon Kiro IDE | Spec-driven development |
| **Version Control** | Git + GitHub | Repository scanning and source control |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- AWS Account with Bedrock access
- Git

### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Configure environment variables
export AWS_REGION=us-east-1
export ENABLE_AI_ANALYSIS=true
export BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install

# Configure API endpoint (optional, defaults to localhost:8000)
export REACT_APP_API_URL=http://localhost:8000

# Start development server
npm start
```

Frontend runs on `http://localhost:3000`

---

## 📖 Usage

### Analyze a Single Contract

1. Paste your Solidity code into the editor
2. Click **"Analyze Contract"**
3. View vulnerabilities with risk scores, descriptions, and fixes

### Analyze a GitHub Repository

1. Enter a GitHub repository URL (e.g., `https://github.com/user/repo`)
2. Click **"Analyze Repo"**
3. View aggregate statistics and click tabs to see individual file reports

---

## 🎬 Demo Video Script

A complete 3-minute demo video script is available in [`VIDEO_GUIDE.md`](./VIDEO_GUIDE.md), including:
- The Hook (0:00 - 0:30): The billion-dollar problem
- The Solution (0:30 - 1:30): Live demo of single contract analysis
- The "Wow" Feature (1:30 - 2:00): Repository scanner in action
- How We Built It (2:00 - 2:45): Amazon Q and Kiro IDE acceleration
- The Close (2:45 - 3:00): Call to action

---

## 🎯 Hackathon Track

**🔒 AI Cybersecurity & Privacy**

Auralis is an AI-powered tool that bolsters smart contract security by detecting vulnerabilities, preventing exploits, and protecting blockchain assets worth billions of dollars.

---

## 🏆 Hackathon Proof of Work

**Auralis was built from scratch for the AWS Global Vibe Hackathon 2025.**

### 🤖 Amazon Kiro IDE Usage

The entire development was done using **Amazon Kiro IDE** with spec-driven development:
- ✅ Full application built inside Kiro IDE
- ✅ Code generation (React components, FastAPI endpoints)
- ✅ Vulnerability pattern creation (20 detection patterns)
- ✅ Debugging and error resolution
- ✅ CSS styling and theme system
- ✅ Export functionality implementation

🎬 **1-Hour Kiro Development Recording Available**

📖 **Detailed Tool Usage:** [`AMAZON_Q_USAGE.md`](./AMAZON_Q_USAGE.md)

📓 **Development Journal:** [`HACKATHON_JOURNAL.md`](./HACKATHON_JOURNAL.md)

---

## 📊 Architecture

```
┌─────────────────┐
│  React Frontend │
│    (VERCEL)     │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  FastAPI Backend│
│  (RENDER.COM)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Static Analyzer │
│ (20 Patterns)   │
└─────────────────┘
```

**Key Design Decisions:**
- **Pattern-Based Analysis:** 20 regex patterns for common vulnerabilities
- **Real-time Detection:** Instant analysis with detailed reports
- **Export Options:** JSON, Markdown, and Plain Text formats
- **Async Processing:** FastAPI handles concurrent requests efficiently

Detailed architecture documentation: [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md)

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Test the Repo Scanner
```bash
python test_repo_scanner.py
```

### Manual Testing Guide
See [`TEST_GUIDE.md`](./TEST_GUIDE.md) for comprehensive testing instructions.

---

## 🚀 Deployment

### Current Deployment

| Component | Platform | URL |
|-----------|----------|-----|
| **Frontend** | Vercel | https://auralis-tawny.vercel.app |
| **Backend** | Render.com | https://auralis-1-doxn.onrender.com |

### Deploy Your Own

**Frontend (Vercel):**
1. Fork this repository
2. Connect to Vercel
3. Set `REACT_APP_API_URL` environment variable
4. Deploy

**Backend (Render):**
1. Create a new Web Service on Render
2. Connect to your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn main_minimal:app`
5. Deploy

---

## 📁 Project Structure

```
Auralis/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── models/            # Pydantic models
│   │   ├── services/          # Business logic
│   │   │   ├── analyzer.py           # Static analyzer
│   │   │   ├── bedrock_analyzer.py   # AI analyzer
│   │   │   └── analysis_orchestrator.py  # Hybrid coordinator
│   │   └── utils/             # Helper functions
│   ├── tests/                 # Pytest test suite
│   ├── main.py               # FastAPI app entry point
│   └── requirements.txt      # Python dependencies
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── CodeEditor.js
│   │   │   ├── VulnerabilityReport.js
│   │   │   └── RiskMeter.js
│   │   ├── pages/           # Page components
│   │   │   └── Home.js
│   │   ├── services/        # API client
│   │   │   └── api.js
│   │   └── styles/          # CSS modules
│   └── package.json
│
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md      # System design
│   └── README.md           # Docs index
│
├── demo-contracts/          # Sample contracts for testing
│   └── VulnerableBank.sol
│
├── HACKATHON_JOURNAL.md    # Development log with proof of work
├── VIDEO_SCRIPT.md         # 3-minute demo script
├── DEPLOYMENT_GUIDE.md     # AWS deployment instructions
├── TEST_GUIDE.md          # Testing documentation
└── README.md              # This file
```

---

## 🔐 Security Vulnerabilities Detected

Auralis detects **20 vulnerability patterns**:

| Vulnerability Type | Severity |
|-------------------|----------|
| Re-entrancy Attacks | Critical |
| Integer Overflow/Underflow | High |
| Unchecked External Calls | High |
| Access Control Issues | High |
| Timestamp Dependence | Medium |
| Uninitialized Storage | Medium |
| Front-Running | Medium |
| Flash Loan Attacks | High |
| Denial of Service | Medium |
| Signature Replay | High |
| Weak Randomness | Medium |
| Missing Zero Address Check | Low |
| Hardcoded Addresses | Low |
| Arbitrary Jump | Critical |
| tx.origin Authentication | High |
| Delegatecall Injection | Critical |
| Self-destruct | High |
| Floating Pragma | Low |
| Unchecked Return Values | Medium |
| Gas Limit Issues | Medium |

---

## 🤝 Contributing

This project was built for the AWS Global Vibe Hackathon. While it's primarily a competition entry, feedback and suggestions are welcome!

---

## 📄 License

See [`LICENSE`](./LICENSE) for details.

---

## 🙏 Acknowledgments

- **Amazon Kiro IDE** - For spec-driven development and AI assistance
- **Vercel** - For frontend hosting
- **Render.com** - For backend hosting
- **FastAPI Community** - For the excellent async framework
- **React Team** - For the powerful UI library

---

## 📞 Contact

Built with ❤️ for the AWS Global Vibe Hackathon

**Questions?** Open an issue or reach out via the hackathon platform.

---

<div align="center">

**⚡ Built with Amazon Kiro IDE | Deployed on Vercel + Render ⚡**

</div>
