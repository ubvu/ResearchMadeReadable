
"""
Database operations for the research summary application using DuckDB and Parquet storage.
"""
import duckdb
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from typing import List, Optional, Dict, Any
import random
import os

from .models import (
    Paper, Summary, Evaluation, Translation, 
    DuckDBConnection, PARQUET_FILES, get_next_id,
    ensure_parquet_files_exist
)

class DatabaseOperations:
    def __init__(self):
        self.db_conn = DuckDBConnection()
        # Ensure all Parquet files exist on initialization
        ensure_parquet_files_exist()
    
    def close(self):
        """Close database connection (kept for compatibility)."""
        pass
    
    def _append_to_parquet(self, table_name: str, data: Dict[str, Any]) -> int:
        """Append a record to a Parquet file and return the new record's ID."""
        parquet_path = PARQUET_FILES[table_name]
        
        # Get next ID
        new_id = get_next_id(table_name)
        data['id'] = new_id
        
        # Add timestamp if not provided
        if 'created_at' not in data or data['created_at'] is None:
            data['created_at'] = datetime.utcnow()
        
        # Read existing data
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
        else:
            existing_df = pd.DataFrame()
        
        # Create new record DataFrame
        new_record_df = pd.DataFrame([data])
        
        # Combine and save
        updated_df = pd.concat([existing_df, new_record_df], ignore_index=True)
        updated_df.to_parquet(parquet_path, index=False)
        
        return new_id
    
    def add_paper(self, title: str, authors: str = None, abstract: str = None, 
                  doi: str = None, year: int = None, journal: str = None,
                  pdf_path: str = None, pdf_text: str = None, bibtex_entry: str = None) -> Paper:
        """Add a new paper to the database."""
        data = {
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'doi': doi,
            'year': year,
            'journal': journal,
            'pdf_path': pdf_path,
            'pdf_text': pdf_text,
            'bibtex_entry': bibtex_entry
        }
        
        paper_id = self._append_to_parquet('papers', data)
        
        # Create and return Paper object
        paper = Paper(
            id=paper_id,
            title=title,
            authors=authors,
            abstract=abstract,
            doi=doi,
            year=year,
            journal=journal,
            pdf_path=pdf_path,
            pdf_text=pdf_text,
            bibtex_entry=bibtex_entry,
            created_at=data['created_at']
        )
        
        return paper
    
    def add_summary(self, paper_id: int, content: str, model_used: str, 
                    input_mode: str, prompt_used: str = None, temperature: float = 0.7) -> Summary:
        """Add a new summary to the database."""
        data = {
            'paper_id': paper_id,
            'content': content,
            'model_used': model_used,
            'input_mode': input_mode,
            'prompt_used': prompt_used,
            'temperature': temperature
        }
        
        summary_id = self._append_to_parquet('summaries', data)
        
        # Create and return Summary object
        summary = Summary(
            id=summary_id,
            paper_id=paper_id,
            content=content,
            model_used=model_used,
            input_mode=input_mode,
            prompt_used=prompt_used,
            temperature=temperature,
            created_at=data['created_at']
        )
        
        return summary
    
    def add_evaluation(self, paper_id: int, summary_id: int, factuality_score: int, 
                       readability_score: int, evaluator_comments: str = None) -> Evaluation:
        """Add a new evaluation to the database."""
        data = {
            'paper_id': paper_id,
            'summary_id': summary_id,
            'factuality_score': factuality_score,
            'readability_score': readability_score,
            'evaluator_comments': evaluator_comments
        }
        
        evaluation_id = self._append_to_parquet('evaluations', data)
        
        # Create and return Evaluation object
        evaluation = Evaluation(
            id=evaluation_id,
            paper_id=paper_id,
            summary_id=summary_id,
            factuality_score=factuality_score,
            readability_score=readability_score,
            evaluator_comments=evaluator_comments,
            created_at=data['created_at']
        )
        
        return evaluation
    
    def add_translation(self, summary_id: int, target_language: str, translated_content: str, 
                       model_used: str, temperature: float = 0.3) -> Translation:
        """Add a new translation to the database."""
        data = {
            'summary_id': summary_id,
            'target_language': target_language,
            'translated_content': translated_content,
            'model_used': model_used,
            'temperature': temperature
        }
        
        translation_id = self._append_to_parquet('translations', data)
        
        # Create and return Translation object
        translation = Translation(
            id=translation_id,
            summary_id=summary_id,
            target_language=target_language,
            translated_content=translated_content,
            model_used=model_used,
            temperature=temperature,
            created_at=data['created_at']
        )
        
        return translation
    
    def get_translations_by_summary(self, summary_id: int) -> List[Translation]:
        """Get all translations for a specific summary."""
        translations_path = PARQUET_FILES["translations"]
        query = f"""
        SELECT * FROM read_parquet('{translations_path}')
        WHERE summary_id = ?
        """
        
        try:
            df = self.db_conn.execute_query_df(query, (summary_id,))
            translations = []
            
            for _, row in df.iterrows():
                translation = Translation(
                    id=row['id'],
                    summary_id=row['summary_id'],
                    target_language=row['target_language'],
                    translated_content=row['translated_content'],
                    model_used=row['model_used'],
                    temperature=row['temperature'],
                    created_at=row['created_at']
                )
                translations.append(translation)
            
            return translations
        except:
            return []
    
    def get_translation_by_language(self, summary_id: int, target_language: str) -> Optional[Translation]:
        """Get translation for a specific summary and language."""
        translations_path = PARQUET_FILES["translations"]
        query = f"""
        SELECT * FROM read_parquet('{translations_path}')
        WHERE summary_id = ? AND target_language = ?
        LIMIT 1
        """
        
        try:
            df = self.db_conn.execute_query_df(query, (summary_id, target_language))
            
            if df.empty:
                return None
            
            row = df.iloc[0]
            return Translation(
                id=row['id'],
                summary_id=row['summary_id'],
                target_language=row['target_language'],
                translated_content=row['translated_content'],
                model_used=row['model_used'],
                temperature=row['temperature'],
                created_at=row['created_at']
            )
        except:
            return None
    
    def get_papers_with_summaries(self, limit: int = 50) -> List[Paper]:
        """Get papers that have summaries for evaluation."""
        papers_path = PARQUET_FILES["papers"]
        summaries_path = PARQUET_FILES["summaries"]
        query = f"""
        SELECT DISTINCT p.* FROM read_parquet('{papers_path}') p
        JOIN read_parquet('{summaries_path}') s ON p.id = s.paper_id
        LIMIT ?
        """
        
        try:
            df = self.db_conn.execute_query_df(query, (limit,))
            papers = []
            
            for _, row in df.iterrows():
                paper = Paper(
                    id=row['id'],
                    title=row['title'],
                    authors=row.get('authors'),
                    abstract=row.get('abstract'),
                    doi=row.get('doi'),
                    year=row.get('year'),
                    journal=row.get('journal'),
                    pdf_path=row.get('pdf_path'),
                    pdf_text=row.get('pdf_text'),
                    bibtex_entry=row.get('bibtex_entry'),
                    created_at=row['created_at']
                )
                papers.append(paper)
            
            return papers
        except:
            return []
    
    def get_random_paper_for_evaluation(self) -> Optional[Paper]:
        """Get a random paper with summaries for evaluation."""
        papers = self.get_papers_with_summaries()
        if not papers:
            return None
        return random.choice(papers)
    
    def get_summaries_by_paper(self, paper_id: int) -> List[Summary]:
        """Get all summaries for a specific paper."""
        summaries_path = PARQUET_FILES["summaries"]
        query = f"""
        SELECT * FROM read_parquet('{summaries_path}')
        WHERE paper_id = ?
        ORDER BY created_at DESC
        """
        
        try:
            df = self.db_conn.execute_query_df(query, (paper_id,))
            summaries = []
            
            for _, row in df.iterrows():
                summary = Summary(
                    id=row['id'],
                    paper_id=row['paper_id'],
                    content=row['content'],
                    model_used=row['model_used'],
                    input_mode=row['input_mode'],
                    prompt_used=row.get('prompt_used'),
                    temperature=row['temperature'],
                    created_at=row['created_at']
                )
                summaries.append(summary)
            
            return summaries
        except:
            return []
    
    def get_evaluation_stats(self) -> Dict[str, Any]:
        """Get evaluation statistics for dashboard."""
        try:
            # Total evaluations
            evaluations_path = PARQUET_FILES["evaluations"]
            total_query = f"SELECT COUNT(*) as count FROM read_parquet('{evaluations_path}')"
            total_result = self.db_conn.execute_query_df(total_query)
            total_evaluations = total_result.iloc[0]['count'] if not total_result.empty else 0
            
            # Average scores
            avg_query = f"""
            SELECT 
                AVG(factuality_score) as avg_factuality,
                AVG(readability_score) as avg_readability
            FROM read_parquet('{evaluations_path}')
            """
            avg_result = self.db_conn.execute_query_df(avg_query)
            
            if not avg_result.empty and total_evaluations > 0:
                avg_factuality = avg_result.iloc[0]['avg_factuality'] or 0
                avg_readability = avg_result.iloc[0]['avg_readability'] or 0
            else:
                avg_factuality = 0
                avg_readability = 0
            
            # Model performance
            summaries_path = PARQUET_FILES["summaries"]
            model_query = f"""
            SELECT 
                s.model_used,
                AVG(e.factuality_score) as avg_factuality,
                AVG(e.readability_score) as avg_readability,
                COUNT(e.id) as eval_count
            FROM read_parquet('{summaries_path}') s
            JOIN read_parquet('{evaluations_path}') e ON s.id = e.summary_id
            GROUP BY s.model_used
            """
            
            try:
                model_stats_df = self.db_conn.execute_query_df(model_query)
                model_stats = []
                for _, row in model_stats_df.iterrows():
                    model_stats.append({
                        'model_used': row['model_used'],
                        'avg_factuality': row['avg_factuality'],
                        'avg_readability': row['avg_readability'],
                        'eval_count': row['eval_count']
                    })
            except:
                model_stats = []
            
            return {
                'total_evaluations': total_evaluations,
                'avg_factuality': round(avg_factuality, 2),
                'avg_readability': round(avg_readability, 2),
                'model_stats': model_stats
            }
        except:
            return {
                'total_evaluations': 0,
                'avg_factuality': 0,
                'avg_readability': 0,
                'model_stats': []
            }
    
    def export_all_data(self) -> Dict[str, pd.DataFrame]:
        """Export all data as DataFrames for CSV export."""
        result = {}
        
        for table_name, parquet_path in PARQUET_FILES.items():
            try:
                if os.path.exists(parquet_path):
                    df = pd.read_parquet(parquet_path)
                    result[table_name] = df
                else:
                    # Return empty DataFrame with proper columns if file doesn't exist
                    result[table_name] = pd.DataFrame()
            except:
                result[table_name] = pd.DataFrame()
        
        # Add translations to the export
        if 'translations' not in result:
            try:
                translations_df = pd.read_parquet(PARQUET_FILES['translations'])
                result['translations'] = translations_df
            except:
                result['translations'] = pd.DataFrame()
        
        return result
    
    def get_recent_summaries(self, limit: int = 10) -> List[Summary]:
        """Get recent summaries for history display."""
        summaries_path = PARQUET_FILES["summaries"]
        papers_path = PARQUET_FILES["papers"]
        query = f"""
        SELECT s.*, p.title as paper_title
        FROM read_parquet('{summaries_path}') s
        JOIN read_parquet('{papers_path}') p ON s.paper_id = p.id
        ORDER BY s.created_at DESC
        LIMIT ?
        """
        
        try:
            df = self.db_conn.execute_query_df(query, (limit,))
            summaries = []
            
            for _, row in df.iterrows():
                summary = Summary(
                    id=row['id'],
                    paper_id=row['paper_id'],
                    content=row['content'],
                    model_used=row['model_used'],
                    input_mode=row['input_mode'],
                    prompt_used=row.get('prompt_used'),
                    temperature=row['temperature'],
                    created_at=row['created_at']
                )
                # Add paper title as an attribute for display
                summary.paper_title = row.get('paper_title', 'Unknown Paper')
                summaries.append(summary)
            
            return summaries
        except:
            return []
