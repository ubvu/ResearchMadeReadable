
"""
Database models and schema for the research summary application.
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not found")

Base = declarative_base()

class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    authors = Column(Text)
    abstract = Column(Text)
    doi = Column(String(100))
    year = Column(Integer)
    journal = Column(String(200))
    pdf_path = Column(String(500))
    pdf_text = Column(Text)
    bibtex_entry = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    summaries = relationship("Summary", back_populates="paper")
    evaluations = relationship("Evaluation", back_populates="paper")

class Summary(Base):
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    content = Column(Text, nullable=False)
    model_used = Column(String(50), nullable=False)
    input_mode = Column(String(20), nullable=False)  # 'abstract' or 'full_pdf'
    prompt_used = Column(Text)
    temperature = Column(Float, default=0.7)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    paper = relationship("Paper", back_populates="summaries")
    evaluations = relationship("Evaluation", back_populates="summary")

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    summary_id = Column(Integer, ForeignKey("summaries.id"), nullable=False)
    factuality_score = Column(Integer, nullable=False)  # 1-5 scale
    readability_score = Column(Integer, nullable=False)  # 1-5 scale
    evaluator_comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    paper = relationship("Paper", back_populates="evaluations")
    summary = relationship("Summary", back_populates="evaluations")

# Database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
