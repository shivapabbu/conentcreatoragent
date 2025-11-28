"""
Content generation logic using AWS Bedrock.
Supports both AWS Bedrock and local mock for development.
"""
import os
import json
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError

from vector_store import VectorStore
from bedrock_mock import BedrockMock


class ContentGenerator:
    """Generates content using AWS Bedrock Claude models"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.use_local_mocks = os.getenv("USE_LOCAL_MOCKS", "true").lower() == "true"
        self.region = os.getenv("AWS_REGION", "us-east-1")
        
        if not self.use_local_mocks:
            self.bedrock_runtime = boto3.client(
                'bedrock-runtime',
                region_name=self.region
            )
            self.model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
        else:
            self.bedrock_mock = BedrockMock()
    
    def generate(
        self,
        title: str,
        description: str,
        tone: str = "professional",
        language: str = "en",
        content_type: str = "landing_page"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive content for a page.
        
        Args:
            title: Page title
            description: Product/service description
            tone: Content tone (professional, casual, etc.)
            language: Language code
            content_type: Type of content to generate
            
        Returns:
            Dictionary with generated content sections
        """
        # Retrieve relevant context from vector store
        relevant_context = self.vector_store.search(description, top_k=3)
        
        # Build prompt
        prompt = self._build_prompt(
            title=title,
            description=description,
            tone=tone,
            language=language,
            content_type=content_type,
            context=relevant_context
        )
        
        # Call Bedrock
        if self.use_local_mocks:
            response_text = self.bedrock_mock.generate(prompt)
        else:
            response_text = self._call_bedrock(prompt)
        
        # Parse and structure response
        content = self._parse_response(response_text, title, description)
        
        return content
    
    def _build_prompt(
        self,
        title: str,
        description: str,
        tone: str,
        language: str,
        content_type: str,
        context: List[str]
    ) -> str:
        """Build the prompt for Claude"""
        
        context_text = "\n".join([f"- {c}" for c in context]) if context else "No specific context available."
        
        prompt = f"""You are an expert content creator specializing in {content_type} creation.

Task: Generate comprehensive, engaging content for a {content_type} about: {title}

Product/Service Description:
{description}

Relevant Context from Knowledge Base:
{context_text}

Requirements:
1. Tone: {tone}
2. Language: {language}
3. Content Type: {content_type}

Generate the following sections in JSON format:

{{
  "hero_section": "A compelling hero message (2-3 sentences)",
  "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
  "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
  "seo_meta": {{
    "title": "SEO optimized title (60 chars max)",
    "description": "SEO meta description (160 chars max)",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
  }},
  "cta": "Clear call-to-action message",
  "faqs": [
    {{"question": "Question 1", "answer": "Answer 1"}},
    {{"question": "Question 2", "answer": "Answer 2"}},
    {{"question": "Question 3", "answer": "Answer 3"}}
  ]
}}

Ensure all content:
- Aligns with STANDs framework (Secure, Trusted, Aligned, Neutral, Defendable, Sustainable)
- Is engaging and conversion-focused
- Maintains the specified tone
- Is in {language}
- Is original and compelling

Return ONLY valid JSON, no additional text."""
        
        return prompt
    
    def _call_bedrock(self, prompt: str) -> str:
        """Call AWS Bedrock Claude model"""
        try:
            # Prepare the request body for Claude
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
            
            # Invoke Bedrock
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType="application/json"
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except ClientError as e:
            raise Exception(f"Bedrock API error: {str(e)}")
    
    def _parse_response(
        self,
        response_text: str,
        title: str,
        description: str
    ) -> Dict[str, Any]:
        """Parse Claude's response and generate HTML/Markdown"""
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_text = response_text.strip()
            if "```json" in json_text:
                json_text = json_text.split("```json")[1].split("```")[0].strip()
            elif "```" in json_text:
                json_text = json_text.split("```")[1].split("```")[0].strip()
            
            content_data = json.loads(json_text)
            
            # Generate HTML and Markdown
            html_content = self._generate_html(content_data, title)
            markdown_content = self._generate_markdown(content_data, title)
            
            return {
                **content_data,
                "html_content": html_content,
                "markdown_content": markdown_content
            }
            
        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            return self._create_fallback_content(title, description, response_text)
    
    def _generate_html(self, content: Dict[str, Any], title: str) -> str:
        """Generate HTML content"""
        features_html = "".join([f"<li>{f}</li>" for f in content.get("features", [])])
        benefits_html = "".join([f"<li>{b}</li>" for b in content.get("benefits", [])])
        faqs_html = "".join([
            f'<div class="faq"><h3>{faq["question"]}</h3><p>{faq["answer"]}</p></div>'
            for faq in content.get("faqs", [])
        ])
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content.get("seo_meta", {}).get("title", title)}</title>
    <meta name="description" content="{content.get("seo_meta", {}).get("description", "")}">
    <meta name="keywords" content="{", ".join(content.get("seo_meta", {}).get("keywords", []))}">
</head>
<body>
    <header>
        <h1>{title}</h1>
    </header>
    <main>
        <section class="hero">
            <p>{content.get("hero_section", "")}</p>
        </section>
        <section class="features">
            <h2>Features</h2>
            <ul>{features_html}</ul>
        </section>
        <section class="benefits">
            <h2>Benefits</h2>
            <ul>{benefits_html}</ul>
        </section>
        <section class="cta">
            <button>{content.get("cta", "Get Started")}</button>
        </section>
        <section class="faqs">
            <h2>Frequently Asked Questions</h2>
            {faqs_html}
        </section>
    </main>
</body>
</html>"""
    
    def _generate_markdown(self, content: Dict[str, Any], title: str) -> str:
        """Generate Markdown content"""
        features_md = "\n".join([f"- {f}" for f in content.get("features", [])])
        benefits_md = "\n".join([f"- {b}" for b in content.get("benefits", [])])
        faqs_md = "\n".join([
            f"### {faq['question']}\n\n{faq['answer']}\n"
            for faq in content.get("faqs", [])
        ])
        
        return f"""# {title}

{content.get("hero_section", "")}

## Features

{features_md}

## Benefits

{benefits_md}

## Call to Action

{content.get("cta", "")}

## Frequently Asked Questions

{faqs_md}
"""
    
    def _create_fallback_content(
        self,
        title: str,
        description: str,
        raw_response: str
    ) -> Dict[str, Any]:
        """Create fallback content if JSON parsing fails"""
        return {
            "hero_section": f"Welcome to {title}. {description}",
            "features": ["Feature 1", "Feature 2", "Feature 3"],
            "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
            "seo_meta": {
                "title": title,
                "description": description[:160],
                "keywords": ["keyword1", "keyword2", "keyword3"]
            },
            "cta": "Get Started Today",
            "faqs": [
                {"question": "What is this?", "answer": description}
            ],
            "html_content": f"<html><body><h1>{title}</h1><p>{description}</p></body></html>",
            "markdown_content": f"# {title}\n\n{description}"
        }

