# Troubleshooting Guide

## Common Issues and Solutions

### ChromaDB Installation Fails

**Problem**: Error during `pip install chromadb` or build failures.

**Solution**: ChromaDB is **optional**. The app works perfectly without it using mock vector search responses.

1. Skip ChromaDB installation - just install core requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. The app will automatically detect ChromaDB is missing and use mock responses.

3. If you want to try installing ChromaDB later:
   ```bash
   pip install chromadb
   ```

**Note**: ChromaDB requires compilation and may fail on some systems. This is normal and doesn't affect functionality.

### Python Version Issues

**Problem**: Package installation fails or incompatible versions.

**Solution**: 
- Ensure Python 3.12+ is installed: `python3 --version`
- Upgrade pip: `pip install --upgrade pip`
- Use a fresh virtual environment:
  ```bash
  rm -rf venv
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

### Port Already in Use

**Problem**: `Address already in use` error.

**Solution**:
1. Change the port in `backend/.env`:
   ```
   PORT=8001
   ```

2. Update `frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8001
   ```

### Module Import Errors

**Problem**: `ModuleNotFoundError` when running the server.

**Solution**:
1. Ensure virtual environment is activated: `source venv/bin/activate`
2. Verify packages are installed: `pip list`
3. Reinstall requirements: `pip install -r requirements.txt`

### Frontend Build Errors

**Problem**: Next.js build or TypeScript errors.

**Solution**:
1. Clear cache and reinstall:
   ```bash
   rm -rf node_modules .next
   npm install
   ```

2. Check Node.js version (requires 18+):
   ```bash
   node --version
   ```

### CORS Errors

**Problem**: CORS errors when frontend calls backend.

**Solution**:
1. Ensure backend is running on the port specified in `NEXT_PUBLIC_API_URL`
2. Check `local_server.py` has CORS middleware enabled (it does by default)
3. Verify frontend `.env.local` has correct API URL

### Vector Search Returns Empty Results

**Problem**: Vector search always returns empty or mock results.

**Solution**: This is expected behavior when:
- ChromaDB is not installed (uses mock responses)
- Vector store is not initialized with data

The app is fully functional with mock vector search. For real vector search:
1. Install ChromaDB: `pip install chromadb`
2. Restart the backend server
3. The vector store will initialize with sample data

### AWS Bedrock Errors (Production)

**Problem**: Bedrock API errors when `USE_LOCAL_MOCKS=false`.

**Solution**:
1. Verify AWS credentials: `aws configure`
2. Check IAM permissions for Bedrock
3. Verify model ID is correct in `.env`
4. Ensure region is correct: `AWS_REGION=us-east-1`
5. For local dev, use: `USE_LOCAL_MOCKS=true`

## Getting Help

If you encounter issues not covered here:

1. Check the error message carefully
2. Verify all prerequisites are met
3. Try a fresh installation:
   ```bash
   # Backend
   rm -rf venv chroma_db
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # Frontend
   rm -rf node_modules .next
   npm install
   ```

4. Check logs in terminal for detailed error messages

