
"""
Streamlit UI components for the content generator interface.
"""
import streamlit as st
from typing import Dict, Any, Optional
import tempfile
import os
from ..parsers.bibtex_parser import BibtexParser
from ..parsers.pdf_parser import PDFParser
from ..ai_models.model_interface import ModelManager
from ..ai_models.prompts import get_prompt_template, get_available_templates
from ..database.operations import DatabaseOperations

class GeneratorInterface:
    def __init__(self):
        self.bibtex_parser = BibtexParser()
        self.pdf_parser = PDFParser()
        self.model_manager = ModelManager()
        self.db_ops = DatabaseOperations()
    
    def render(self):
        """Render the content generator interface."""
        st.title("📚 Summary Generator")
        st.write("Upload research papers and generate AI-powered summaries")
        
        # Initialize session state
        if 'parsed_papers' not in st.session_state:
            st.session_state.parsed_papers = []
        if 'selected_paper' not in st.session_state:
            st.session_state.selected_paper = None
        if 'generated_summary' not in st.session_state:
            st.session_state.generated_summary = None
        if 'summary_translations' not in st.session_state:
            st.session_state.summary_translations = {}
        
        # Create two columns for layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            self._render_file_upload_section()
            self._render_configuration_section()
        
        with col2:
            self._render_output_section()
            self._render_history_section()
    
    def _render_file_upload_section(self):
        """Render file upload section."""
        st.subheader("📁 File Upload")
        
        # BibTeX file upload
        st.write("**Upload BibTeX File**")
        bibtex_file = st.file_uploader(
            "Choose a BibTeX file",
            type=['bib', 'bibtex'],
            help="Upload a BibTeX file containing paper metadata and abstracts"
        )
        
        if bibtex_file is not None:
            self._process_bibtex_file(bibtex_file)
        
        # PDF file upload
        st.write("**Upload PDF Files**")
        pdf_files = st.file_uploader(
            "Choose PDF files",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload PDF files of research papers"
        )
        
        if pdf_files:
            self._process_pdf_files(pdf_files)
    
    def _process_bibtex_file(self, bibtex_file):
        """Process uploaded BibTeX file."""
        try:
            content = bibtex_file.read().decode('utf-8')
            papers = self.bibtex_parser.parse_bibtex_file(content)
            
            if papers:
                st.success(f"✅ Parsed {len(papers)} papers from BibTeX file")
                
                # Add to database and session state if database is available
                if st.session_state.get('database_available', False):
                    for paper_data in papers:
                        paper = self.db_ops.add_paper(**paper_data)
                        st.session_state.parsed_papers.append(paper)
                else:
                    # If database is not available, create mock paper objects
                    for i, paper_data in enumerate(papers):
                        # Create a simple mock paper object
                        class MockPaper:
                            def __init__(self, data):
                                self.id = i + 1
                                self.title = data['title']
                                self.authors = data['authors']
                                self.abstract = data['abstract']
                                self.year = data['year']
                                self.journal = data['journal']
                                self.doi = data['doi']
                                self.pdf_text = data.get('pdf_text', '')
                        
                        paper = MockPaper(paper_data)
                        st.session_state.parsed_papers.append(paper)
                
                # Show preview
                with st.expander("📋 Preview Parsed Papers"):
                    for i, paper in enumerate(papers):
                        st.write(f"**{i+1}. {paper['title'][:60]}...**")
                        st.write(f"Authors: {paper['authors'][:50]}...")
                        st.write(f"Year: {paper['year']}")
                        st.write("---")
            else:
                st.error("❌ No papers found in BibTeX file")
                
        except Exception as e:
            st.error(f"❌ Error processing BibTeX file: {str(e)}")
    
    def _process_pdf_files(self, pdf_files):
        """Process uploaded PDF files."""
        for pdf_file in pdf_files:
            try:
                # Extract text from PDF
                text = self.pdf_parser.extract_text_from_pdf(pdf_file)
                metadata = self.pdf_parser.get_pdf_metadata(pdf_file)
                
                if text:
                    # Save PDF temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(pdf_file.read())
                        pdf_path = tmp_file.name
                    
                    # Add to database
                    paper = self.db_ops.add_paper(
                        title=metadata.get('title', pdf_file.name),
                        authors=metadata.get('author', ''),
                        pdf_path=pdf_path,
                        pdf_text=text
                    )
                    
                    st.session_state.parsed_papers.append(paper)
                    st.success(f"✅ Processed PDF: {pdf_file.name}")
                else:
                    st.error(f"❌ Could not extract text from: {pdf_file.name}")
                    
            except Exception as e:
                st.error(f"❌ Error processing PDF {pdf_file.name}: {str(e)}")
    
    def _render_configuration_section(self):
        """Render configuration section."""
        st.subheader("⚙️ Configuration")
        
        # Paper selection
        if st.session_state.parsed_papers:
            paper_options = [
                f"{paper.title[:50]}... ({paper.id})" 
                for paper in st.session_state.parsed_papers
            ]
            
            selected_index = st.selectbox(
                "Select Paper",
                range(len(paper_options)),
                format_func=lambda x: paper_options[x],
                help="Choose a paper to generate summary for"
            )
            
            st.session_state.selected_paper = st.session_state.parsed_papers[selected_index]
        
        # Input mode selection
        input_mode = st.radio(
            "Input Mode",
            ["Abstract", "Full PDF"],
            help="Choose whether to summarize from abstract or full PDF text"
        )
        
        # AI model selection
        model_name = st.selectbox(
            "AI Model",
            self.model_manager.get_available_models(),
            help="Select the AI model for summary generation"
        )
        
        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Control creativity of the AI model (0.0 = deterministic, 1.0 = creative)"
        )
        
        # Prompt template selection
        template_name = st.selectbox(
            "Prompt Template",
            get_available_templates(),
            help="Choose a prompt template for summary generation"
        )
        
        # Custom prompt
        default_prompt = get_prompt_template(template_name)
        custom_prompt = st.text_area(
            "Custom Prompt",
            value=default_prompt,
            height=150,
            help="Edit the prompt for summary generation"
        )
        
        # Generate button
        if st.button("🚀 Generate Summary", type="primary"):
            if st.session_state.selected_paper:
                self._generate_summary(
                    st.session_state.selected_paper,
                    input_mode.lower().replace(' ', '_'),
                    model_name,
                    custom_prompt,
                    temperature
                )
            else:
                st.error("❌ Please select a paper first")
    
    def _generate_summary(self, paper, input_mode: str, model_name: str, 
                         prompt: str, temperature: float):
        """Generate summary for the selected paper."""
        try:
            # Determine input text based on mode
            if input_mode == "abstract":
                if not paper.abstract:
                    st.error("❌ No abstract available for this paper")
                    return
                input_text = paper.abstract
            else:  # full_pdf
                if not paper.pdf_text:
                    st.error("❌ No PDF text available for this paper")
                    return
                input_text = paper.pdf_text
            
            # Show progress
            with st.spinner(f"Generating summary using {model_name}..."):
                summary = self.model_manager.generate_summary(
                    model_name, input_text, prompt, temperature
                )
            
            if summary:
                # Save to database
                summary_obj = self.db_ops.add_summary(
                    paper_id=paper.id,
                    content=summary,
                    model_used=model_name,
                    input_mode=input_mode,
                    prompt_used=prompt,
                    temperature=temperature
                )
                
                st.session_state.generated_summary = summary_obj
                st.success("✅ Summary generated successfully!")
            else:
                st.error("❌ Failed to generate summary")
                
        except Exception as e:
            st.error(f"❌ Error generating summary: {str(e)}")
    
    def _translate_summary(self, summary, target_language: str):
        """Translate the summary to the target language."""
        try:
            # Check if translation already exists
            if hasattr(summary, 'id'):
                existing_translation = self.db_ops.get_translation_by_language(summary.id, target_language)
                if existing_translation:
                    # Load existing translation
                    if summary.id not in st.session_state.summary_translations:
                        st.session_state.summary_translations[summary.id] = {}
                    st.session_state.summary_translations[summary.id][target_language] = {
                        'content': existing_translation.translated_content,
                        'model': existing_translation.model_used,
                        'created_at': existing_translation.created_at
                    }
                    st.success(f"✅ Loaded existing {target_language} translation!")
                    return
            
            # Use the same model as the original summary
            model_name = summary.model_used
            
            # Show progress
            with st.spinner(f"Translating summary to {target_language}..."):
                translated_content = self.model_manager.translate_text(
                    model_name, summary.content, target_language
                )
            
            if translated_content:
                # Save to database if summary has ID
                if hasattr(summary, 'id'):
                    translation_obj = self.db_ops.add_translation(
                        summary_id=summary.id,
                        target_language=target_language,
                        translated_content=translated_content,
                        model_used=model_name
                    )
                    
                    # Store in session state
                    if summary.id not in st.session_state.summary_translations:
                        st.session_state.summary_translations[summary.id] = {}
                    st.session_state.summary_translations[summary.id][target_language] = {
                        'content': translated_content,
                        'model': model_name,
                        'created_at': translation_obj.created_at
                    }
                else:
                    # Store in session state for mock objects
                    mock_id = f"mock_{id(summary)}"
                    if mock_id not in st.session_state.summary_translations:
                        st.session_state.summary_translations[mock_id] = {}
                    st.session_state.summary_translations[mock_id][target_language] = {
                        'content': translated_content,
                        'model': model_name,
                        'created_at': 'Just now'
                    }
                
                st.success(f"✅ Successfully translated to {target_language}!")
            else:
                st.error("❌ Failed to translate summary")
                
        except Exception as e:
            st.error(f"❌ Error translating summary: {str(e)}")
    
    def _load_existing_translations(self, summary_id: int):
        """Load existing translations from database."""
        try:
            translations = self.db_ops.get_translations_by_summary(summary_id)
            if translations:
                if summary_id not in st.session_state.summary_translations:
                    st.session_state.summary_translations[summary_id] = {}
                
                for translation in translations:
                    st.session_state.summary_translations[summary_id][translation.target_language] = {
                        'content': translation.translated_content,
                        'model': translation.model_used,
                        'created_at': translation.created_at
                    }
        except Exception as e:
            # Silently handle database errors for existing translations
            pass
    
    def _render_output_section(self):
        """Render output section."""
        st.subheader("📄 Generated Summary")
        
        if st.session_state.generated_summary:
            summary = st.session_state.generated_summary
            
            # Show metadata
            st.write("**Summary Details:**")
            st.write(f"- **Model:** {summary.model_used}")
            st.write(f"- **Input Mode:** {summary.input_mode}")
            st.write(f"- **Temperature:** {summary.temperature}")
            st.write(f"- **Created:** {summary.created_at}")
            
            # Show original summary content
            st.write("**Original Summary (English):**")
            st.write(summary.content)
            
            # Translation section
            st.write("---")
            st.subheader("🌍 Translation")
            
            # Available languages
            languages = {
                "Dutch": "Dutch",
                "Spanish": "Spanish", 
                "French": "French",
                "German": "German",
                "Italian": "Italian",
                "Portuguese": "Portuguese",
                "Chinese": "Chinese",
                "Japanese": "Japanese",
                "Korean": "Korean",
                "Arabic": "Arabic",
                "Russian": "Russian",
                "Hindi": "Hindi"
            }
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                target_language = st.selectbox(
                    "Select Target Language",
                    list(languages.keys()),
                    index=0,  # Dutch as default
                    help="Choose the language for translation"
                )
            
            with col2:
                if st.button("🔄 Translate Summary", type="primary"):
                    self._translate_summary(summary, target_language)
            
            # Show existing translations
            translation_key = summary.id if hasattr(summary, 'id') else f"mock_{id(summary)}"
            
            # Load existing translations from database
            if hasattr(summary, 'id'):
                self._load_existing_translations(summary.id)
            
            # Display translations if available
            if translation_key in st.session_state.summary_translations:
                translations = st.session_state.summary_translations[translation_key]
                if target_language in translations:
                    st.write(f"**Translated Summary ({target_language}):**")
                    st.write(translations[target_language]['content'])
                    st.write(f"*Translated using {translations[target_language]['model']} at {translations[target_language]['created_at']}*")
            
            # Save button
            if st.button("💾 Save Summary"):
                st.success("✅ Summary saved to database!")
        else:
            st.info("Generate a summary to see results here")
    
    def _render_history_section(self):
        """Render history section."""
        st.subheader("📚 Recent Summaries")
        
        try:
            recent_summaries = self.db_ops.get_recent_summaries(limit=5)
            
            if recent_summaries:
                for summary in recent_summaries:
                    with st.expander(f"{summary.paper.title[:50]}... - {summary.model_used}"):
                        st.write(f"**Model:** {summary.model_used}")
                        st.write(f"**Input Mode:** {summary.input_mode}")
                        st.write(f"**Temperature:** {summary.temperature}")
                        st.write(f"**Created:** {summary.created_at}")
                        st.write("**Summary:**")
                        st.write(summary.content)
            else:
                st.info("No summaries generated yet")
                
        except Exception as e:
            st.error(f"Error loading history: {str(e)}")
