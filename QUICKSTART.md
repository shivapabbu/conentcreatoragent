# Quick Start Guide

## Prerequisites

- **Node.js 18+** and npm/yarn
- **Python 3.12+**
- **AWS CLI** (optional, only for deployment)

## Quick Setup (Automated)

Run the setup script:

```bash
./setup.sh
```

## Manual Setup

### 1. Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local  # Edit if needed
npm run dev
```

Frontend will run on **http://localhost:3000**

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip  # Upgrade pip first
pip install -r requirements.txt

# Optional: Install ChromaDB for vector search
# pip install chromadb  # Skip if build fails - app works without it

cp .env.example .env  # Edit if needed
python local_server.py
```

**Note**: If ChromaDB installation fails (common on some systems), the app will automatically use mock vector search responses. The app is fully functional without ChromaDB.

Backend will run on **http://localhost:8000**

## Running the Application

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   source venv/bin/activate
   python local_server.py
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser**: Navigate to http://localhost:3000

## Testing the Application

1. Fill in the form:
   - **Title**: "My Awesome Product"
   - **Description**: "A revolutionary solution that transforms how businesses operate"
   - **Tone**: Select from dropdown
   - **Language**: Select from dropdown
   - **Content Type**: Select from dropdown

2. Click **"Generate Content"**

3. View results in different formats (Preview, HTML, Markdown, JSON)

4. Export content using the export buttons

## Local Development Features

- ✅ **Mock Bedrock**: No AWS credentials needed for local dev
- ✅ **ChromaDB**: Local vector database (no AWS setup required)
- ✅ **FastAPI Server**: Local backend server for development
- ✅ **Hot Reload**: Both frontend and backend support hot reload

## Switching to AWS (Production)

1. Update `backend/.env`:
   ```env
   USE_LOCAL_MOCKS=false
   VECTOR_DB_TYPE=opensearch
   AWS_REGION=us-east-1
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```

3. Deploy infrastructure:
   ```bash
   cd infrastructure
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cdk bootstrap  # First time only
   cdk deploy
   ```

4. Deploy Lambda function:
   ```bash
   cd backend
   ./deploy.sh
   ```

## Troubleshooting

### Port Already in Use
- Change `PORT` in `backend/.env`
- Update `NEXT_PUBLIC_API_URL` in `frontend/.env.local`

### Python Dependencies Issues
- Ensure Python 3.12+ is installed
- Try: `pip install --upgrade pip`
- Recreate venv: `rm -rf venv && python3 -m venv venv`

### Node Modules Issues
- Delete `node_modules` and `package-lock.json`
- Run: `npm install` again

### ChromaDB Issues
- Delete `backend/chroma_db` directory
- Restart the backend server

