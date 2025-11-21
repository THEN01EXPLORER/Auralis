# Backend Structure Documentation

## Main Entry Point
- **`main.py`** - Main FastAPI application with all endpoints and configurations
  - This is the PRIMARY entry point for the backend
  - Used by: uvicorn, gunicorn, docker, and local development

## App Directory Structure
```
app/
├── __init__.py              # Package marker (intentionally minimal)
├── models/                  # Data models
│   ├── contract.py          # Pydantic models for API requests/responses
│   └── __init__.py
├── services/                # Business logic services
│   ├── analyzer.py          # Static vulnerability analyzer
│   ├── bedrock_analyzer.py  # AI-powered analyzer (AWS Bedrock)
│   ├── analysis_orchestrator.py  # Coordinates static + AI analysis
│   ├── vulnerability_merger.py   # Merges results from multiple analyzers
│   ├── dread_scorer.py      # DREAD risk scoring
│   ├── pdf_report_generator.py   # PDF report generation
│   ├── slither_service.py   # Slither integration
│   └── __init__.py
├── utils/                   # Utility functions
│   ├── risk_calculator.py   # Risk score calculations
│   └── __init__.py
└── adapters/                # External integrations
    └── chain_adapter.py     # Blockchain-specific logic
```

## Lambda Handlers (AWS Deployment)
- **`lambda_handler.py`** - AWS Lambda entry point using Mangum
- **`lambda_function.py`** - Alternative Lambda entry point
- Both import from `main.py`

## Configuration Files
- **`requirements.txt`** - Python dependencies for production
- **`requirements-full.txt`** - Full dependencies including dev tools
- **`requirements-lambda.txt`** - Minimal dependencies for Lambda
- **`gunicorn.conf.py`** - Gunicorn configuration for production
- **`Dockerfile`** - Container configuration
- **`serverless.yml`** - Serverless Framework configuration
- **`template.yaml`** - AWS SAM template

## Running the Backend

### Local Development
```bash
# Using the start script
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using the batch file
start.bat
```

### Production
```bash
# Using Gunicorn
gunicorn -c gunicorn.conf.py main:app

# Using Docker
docker build -t auralis-backend .
docker run -p 8000:8000 auralis-backend
```

### Docker Compose
```bash
docker-compose up backend
```

## API Endpoints

### Core Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/analyze` - Analyze single contract
- `POST /api/v1/analyze_repo` - Analyze GitHub repository
- `POST /api/v1/dread_score` - Calculate DREAD scores
- `POST /api/v1/generate_report` - Generate PDF audit report

## Environment Variables
- `AWS_REGION` - AWS region for Bedrock (default: us-east-1)
- `ENABLE_AI_ANALYSIS` - Enable/disable AI analysis (default: true)
- `AI_ANALYSIS_REQUIRED` - Fail if AI unavailable (default: false)
- `LOG_LEVEL` - Logging level (default: INFO)
- `BEDROCK_MODEL_ID` - Bedrock model ID
- `ALLOWED_ORIGINS` - CORS allowed origins (default: *)
- `AWS_ACCESS_KEY_ID` - AWS credentials
- `AWS_SECRET_ACCESS_KEY` - AWS credentials

## Important Notes

1. **Main Application**: Always use `main.py` as the entry point
2. **App Directory**: Contains reusable modules, NOT a separate application
3. **Import Pattern**: Services import from `app.services`, `app.models`, etc.
4. **Lambda**: Uses Mangum to adapt FastAPI for AWS Lambda
5. **CORS**: Configured to allow all origins by default (restrict in production)

## Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py
```
