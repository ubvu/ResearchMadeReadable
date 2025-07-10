
#!/usr/bin/env python3
"""
Test script to verify the fixed BibTeX parser works correctly.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from parsers.bibtex_parser import BibtexParser

# The original problematic BibTeX content (with spaces in key)
original_bibtex_content = """@article{Hana KIKUCHI20252024-0217,
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

def test_fixed_parser():
    """Test the fixed BibTeX parser with the original problematic content."""
    print("Testing Fixed BibTeX Parser")
    print("=" * 50)
    
    parser = BibtexParser()
    
    print("Original BibTeX content (with spaces in key):")
    print(original_bibtex_content[:200] + "...")
    print("\n" + "=" * 50)
    
    # Test the preprocessing
    print("Testing preprocessing...")
    cleaned_content = parser._preprocess_bibtex_content(original_bibtex_content)
    print(f"Cleaned content (first 200 chars): {cleaned_content[:200]}...")
    
    # Test full parsing
    print("\nTesting full parsing...")
    papers = parser.parse_bibtex_file(original_bibtex_content)
    
    if papers:
        print(f"✅ SUCCESS! Parser returned {len(papers)} papers")
        
        for i, paper in enumerate(papers):
            print(f"\nPaper {i+1}:")
            print(f"  Title: {paper['title'][:60]}...")
            print(f"  Authors: {paper['authors'][:60]}...")
            print(f"  Year: {paper['year']}")
            print(f"  Journal: {paper['journal']}")
            print(f"  DOI: {paper['doi']}")
            print(f"  Abstract length: {len(paper['abstract'])}")
            print(f"  Abstract preview: {paper['abstract'][:100]}...")
            
            # Test validation
            print(f"  Validation: {'✅ Valid' if paper['title'] and paper['authors'] else '❌ Invalid'}")
    else:
        print("❌ FAILURE! No papers found")
    
    print("\n" + "=" * 50)
    print("Testing with additional problematic BibTeX formats...")
    
    # Test other problematic formats
    test_cases = [
        # Multiple spaces in key
        "@article{Author Name 2024 Title,\n  title={Test Title},\n  author={Test Author},\n  year={2024}\n}",
        
        # Empty number field
        "@article{test2024,\n  title={Test Title},\n  author={Test Author},\n  number={ },\n  year={2024}\n}",
        
        # Multiple entries with various issues
        """@article{First Author 2024,
  title={First Paper},
  author={First Author},
  year={2024}
}

@article{Second Author 2025,
  title={Second Paper},
  author={Second Author},
  number={ },
  year={2025}
}"""
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest case {i+1}:")
        papers = parser.parse_bibtex_file(test_case)
        print(f"  Found {len(papers)} papers: {'✅' if papers else '❌'}")
        
        if papers:
            for j, paper in enumerate(papers):
                print(f"    Paper {j+1}: {paper['title'][:30]}... by {paper['authors'][:20]}...")

if __name__ == "__main__":
    test_fixed_parser()
