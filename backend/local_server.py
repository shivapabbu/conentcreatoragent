"""
Local development server for the content creation backend.
This mimics the Lambda function behavior for local testing.
"""
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from lambda_function import lambda_handler

load_dotenv()

app = FastAPI(title="Content Creator API", version="1.0.0")

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContentRequest(BaseModel):
    title: str
    description: str
    tone: str = "professional"
    language: str = "en"
    content_type: str = "landing_page"


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/generate")
async def generate_content(request: ContentRequest):
    """Generate content using the Lambda handler logic"""
    try:
        # Convert FastAPI request to Lambda event format
        event = {
            "body": request.model_dump_json(),
            "headers": {},
            "requestContext": {
                "requestId": "local-request"
            }
        }
        
        context = type('Context', (), {
            'aws_request_id': 'local-request-id',
            'function_name': 'content-generator-local'
        })()
        
        # Call the Lambda handler
        response = lambda_handler(event, context)
        
        # Parse the Lambda response
        if response.get("statusCode") == 200:
            import json
            return json.loads(response["body"])
        else:
            raise HTTPException(
                status_code=response.get("statusCode", 500),
                detail=response.get("body", "Unknown error")
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)

