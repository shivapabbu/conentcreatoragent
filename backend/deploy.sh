#!/bin/bash
# Deployment script for Lambda function

set -e

echo "Building Lambda deployment package..."

# Create deployment directory
rm -rf deploy
mkdir -p deploy

# Copy Lambda function files
cp lambda_function.py deploy/
cp content_generator.py deploy/
cp vector_store.py deploy/
cp bedrock_mock.py deploy/

# Install dependencies
pip install -r requirements.txt -t deploy/

# Create deployment package
cd deploy
zip -r ../lambda-deployment.zip .
cd ..

echo "Deployment package created: lambda-deployment.zip"
echo "Upload to Lambda using:"
echo "  aws lambda update-function-code --function-name content-generator --zip-file fileb://lambda-deployment.zip"

