
"""
PDF file parser for extracting text content from research papers.
"""
import PyPDF2
import pdfplumber
from typing import Optional, Dict, Any
import streamlit as st
import io

class PDFParser:
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, pdf_file) -> Optional[str]:
        """Extract text from PDF file using multiple methods."""
        try:
            # First try with pdfplumber (more accurate)
            text = self._extract_with_pdfplumber(pdf_file)
            if text and len(text.strip()) > 100:
                return text
            
            # Fallback to PyPDF2
            pdf_file.seek(0)  # Reset file pointer
            text = self._extract_with_pypdf2(pdf_file)
            if text and len(text.strip()) > 100:
                return text
            
            return None
            
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return None
    
    def _extract_with_pdfplumber(self, pdf_file) -> Optional[str]:
        """Extract text using pdfplumber."""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
        except Exception as e:
            st.warning(f"pdfplumber extraction failed: {str(e)}")
            return None
    
    def _extract_with_pypdf2(self, pdf_file) -> Optional[str]:
        """Extract text using PyPDF2."""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            st.warning(f"PyPDF2 extraction failed: {str(e)}")
            return None
    
    def get_pdf_metadata(self, pdf_file) -> Dict[str, Any]:
        """Extract metadata from PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            metadata = pdf_reader.metadata
            
            return {
                'title': metadata.get('/Title', ''),
                'author': metadata.get('/Author', ''),
                'subject': metadata.get('/Subject', ''),
                'creator': metadata.get('/Creator', ''),
                'producer': metadata.get('/Producer', ''),
                'creation_date': metadata.get('/CreationDate', ''),
                'modification_date': metadata.get('/ModDate', ''),
                'page_count': len(pdf_reader.pages)
            }
        except Exception as e:
            st.warning(f"Could not extract PDF metadata: {str(e)}")
            return {}
    
    def validate_pdf_file(self, pdf_file) -> bool:
        """Validate if file is a valid PDF."""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            return len(pdf_reader.pages) > 0
        except Exception:
            return False
    
    def get_pdf_preview(self, pdf_file, max_chars: int = 500) -> str:
        """Get a preview of the PDF content."""
        try:
            text = self.extract_text_from_pdf(pdf_file)
            if text:
                return text[:max_chars] + "..." if len(text) > max_chars else text
            return "Could not extract preview text"
        except Exception as e:
            return f"Error generating preview: {str(e)}"
