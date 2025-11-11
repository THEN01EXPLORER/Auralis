# 🛡️ Auralis

> An AI-powered security auditor for smart contracts, built for the AWS Global Vibe Hackathon.

[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazon-aws)](https://aws.amazon.com/bedrock/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)](https://reactjs.org/)

---

## 🌐 Live Demo

**[YOUR_LIVE_AMPLIFY_URL_GOES_HERE]**

---

## 🎯 What is Auralis?

Auralis is a next-generation smart contract security auditor that combines traditional static analysis with AI-powered semantic understanding. Built specifically for the AWS Global Vibe Hackathon, it demonstrates how AWS Bedrock can revolutionize blockchain security by detecting vulnerabilities that traditional tools miss.

**The Problem:** Billions of dollars are lost annually to smart contract exploits. Traditional static analyzers catch obvious bugs but miss complex logic flaws and business logic vulnerabilities.

**The Solution:** Auralis uses a hybrid analysis engine that combines pattern-matching with AWS Bedrock's Claude 3 Sonnet model to provide comprehensive security audits with AI-generated remediation code.

---

## ✨ Features

### 🔄 Hybrid Analysis Engine
Combines static pattern-matching with AI-powered semantic analysis from AWS Bedrock. When AI is available, vulnerabilities are cross-validated and enriched with context-aware insights.

### 📦 Automated Repo Scanner
Analyze an entire GitHub repository with one click. Auralis clones the repo, finds all Solidity files, and provides a comprehensive security report for each contract.

### 🔧 Smart Remediation
Every vulnerability includes:
- **AI-generated explanations** of why it's dangerous
- **Working code examples** showing how to fix it
- **Confidence scores** indicating detection reliability
- **Source attribution** (Static, AI, or Hybrid)

### 🎨 Professional UI
- **Empty State:** Clean welcome screen with feature highlights
- **Success State:** Comprehensive vulnerability reports with expandable details
- **Error State:** Graceful error handling with helpful troubleshooting hints
- **Multi-File View:** Tabbed interface for repository analysis with aggregate statistics

---

## 🏗️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React + Vite | Modern, fast UI with code editor |
| **Backend** | FastAPI + Python | High-performance async API |
| **AI Engine** | AWS Bedrock (Claude 3 Sonnet) | Semantic vulnerability analysis |
| **Static Analysis** | Custom Pattern Matcher | Fast, reliable vulnerability detection |
| **Deployment** | AWS Lambda + API Gateway + Amplify | Serverless, scalable infrastructure |
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

A complete 3-minute demo video script is available in [`VIDEO_SCRIPT.md`](./VIDEO_SCRIPT.md), including:
- The Hook (0:00 - 0:30): The billion-dollar problem
- The Solution (0:30 - 1:30): Live demo of single contract analysis
- The "Wow" Feature (1:30 - 2:00): Repository scanner in action
- How We Built It (2:00 - 2:45): Amazon Q and Kiro IDE acceleration
- The Close (2:45 - 3:00): Call to action

---

## 🏆 Hackathon Proof of Work

**Auralis was built from scratch in 30 days for the AWS Global Vibe Hackathon.**

Its development was heavily accelerated by **Amazon Q** and **Kiro IDE**, which were used for:
- ✅ Code generation and refactoring
- ✅ Debugging and error resolution
- ✅ Documentation writing
- ✅ Automated backend development
- ✅ Test suite creation

**Full development journal with timestamps, commits, and evidence:** [`HACKATHON_JOURNAL.md`](./HACKATHON_JOURNAL.md)

---

## 📊 Architecture

```
┌─────────────────┐
│  React Frontend │
│   (Amplify)     │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  API Gateway    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Lambda/FastAPI │─────▶│  AWS Bedrock     │
│  (Orchestrator) │      │  (Claude 3)      │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│ Static Analyzer │
│ (Pattern Match) │
└─────────────────┘
```

**Key Design Decisions:**
- **Hybrid Analysis:** Static analysis runs first (fast), AI enriches results (smart)
- **Graceful Degradation:** If AI fails, static results are still returned
- **Serverless:** Zero infrastructure management, infinite scalability
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

### Deploy Backend to AWS Lambda
```bash
cd backend
pip install -r requirements.txt -t package/
cd package && zip -r ../deployment.zip . && cd ..
zip -g deployment.zip main.py app/

aws lambda update-function-code \
  --function-name auralis-api \
  --zip-file fileb://deployment.zip
```

### Deploy Frontend to AWS Amplify
```bash
cd frontend
npm run build

# Connect your GitHub repo to Amplify Console
# Amplify will auto-deploy on every push to main
```

**Full deployment guide:** [`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md)

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

Auralis can detect:

| Vulnerability Type | Severity | Detection Method |
|-------------------|----------|------------------|
| Re-entrancy Attacks | Critical | Static + AI |
| Integer Overflow/Underflow | High | Static + AI |
| Unchecked External Calls | High | Static + AI |
| Access Control Issues | High | Static + AI |
| Timestamp Dependence | Medium | Static + AI |
| Uninitialized Storage | Medium | Static |
| Gas Limit Issues | Medium | AI |
| Business Logic Flaws | Variable | AI |
| Denial of Service | Medium | Static + AI |
| Front-Running Vulnerabilities | Medium | AI |

---

## 🤝 Contributing

This project was built for the AWS Global Vibe Hackathon. While it's primarily a competition entry, feedback and suggestions are welcome!

---

## 📄 License

See [`LICENSE`](./LICENSE) for details.

---

## 🙏 Acknowledgments

- **AWS Bedrock Team** - For providing access to Claude 3 Sonnet
- **Amazon Q & Kiro IDE** - For accelerating development by 10x
- **FastAPI Community** - For the excellent async framework
- **React Team** - For the powerful UI library

---

## 📞 Contact

Built with ❤️ for the AWS Global Vibe Hackathon

**Questions?** Open an issue or reach out via the hackathon platform.

---

<div align="center">

**⚡ Powered by AWS Bedrock | Built with Amazon Q | Deployed on AWS Lambda ⚡**

</div>
