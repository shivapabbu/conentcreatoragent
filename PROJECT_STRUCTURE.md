# Project Structure

```
conentcreatoragent/
├── frontend/                    # Next.js React Application
│   ├── app/
│   │   ├── layout.tsx          # Root layout component
│   │   ├── page.tsx            # Main content creation UI
│   │   └── globals.css         # Global styles
│   ├── package.json            # Frontend dependencies
│   ├── tsconfig.json           # TypeScript configuration
│   ├── next.config.js          # Next.js configuration
│   └── .eslintrc.json          # ESLint configuration
│
├── backend/                     # Python Lambda + Local Server
│   ├── lambda_function.py      # AWS Lambda handler
│   ├── local_server.py         # FastAPI local dev server
│   ├── content_generator.py    # Content generation logic
│   ├── vector_store.py         # Vector DB abstraction
│   ├── bedrock_mock.py         # Mock Bedrock for local dev
│   ├── requirements.txt        # Python dependencies
│   ├── deploy.sh               # Lambda deployment script
│   └── __init__.py
│
├── infrastructure/              # AWS CDK Infrastructure
│   ├── app.py                  # CDK app entry point
│   ├── cdk.json                # CDK configuration
│   ├── requirements.txt        # CDK dependencies
│   └── stacks/
│       ├── __init__.py
│       └── content_creator_stack.py  # Main CDK stack
│
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
├── setup.sh                     # Automated setup script
└── .gitignore                   # Git ignore rules
```

## Key Components

### Frontend (Next.js)
- **Technology**: React 18, Next.js 14, TypeScript
- **Features**: 
  - Content creation form
  - Real-time content generation
  - Multiple export formats (HTML, Markdown, JSON)
  - Tabbed preview interface
  - Responsive design

### Backend (Python)
- **Technology**: FastAPI (local), AWS Lambda (production)
- **Features**:
  - Content generation using Bedrock/Claude
  - Vector search for context retrieval
  - Local mock support for development
  - STANDs framework alignment

### Infrastructure (AWS CDK)
- **Resources**:
  - Lambda function
  - API Gateway
  - S3 bucket
  - DynamoDB table
  - IAM roles and policies
  - Bedrock permissions

## Development Workflow

1. **Local Development**: Use mocks and local services
2. **Testing**: Test locally before deployment
3. **Deployment**: Use CDK to deploy infrastructure
4. **Production**: Switch to real AWS services

