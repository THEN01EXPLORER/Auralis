# 🛡️ Auralis - Smart Contract Security Auditor

> AI-powered smart contract security auditing platform for comprehensive vulnerability detection and analysis.

## ✨ Features

- 🔍 **Smart Contract Vulnerability Detection** - Automated scanning for common security issues
- 🤖 **AI-Powered Analysis** - Leverages AWS Bedrock for intelligent security insights
- 📊 **Real-Time Audit Reports** - Instant feedback on contract security
- ⛓️ **Multi-Chain Support** - Compatible with multiple blockchain platforms
- 🚀 **Serverless Architecture** - Scalable AWS Lambda deployment

## 📁 Project Structure

```
Auralis/
├── backend/              # FastAPI backend application
│   ├── app/             # Main application code
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core configurations
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utility functions
│   ├── tests/           # Test suite
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   └── styles/      # CSS styles
│   └── package.json     # Node dependencies
├── docs/                # Documentation
└── screenshots/         # Application screenshots
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- AWS Account (for deployment)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Configure your environment variables
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will run on `http://localhost:3000`

## 🔧 Configuration

Create a `.env` file in the backend directory:

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

## 📚 Documentation

- [Architecture Guide](./docs/ARCHITECTURE.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Quick Deploy](./QUICK_DEPLOY.md)
- [Test Guide](./TEST_GUIDE.md)

## 🧪 Testing

```bash
cd backend
python -m pytest tests/
```

## 📦 Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

## 📸 Screenshots

Application screenshots are available in the [screenshots](./screenshots) directory.

## 📄 License

See [LICENSE](./Auralis/LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ using AWS Bedrock, FastAPI, and React**
