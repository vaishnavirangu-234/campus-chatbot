# src/knowledge_base.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import Config
from langchain.vectorstores import FAISS
from langchain.schema import Document
from typing import List, Dict
import os

class KnowledgeBase:
    def __init__(self, vector_store_path: str = "./data/faiss_index", 
                 chunk_size: int = 2000, chunk_overlap: int = 100):
        self.vector_store_path = vector_store_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=Config.GOOGLE_API_KEY
        )
        
        self.vector_store = None
        self._load_vector_store()
    
    def _load_vector_store(self):
        """Load existing vector store or create new one"""
        if os.path.exists(self.vector_store_path):
            try:
                self.vector_store = FAISS.load_local(
                    self.vector_store_path, 
                    self.embeddings,allow_dangerous_deserialization=True
                )
            except Exception as e:
                print(f"Error loading vector store: {e}")
                self.vector_store = None
        else:
            self.vector_store = None
    
    def add_documents(self, documents: List[Dict]):
        """Add documents to knowledge base"""
        # Convert to LangChain Document format
        lang_docs = [
            Document(
                page_content=doc.get('page_content', ''),
                metadata=doc.get('metadata', {})
            )
            for doc in documents
        ]
        
        # Split documents
        split_docs = self.text_splitter.split_documents(lang_docs)
        print("Split docs:", len(split_docs))
        
        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(
                split_docs, 
                self.embeddings
            )
        else:
            self.vector_store.add_documents(split_docs)
        
        # Save vector store
        self._save_vector_store()
        
        return len(split_docs)
    
    def _save_vector_store(self):
        """Save vector store to disk"""
        if self.vector_store:
            os.makedirs(self.vector_store_path, exist_ok=True)
            self.vector_store.save_local(self.vector_store_path)
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        if not self.vector_store:
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            return [
                {
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': score
                }
                for doc, score in results
            ]
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []
    
    def similarity_search_with_metadata(self, query: str, k: int = 5) -> List[Dict]:
        """Search with metadata filtering"""
        results = self.search(query, k=k)
        return results