
"""
Streamlit UI components for the dashboard interface.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any
import io
from ..database.operations import DatabaseOperations

class DashboardInterface:
    def __init__(self):
        self.db_ops = DatabaseOperations()
    
    def render(self):
        """Render the dashboard interface."""
        st.title("📈 Research Summary Dashboard")
        st.write("Analytics and insights from summary evaluations")
        
        try:
            # Get statistics
            stats = self.db_ops.get_evaluation_stats()
            
            if stats['total_evaluations'] == 0:
                st.info("📊 No evaluations available yet. Complete some evaluations to see dashboard data.")
                return
            
            # Overview metrics
            self._render_overview_metrics(stats)
            
            # Model performance charts
            self._render_model_performance(stats)
            
            # Data export section
            self._render_data_export()
            
        except Exception as e:
            st.error(f"Error loading dashboard data: {str(e)}")
    
    def _render_overview_metrics(self, stats: Dict[str, Any]):
        """Render overview metrics."""
        st.subheader("📊 Overview Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Evaluations",
                stats['total_evaluations'],
                help="Total number of evaluations completed"
            )
        
        with col2:
            st.metric(
                "Avg Factuality Score",
                f"{stats['avg_factuality']}/5",
                help="Average factuality rating across all evaluations"
            )
        
        with col3:
            st.metric(
                "Avg Readability Score",
                f"{stats['avg_readability']}/5",
                help="Average readability rating across all evaluations"
            )
    
    def _render_model_performance(self, stats: Dict[str, Any]):
        """Render model performance charts."""
        st.subheader("🤖 Model Performance")
        
        if not stats['model_stats']:
            st.info("No model performance data available yet.")
            return
        
        # Prepare data for visualization
        model_data = []
        for model_stat in stats['model_stats']:
            model_data.append({
                'Model': model_stat.model_used,
                'Avg Factuality': float(model_stat.avg_factuality),
                'Avg Readability': float(model_stat.avg_readability),
                'Evaluation Count': model_stat.eval_count
            })
        
        df = pd.DataFrame(model_data)
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Factuality and Readability comparison
            fig_comparison = go.Figure()
            
            fig_comparison.add_trace(go.Bar(
                name='Factuality',
                x=df['Model'],
                y=df['Avg Factuality'],
                marker_color='#2563EB'
            ))
            
            fig_comparison.add_trace(go.Bar(
                name='Readability',
                x=df['Model'],
                y=df['Avg Readability'],
                marker_color='#7C3AED'
            ))
            
            fig_comparison.update_layout(
                title="Average Scores by Model",
                xaxis_title="AI Model",
                yaxis_title="Average Score (1-5)",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)
        
        with col2:
            # Evaluation count pie chart
            fig_count = px.pie(
                df,
                values='Evaluation Count',
                names='Model',
                title="Evaluation Distribution by Model"
            )
            fig_count.update_layout(height=400)
            st.plotly_chart(fig_count, use_container_width=True)
        
        # Detailed model performance table
        st.subheader("📋 Detailed Model Performance")
        
        # Format the dataframe for display
        display_df = df.copy()
        display_df['Avg Factuality'] = display_df['Avg Factuality'].round(2)
        display_df['Avg Readability'] = display_df['Avg Readability'].round(2)
        
        # Add ranking
        display_df['Overall Score'] = (display_df['Avg Factuality'] + display_df['Avg Readability']) / 2
        display_df = display_df.sort_values('Overall Score', ascending=False)
        display_df['Rank'] = range(1, len(display_df) + 1)
        
        # Reorder columns
        display_df = display_df[['Rank', 'Model', 'Avg Factuality', 'Avg Readability', 
                                'Overall Score', 'Evaluation Count']]
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Best performing model highlight
        best_model = display_df.iloc[0]
        st.success(f"🏆 Best performing model: **{best_model['Model']}** with overall score of {best_model['Overall Score']:.2f}")
    
    def _render_data_export(self):
        """Render data export section."""
        st.subheader("📥 Data Export")
        
        try:
            # Export all data
            if st.button("📊 Export All Data as CSV"):
                data = self.db_ops.export_all_data()
                
                # Create ZIP file with all CSV files
                import zipfile
                import tempfile
                
                with tempfile.NamedTemporaryFile(mode='w+b', suffix='.zip', delete=False) as tmp_file:
                    with zipfile.ZipFile(tmp_file, 'w') as zip_file:
                        for table_name, df in data.items():
                            csv_buffer = io.StringIO()
                            df.to_csv(csv_buffer, index=False)
                            zip_file.writestr(f"{table_name}.csv", csv_buffer.getvalue())
                    
                    tmp_file.seek(0)
                    
                    st.download_button(
                        label="💾 Download Data Archive",
                        data=tmp_file.read(),
                        file_name="research_summary_data.zip",
                        mime="application/zip"
                    )
                
                st.success("✅ Data export ready for download!")
            
            # Show data preview
            with st.expander("👀 Data Preview"):
                data = self.db_ops.export_all_data()
                
                tab1, tab2, tab3 = st.tabs(["Papers", "Summaries", "Evaluations"])
                
                with tab1:
                    st.write("**Papers Data**")
                    if not data['papers'].empty:
                        st.dataframe(data['papers'].head(10))
                    else:
                        st.info("No papers data available")
                
                with tab2:
                    st.write("**Summaries Data**")
                    if not data['summaries'].empty:
                        st.dataframe(data['summaries'].head(10))
                    else:
                        st.info("No summaries data available")
                
                with tab3:
                    st.write("**Evaluations Data**")
                    if not data['evaluations'].empty:
                        st.dataframe(data['evaluations'].head(10))
                    else:
                        st.info("No evaluations data available")
        
        except Exception as e:
            st.error(f"Error exporting data: {str(e)}")
