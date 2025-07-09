
"""
Database operations for the research summary application.
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from .models import Paper, Summary, Evaluation, SessionLocal, get_db
from typing import List, Optional, Dict, Any
import pandas as pd

class DatabaseOperations:
    def __init__(self):
        self.db = SessionLocal()
    
    def close(self):
        self.db.close()
    
    def add_paper(self, title: str, authors: str = None, abstract: str = None, 
                  doi: str = None, year: int = None, journal: str = None,
                  pdf_path: str = None, pdf_text: str = None, bibtex_entry: str = None) -> Paper:
        """Add a new paper to the database."""
        paper = Paper(
            title=title,
            authors=authors,
            abstract=abstract,
            doi=doi,
            year=year,
            journal=journal,
            pdf_path=pdf_path,
            pdf_text=pdf_text,
            bibtex_entry=bibtex_entry
        )
        self.db.add(paper)
        self.db.commit()
        self.db.refresh(paper)
        return paper
    
    def add_summary(self, paper_id: int, content: str, model_used: str, 
                    input_mode: str, prompt_used: str = None, temperature: float = 0.7) -> Summary:
        """Add a new summary to the database."""
        summary = Summary(
            paper_id=paper_id,
            content=content,
            model_used=model_used,
            input_mode=input_mode,
            prompt_used=prompt_used,
            temperature=temperature
        )
        self.db.add(summary)
        self.db.commit()
        self.db.refresh(summary)
        return summary
    
    def add_evaluation(self, paper_id: int, summary_id: int, factuality_score: int, 
                       readability_score: int, evaluator_comments: str = None) -> Evaluation:
        """Add a new evaluation to the database."""
        evaluation = Evaluation(
            paper_id=paper_id,
            summary_id=summary_id,
            factuality_score=factuality_score,
            readability_score=readability_score,
            evaluator_comments=evaluator_comments
        )
        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation
    
    def get_papers_with_summaries(self, limit: int = 50) -> List[Paper]:
        """Get papers that have summaries for evaluation."""
        return self.db.query(Paper).join(Summary).limit(limit).all()
    
    def get_random_paper_for_evaluation(self) -> Optional[Paper]:
        """Get a random paper with summaries for evaluation."""
        papers_with_summaries = self.db.query(Paper).join(Summary).all()
        if not papers_with_summaries:
            return None
        import random
        return random.choice(papers_with_summaries)
    
    def get_summaries_by_paper(self, paper_id: int) -> List[Summary]:
        """Get all summaries for a specific paper."""
        return self.db.query(Summary).filter(Summary.paper_id == paper_id).all()
    
    def get_evaluation_stats(self) -> Dict[str, Any]:
        """Get evaluation statistics for dashboard."""
        total_evaluations = self.db.query(Evaluation).count()
        avg_factuality = self.db.query(func.avg(Evaluation.factuality_score)).scalar() or 0
        avg_readability = self.db.query(func.avg(Evaluation.readability_score)).scalar() or 0
        
        # Model performance
        model_stats = self.db.query(
            Summary.model_used,
            func.avg(Evaluation.factuality_score).label('avg_factuality'),
            func.avg(Evaluation.readability_score).label('avg_readability'),
            func.count(Evaluation.id).label('eval_count')
        ).join(Evaluation).group_by(Summary.model_used).all()
        
        return {
            'total_evaluations': total_evaluations,
            'avg_factuality': round(avg_factuality, 2),
            'avg_readability': round(avg_readability, 2),
            'model_stats': model_stats
        }
    
    def export_all_data(self) -> Dict[str, pd.DataFrame]:
        """Export all data as DataFrames for CSV export."""
        papers_df = pd.read_sql_query(
            "SELECT * FROM papers", 
            self.db.get_bind()
        )
        summaries_df = pd.read_sql_query(
            "SELECT * FROM summaries", 
            self.db.get_bind()
        )
        evaluations_df = pd.read_sql_query(
            "SELECT * FROM evaluations", 
            self.db.get_bind()
        )
        
        return {
            'papers': papers_df,
            'summaries': summaries_df,
            'evaluations': evaluations_df
        }
    
    def get_recent_summaries(self, limit: int = 10) -> List[Summary]:
        """Get recent summaries for history display."""
        return self.db.query(Summary).join(Paper).order_by(desc(Summary.created_at)).limit(limit).all()
