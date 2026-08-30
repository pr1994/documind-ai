# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for DocuMind AI"""
    
    # API Keys & URLs
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    
    # Model Settings
    MODEL_NAME = "openai/gpt-oss-120b"  # Groq's default fast model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # For embeddings
    
    # App Settings
    CHUNK_SIZE = 500  # Split documents into 500-char chunks
    CHUNK_OVERLAP = 50  # Overlap chunks by 50 chars for context
    TOP_K_RESULTS = 5  # Return top 5 search results
    
    def validate(self):
        """Check if all required keys are set"""
        if not self.GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY not found in .env file!")
        if not self.QDRANT_URL:
            raise ValueError("❌ QDRANT_URL not found in .env file!")
        if not self.QDRANT_API_KEY:
            raise ValueError("❌ QDRANT_API_KEY not found in .env file!")
        print("✅ All configuration keys loaded successfully!")

# Create a single config instance
config = Config()