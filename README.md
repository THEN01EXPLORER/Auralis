# 🛡️ Auralis - AI Smart Contract Security Auditor

> Instantly detect vulnerabilities in Solidity smart contracts using pattern-based static analysis.

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org/)

---

## ✨ Features

- 🔍 **20 Vulnerability Patterns** - Re-entrancy, Integer Overflow, Access Control, Flash Loans, and more
- 📦 **GitHub Repo Scanner** - Analyze entire repositories with one click
- 📤 **Export Reports** - JSON, Markdown, and Plain Text formats
- 🎨 **Modern UI** - Dark mode, keyboard shortcuts, severity badges

---

## 🚀 Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm start
```

Open `http://localhost:3000`

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18 |
| Backend | FastAPI + Python |
| Analysis | Custom Pattern Matcher |

---

## 📊 Detected Vulnerabilities

| Type | Severity |
|------|----------|
| Re-entrancy Attack | Critical |
| Integer Overflow/Underflow | High |
| Access Control Violation | High |
| Unchecked External Call | High |
| Flash Loan Attack | High |
| Front-Running | Medium |
| Timestamp Dependence | Medium |
| Weak Randomness | Medium |

---

## 📁 Project Structure

```
Auralis/
├── backend/         # FastAPI server
├── frontend/        # React app
├── demo-contracts/  # Sample vulnerable contracts
├── tests/           # Test suite
└── docs/            # Documentation
```

---

## 📄 License

MIT License

---

Built with ❤️ for blockchain security
