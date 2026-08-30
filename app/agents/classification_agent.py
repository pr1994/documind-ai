# app/agents/classification_agent.py
from app.tools.llm_client import llm
from app.models.schemas import DocumentState

class ClassificationAgent:
    """Agent that classifies document type (Invoice, Contract, Policy, etc.)"""
    
    def process(self, state: DocumentState) -> DocumentState:
        """
        Classify the document type.
        
        Args:
            state: Current document state
        
        Returns:
            Updated state with classification
        """
        # Check if we have text to classify
        if not state.raw_text or len(state.raw_text) == 0:
            state.status = "error"
            state.error_message = "No text to classify"
            return state
        
        try:
            # Use LLM to classify
            doc_type = llm.classify_document(state.raw_text)
            
            # Update state
            state.classification = doc_type
            state.metadata.doc_type = doc_type
            state.status = "classified"
            
            print(f"✅ Classified as: {doc_type}")
            return state
            
        except Exception as e:
            state.status = "error"
            state.error_message = f"Classification failed: {str(e)}"
            print(f"❌ Classification error: {str(e)}")
            return state