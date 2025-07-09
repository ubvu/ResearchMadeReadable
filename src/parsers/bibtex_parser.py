
"""
BibTeX file parser for extracting research paper metadata.
"""
import bibtexparser
from bibtexparser.bparser import BibTexParser
from typing import List, Dict, Any
import streamlit as st
import re

class BibtexParser:
    def __init__(self):
        pass
    
    def _create_parser(self):
        """Create a fresh parser instance for each parse operation."""
        parser = BibTexParser()
        parser.ignore_nonstandard_types = True
        parser.homogenize_fields = True
        parser.common_strings = True
        return parser
    
    def parse_bibtex_file(self, file_content: str) -> List[Dict[str, Any]]:
        """Parse BibTeX file content and extract paper information."""
        try:
            # Pre-process the BibTeX content to fix common formatting issues
            cleaned_content = self._preprocess_bibtex_content(file_content)
            
            # Create a fresh parser instance for each parse operation
            parser = self._create_parser()
            bib_database = bibtexparser.loads(cleaned_content, parser=parser)
            papers = []
            
            for entry in bib_database.entries:
                # Validate entry has minimum required fields
                if not self.validate_bibtex_entry(entry):
                    continue
                    
                # Create a BibDatabase with this entry for generating BibTeX string
                bib_db = bibtexparser.bibdatabase.BibDatabase()
                bib_db.entries = [entry]
                
                paper = {
                    'title': self._clean_field(entry.get('title', '')),
                    'authors': self._clean_field(entry.get('author', '')),
                    'abstract': self._clean_field(entry.get('abstract', '')),
                    'doi': entry.get('doi', ''),
                    'year': self._extract_year(entry.get('year', '')),
                    'journal': entry.get('journal', '') or entry.get('booktitle', ''),
                    'bibtex_entry': bibtexparser.dumps(bib_db)
                }
                papers.append(paper)
            
            return papers
            
        except Exception as e:
            # Log the error for debugging
            error_msg = f"Error parsing BibTeX file: {str(e)}"
            if hasattr(st, 'error'):
                st.error(error_msg)
            else:
                print(error_msg)
            return []
    
    def _preprocess_bibtex_content(self, content: str) -> str:
        """Pre-process BibTeX content to fix common formatting issues."""
        # Fix 1: Remove spaces from entry keys
        # Pattern: @entrytype{key with spaces, -> @entrytype{key_without_spaces,
        def fix_entry_key(match):
            entry_type = match.group(1)
            key = match.group(2)
            # Remove spaces and replace with underscores
            cleaned_key = re.sub(r'\s+', '_', key.strip())
            return f"@{entry_type}{{{cleaned_key},"
        
        # Match @entrytype{key with potential spaces,
        content = re.sub(r'@(\w+)\{([^,]+),', fix_entry_key, content)
        
        # Fix 2: Remove empty fields like "number={ },"
        content = re.sub(r'\s*\w+\s*=\s*\{\s*\},?\s*\n', '', content)
        
        # Fix 3: Ensure proper line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        return content
    
    def _clean_field(self, field_value: str) -> str:
        """Clean a field value by removing extra braces and whitespace."""
        if not field_value:
            return ''
        
        # Remove outer braces if present
        cleaned = field_value.strip()
        if cleaned.startswith('{') and cleaned.endswith('}'):
            cleaned = cleaned[1:-1]
        
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
    
    def _extract_year(self, year_str: str) -> int:
        """Extract year as integer from year string."""
        if not year_str:
            return None
        try:
            # Extract first 4 digits from year string
            import re
            year_match = re.search(r'\d{4}', year_str)
            if year_match:
                return int(year_match.group())
            return None
        except:
            return None
    
    def validate_bibtex_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate if a BibTeX entry has minimum required fields."""
        required_fields = ['title']
        return all(field in entry and entry[field] for field in required_fields)
    
    def get_paper_preview(self, entry: Dict[str, Any]) -> str:
        """Generate a preview string for a paper entry."""
        title = entry.get('title', 'Unknown Title')
        authors = entry.get('authors', 'Unknown Authors')
        year = entry.get('year', 'Unknown Year')
        
        return f"{title[:60]}... - {authors[:30]}... ({year})"
