# app/agents/ingestion_agent.py
from app.tools.document_parser import DocumentParser
from app.models.schemas import DocumentState, DocumentMetadata
import uuid

class IngestionAgent:
    """Agent that ingests documents and prepares them for processing"""
    
    def __init__(self):
        self.parser = DocumentParser()
    
    def process(self, state: DocumentState) -> DocumentState:
        """
        Ingest a document: parse, chunk, and create initial state.

        Args:
            state: DocumentState with filename and file_bytes

        Returns:
            DocumentState with parsed text and chunks
        """
        try:
            print(f"🔄 [Ingestion] Starting... filename={state.filename}")

            # Parse document using file_bytes and filename from state
            print(f"🔄 [Ingestion] Parsing file...")
            parsed = self.parser.parse(state.file_bytes, state.filename)

            # Chunk the text
            chunks = self.parser.chunk_text(
                parsed["text"],
                chunk_size=500,
                overlap=50
            )

            # Create unique document ID
            doc_id = str(uuid.uuid4())[:8]

            # Create metadata
            metadata = DocumentMetadata(
                filename=state.filename,
                page_count=parsed["page_count"],
                word_count=parsed["word_count"]
            )

            # Update state
            state.document_id = doc_id
            state.raw_text = parsed["text"]
            state.chunks = chunks
            state.metadata = metadata
            state.status = "ingested"

            print(f"✅ Ingested '{state.filename}' → {len(chunks)} chunks, {parsed['word_count']} words")
            return state

        except Exception as e:
            state.status = "error"
            state.error_message = str(e)
            print(f"❌ Error ingesting '{state.filename}': {str(e)}")
            return state