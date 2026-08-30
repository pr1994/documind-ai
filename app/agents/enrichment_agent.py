# app/agents/enrichment_agent.py
from app.tools.llm_client import llm
from app.tools.vector_store import vector_store
from app.models.schemas import DocumentState

class EnrichmentAgent:
    """Agent that enriches documents with summaries, entities, and embeddings"""
    
    def process(self, state: DocumentState) -> DocumentState:
        """
        Enrich document: generate summary, extract entities, create embeddings.
        
        Args:
            state: Current document state
        
        Returns:
            Updated state with enrichment data
        """
        if not state.raw_text:
            state.status = "error"
            state.error_message = "No text to enrich"
            return state
        
        try:
            # Step 1: Generate summary
            print("📝 Generating summary...")
            summary = llm.generate_summary(state.raw_text)
            state.metadata.summary = summary
            print(f"✅ Summary: {summary[:100]}...")
            
            # Step 2: Extract entities
            print("🔍 Extracting entities...")
            entities = llm.extract_entities(state.raw_text)
            state.metadata.extracted_entities = entities
            print(f"✅ Extracted entities: {len(entities.get('persons', []))} persons, "
                  f"{len(entities.get('dates', []))} dates")
            
            # Step 3: Generate embeddings and store in Qdrant
            if state.chunks and len(state.chunks) > 0:
                print("🧠 Generating embeddings and storing in Qdrant...")
                
                # Generate embeddings
                embeddings = vector_store.embed_chunks(state.chunks)
                state.embeddings = embeddings
                
                # Store in Qdrant
                vector_store.upsert_document(
                    document_id=state.document_id,
                    chunks=state.chunks,
                    metadata={
                        "filename": state.filename,
                        "doc_type": state.classification or "UNKNOWN",
                        "summary": summary[:200] if summary else ""
                    }
                )
                print(f"✅ Stored {len(embeddings)} embeddings in Qdrant")
            
            # Update status
            state.status = "enriched"
            print("✅ Enrichment complete!")
            return state
            
        except Exception as e:
            state.status = "error"
            state.error_message = f"Enrichment failed: {str(e)}"
            print(f"❌ Enrichment error: {str(e)}")
            return state