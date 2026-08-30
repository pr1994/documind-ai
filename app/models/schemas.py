# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class DocumentMetadata(BaseModel):
    """Metadata about a document"""
    filename: str
    page_count: int = 0
    word_count: int = 0
    doc_type: Optional[str] = None
    summary: Optional[str] = None
    risk_score: float = 0.0
    compliance_flags: List[str] = []
    extracted_entities: Optional[dict] = None

class DocumentState(BaseModel):
    """State of a document as it moves through the pipeline"""
    document_id: str
    filename: str
    raw_text: str
    file_bytes: bytes = Field(default=b"", exclude=True)  # FIXED: exclude from JSON
    chunks: List[str] = []
    embeddings: List[List[float]] = []
    metadata: DocumentMetadata
    classification: Optional[str] = None
    compliance_passed: bool = True
    status: str = "pending"
    error_message: Optional[str] = None

class QueryRequest(BaseModel):
    """A user's question about documents"""
    question: str
    document_ids: Optional[List[str]] = None
    top_k: int = 5

class QueryResponse(BaseModel):
    """Answer to a user's question"""
    answer: str
    sources: List[dict]
    confidence: float