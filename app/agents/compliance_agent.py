# app/agents/compliance_agent.py
from app.tools.llm_client import llm
from app.models.schemas import DocumentState

class ComplianceAgent:
    """Agent that checks for PII, sensitive data, and compliance issues"""
    
    def process(self, state: DocumentState) -> DocumentState:
        """
        Check document for compliance and sensitivity issues.
        
        Args:
            state: Current document state
        
        Returns:
            Updated state with compliance info
        """
        if not state.raw_text:
            state.status = "error"
            state.error_message = "No text to check"
            return state
        
        try:
            # Check compliance using LLM
            result = llm.check_compliance(state.raw_text)
            
            # Extract fields from result
            risk_score = result.get("risk_score", 0.5)
            flags = result.get("flags", [])
            
            # Update metadata
            state.metadata.risk_score = min(risk_score, 1.0)  # Ensure 0.0-1.0
            state.metadata.compliance_flags = flags
            
            # Determine if compliance passed
            # Pass if risk score is low (< 0.7)
            state.compliance_passed = risk_score < 0.7
            
            # Update status
            if state.compliance_passed:
                state.status = "compliant"
                print(f"✅ Compliance passed (risk score: {risk_score:.2f})")
            else:
                state.status = "flagged"
                print(f"⚠️  Compliance flagged (risk score: {risk_score:.2f})")
                print(f"   Flags: {flags}")
            
            return state
            
        except Exception as e:
            state.status = "error"
            state.error_message = f"Compliance check failed: {str(e)}"
            print(f"❌ Compliance error: {str(e)}")
            return state