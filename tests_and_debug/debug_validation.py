
#!/usr/bin/env python3
"""
Debug the validation step to see what's happening.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import bibtexparser
from bibtexparser.bparser import BibTexParser
import re

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

def preprocess_bibtex_content(content: str) -> str:
    """Pre-process BibTeX content to fix common formatting issues."""
    # Fix 1: Remove spaces from entry keys
    def fix_entry_key(match):
        entry_type = match.group(1)
        key = match.group(2)
        cleaned_key = re.sub(r'\s+', '_', key.strip())
        return f"@{entry_type}{{{cleaned_key},"
    
    content = re.sub(r'@(\w+)\{([^,]+),', fix_entry_key, content)
    
    # Fix 2: Remove empty fields like "number={ },"
    content = re.sub(r'\s*\w+\s*=\s*\{\s*\},?\s*\n', '', content)
    
    # Fix 3: Ensure proper line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    return content

def validate_bibtex_entry(entry) -> bool:
    """Validate if a BibTeX entry has minimum required fields."""
    required_fields = ['title']
    return all(field in entry and entry[field] for field in required_fields)

def debug_parsing():
    """Debug the parsing step by step."""
    print("Step-by-step BibTeX parsing debug")
    print("=" * 50)
    
    # Step 1: Show original content
    print("1. Original content:")
    print(test_bibtex[:200] + "...")
    
    # Step 2: Preprocess
    print("\n2. After preprocessing:")
    cleaned_content = preprocess_bibtex_content(test_bibtex)
    print(cleaned_content[:200] + "...")
    
    # Step 3: Parse with bibtexparser
    print("\n3. Parsing with bibtexparser:")
    parser = BibTexParser()
    parser.ignore_nonstandard_types = True
    parser.homogenize_fields = True
    parser.common_strings = True
    
    try:
        bib_database = bibtexparser.loads(cleaned_content, parser=parser)
        print(f"   Found {len(bib_database.entries)} entries")
        
        if bib_database.entries:
            entry = bib_database.entries[0]
            print(f"   Entry keys: {list(entry.keys())}")
            print(f"   Entry ID: {entry.get('ID', 'N/A')}")
            print(f"   Entry type: {entry.get('ENTRYTYPE', 'N/A')}")
            
            # Check each field
            print("\n4. Field extraction:")
            fields = ['title', 'author', 'abstract', 'journal', 'year', 'doi']
            for field in fields:
                value = entry.get(field, '')
                print(f"   {field}: {'✅' if value else '❌'} ({len(value)} chars)")
                if value:
                    print(f"      Preview: {value[:50]}...")
            
            # Check validation
            print("\n5. Validation:")
            is_valid = validate_bibtex_entry(entry)
            print(f"   Valid: {'✅' if is_valid else '❌'}")
            
            # Check required fields specifically
            required_fields = ['title']
            for field in required_fields:
                has_field = field in entry
                has_value = entry.get(field, '') if has_field else False
                print(f"   {field}: in entry={has_field}, has value={bool(has_value)}")
                
        else:
            print("   ❌ No entries found")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_parsing()
