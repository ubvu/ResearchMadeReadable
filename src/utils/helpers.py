
"""
Utility helper functions for the research summary application.
"""
import streamlit as st
import os
import tempfile
from typing import Any, Dict, List, Optional
import pandas as pd
import plotly.graph_objects as go

def save_uploaded_file(uploaded_file, folder: str = "uploads") -> str:
    """Save uploaded file to temporary directory."""
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(os.getcwd(), "data", folder)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None

def format_text_preview(text: str, max_length: int = 200) -> str:
    """Format text for preview display."""
    if not text:
        return "No content available"
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."

def create_download_link(data: Any, filename: str, mime_type: str = "text/csv") -> str:
    """Create a download link for data."""
    try:
        if isinstance(data, pd.DataFrame):
            csv_buffer = data.to_csv(index=False)
            return st.download_button(
                label=f"Download {filename}",
                data=csv_buffer,
                file_name=filename,
                mime=mime_type
            )
        else:
            return st.download_button(
                label=f"Download {filename}",
                data=data,
                file_name=filename,
                mime=mime_type
            )
    except Exception as e:
        st.error(f"Error creating download link: {str(e)}")
        return None

def validate_file_type(file, allowed_types: List[str]) -> bool:
    """Validate uploaded file type."""
    if not file:
        return False
    
    file_extension = file.name.split('.')[-1].lower()
    return file_extension in allowed_types

def display_success_message(message: str):
    """Display success message with custom styling."""
    st.success(f"✅ {message}")

def display_error_message(message: str):
    """Display error message with custom styling."""
    st.error(f"❌ {message}")

def display_info_message(message: str):
    """Display info message with custom styling."""
    st.info(f"ℹ️ {message}")

def display_warning_message(message: str):
    """Display warning message with custom styling."""
    st.warning(f"⚠️ {message}")

def create_metric_card(title: str, value: Any, delta: Optional[str] = None, 
                      help_text: Optional[str] = None):
    """Create a metric card display."""
    st.metric(
        label=title,
        value=value,
        delta=delta,
        help=help_text
    )

def render_loading_spinner(text: str = "Loading..."):
    """Render loading spinner with custom text."""
    return st.spinner(text)

def safe_divide(numerator: float, denominator: float) -> float:
    """Safely divide two numbers, returning 0 if denominator is 0."""
    if denominator == 0:
        return 0
    return numerator / denominator

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_datetime(dt) -> str:
    """Format datetime for display."""
    if dt is None:
        return "Unknown"
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_score_color(score: float, max_score: float = 5.0) -> str:
    """Calculate color based on score."""
    normalized_score = score / max_score
    if normalized_score >= 0.8:
        return "green"
    elif normalized_score >= 0.6:
        return "yellow"
    else:
        return "red"

def create_progress_bar(current: int, total: int, text: str = "Progress"):
    """Create a progress bar."""
    if total == 0:
        progress = 0
    else:
        progress = current / total
    
    st.progress(progress, text=f"{text}: {current}/{total}")

def clean_text(text: str) -> str:
    """Clean text for display."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters that might cause issues
    text = text.replace('\r', '\n').replace('\n\n', '\n')
    
    return text.strip()
