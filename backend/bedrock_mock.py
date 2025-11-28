"""
Mock AWS Bedrock for local development.
Generates realistic responses without calling AWS.
"""
import json
import random


class BedrockMock:
    """Mock Bedrock client for local development"""
    
    def generate(self, prompt: str) -> str:
        """
        Generate a mock response that mimics Claude's output.
        
        Args:
            prompt: The prompt to generate content for
            
        Returns:
            JSON string with generated content
        """
        # Extract information from prompt
        title = self._extract_from_prompt(prompt, "about:", "\n")
        description = self._extract_from_prompt(prompt, "Description:\n", "\n\n")
        tone = self._extract_from_prompt(prompt, "Tone:", "\n")
        content_type = self._extract_from_prompt(prompt, "Content Type:", "\n")
        
        # Generate mock content based on prompt
        hero_section = self._generate_hero(title, description, tone)
        features = self._generate_features(description)
        benefits = self._generate_benefits(description)
        seo_meta = self._generate_seo(title, description)
        cta = self._generate_cta(tone)
        faqs = self._generate_faqs(title, description)
        
        response = {
            "hero_section": hero_section,
            "features": features,
            "benefits": benefits,
            "seo_meta": seo_meta,
            "cta": cta,
            "faqs": faqs
        }
        
        return json.dumps(response, indent=2)
    
    def _extract_from_prompt(self, prompt: str, start: str, end: str) -> str:
        """Extract text between start and end markers"""
        try:
            start_idx = prompt.find(start)
            if start_idx == -1:
                return ""
            start_idx += len(start)
            end_idx = prompt.find(end, start_idx)
            if end_idx == -1:
                end_idx = start_idx + 100
            return prompt[start_idx:end_idx].strip()
        except:
            return ""
    
    def _generate_hero(self, title: str, description: str, tone: str) -> str:
        """Generate hero section"""
        tone_words = {
            "professional": "Discover", "Transform", "Elevate",
            "casual": "Check out", "Get started with", "Try",
            "friendly": "Welcome to", "Join us for", "Experience",
            "formal": "We present", "Introducing", "We offer",
            "conversational": "Hey there!", "Ready to", "Let's explore"
        }
        
        action = tone_words.get(tone, "Discover")
        return f"{action} {title}. {description[:100]}... Experience the future of innovation and excellence."
    
    def _generate_features(self, description: str) -> list:
        """Generate features list"""
        base_features = [
            "Advanced security and encryption",
            "Real-time analytics and insights",
            "Seamless integration capabilities",
            "24/7 customer support",
            "Scalable infrastructure",
            "User-friendly interface"
        ]
        
        # Select 4 random features
        return random.sample(base_features, 4)
    
    def _generate_benefits(self, description: str) -> list:
        """Generate benefits list"""
        base_benefits = [
            "Increase productivity and efficiency",
            "Reduce operational costs",
            "Improve customer satisfaction",
            "Enhance security and compliance",
            "Accelerate time to market",
            "Enable data-driven decisions"
        ]
        
        # Select 3 random benefits
        return random.sample(base_benefits, 3)
    
    def _generate_seo(self, title: str, description: str) -> dict:
        """Generate SEO metadata"""
        keywords = [
            title.lower().split()[0] if title else "solution",
            "enterprise",
            "platform",
            "software",
            "technology"
        ]
        
        return {
            "title": title[:60] if len(title) <= 60 else title[:57] + "...",
            "description": description[:160] if len(description) <= 160 else description[:157] + "...",
            "keywords": keywords
        }
    
    def _generate_cta(self, tone: str) -> str:
        """Generate call-to-action"""
        ctas = {
            "professional": "Get Started Today",
            "casual": "Try It Now",
            "friendly": "Join Us Now",
            "formal": "Request a Demo",
            "conversational": "Let's Get Started!"
        }
        return ctas.get(tone, "Get Started")
    
    def _generate_faqs(self, title: str, description: str) -> list:
        """Generate FAQs"""
        return [
            {
                "question": f"What is {title}?",
                "answer": f"{title} is a comprehensive solution that {description[:80]}..."
            },
            {
                "question": "How does it work?",
                "answer": "Our platform uses advanced technology to provide seamless integration and powerful features that help you achieve your goals efficiently."
            },
            {
                "question": "Is it secure?",
                "answer": "Yes, we implement enterprise-grade security measures including encryption, access controls, and compliance with industry standards."
            }
        ]

