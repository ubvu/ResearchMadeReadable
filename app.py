
"""
Main Streamlit application for Research Paper Summary Generation and Evaluation.
"""
import streamlit as st
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import components
from src.ui_components.generator_interface import GeneratorInterface
from src.ui_components.evaluator_interface import EvaluatorInterface
from src.ui_components.dashboard_interface import DashboardInterface
from src.utils.session_manager import SessionManager
from src.database.models import create_tables

# Page configuration
st.set_page_config(
    page_title="ResearchLens - AI Summary & Evaluation",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2563EB;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    
    .role-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .role-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: #F8F9FA;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #2563EB;
        margin: 1rem 0;
    }
    
    .sidebar-nav {
        background: #F1F5F9;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_app():
    """Initialize the application."""
    # Initialize session state
    SessionManager.init_session_state()
    
    # Create database tables
    try:
        create_tables()
        st.session_state.database_available = True
    except Exception as e:
        st.session_state.database_available = False
        st.warning(f"Database not available: {str(e)}. Some features may be limited.")

def render_sidebar():
    """Render the sidebar navigation."""
    st.sidebar.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    st.sidebar.title("🔍 ResearchLens")
    st.sidebar.markdown("*AI-Powered Research Summary Platform*")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation menu
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["🏠 Home", "📝 Generator", "🔍 Evaluator", "📊 Dashboard"],
        index=0
    )
    
    # Set current page in session state
    page_mapping = {
        "🏠 Home": "home",
        "📝 Generator": "generator",
        "🔍 Evaluator": "evaluator",
        "📊 Dashboard": "dashboard"
    }
    
    SessionManager.set_state('current_page', page_mapping[page])
    
    # Sidebar statistics
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Quick Stats")
    
    if st.session_state.get('database_available', False):
        try:
            from src.database.operations import DatabaseOperations
            db_ops = DatabaseOperations()
            stats = db_ops.get_evaluation_stats()
            
            st.sidebar.metric("Total Evaluations", stats['total_evaluations'])
            st.sidebar.metric("Avg Factuality", f"{stats['avg_factuality']}/5")
            st.sidebar.metric("Avg Readability", f"{stats['avg_readability']}/5")
            
            db_ops.close()
        except Exception as e:
            st.sidebar.error("Unable to load stats")
    else:
        st.sidebar.info("Database not available")
    
    # Help section
    st.sidebar.markdown("---")
    st.sidebar.subheader("❓ Help")
    st.sidebar.markdown("""
    **Generator**: Upload papers and create AI summaries
    
    **Evaluator**: Rate summaries for quality and accuracy
    
    **Dashboard**: View analytics and export data
    """)

def render_home_page():
    """Render the home page with role selection."""
    st.markdown('<h1 class="main-header">🔍 ResearchLens</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Research Summary Generation & Evaluation Platform</p>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Welcome to ResearchLens, a comprehensive platform for generating and evaluating AI-powered research paper summaries.
    This tool helps researchers, students, and academics quickly understand complex research papers through intelligent summarization.
    """)
    
    # Role selection cards
    st.subheader("🎯 Choose Your Role")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📝 Content Generator", use_container_width=True, type="primary"):
            SessionManager.set_state('current_page', 'generator')
            st.rerun()
        
        st.markdown("""
        **Generate AI Summaries**
        - Upload BibTeX and PDF files
        - Configure AI models and prompts
        - Generate layman summaries
        - View generation history
        """)
    
    with col2:
        if st.button("🔍 Content Evaluator", use_container_width=True, type="secondary"):
            SessionManager.set_state('current_page', 'evaluator')
            st.rerun()
        
        st.markdown("""
        **Evaluate Summary Quality**
        - Review generated summaries
        - Rate factuality and readability
        - Provide feedback and comments
        - Help improve AI models
        """)
    
    # Quick access to dashboard
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("📊 View Dashboard", use_container_width=True):
            SessionManager.set_state('current_page', 'dashboard')
            st.rerun()
    
    # Features overview
    st.markdown("---")
    st.subheader("✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🤖 Multi-Model AI**
        - GPT-4, Claude, Deepseek
        - Llama, Mistral support
        - Customizable parameters
        """)
    
    with col2:
        st.markdown("""
        **📊 Quality Evaluation**
        - Factuality assessment
        - Readability scoring
        - Comparative analysis
        """)
    
    with col3:
        st.markdown("""
        **📈 Analytics Dashboard**
        - Model performance metrics
        - Data visualization
        - Export capabilities
        """)
    
    # About section
    with st.expander("ℹ️ About ResearchLens"):
        st.markdown("""
        ResearchLens is designed to bridge the gap between complex academic research and accessible understanding.
        Our platform leverages state-of-the-art AI models to create high-quality summaries that maintain scientific
        accuracy while improving readability for diverse audiences.
        
        **How it works:**
        1. Upload research papers (BibTeX metadata or PDF files)
        2. Configure AI models and summarization prompts
        3. Generate summaries using various AI models
        4. Evaluate summary quality through human review
        5. Analyze performance metrics and export data
        
        **Supported formats:**
        - BibTeX (.bib) files with abstracts
        - PDF research papers
        - Multiple AI model integrations
        """)

def main():
    """Main application function."""
    # Initialize the application
    initialize_app()
    
    # Render sidebar
    render_sidebar()
    
    # Get current page
    current_page = SessionManager.get_state('current_page', 'home')
    
    # Render appropriate page
    if current_page == 'home':
        render_home_page()
    elif current_page == 'generator':
        generator = GeneratorInterface()
        generator.render()
    elif current_page == 'evaluator':
        evaluator = EvaluatorInterface()
        evaluator.render()
    elif current_page == 'dashboard':
        dashboard = DashboardInterface()
        dashboard.render()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B7280; padding: 2rem;">
        <p>ResearchLens - AI-Powered Research Summary Platform</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
