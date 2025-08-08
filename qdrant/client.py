from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams, PointStruct
from .config import Setting
from .embedding import EmbeddingService
from transformers import AutoTokenizer
import os
import uuid
from typing import List, Dict, Any

os.environ['HF_HOME'] = "./qdrant/models"

setting = Setting()

class Client:
    """
    Qdrant client for document indexing and retrieval using embeddings.
    """
    
    def __init__(self):
        self.client = QdrantClient(path="./qdrant/database")
        self.setting = setting
        self.embedding_service = EmbeddingService()
        self.tokenizer = None
        self._initialize_tokenizer()
        self._ensure_collection_exists()
    
    def _initialize_tokenizer(self):
        """Initialize the tokenizer for token-based chunking."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.setting.EMBEDDING_MODEL)
            print(f"Tokenizer for '{self.setting.EMBEDDING_MODEL}' loaded successfully.")
        except Exception as e:
            print(f"Error loading tokenizer: {e}")
            raise e
    
    def _ensure_collection_exists(self):
        """Ensure the collection exists with proper vector configuration."""
        try:
            # Get embedding dimension from the model
            embedding_dim = self.embedding_service.get_embedding_dimension()
            
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_exists = any(col.name == self.setting.COLLECTION_NAME for col in collections)
            
            if not collection_exists:
                # Create collection with proper vector configuration
                self.client.create_collection(
                    collection_name=self.setting.COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=embedding_dim,
                        distance=Distance.COSINE
                    )
                )
                print(f"Created collection '{self.setting.COLLECTION_NAME}' with dimension {embedding_dim}")
            else:
                print(f"Collection '{self.setting.COLLECTION_NAME}' already exists")
                
        except Exception as e:
            print(f"Error ensuring collection exists: {e}")
            raise e
    
    def _chunk_document(self, document: str) -> List[str]:
        """
        Split document into chunks using Recursive Text Splitter approach.
        Tries different separators hierarchically to maintain document structure.
        """
        if not self.tokenizer:
            raise RuntimeError("Tokenizer not initialized")
        
        # Define separators in order of preference (most to least structural)
        separators = [
            "\n\n",      # Paragraph breaks
            "\n",        # Line breaks
            ". ",        # Sentence endings
            "! ",        # Exclamation sentences
            "? ",        # Question sentences
            "; ",        # Semicolon breaks
            ", ",        # Comma breaks
            " ",         # Word breaks
            ""           # Character breaks (last resort)
        ]
        
        return self._recursive_split(document, separators, 0)
    
    def _recursive_split(self, text: str, separators: List[str], sep_index: int) -> List[str]:
        """
        Recursively split text using different separators.
        
        Args:
            text: Text to split
            separators: List of separators to try
            sep_index: Current separator index
            
        Returns:
            List of text chunks
        """
        # Check if text is small enough
        if self._get_token_count(text) <= self.setting.CHUNK_SIZE:
            return [text.strip()] if text.strip() else []
        
        # If we've exhausted all separators, force split by tokens
        if sep_index >= len(separators):
            return self._force_split_by_tokens(text)
        
        separator = separators[sep_index]
        chunks = []
        
        if separator == "":
            # Character-level splitting (last resort)
            return self._force_split_by_tokens(text)
        
        # Split by current separator
        splits = text.split(separator)
        
        current_chunk = ""
        
        for i, split in enumerate(splits):
            # Reconstruct the separator (except for the last split)
            test_chunk = current_chunk
            if test_chunk and i > 0:
                test_chunk += separator
            test_chunk += split
            
            # Check if adding this split would exceed chunk size
            if self._get_token_count(test_chunk) <= self.setting.CHUNK_SIZE:
                current_chunk = test_chunk
            else:
                # Current chunk is full, save it and start new chunk
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                # If single split is too large, recursively split it
                if self._get_token_count(split) > self.setting.CHUNK_SIZE:
                    chunks.extend(self._recursive_split(split, separators, sep_index + 1))
                    current_chunk = ""
                else:
                    current_chunk = split
        
        # Add remaining chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # Apply overlap between chunks
        return self._apply_overlap(chunks)
    
    def _get_token_count(self, text: str) -> int:
        """Get the number of tokens in text."""
        try:
            tokens = self.tokenizer.encode(text, add_special_tokens=False)
            return len(tokens)
        except Exception:
            # Fallback to word count estimation
            return len(text.split())
    
    def _force_split_by_tokens(self, text: str) -> List[str]:
        """Force split text by tokens when no separators work."""
        try:
            tokens = self.tokenizer.encode(text, add_special_tokens=False)
            chunks = []
            
            for i in range(0, len(tokens), self.setting.CHUNK_SIZE):
                chunk_end = min(i + self.setting.CHUNK_SIZE, len(tokens))
                chunk_tokens = tokens[i:chunk_end]
                chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
                if chunk_text.strip():
                    chunks.append(chunk_text.strip())
            
            return chunks
        except Exception:
            # Ultimate fallback
            return [text] if text.strip() else []
    
    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        """Apply overlap between chunks."""
        if len(chunks) <= 1 or self.setting.CHUNK_OVERLAP <= 0:
            return chunks
        
        overlapped_chunks = []
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                # First chunk, no previous overlap needed
                overlapped_chunks.append(chunk)
            else:
                # Get overlap from previous chunk
                prev_chunk = chunks[i - 1]
                overlap_text = self._get_chunk_overlap(prev_chunk, self.setting.CHUNK_OVERLAP)
                
                # Combine overlap with current chunk
                if overlap_text:
                    combined_chunk = overlap_text + " " + chunk
                    # Ensure combined chunk doesn't exceed size limit
                    if self._get_token_count(combined_chunk) <= self.setting.CHUNK_SIZE + self.setting.CHUNK_OVERLAP:
                        overlapped_chunks.append(combined_chunk)
                    else:
                        overlapped_chunks.append(chunk)
                else:
                    overlapped_chunks.append(chunk)
        
        return overlapped_chunks
    
    def _get_chunk_overlap(self, text: str, overlap_size: int) -> str:
        """Get the last overlap_size tokens from text."""
        try:
            tokens = self.tokenizer.encode(text, add_special_tokens=False)
            if len(tokens) <= overlap_size:
                return text
            
            overlap_tokens = tokens[-overlap_size:]
            return self.tokenizer.decode(overlap_tokens, skip_special_tokens=True).strip()
        except Exception:
            # Fallback to word-based overlap
            words = text.split()
            if len(words) <= overlap_size:
                return text
            return " ".join(words[-overlap_size:])
    
    def _chunk_document_fallback(self, document: str) -> List[str]:
        """Fallback word-based chunking if recursive splitting fails."""
        words = document.split()
        chunks = []
        
        for i in range(0, len(words), self.setting.CHUNK_SIZE - self.setting.CHUNK_OVERLAP):
            chunk_end = min(i + self.setting.CHUNK_SIZE, len(words))
            chunk = " ".join(words[i:chunk_end])
            chunks.append(chunk)
            
            if chunk_end >= len(words):
                break
                
        return chunks if chunks else [document]
    
    def update(self, new_doc: str):
        """
        Clear existing collection and reindex the new document.
        
        Args:
            new_doc (str): The new document to index
        """
        try:
            # Clear existing collection by recreating it
            print(f"Clearing collection '{self.setting.COLLECTION_NAME}'...")
            
            # Delete collection if it exists
            try:
                self.client.delete_collection(self.setting.COLLECTION_NAME)
                print(f"Deleted existing collection '{self.setting.COLLECTION_NAME}'")
            except Exception:
                pass  # Collection might not exist
            
            # Recreate collection
            self._ensure_collection_exists()
            
            # Chunk the document
            chunks = self._chunk_document(new_doc)
            print(f"Split document into {len(chunks)} chunks")
            
            # Generate embeddings for all chunks
            embeddings = self.embedding_service.encode_documents(chunks)
            
            # Create points for insertion
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.tolist(),
                    payload={
                        "text": chunk,
                        "chunk_index": i,
                        "document_id": "main_document"
                    }
                )
                points.append(point)
            
            # Insert points into collection
            self.client.upsert(
                collection_name=self.setting.COLLECTION_NAME,
                points=points
            )
            
            print(f"Successfully indexed {len(points)} chunks into collection '{self.setting.COLLECTION_NAME}'")
            
        except Exception as e:
            print(f"Error updating document: {e}")
            raise e
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks using the query.
        
        Args:
            query (str): The search query
            
        Returns:
            List[Dict[str, Any]]: List of search results with text and scores
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.encode_query(query)
            
            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.setting.COLLECTION_NAME,
                query_vector=query_embedding.tolist(),
                limit=self.setting.TOP_K,
                with_payload=True,
                with_vectors=False
            )
            
            # Format results
            results = []
            for result in search_results:
                results.append({
                    "text": result.payload.get("text", ""),
                    "score": result.score,
                    "chunk_index": result.payload.get("chunk_index", -1),
                    "document_id": result.payload.get("document_id", "")
                })
            
            return results
            
        except Exception as e:
            print(f"Error searching: {e}")
            raise e


# Global service instance for easy access
qdrant_service = Client()

import atexit
def cleanup():
    try:
        if hasattr(qdrant_service, 'client'):
            qdrant_service.client.close()
    except:
        pass

atexit.register(cleanup)