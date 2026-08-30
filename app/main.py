# app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import config
from app.models.schemas import QueryRequest, QueryResponse, DocumentState
from app.agents.orchestrator import Orchestrator
from app.agents.rag_agent import RAGAgent
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="DocuMind AI",
    description="Enterprise Document Intelligence Platform",
    version="1.0.0"
)

# Add CORS middleware (allow requests from any origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
orchestrator = Orchestrator()
rag_agent = RAGAgent()

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/")
def health():
    """Health check endpoint"""
    return {
        "status": "DocuMind AI is running ✅",
        "version": "1.0.0",
        "message": "Upload documents via POST /upload or ask questions via POST /query"
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document.
    
    Accepts: PDF, DOCX, TXT files
    
    Returns: DocumentState with processing results
    """
    try:
        contents = await file.read()
        filename = file.filename or "unknown_file"
        
        result = orchestrator.process_document(filename, contents)
        
        # Return only serializable fields
        return {
            "document_id": result.document_id,
            "filename": result.filename,
            "status": result.status,
            "classification": result.classification,
            "chunks_count": len(result.chunks),
            "word_count": result.metadata.word_count,
            "summary": result.metadata.summary,
            "risk_score": result.metadata.risk_score,
            "compliance_passed": result.compliance_passed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Ask a question about uploaded documents.

    
    Request body:
    {
        "question": "What is this document about?",
        "document_ids": ["doc-id-1", "doc-id-2"],  # optional filter
        "top_k": 5  # number of results
    }
    
    Returns: Answer with sources and confidence score
    """
    try:
        return rag_agent.answer(request)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.get("/documents/{doc_id}")
async def get_document_status(doc_id: str):
    """Get status of a processed document (placeholder)"""
    return {
        "document_id": doc_id,
        "status": "completed",
        "note": "Full document storage will be implemented with database"
    }

# ============================================================================
# STARTUP & RUN
# ============================================================================

if __name__ == "__main__":
    # Validate config before running
    config.validate()
    
    # Run server
    print("\n🚀 Starting DocuMind AI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)