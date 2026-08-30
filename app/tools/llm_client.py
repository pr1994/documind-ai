# app/tools/llm_client.py
from groq import Groq
from app.config import config
import json
from typing import Optional

class LLMClient:
    """Wrapper around Groq API for document processing tasks"""
    
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.MODEL_NAME
    
    def invoke(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a prompt to Groq and get a response.
        
        Args:
            prompt: User message
            system_prompt: System instructions (optional)
        
        Returns:
            str: The LLM's response
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=1000,
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        return content if content else ""
    
    def classify_document(self, text: str) -> str:
        """
        Classify document type (Invoice, Contract, Policy, Resume, Other).
        
        Args:
            text: Document text
        
        Returns:
            str: Document classification
        """
        prompt = f"""You are a document classifier. Read this document and classify it as ONE of: Invoice, Contract, Policy, Resume, Email, or Other.

Document:
{text[:1000]}...

Respond with ONLY the classification, nothing else. Example: "Invoice" """
        
        response = self.invoke(prompt)
        return response.strip()
    
    def check_compliance(self, text: str) -> dict:
        """
        Check document for PII, sensitive data, and compliance issues.
        
        Args:
            text: Document text
        
        Returns:
            dict: Compliance analysis
        """
        prompt = f"""You are a compliance officer. Analyze this document for sensitive data and compliance issues.

Document:
{text[:2000]}...

Respond with a JSON object containing:
- risk_score (0.0 to 1.0)
- has_pii (true/false)
- flags (list of issues)

Example: {{"risk_score": 0.5, "has_pii": true, "flags": ["Contains social security numbers", "Marked confidential"]}}"""
        
        response = self.invoke(prompt)
        
        # Try to parse JSON
        try:
            # Clean up response if it has markdown code fences
            clean_response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_response)
        except:
            # Fallback if JSON parsing fails
            return {
                "raw_analysis": response,
                "risk_score": 0.5,
                "has_pii": False,
                "flags": []
            }
    
    def generate_summary(self, text: str) -> str:
        """
        Generate a concise summary of the document.
        
        Args:
            text: Document text
        
        Returns:
            str: Summary
        """
        prompt = f"""Summarize this document in 2-3 sentences:

{text[:2000]}...

Summary:"""
        
        return self.invoke(prompt).strip()
    
    def extract_entities(self, text: str) -> dict:
        """
        Extract key entities (names, dates, amounts) from document.
        
        Args:
            text: Document text
        
        Returns:
            dict: Extracted entities
        """
        prompt = f"""Extract key entities from this document. Return a JSON object with:
- persons (list of person names)
- dates (list of important dates)
- amounts (list of money amounts)
- organizations (list of company/org names)

Document:
{text[:2000]}...

JSON response only:"""
        
        response = self.invoke(prompt)
        
        try:
            clean_response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_response)
        except:
            return {
                "persons": [],
                "dates": [],
                "amounts": [],
                "organizations": []
            }

# Create a single instance to use throughout the app
llm = LLMClient()