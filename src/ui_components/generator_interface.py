
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
        st.title("📚 Research Summary Generator")
        st.write("Upload research papers and generate AI-powered summaries")
        
        # Initialize session state
        if 'parsed_papers' not in st.session_state:
            st.session_state.parsed_papers = []
        if 'selected_paper' not in st.session_state:
            st.session_state.selected_paper = None
        if 'generated_summary' not in st.session_state:
            st.session_state.generated_summary = None
        
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
                
                # Add to database and session state
                for paper_data in papers:
                    paper = self.db_ops.add_paper(**paper_data)
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
            
            # Show summary content
            st.write("**Summary Content:**")
            st.write(summary.content)
            
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
