
#!/usr/bin/env python3
"""
Debug script to test BibTeX parsing with the failing content.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from parsers.bibtex_parser import BibtexParser

# The problematic BibTeX content
test_bibtex_content = """@article{Hana KIKUCHI20252024-0217,
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

def test_bibtex_parsing():
    """Test the BibTeX parsing functionality."""
    print("Testing BibTeX Parser...")
    print("=" * 50)
    
    parser = BibtexParser()
    
    print("BibTeX content:")
    print(test_bibtex_content)
    print("\n" + "=" * 50)
    
    # Test parsing
    try:
        papers = parser.parse_bibtex_file(test_bibtex_content)
        print(f"Parser returned {len(papers)} papers")
        
        if papers:
            print("\nParsed paper details:")
            for i, paper in enumerate(papers):
                print(f"\nPaper {i+1}:")
                print(f"  Title: {paper.get('title', 'N/A')}")
                print(f"  Authors: {paper.get('authors', 'N/A')}")
                print(f"  Year: {paper.get('year', 'N/A')}")
                print(f"  Journal: {paper.get('journal', 'N/A')}")
                print(f"  DOI: {paper.get('doi', 'N/A')}")
                print(f"  Abstract length: {len(paper.get('abstract', ''))}")
                print(f"  Abstract preview: {paper.get('abstract', '')[:100]}...")
        else:
            print("❌ No papers found - this is the bug!")
            
    except Exception as e:
        print(f"❌ Error during parsing: {e}")
        import traceback
        traceback.print_exc()

    # Test with direct bibtexparser usage
    print("\n" + "=" * 50)
    print("Testing with direct bibtexparser usage...")
    
    try:
        import bibtexparser
        from bibtexparser.bparser import BibTexParser
        
        parser_direct = BibTexParser()
        parser_direct.ignore_nonstandard_types = True
        parser_direct.homogenize_fields = True
        
        bib_database = bibtexparser.loads(test_bibtex_content, parser=parser_direct)
        print(f"Direct parser found {len(bib_database.entries)} entries")
        
        if bib_database.entries:
            entry = bib_database.entries[0]
            print(f"Entry keys: {list(entry.keys())}")
            print(f"Entry type: {entry.get('ENTRYTYPE', 'N/A')}")
            print(f"Entry ID: {entry.get('ID', 'N/A')}")
            print(f"Title: {entry.get('title', 'N/A')}")
            print(f"Author: {entry.get('author', 'N/A')}")
            print(f"Abstract: {entry.get('abstract', 'N/A')[:100]}...")
        else:
            print("❌ No entries found with direct parser either!")
            
    except Exception as e:
        print(f"❌ Error with direct parser: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bibtex_parsing()
