# app/tools/document_parser.py
from io import BytesIO

import PyPDF2
from docx import Document
from typing import Dict, List

class DocumentParser:
    """Extract and process text from various document formats"""
    
    @staticmethod
    def parse(file_bytes: bytes, filename: str) -> Dict:
        """
        Parse a document and extract text.
        
        Args:
            file_bytes: File content as bytes
            filename: Original filename (used to detect file type)
        
        Returns:
            dict with keys: text, page_count, word_count
        """
        if filename.lower().endswith('.pdf'):
            return DocumentParser._parse_pdf(file_bytes, filename)
        elif filename.lower().endswith('.docx'):
            return DocumentParser._parse_docx(file_bytes, filename)
        elif filename.lower().endswith('.txt'):
            return DocumentParser._parse_txt(file_bytes, filename)
        else:
            raise ValueError(f"Unsupported file type: {filename}")
    
    @staticmethod
    def _parse_pdf(file_bytes: bytes, filename: str) -> Dict:
        """Extract text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            text_parts = []
            page_count = len(pdf_reader.pages)
            
            # Extract text from each page
            for page_num in range(page_count):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            full_text = "\n\n".join(text_parts)
            word_count = len(full_text.split())
            
            return {
                "text": full_text,
                "page_count": page_count,
                "word_count": word_count,
                "filename": filename
            }
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def _parse_docx(file_bytes: bytes, filename: str) -> Dict:
        """Extract text from DOCX (Word document)"""
        try:
            from io import BytesIO
            doc = Document(BytesIO(file_bytes))
            
            # Extract text from all paragraphs
            text_parts = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text_parts.append(para.text)
            
            full_text = "\n\n".join(text_parts)
            word_count = len(full_text.split())
            
            return {
                "text": full_text,
                "page_count": 1,  # DOCX doesn't have "pages" like PDF
                "word_count": word_count,
                "filename": filename
            }
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {str(e)}")
    
    @staticmethod
    def _parse_txt(file_bytes: bytes, filename: str) -> Dict:
        """Extract text from plain text file"""
        try:
            # Try UTF-8 first, then fall back to UTF-16, then Latin-1
            text = None
            try:
                text = file_bytes.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text = file_bytes.decode('utf-16')
                except:
                    text = file_bytes.decode('latin-1', errors='ignore')

            word_count = len(text.split())

            return {
                "text": text,
                "page_count": 1,
                "word_count": word_count,
                "filename": filename
            }
        except Exception as e:
            raise ValueError(f"Error parsing TXT: {str(e)}")
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Full document text
            chunk_size: Size of each chunk (characters)
            overlap: How many characters to overlap between chunks
        
        Returns:
            List of text chunks
        
        Example:
            text = "Hello world. This is a test. It has multiple sentences."
            chunks = chunk_text(text, chunk_size=20, overlap=5)
            # chunks = ["Hello world. This is", " is a test. It has", "has multiple senten..."]
        """
        chunks = []
        start = 0
        
        while start < len(text):
            # End position of this chunk
            end = start + chunk_size
            
            # Get the chunk
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Move start position (with overlap)
            start = end - overlap
        
        return chunks

# Create a single instance to use throughout the app
parser = DocumentParser()