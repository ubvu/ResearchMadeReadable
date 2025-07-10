
"""
Database models and schema for the research summary application using DuckDB and Parquet storage.
"""
import duckdb
import pandas as pd
import os
from datetime import datetime
from typing import Dict, Any, Optional
import pyarrow as pa
import pyarrow.parquet as pq

# Database configuration
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'db')
DUCKDB_PATH = os.path.join(DB_PATH, 'research_app.duckdb')

# Parquet file paths
PARQUET_FILES = {
    'papers': os.path.join(DB_PATH, 'papers.parquet'),
    'summaries': os.path.join(DB_PATH, 'summaries.parquet'),
    'translations': os.path.join(DB_PATH, 'translations.parquet'),
    'evaluations': os.path.join(DB_PATH, 'evaluations.parquet')
}

# Schema definitions for DuckDB tables
SCHEMAS = {
    'papers': {
        'id': 'INTEGER PRIMARY KEY',
        'title': 'VARCHAR(500) NOT NULL',
        'authors': 'TEXT',
        'abstract': 'TEXT',
        'doi': 'VARCHAR(100)',
        'year': 'INTEGER',
        'journal': 'VARCHAR(200)',
        'pdf_path': 'VARCHAR(500)',
        'pdf_text': 'TEXT',
        'bibtex_entry': 'TEXT',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    },
    'summaries': {
        'id': 'INTEGER PRIMARY KEY',
        'paper_id': 'INTEGER NOT NULL',
        'content': 'TEXT NOT NULL',
        'model_used': 'VARCHAR(50) NOT NULL',
        'input_mode': 'VARCHAR(20) NOT NULL',
        'prompt_used': 'TEXT',
        'temperature': 'DOUBLE DEFAULT 0.7',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    },
    'translations': {
        'id': 'INTEGER PRIMARY KEY',
        'summary_id': 'INTEGER NOT NULL',
        'target_language': 'VARCHAR(50) NOT NULL',
        'translated_content': 'TEXT NOT NULL',
        'model_used': 'VARCHAR(50) NOT NULL',
        'temperature': 'DOUBLE DEFAULT 0.3',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    },
    'evaluations': {
        'id': 'INTEGER PRIMARY KEY',
        'paper_id': 'INTEGER NOT NULL',
        'summary_id': 'INTEGER NOT NULL',
        'factuality_score': 'INTEGER NOT NULL',
        'readability_score': 'INTEGER NOT NULL',
        'evaluator_comments': 'TEXT',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
}

# PyArrow schemas for Parquet files
PARQUET_SCHEMAS = {
    'papers': pa.schema([
        ('id', pa.int64()),
        ('title', pa.string()),
        ('authors', pa.string()),
        ('abstract', pa.string()),
        ('doi', pa.string()),
        ('year', pa.int64()),
        ('journal', pa.string()),
        ('pdf_path', pa.string()),
        ('pdf_text', pa.string()),
        ('bibtex_entry', pa.string()),
        ('created_at', pa.timestamp('us'))
    ]),
    'summaries': pa.schema([
        ('id', pa.int64()),
        ('paper_id', pa.int64()),
        ('content', pa.string()),
        ('model_used', pa.string()),
        ('input_mode', pa.string()),
        ('prompt_used', pa.string()),
        ('temperature', pa.float64()),
        ('created_at', pa.timestamp('us'))
    ]),
    'translations': pa.schema([
        ('id', pa.int64()),
        ('summary_id', pa.int64()),
        ('target_language', pa.string()),
        ('translated_content', pa.string()),
        ('model_used', pa.string()),
        ('temperature', pa.float64()),
        ('created_at', pa.timestamp('us'))
    ]),
    'evaluations': pa.schema([
        ('id', pa.int64()),
        ('paper_id', pa.int64()),
        ('summary_id', pa.int64()),
        ('factuality_score', pa.int64()),
        ('readability_score', pa.int64()),
        ('evaluator_comments', pa.string()),
        ('created_at', pa.timestamp('us'))
    ])
}

class DuckDBConnection:
    """Manages DuckDB connection and operations."""
    
    def __init__(self):
        self.db_path = DUCKDB_PATH
        
    def get_connection(self):
        """Get a DuckDB connection."""
        return duckdb.connect(self.db_path)
    
    def execute_query(self, query: str, params: Optional[tuple] = None):
        """Execute a query and return results."""
        with self.get_connection() as conn:
            if params:
                return conn.execute(query, params).fetchall()
            return conn.execute(query).fetchall()
    
    def execute_query_df(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """Execute a query and return results as DataFrame."""
        with self.get_connection() as conn:
            if params:
                return conn.execute(query, params).df()
            return conn.execute(query).df()

def create_empty_parquet_file(table_name: str):
    """Create an empty Parquet file with the correct schema."""
    schema = PARQUET_SCHEMAS[table_name]
    # Create empty arrays for each field in the schema
    empty_data = {field.name: pa.array([], type=field.type) for field in schema}
    empty_table = pa.table(empty_data, schema=schema)
    pq.write_table(empty_table, PARQUET_FILES[table_name])

def ensure_parquet_files_exist():
    """Ensure all Parquet files exist, create empty ones if they don't."""
    os.makedirs(DB_PATH, exist_ok=True)
    
    for table_name in PARQUET_FILES:
        if not os.path.exists(PARQUET_FILES[table_name]):
            create_empty_parquet_file(table_name)

def create_tables():
    """Initialize DuckDB tables and Parquet files."""
    # Ensure Parquet files exist
    ensure_parquet_files_exist()
    
    # Create DuckDB connection and register Parquet files as tables
    with duckdb.connect(DUCKDB_PATH) as conn:
        for table_name, parquet_path in PARQUET_FILES.items():
            # Register Parquet file as a view in DuckDB
            conn.execute(f"""
                CREATE OR REPLACE VIEW {table_name} AS 
                SELECT * FROM read_parquet('{parquet_path}')
            """)

def get_next_id(table_name: str) -> int:
    """Get the next available ID for a table."""
    try:
        with duckdb.connect(DUCKDB_PATH) as conn:
            result = conn.execute(f"SELECT COALESCE(MAX(id), 0) + 1 FROM {table_name}").fetchone()
            return result[0] if result else 1
    except:
        return 1

# Data classes for type hints and data validation
class Paper:
    def __init__(self, id: int = None, title: str = None, authors: str = None, 
                 abstract: str = None, doi: str = None, year: int = None,
                 journal: str = None, pdf_path: str = None, pdf_text: str = None,
                 bibtex_entry: str = None, created_at: datetime = None):
        self.id = id
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.doi = doi
        self.year = year
        self.journal = journal
        self.pdf_path = pdf_path
        self.pdf_text = pdf_text
        self.bibtex_entry = bibtex_entry
        self.created_at = created_at or datetime.utcnow()

class Summary:
    def __init__(self, id: int = None, paper_id: int = None, content: str = None,
                 model_used: str = None, input_mode: str = None, prompt_used: str = None,
                 temperature: float = 0.7, created_at: datetime = None):
        self.id = id
        self.paper_id = paper_id
        self.content = content
        self.model_used = model_used
        self.input_mode = input_mode
        self.prompt_used = prompt_used
        self.temperature = temperature
        self.created_at = created_at or datetime.utcnow()

class Translation:
    def __init__(self, id: int = None, summary_id: int = None, target_language: str = None,
                 translated_content: str = None, model_used: str = None, 
                 temperature: float = 0.3, created_at: datetime = None):
        self.id = id
        self.summary_id = summary_id
        self.target_language = target_language
        self.translated_content = translated_content
        self.model_used = model_used
        self.temperature = temperature
        self.created_at = created_at or datetime.utcnow()

class Evaluation:
    def __init__(self, id: int = None, paper_id: int = None, summary_id: int = None,
                 factuality_score: int = None, readability_score: int = None,
                 evaluator_comments: str = None, created_at: datetime = None):
        self.id = id
        self.paper_id = paper_id
        self.summary_id = summary_id
        self.factuality_score = factuality_score
        self.readability_score = readability_score
        self.evaluator_comments = evaluator_comments
        self.created_at = created_at or datetime.utcnow()
