# Intelligent Page Content Creation Platform

AWS-native, Bedrock-powered, STANDs-aligned Intelligent Page Content Creation platform.

## Architecture

- **Frontend**: Next.js (React)
- **Backend**: AWS Lambda (Python 3.12) with local development server
- **AI**: AWS Bedrock (Claude 3.5 Sonnet/Haiku, Titan Embeddings)
- **Vector DB**: Amazon OpenSearch Serverless (ChromaDB for local dev)
- **Storage**: S3 + DynamoDB (local file system for dev)
- **Infrastructure**: AWS CDK (Python)

## Quick Start

### Automated Setup

```bash
./setup.sh
```

Then start the services:
- **Terminal 1**: `cd backend && source venv/bin/activate && python local_server.py`
- **Terminal 2**: `cd frontend && npm run dev`

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## Local Development Setup

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.12+
- AWS CLI configured (for deployment only)

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local  # Optional: edit if needed
npm run dev
```

Frontend runs on http://localhost:3000

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip  # Upgrade pip first
pip install -r requirements.txt

# Optional: Install ChromaDB for vector search (if build succeeds)
# pip install chromadb  # or: pip install -r requirements-dev.txt

cp .env.example .env  # Optional: edit if needed
python local_server.py
```

**Note**: ChromaDB is optional. If installation fails, the app will work with mock vector search responses.

Backend runs on http://localhost:8000

### Environment Variables

**Frontend** (`.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend** (`.env`):
```
AWS_REGION=us-east-1
USE_LOCAL_MOCKS=true
VECTOR_DB_TYPE=chroma  # or 'opensearch' for AWS
PORT=8000
```

## Features

- ✅ Landing page content generation
- ✅ Hero messages
- ✅ Product descriptions
- ✅ SEO metadata
- ✅ CTA buttons
- ✅ FAQs
- ✅ HTML-ready content
- ✅ Multilingual support
- ✅ STANDs framework alignment

## Deployment

### Deploy Infrastructure

```bash
cd infrastructure
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cdk deploy
```

### Deploy Backend

```bash
cd backend
./deploy.sh
```

## Project Structure

```
.
├── frontend/          # Next.js application
├── backend/           # Python Lambda functions + local server
├── infrastructure/    # AWS CDK infrastructure code
└── shared/            # Shared types and utilities
```

