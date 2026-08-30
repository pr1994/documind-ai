# OPTIMIZATION NOTE:
# Current: 4 LLM calls per document (clear, modular)
# Production: Could batch into 1 call (4x faster, 75% cheaper)
# Trade-off: Current design prioritizes readability & maintainability

# app/agents/orchestrator.py
from app.models.schemas import DocumentState, DocumentMetadata
from app.agents.ingestion_agent import IngestionAgent
from app.agents.classification_agent import ClassificationAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.enrichment_agent import EnrichmentAgent

class Orchestrator:
    """Master agent that orchestrates the document processing pipeline"""
    
    def __init__(self):
        """Initialize all sub-agents"""
        self.ingestion = IngestionAgent()
        self.classification = ClassificationAgent()
        self.compliance = ComplianceAgent()
        self.enrichment = EnrichmentAgent()
        self._current_file_bytes = None  # ADD THIS
    
    def process_document(self, filename: str, file_bytes: bytes) -> DocumentState:
        """
        Process a document through the simple pipeline.
        
        Args:
            filename: Original filename
            file_bytes: File content as bytes
        
        Returns:
            Final DocumentState after all processing
        """
        # Store file_bytes for use in nodes
        self._current_file_bytes = file_bytes
        
        print("\n" + "="*60)
        print(f"🚀 Starting document processing pipeline for: {filename}")
        print("="*60 + "\n")
        
        # Create initial state
        state = DocumentState(
            document_id="",
            filename=filename,
            raw_text="",
            chunks=[],
            metadata=DocumentMetadata(filename=filename),
            status="pending"
        )
        
        # Step 1: Ingestion
        print("[1/4] INGESTION AGENT")
        print("-" * 40)
        state.file_bytes = self._current_file_bytes
        state = self.ingestion.process(state)
        print()
        
        if state.status == "error":
            print("❌ Pipeline halted at ingestion")
            return state
        
        # Step 2: Classification
        print("[2/4] CLASSIFICATION AGENT")
        print("-" * 40)
        state = self.classification.process(state)
        print()
        
        if state.status == "error":
            print("❌ Pipeline halted at classification")
            return state
        
        # Step 3: Compliance Check
        print("[3/4] COMPLIANCE AGENT")
        print("-" * 40)
        state = self.compliance.process(state)
        print()
        
        if state.status == "error":
            print("❌ Pipeline halted at compliance check")
            return state
        
        # Step 4: Enrichment (conditional)
        if state.compliance_passed or state.metadata.risk_score < 0.8:
            print("[4/4] ENRICHMENT AGENT")
            print("-" * 40)
            state = self.enrichment.process(state)
            state.status = "completed"
            print()
        else:
            state.status = "blocked"
            print("[4/4] ENRICHMENT AGENT")
            print("-" * 40)
            print("⛔ Enrichment skipped - document blocked due to high compliance risk")
            print()
        
        print("="*60)
        print(f"✅ PIPELINE COMPLETE - Status: {state.status.upper()}")
        print("="*60 + "\n")
        
        return state