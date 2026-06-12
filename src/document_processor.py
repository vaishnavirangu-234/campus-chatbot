import PyPDF2
from typing import List, Dict
import json
from pathlib import Path

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page.extract_text()
        except Exception as e:
            print(f"Error processing PDF: {e}")
        
        return text
    
    def load_json_file(self, json_path: str) -> Dict:
        """Load JSON file"""
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return {}
    
    def chunk_text(self, text: str, chunk_size: int = None, 
                   chunk_overlap: int = None) -> List[str]:
        """Split text into overlapping chunks"""
        if chunk_size is None:
            chunk_size = self.chunk_size
        if chunk_overlap is None:
            chunk_overlap = self.chunk_overlap
        
        chunks = []
        for i in range(0, len(text), chunk_size - chunk_overlap):
            chunk = text[i:i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def process_handbook(self, pdf_path: str) -> List[Dict]:
        """Process college handbook PDF"""
        text = self.extract_text_from_pdf(pdf_path)
        chunks = self.chunk_text(text)
        
        documents = []
        for i, chunk in enumerate(chunks):
            documents.append({
                "page_content": chunk,
                "metadata": {
                    "source": pdf_path,
                    "chunk_id": i,
                    "type": "handbook"
                }
            })
        
        return documents
    
    def process_multiple_documents(self, doc_paths: List[str]) -> List[Dict]:
        """Process multiple documents"""
        all_documents = []
        
        for doc_path in doc_paths:
            if doc_path.endswith('.pdf'):
                docs = self.process_handbook(doc_path)
                all_documents.extend(docs)
            elif doc_path.endswith('.json'):
                json_data = self.load_json_file(doc_path)
                doc = {
                    "page_content": json.dumps(json_data),
                    "metadata": {
                        "source": doc_path,
                        "type": "json"
                    }
                }
                all_documents.append(doc)
        
        return all_documents