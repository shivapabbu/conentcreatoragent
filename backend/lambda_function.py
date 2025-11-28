"""
AWS Lambda handler for content generation.
This is the main entry point for the serverless function.
"""
import json
import os
from typing import Dict, Any

from content_generator import ContentGenerator
from vector_store import VectorStore


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function.
    
    Args:
        event: Lambda event containing request data
        context: Lambda context object
        
    Returns:
        Lambda response with status code and body
    """
    try:
        # Parse request body
        if isinstance(event.get("body"), str):
            body = json.loads(event["body"])
        else:
            body = event.get("body", {})
        
        # Extract request parameters
        title = body.get("title", "")
        description = body.get("description", "")
        tone = body.get("tone", "professional")
        language = body.get("language", "en")
        content_type = body.get("content_type", "landing_page")
        
        # Validate required fields
        if not title or not description:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "error": "Title and description are required"
                })
            }
        
        # Initialize components
        vector_store = VectorStore()
        content_generator = ContentGenerator(vector_store)
        
        # Generate content
        result = content_generator.generate(
            title=title,
            description=description,
            tone=tone,
            language=language,
            content_type=content_type
        )
        
        # Return success response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }
        
    except Exception as e:
        # Log error (in production, use CloudWatch)
        print(f"Error: {str(e)}")
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Internal server error",
                "detail": str(e)
            })
        }

