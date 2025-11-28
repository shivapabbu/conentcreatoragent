#!/bin/bash
# Quick setup script for the Content Creator project

set -e

echo "🚀 Setting up Content Creator Platform..."

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

# Backend setup
echo "🐍 Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Try to install ChromaDB (optional - app works without it)
echo "Installing optional ChromaDB (may fail on some systems - that's OK)..."
pip install chromadb 2>/dev/null || echo "ChromaDB installation skipped - app will use mock vector search"

cd ..

# Create .env files if they don't exist
if [ ! -f "frontend/.env.local" ]; then
    echo "Creating frontend/.env.local..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
fi

if [ ! -f "backend/.env" ]; then
    echo "Creating backend/.env..."
    cat > backend/.env << EOF
AWS_REGION=us-east-1
USE_LOCAL_MOCKS=true
VECTOR_DB_TYPE=chroma
PORT=8000
EOF
fi

echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Terminal 1: cd backend && source venv/bin/activate && python local_server.py"
echo "  2. Terminal 2: cd frontend && npm run dev"
echo ""
echo "Frontend will be available at http://localhost:3000"
echo "Backend will be available at http://localhost:8000"

