
"""
BibTeX file parser for extracting research paper metadata.
"""
import bibtexparser
from bibtexparser.bparser import BibTexParser
from typing import List, Dict, Any
import streamlit as st

class BibtexParser:
    def __init__(self):
        self.parser = BibTexParser()
        self.parser.ignore_nonstandard_types = True
        self.parser.homogenize_fields = True
    
    def parse_bibtex_file(self, file_content: str) -> List[Dict[str, Any]]:
        """Parse BibTeX file content and extract paper information."""
        try:
            bib_database = bibtexparser.loads(file_content, parser=self.parser)
            papers = []
            
            for entry in bib_database.entries:
                paper = {
                    'title': entry.get('title', '').replace('{', '').replace('}', ''),
                    'authors': entry.get('author', ''),
                    'abstract': entry.get('abstract', ''),
                    'doi': entry.get('doi', ''),
                    'year': self._extract_year(entry.get('year', '')),
                    'journal': entry.get('journal', '') or entry.get('booktitle', ''),
                    'bibtex_entry': bibtexparser.dumps(bibtexparser.bibdatabase.BibDatabase([entry]))
                }
                papers.append(paper)
            
            return papers
            
        except Exception as e:
            st.error(f"Error parsing BibTeX file: {str(e)}")
            return []
    
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
