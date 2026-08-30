# app/agents/rag_agent.py
from app.tools.vector_store import get_vector_store
from app.tools.llm_client import llm
from app.models.schemas import QueryRequest, QueryResponse
from typing import List, Dict

class RAGAgent:
    """Agent that answers questions using RAG (Retrieval-Augmented Generation)"""
    
    def answer(self, request: QueryRequest) -> QueryResponse:
        """
        Answer a question by retrieving relevant documents and using LLM.
        
        Args:
            request: QueryRequest with question and filters
        
        Returns:
            QueryResponse with answer and sources
        """
        try:
            print(f"🔍 Searching for: '{request.question}'")
            
            # Step 1: Retrieve relevant chunks from Qdrant
            vector_store = get_vector_store()
            results = vector_store.search(
                query=request.question,
                top_k=request.top_k,
                document_ids=request.document_ids
            )
            
            # Step 2: Check if we found anything
            if not results or len(results) == 0:
                print("❌ No relevant documents found")
                return QueryResponse(
                    answer="I couldn't find relevant information in the documents.",
                    sources=[],
                    confidence=0.0
                )
            
            print(f"✅ Found {len(results)} relevant chunks")
            
            # Step 3: Build context from retrieved chunks
            context_parts = []
            for i, result in enumerate(results, 1):
                context_parts.append(
                    f"[Source {i} - {result['filename']}]\n{result['text'][:500]}..."
                )
            
            context = "\n\n".join(context_parts)
            
            # Step 4: Create prompt for LLM
            system_prompt = """You are an enterprise document analyst. Answer the user's question using ONLY the provided context.
If the answer is not in the context, say "I don't have enough information to answer that."
Always cite your sources like [Source 1], [Source 2] when applicable."""
            
            user_prompt = f"""Context from documents:

{context}

Question: {request.question}

Answer:"""
            
            # Step 5: Get answer from LLM
            print("🤖 Generating answer...")
            answer = llm.invoke(user_prompt, system_prompt)
            
            # Step 6: Format sources
            sources = [
                {
                    "document_id": r["document_id"],
                    "filename": r["filename"],
                    "text_preview": r["text"][:200] + "...",
                    "relevance_score": round(r["score"], 3)
                }
                for r in results
            ]
            
            # Step 7: Calculate confidence
            confidence = round(sum(r["score"] for r in results) / len(results), 3)
            confidence = min(confidence, 1.0)
            
            print(f"✅ Answer generated (confidence: {confidence})")
            
            return QueryResponse(
                answer=answer,
                sources=sources,
                confidence=confidence
            )
            
        except Exception as e:
            print(f"❌ RAG error: {str(e)}")
            return QueryResponse(
                answer=f"Error processing question: {str(e)}",
                sources=[],
                confidence=0.0
            )