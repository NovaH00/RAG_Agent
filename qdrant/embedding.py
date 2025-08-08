import os
from pathlib import Path
from typing import List, Union
import numpy as np

# Set HF_HOME to absolute path before importing any HF libraries
current_dir = Path(__file__).parent
models_dir = current_dir / "models"
os.environ['HF_HOME'] = str(models_dir)

from sentence_transformers import SentenceTransformer
from .config import Setting


class EmbeddingService:
    """
    Embedding service for generating embeddings for both queries and documents.
    Provides methods for indexing documents and retrieving embeddings for search queries.
    """
    
    def __init__(self):
        self.setting = Setting()
        self._model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the SentenceTransformer model with proper configuration."""
        try:
            self._model = SentenceTransformer(
                self.setting.EMBEDDING_MODEL,
                model_kwargs={
                    "device_map": "cpu"
                },
                tokenizer_kwargs={"padding_side": "left"},
            )
            print(f"Embedding model '{self.setting.EMBEDDING_MODEL}' loaded successfully.")
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            raise e
    
    def encode_query(self, query: str) -> np.ndarray:
        """
        Encode a search query into embeddings.
        Uses query-specific prompt for better retrieval performance.
        
        Args:
            query (str): The search query text
            
        Returns:
            np.ndarray: Query embedding vector
        """
        if not self._model:
            raise RuntimeError("Embedding model not initialized")
        
        try:
            # Use query prompt for better retrieval performance
            embedding = self._model.encode([query], prompt_name="query")
            return embedding[0]  # Return single embedding vector
        except Exception as e:
            print(f"Error encoding query: {e}")
            # Fallback to encoding without prompt if prompt fails
            embedding = self._model.encode([query])
            return embedding[0]
    
    def encode_document(self, document: str) -> np.ndarray:
        """
        Encode a document into embeddings for indexing.
        Uses document-specific prompt for better indexing performance.
        
        Args:
            document (str): The document text to encode
            
        Returns:
            np.ndarray: Document embedding vector
        """
        if not self._model:
            raise RuntimeError("Embedding model not initialized")
        
        try:
            # Use document prompt for better indexing performance
            embedding = self._model.encode([document], prompt_name="document")
            return embedding[0]  # Return single embedding vector
        except Exception as e:
            print(f"Error encoding document with prompt: {e}")
            # Fallback to encoding without prompt if prompt fails
            embedding = self._model.encode([document])
            return embedding[0]
    
    def encode_documents(self, documents: List[str]) -> np.ndarray:
        """
        Encode multiple documents into embeddings for batch indexing.
        Uses document-specific prompt for better indexing performance.
        
        Args:
            documents (List[str]): List of document texts to encode
            
        Returns:
            np.ndarray: Array of document embedding vectors
        """
        if not self._model:
            raise RuntimeError("Embedding model not initialized")
        
        if not documents:
            return np.array([])
        
        try:
            # Use document prompt for better indexing performance
            embeddings = self._model.encode(documents, prompt_name="document")
            return embeddings
        except Exception as e:
            print(f"Error encoding documents with prompt: {e}")
            # Fallback to encoding without prompt if prompt fails
            embeddings = self._model.encode(documents)
            return embeddings
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            int: Embedding dimension
        """
        if not self._model:
            raise RuntimeError("Embedding model not initialized")
        
        # Get dimension by encoding a dummy text
        dummy_embedding = self._model.encode(["dummy"])
        return dummy_embedding.shape[1]
    
    def compute_similarity(self, query_embedding: np.ndarray, document_embeddings: np.ndarray) -> np.ndarray:
        """
        Compute cosine similarity between query and document embeddings.
        
        Args:
            query_embedding (np.ndarray): Query embedding vector
            document_embeddings (np.ndarray): Document embedding vectors
            
        Returns:
            np.ndarray: Similarity scores
        """
        if not self._model:
            raise RuntimeError("Embedding model not initialized")
        
        return self._model.similarity(query_embedding.reshape(1, -1), document_embeddings)
