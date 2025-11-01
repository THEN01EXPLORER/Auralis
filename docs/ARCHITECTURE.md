# Auralis System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                          │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                    React Frontend (Port 3000)                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │    │
│  │  │  Upload  │  │ Analysis │  │  Report  │  │Dashboard │     │    │
│  │  │   Page   │  │   Page   │  │   Page   │  │   Page   │     │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │    │
│  └───────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS/REST API
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         APPLICATION LAYER                               │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │              FastAPI Backend (Port 8000)                       │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │    │
│  │  │   API Routes │  │   Services   │  │    Models    │        │    │
│  │  │              │  │              │  │              │        │    │
│  │  │ /upload      │  │ Parser       │  │ Contract     │        │    │
│  │  │ /analyze     │  │ Analyzer     │  │ Vulnerability│        │    │
│  │  │ /report      │  │ AI Service   │  │ Report       │        │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │    │
│  └───────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         AI & PROCESSING LAYER                           │
│                                                                         │
│  ┌──────────────────────┐  ┌──────────────────────┐                   │
│  │   AWS Bedrock API    │  │   Pattern Matching   │                   │
│  │                      │  │                      │                   │
│  │  ┌────────────────┐  │  │  ┌────────────────┐ │                   │
│  │  │ Claude 3       │  │  │  │ Re-entrancy    │ │                   │
│  │  │ (AI Analysis)  │  │  │  │ Integer O/F    │ │                   │
│  │  └────────────────┘  │  │  │ Access Control │ │                   │
│  │                      │  │  │ Return Values  │ │                   │
│  └──────────────────────┘  │  └────────────────┘ │                   │
│                            └──────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                    │
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │
│  │   PostgreSQL     │  │   S3 Storage     │  │   DynamoDB       │    │
│  │                  │  │                  │  │                  │    │
│  │ - Audit History  │  │ - Contracts      │  │ - Session Data   │    │
│  │ - User Data      │  │ - Reports        │  │ - Cache          │    │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────┐
│  User    │
└────┬─────┘
     │ 1. Upload Smart Contract (.sol file)
     ▼
┌─────────────────────────────────────┐
│   React Frontend                    │
│   - Validate file                   │
│   - Display upload status           │
└────┬────────────────────────────────┘
     │ 2. POST /api/v1/analyze
     │    { contract_code, chain_type }
     ▼
┌─────────────────────────────────────┐
│   FastAPI Backend                   │
│   - Receive contract                │
│   - Generate analysis ID            │
└────┬────────────────────────────────┘
     │ 3. Parse contract
     ▼
┌─────────────────────────────────────┐
│   Contract Parser Service           │
│   - Extract functions               │
│   - Identify patterns               │
│   - Build AST                       │
└────┬────────────────────────────────┘
     │ 4. Static analysis
     ▼
┌─────────────────────────────────────┐
│   Vulnerability Detector            │
│   - Re-entrancy check               │
│   - Integer overflow check          │
│   - Access control check            │
│   - Return value check              │
└────┬────────────────────────────────┘
     │ 5. Send to AI for deep analysis
     ▼
┌─────────────────────────────────────┐
│   AWS Bedrock (Claude 3)            │
│   - Semantic analysis               │
│   - Context understanding           │
│   - Risk assessment                 │
│   - Recommendation generation       │
└────┬────────────────────────────────┘
     │ 6. Aggregate results
     ▼
┌─────────────────────────────────────┐
│   Report Generator                  │
│   - Combine static + AI findings    │
│   - Calculate risk scores           │
│   - Generate recommendations        │
└────┬────────────────────────────────┘
     │ 7. Store results
     ▼
┌─────────────────────────────────────┐
│   Database (PostgreSQL)             │
│   - Save audit report               │
│   - Store vulnerability data        │
└────┬────────────────────────────────┘
     │ 8. Return report
     ▼
┌─────────────────────────────────────┐
│   React Frontend                    │
│   - Display vulnerabilities         │
│   - Show risk scores                │
│   - Provide recommendations         │
└─────────────────────────────────────┘
```

## AWS Lambda Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          AWS CLOUD INFRASTRUCTURE                       │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                    CloudFront CDN                              │    │
│  │              (React Frontend Distribution)                     │    │
│  └────────────────────────┬──────────────────────────────────────┘    │
│                           │                                            │
│  ┌────────────────────────┴──────────────────────────────────────┐    │
│  │                      S3 Bucket                                 │    │
│  │                (Static Frontend Assets)                        │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                   API Gateway (REST API)                       │    │
│  │                  https://api.auralis.com                       │    │
│  └────────────────────────┬──────────────────────────────────────┘    │
│                           │                                            │
│           ┌───────────────┼───────────────┐                           │
│           │               │               │                           │
│           ▼               ▼               ▼                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │
│  │   Lambda 1   │ │   Lambda 2   │ │   Lambda 3   │                 │
│  │              │ │              │ │              │                 │
│  │  /upload     │ │  /analyze    │ │  /report     │                 │
│  │  Handler     │ │  Handler     │ │  Handler     │                 │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘                 │
│         │                │                │                           │
│         └────────────────┼────────────────┘                           │
│                          │                                            │
│                          ▼                                            │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                    AWS Bedrock                                 │    │
│  │              (Claude 3 Sonnet/Haiku)                           │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                      RDS PostgreSQL                            │    │
│  │                   (Audit Data Storage)                         │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                    S3 Bucket (Private)                         │    │
│  │              (Contract Files & Reports)                        │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (React)
- **Technology**: React 18, React Router, Axios
- **Hosting**: AWS S3 + CloudFront
- **Key Features**: File upload, real-time analysis status, report visualization

### Backend (FastAPI)
- **Technology**: FastAPI, Python 3.11, Pydantic
- **Deployment**: AWS Lambda + API Gateway
- **Key Features**: RESTful API, async processing, JWT authentication

### AI Analysis (AWS Bedrock)
- **Model**: Claude 3 Sonnet
- **Purpose**: Deep semantic analysis, context understanding
- **Input**: Parsed contract code + static analysis results
- **Output**: Vulnerability insights, risk scores, recommendations

### Database
- **Primary**: PostgreSQL (RDS) - Audit history, user data
- **Storage**: S3 - Contract files, generated reports
- **Cache**: DynamoDB - Session data, temporary results

## Security Considerations

1. **API Security**: JWT authentication, rate limiting
2. **Data Encryption**: TLS in transit, AES-256 at rest
3. **Access Control**: IAM roles, least privilege principle
4. **Input Validation**: Contract size limits, file type validation
5. **Secrets Management**: AWS Secrets Manager for API keys

## Scalability

- **Lambda Auto-scaling**: Handles concurrent requests
- **CloudFront CDN**: Global content delivery
- **RDS Read Replicas**: Database read scaling
- **S3**: Unlimited storage capacity
- **API Gateway**: Throttling and caching

## Cost Optimization

- **Lambda**: Pay per execution
- **Bedrock**: Pay per token
- **S3**: Lifecycle policies for old reports
- **CloudFront**: Edge caching reduces origin requests
