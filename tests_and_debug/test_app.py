
import streamlit as st
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Test the BibTeX parser
from src.parsers.bibtex_parser import BibtexParser

st.title("BibTeX Parser Test")

# Test BibTeX content
test_bibtex = """@article{Hana KIKUCHI20252024-0217,
  title={Verbal Memory Localized in Non-language-dominant Hemisphere: Atypical Lateralization Revealed by Material-specific Memory Evaluation Using Super-selective Wada Test},
  author={Hana KIKUCHI and Shin-Ichiro OSAWA and Kazuo KAKINUMA and Shoko OTA and Kazuto KATSUSE and Kazushi UKISHIRO and Kazutaka JIN and Hidenori ENDO and Nobukazu NAKASATO and Kyoko SUZUKI},
  journal={NMC Case Report Journal},
  abstract={Hippocampectomy is effective for drug-resistant mesial temporal lobe epilepsy with hippocampal sclerosis. However, multiple studies have reported high risks associated with hippocampectomy in patients with mesial temporal lobe epilepsy without hippocampal sclerosis on magnetic resonance imaging and in those with preserved memory function. Verbal memory and language functions are believed to coexist in the same hemisphere. We present a case of left mesial temporal lobe epilepsy with atypical memory function lateralization revealed by super-selective infusion of propofol to the intracranial artery (super-selective Wada test). A 24-year-old right-handed man with drug-resistant focal impaired awareness seizures was diagnosed with left mesial temporal lobe epilepsy without hippocampal sclerosis, but he showed preserved verbal intelligence quotient and memory, suggesting a high risk of severe memory decline after hippocampectomy. We performed super-selective Wada test to the posterior cerebral artery to assess the lateralization of verbal and visual memory separately, and to the middle cerebral artery to assess language function. The results revealed right-sided dominance for both verbal and visual memory, although the language was left-dominant. Hippocampectomy was performed and resulted in freedom from seizures. Memory assessments 1 year postoperatively showed no decline in all subtests. In patients with drug-resistant epilepsy exhibiting atypical neuropsychological profiles, the memory-dominant, and language-dominant hemispheres may not align; detailed evaluations of function lateralization are necessary for tailored treatment.},
  volume={12},
  number={ },
  pages={65-71},
  year={2025},
  doi={10.2176/jns-nmc.2024-0217}
}"""

st.subheader("Test BibTeX Content")
st.code(test_bibtex[:200] + "...")

if st.button("Test BibTeX Parser"):
    with st.spinner("Parsing BibTeX..."):
        try:
            parser = BibtexParser()
            papers = parser.parse_bibtex_file(test_bibtex)
            
            if papers:
                st.success(f"✅ Successfully parsed {len(papers)} papers!")
                
                for i, paper in enumerate(papers):
                    st.write(f"**Paper {i+1}:**")
                    st.write(f"- **Title:** {paper['title'][:60]}...")
                    st.write(f"- **Authors:** {paper['authors'][:60]}...")
                    st.write(f"- **Year:** {paper['year']}")
                    st.write(f"- **Journal:** {paper['journal']}")
                    st.write(f"- **DOI:** {paper['doi']}")
                    st.write(f"- **Abstract length:** {len(paper['abstract'])} characters")
                    st.write(f"- **Abstract preview:** {paper['abstract'][:100]}...")
                    st.write("---")
            else:
                st.error("❌ No papers found in BibTeX content")
                
        except Exception as e:
            st.error(f"❌ Error parsing BibTeX: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

st.subheader("File Upload Test")
uploaded_file = st.file_uploader("Upload a BibTeX file", type=['bib', 'bibtex'])

if uploaded_file is not None:
    try:
        content = uploaded_file.read().decode('utf-8')
        st.code(content[:500] + "...")
        
        if st.button("Parse Uploaded File"):
            with st.spinner("Parsing uploaded file..."):
                try:
                    parser = BibtexParser()
                    papers = parser.parse_bibtex_file(content)
                    
                    if papers:
                        st.success(f"✅ Successfully parsed {len(papers)} papers from uploaded file!")
                        
                        for i, paper in enumerate(papers):
                            st.write(f"**Paper {i+1}:**")
                            st.write(f"- **Title:** {paper['title']}")
                            st.write(f"- **Authors:** {paper['authors']}")
                            st.write(f"- **Year:** {paper['year']}")
                            st.write(f"- **Journal:** {paper['journal']}")
                            st.write(f"- **DOI:** {paper['doi']}")
                            st.write(f"- **Abstract length:** {len(paper['abstract'])} characters")
                            st.write("---")
                    else:
                        st.error("❌ No papers found in uploaded BibTeX file")
                        
                except Exception as e:
                    st.error(f"❌ Error parsing uploaded file: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
                    
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
