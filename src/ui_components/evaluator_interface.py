
"""
Streamlit UI components for the content evaluator interface.
"""
import streamlit as st
from typing import Dict, Any, Optional
import random
from ..database.operations import DatabaseOperations

class EvaluatorInterface:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        
        # Rating scale descriptions
        self.factuality_scale = {
            1: "Completely inaccurate - Contains major factual errors",
            2: "Mostly inaccurate - Contains several factual errors",
            3: "Partially accurate - Some facts are correct but some are wrong",
            4: "Mostly accurate - Minor factual issues",
            5: "Completely accurate - All facts are correct"
        }
        
        self.readability_scale = {
            1: "Very difficult to read - Unclear and confusing",
            2: "Difficult to read - Hard to follow",
            3: "Moderately readable - Some clarity issues",
            4: "Easy to read - Clear and well-written",
            5: "Very easy to read - Excellent clarity and flow"
        }
    
    def render(self):
        """Render the content evaluator interface."""
        st.title("🔍 Research Summary Evaluator")
        st.write("Review and rate AI-generated summaries for quality and accuracy")
        
        # Initialize session state
        if 'current_paper' not in st.session_state:
            st.session_state.current_paper = None
        if 'current_summary' not in st.session_state:
            st.session_state.current_summary = None
        if 'evaluation_count' not in st.session_state:
            st.session_state.evaluation_count = 0
        
        # Load paper for evaluation if none is loaded
        if st.session_state.current_paper is None:
            self._load_next_paper()
        
        # Show evaluation interface
        if st.session_state.current_paper and st.session_state.current_summary:
            self._render_evaluation_interface()
        else:
            st.info("📋 No papers with summaries available for evaluation. Please generate some summaries first.")
    
    def _load_next_paper(self):
        """Load the next paper for evaluation."""
        try:
            paper = self.db_ops.get_random_paper_for_evaluation()
            if paper:
                summaries = self.db_ops.get_summaries_by_paper(paper.id)
                if summaries:
                    st.session_state.current_paper = paper
                    st.session_state.current_summary = random.choice(summaries)
                else:
                    st.session_state.current_paper = None
                    st.session_state.current_summary = None
            else:
                st.session_state.current_paper = None
                st.session_state.current_summary = None
                
        except Exception as e:
            st.error(f"Error loading paper for evaluation: {str(e)}")
    
    def _render_evaluation_interface(self):
        """Render the main evaluation interface."""
        paper = st.session_state.current_paper
        summary = st.session_state.current_summary
        
        # Progress indicator
        st.write(f"**Evaluations completed:** {st.session_state.evaluation_count}")
        
        # Display paper and summary in columns
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📖 Original Abstract")
            if paper.abstract:
                st.write(paper.abstract)
            else:
                st.write("*No abstract available*")
            
            # Show paper metadata
            with st.expander("📝 Paper Details"):
                st.write(f"**Title:** {paper.title}")
                st.write(f"**Authors:** {paper.authors or 'Unknown'}")
                st.write(f"**Year:** {paper.year or 'Unknown'}")
                st.write(f"**Journal:** {paper.journal or 'Unknown'}")
        
        with col2:
            st.subheader("🤖 AI Generated Summary")
            st.write(summary.content)
            
            # Show summary metadata
            with st.expander("⚙️ Summary Details"):
                st.write(f"**Model:** {summary.model_used}")
                st.write(f"**Input Mode:** {summary.input_mode}")
                st.write(f"**Temperature:** {summary.temperature}")
                st.write(f"**Created:** {summary.created_at}")
        
        # Evaluation form
        st.subheader("📊 Evaluation")
        
        # Factuality rating
        st.write("**Factuality Rating**")
        st.write("*How accurately does the summary represent the original content?*")
        
        factuality_score = None
        for score, description in self.factuality_scale.items():
            if st.radio(
                "Factuality",
                [f"{score} - {description}"],
                key=f"factuality_{score}",
                label_visibility="collapsed"
            ):
                factuality_score = score
        
        if factuality_score is None:
            factuality_score = st.radio(
                "Factuality Score",
                list(self.factuality_scale.keys()),
                format_func=lambda x: f"{x} - {self.factuality_scale[x]}",
                key="factuality_radio"
            )
        
        st.write("---")
        
        # Readability rating
        st.write("**Readability Rating**")
        st.write("*How clear and easy to understand is the summary?*")
        
        readability_score = st.radio(
            "Readability Score",
            list(self.readability_scale.keys()),
            format_func=lambda x: f"{x} - {self.readability_scale[x]}",
            key="readability_radio"
        )
        
        # Comments
        st.write("**Additional Comments (Optional)**")
        comments = st.text_area(
            "Comments",
            placeholder="Any additional feedback about the summary...",
            label_visibility="collapsed"
        )
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("✅ Submit Evaluation", type="primary"):
                self._submit_evaluation(factuality_score, readability_score, comments)
        
        with col2:
            if st.button("⏭️ Skip"):
                self._skip_evaluation()
        
        with col3:
            if st.button("🔄 Refresh"):
                self._load_next_paper()
                st.rerun()
    
    def _submit_evaluation(self, factuality_score: int, readability_score: int, comments: str):
        """Submit the evaluation to the database."""
        try:
            self.db_ops.add_evaluation(
                paper_id=st.session_state.current_paper.id,
                summary_id=st.session_state.current_summary.id,
                factuality_score=factuality_score,
                readability_score=readability_score,
                evaluator_comments=comments if comments else None
            )
            
            st.session_state.evaluation_count += 1
            st.success("✅ Evaluation submitted successfully!")
            
            # Load next paper
            self._load_next_paper()
            
            # Auto-refresh after short delay
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error submitting evaluation: {str(e)}")
    
    def _skip_evaluation(self):
        """Skip the current evaluation and load next paper."""
        self._load_next_paper()
        st.info("⏭️ Skipped to next paper")
        st.rerun()
