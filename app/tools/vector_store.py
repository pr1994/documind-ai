# app/tools/vector_store.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from app.config import config
from typing import List, Dict, Optional

class VectorStore:
    """Manage document embeddings and vector search using Qdrant"""
    
    def __init__(self):
        """Initialize Qdrant client and embedding model"""
        # Connect to Qdrant
        self.client = QdrantClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY
        )
        
        # Load embedding model
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        
        # Embedding dimension (all-MiniLM-L6-v2 produces 384-dimensional vectors)
        self.embedding_dim = 384
        
        # Create collection if it doesn't exist
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create the Qdrant collection if it doesn't exist"""
        try:
            # Try to get collection info
            self.client.get_collection("documents")
            print("✅ Qdrant collection 'documents' already exists")
        except:
            # Collection doesn't exist, create it
            self.client.create_collection(
                collection_name="documents",
                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=Distance.COSINE
                )
            )
            print("✅ Created Qdrant collection 'documents'")
    
    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        """
        Convert text chunks to embeddings.
        
        Args:
            chunks: List of text strings
        
        Returns:
            List of embedding vectors (each is a list of floats)
        """
        embeddings = self.embedding_model.encode(chunks, convert_to_tensor=False)
        # sentence-transformers may return a NumPy ndarray; normalize it to a
        # Python list-of-lists so it matches the declared return type.
        if hasattr(embeddings, "tolist"):
            normalized = embeddings.tolist()
            # Handle both batched embeddings and single-vector responses.
            if isinstance(normalized, list) and normalized and isinstance(normalized[0], (int, float)):
                return [list(map(float, normalized))]
            return [list(map(float, vec)) for vec in normalized]
        if isinstance(embeddings, list):
            return [list(map(float, vec)) for vec in embeddings]
        return [[float(value) for value in embeddings]]
    
    def upsert_document(self, document_id: str, chunks: List[str], metadata: Dict) -> None:
        """
        Store document chunks and embeddings in Qdrant.
        
        Args:
            document_id: Unique document identifier
            chunks: List of text chunks
            metadata: Document metadata (filename, doc_type, summary)
        """
        # Generate embeddings for all chunks
        embeddings = self.embed_chunks(chunks)
        
        # Create points for Qdrant
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point_id = int(f"{hash(document_id + str(i)) % 10000000:07d}")
            
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "chunk_index": i,
                    "text": chunk,
                    "filename": metadata.get("filename", "unknown"),
                    "doc_type": metadata.get("doc_type", "unknown"),
                    "summary": metadata.get("summary", "")
                }
            )
            points.append(point)
        
        # Upload to Qdrant
        self.client.upsert(
            collection_name="documents",
            points=points
        )
        print(f"✅ Stored {len(chunks)} chunks for document '{document_id}'")
    
    def search(self, query: str, top_k: int = 5, document_ids: Optional[List[str]] = None) -> List[Dict]:
        """
        Search for relevant document chunks.
        
        Args:
            query: Search question/text
            top_k: Number of results to return
            document_ids: Filter by specific documents (optional)
        
        Returns:
            List of matching chunks with scores
        """
        try:
            # Embed the query
            query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)

            # Search in Qdrant
            search_results = self.client.query_points(
                collection_name="documents",
                query=query_embedding,
                limit=top_k * 2
            )

            # Convert results to readable format
            results = []

            if search_results and hasattr(search_results, 'points'):
                for hit in search_results.points:
                    try:
                        # Safe payload extraction
                        payload = hit.payload
                        doc_id = str(payload.get("document_id", "unknown")) if payload else "unknown"

                        # Filter by document_ids if provided
                        if document_ids is not None and doc_id not in document_ids:
                            continue

                        result_dict = {
                            "document_id": doc_id,
                            "text": str(payload.get("text", "")) if payload else "",
                            "score": float(getattr(hit, 'similarity', 0.5)),
                            "filename": str(payload.get("filename", "unknown")) if payload else "unknown",
                            "doc_type": str(payload.get("doc_type", "unknown")) if payload else "unknown",
                            "chunk_index": int(payload.get("chunk_index", 0)) if payload else 0
                        }
                        results.append(result_dict)
                    except:
                        continue

            return results[:top_k]
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return []

# Create a single instance to use throughout the app
vector_store = None

def get_vector_store():
    global vector_store
    if vector_store is None:
        vector_store = VectorStore()
    return vector_store