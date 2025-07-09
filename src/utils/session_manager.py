
"""
Session state management utilities for the Streamlit application.
"""
import streamlit as st
from typing import Any, Dict, Optional

class SessionManager:
    """Manages session state for the Streamlit application."""
    
    @staticmethod
    def init_session_state():
        """Initialize session state variables."""
        defaults = {
            'current_page': 'home',
            'parsed_papers': [],
            'selected_paper': None,
            'generated_summary': None,
            'current_evaluation_paper': None,
            'current_evaluation_summary': None,
            'evaluation_count': 0,
            'user_role': None
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def get_state(key: str, default: Any = None) -> Any:
        """Get session state value."""
        return st.session_state.get(key, default)
    
    @staticmethod
    def set_state(key: str, value: Any):
        """Set session state value."""
        st.session_state[key] = value
    
    @staticmethod
    def clear_state(key: str):
        """Clear session state value."""
        if key in st.session_state:
            del st.session_state[key]
    
    @staticmethod
    def reset_session():
        """Reset all session state."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        SessionManager.init_session_state()
