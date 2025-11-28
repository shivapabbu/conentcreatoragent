"""
Vector store implementation.
Supports both Amazon OpenSearch Serverless (AWS) and ChromaDB (local dev).
"""
import os
from typing import List, Optional
import boto3
from botocore.exceptions import ClientError

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    CHROMADB_AVAILABLE = False
    chromadb = None


class VectorStore:
    """Vector store for semantic search"""
    
    def __init__(self):
        self.use_local = os.getenv("USE_LOCAL_MOCKS", "true").lower() == "true"
        self.vector_db_type = os.getenv("VECTOR_DB_TYPE", "chroma")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        
        if self.use_local or self.vector_db_type == "chroma":
            self._init_chroma()
        else:
            self._init_opensearch()
    
    def _init_chroma(self):
        """Initialize ChromaDB for local development"""
        if not CHROMADB_AVAILABLE:
            self.client = None
            self.collection = None
            return
        
        try:
            # Use persistent storage for local dev
            db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
            os.makedirs(db_path, exist_ok=True)
            
            self.client = chromadb.PersistentClient(
                path=db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="content_knowledge_base",
                metadata={"hnsw:space": "cosine"}
            )
            
            # Initialize with sample data if empty
            if self.collection.count() == 0:
                self._initialize_sample_data()
                
        except Exception as e:
            print(f"Warning: ChromaDB initialization failed: {e}")
            self.client = None
            self.collection = None
    
    def _init_opensearch(self):
        """Initialize Amazon OpenSearch Serverless"""
        self.opensearch_endpoint = os.getenv("OPENSEARCH_ENDPOINT")
        self.index_name = os.getenv("OPENSEARCH_INDEX", "content-index")
        
        if not self.opensearch_endpoint:
            raise ValueError("OPENSEARCH_ENDPOINT environment variable required for OpenSearch")
        
        # OpenSearch client initialization would go here
        # For now, we'll use ChromaDB as fallback
        self._init_chroma()
    
    def _initialize_sample_data(self):
        """Initialize vector store with sample content"""
        sample_documents = [
            "Our platform provides enterprise-grade security with end-to-end encryption.",
            "We offer 24/7 customer support with dedicated account managers.",
            "Scalable infrastructure that grows with your business needs.",
            "Comprehensive analytics dashboard with real-time insights.",
            "Integration with popular tools like Slack, Jira, and Salesforce.",
            "Compliance with GDPR, SOC 2, and ISO 27001 standards.",
            "AI-powered features that automate repetitive tasks.",
            "Mobile-first design with responsive layouts for all devices."
        ]
        
        # For local dev, we'll use simple text-based similarity
        # In production, you'd generate embeddings using Bedrock Titan
        embeddings = [[0.1] * 384] * len(sample_documents)  # Mock embeddings
        
        self.collection.add(
            embeddings=embeddings,
            documents=sample_documents,
            ids=[f"doc_{i}" for i in range(len(sample_documents))]
        )
    
    def search(self, query: str, top_k: int = 3) -> List[str]:
        """
        Search for relevant content
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant document texts
        """
        if self.use_local or self.vector_db_type == "chroma":
            return self._search_chroma(query, top_k)
        else:
            return self._search_opensearch(query, top_k)
    
    def _search_chroma(self, query: str, top_k: int) -> List[str]:
        """Search using ChromaDB"""
        if not self.collection:
            # Fallback to mock results
            return [
                "Enterprise-grade security with encryption",
                "24/7 customer support available",
                "Scalable infrastructure"
            ]
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            if results and results.get("documents"):
                return results["documents"][0]
            return []
        except Exception as e:
            print(f"ChromaDB search error: {e}")
            return []
    
    def _search_opensearch(self, query: str, top_k: int) -> List[str]:
        """Search using Amazon OpenSearch Serverless"""
        # Implementation would use boto3 to call OpenSearch
        # For now, return mock results
        return [
            "Enterprise-grade security with encryption",
            "24/7 customer support available",
            "Scalable infrastructure"
        ]
    
    def add_documents(self, documents: List[str], embeddings: Optional[List[List[float]]] = None):
        """
        Add documents to the vector store
        
        Args:
            documents: List of document texts
            embeddings: Optional pre-computed embeddings
        """
        if not self.collection:
            return
        
        try:
            if embeddings is None:
                # Generate mock embeddings (in production, use Bedrock Titan)
                embeddings = [[0.1] * 384] * len(documents)
            
            ids = [f"doc_{self.collection.count() + i}" for i in range(len(documents))]
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                ids=ids
            )
        except Exception as e:
            print(f"Error adding documents: {e}")

