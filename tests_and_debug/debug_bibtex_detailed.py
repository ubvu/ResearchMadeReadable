
#!/usr/bin/env python3
"""
Detailed debug script to identify specific BibTeX parsing issues.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import bibtexparser
from bibtexparser.bparser import BibTexParser

# Test different variations of the BibTeX content
test_variations = [
    # Original content
    """@article{Hana KIKUCHI20252024-0217,
  title={Verbal Memory Localized in Non-language-dominant Hemisphere: Atypical Lateralization Revealed by Material-specific Memory Evaluation Using Super-selective Wada Test},
  author={Hana KIKUCHI and Shin-Ichiro OSAWA and Kazuo KAKINUMA and Shoko OTA and Kazuto KATSUSE and Kazushi UKISHIRO and Kazutaka JIN and Hidenori ENDO and Nobukazu NAKASATO and Kyoko SUZUKI},
  journal={NMC Case Report Journal},
  abstract={Hippocampectomy is effective for drug-resistant mesial temporal lobe epilepsy with hippocampal sclerosis. However, multiple studies have reported high risks associated with hippocampectomy in patients with mesial temporal lobe epilepsy without hippocampal sclerosis on magnetic resonance imaging and in those with preserved memory function. Verbal memory and language functions are believed to coexist in the same hemisphere. We present a case of left mesial temporal lobe epilepsy with atypical memory function lateralization revealed by super-selective infusion of propofol to the intracranial artery (super-selective Wada test). A 24-year-old right-handed man with drug-resistant focal impaired awareness seizures was diagnosed with left mesial temporal lobe epilepsy without hippocampal sclerosis, but he showed preserved verbal intelligence quotient and memory, suggesting a high risk of severe memory decline after hippocampectomy. We performed super-selective Wada test to the posterior cerebral artery to assess the lateralization of verbal and visual memory separately, and to the middle cerebral artery to assess language function. The results revealed right-sided dominance for both verbal and visual memory, although the language was left-dominant. Hippocampectomy was performed and resulted in freedom from seizures. Memory assessments 1 year postoperatively showed no decline in all subtests. In patients with drug-resistant epilepsy exhibiting atypical neuropsychological profiles, the memory-dominant, and language-dominant hemispheres may not align; detailed evaluations of function lateralization are necessary for tailored treatment.},
  volume={12},
  number={ },
  pages={65-71},
  year={2025},
  doi={10.2176/jns-nmc.2024-0217}
}""",
    
    # Fix 1: Remove spaces from key
    """@article{HanaKIKUCHI20252024-0217,
  title={Verbal Memory Localized in Non-language-dominant Hemisphere: Atypical Lateralization Revealed by Material-specific Memory Evaluation Using Super-selective Wada Test},
  author={Hana KIKUCHI and Shin-Ichiro OSAWA and Kazuo KAKINUMA and Shoko OTA and Kazuto KATSUSE and Kazushi UKISHIRO and Kazutaka JIN and Hidenori ENDO and Nobukazu NAKASATO and Kyoko SUZUKI},
  journal={NMC Case Report Journal},
  abstract={Hippocampectomy is effective for drug-resistant mesial temporal lobe epilepsy with hippocampal sclerosis. However, multiple studies have reported high risks associated with hippocampectomy in patients with mesial temporal lobe epilepsy without hippocampal sclerosis on magnetic resonance imaging and in those with preserved memory function. Verbal memory and language functions are believed to coexist in the same hemisphere. We present a case of left mesial temporal lobe epilepsy with atypical memory function lateralization revealed by super-selective infusion of propofol to the intracranial artery (super-selective Wada test). A 24-year-old right-handed man with drug-resistant focal impaired awareness seizures was diagnosed with left mesial temporal lobe epilepsy without hippocampal sclerosis, but he showed preserved verbal intelligence quotient and memory, suggesting a high risk of severe memory decline after hippocampectomy. We performed super-selective Wada test to the posterior cerebral artery to assess the lateralization of verbal and visual memory separately, and to the middle cerebral artery to assess language function. The results revealed right-sided dominance for both verbal and visual memory, although the language was left-dominant. Hippocampectomy was performed and resulted in freedom from seizures. Memory assessments 1 year postoperatively showed no decline in all subtests. In patients with drug-resistant epilepsy exhibiting atypical neuropsychological profiles, the memory-dominant, and language-dominant hemispheres may not align; detailed evaluations of function lateralization are necessary for tailored treatment.},
  volume={12},
  number={ },
  pages={65-71},
  year={2025},
  doi={10.2176/jns-nmc.2024-0217}
}""",

    # Fix 2: Remove empty number field
    """@article{HanaKIKUCHI20252024-0217,
  title={Verbal Memory Localized in Non-language-dominant Hemisphere: Atypical Lateralization Revealed by Material-specific Memory Evaluation Using Super-selective Wada Test},
  author={Hana KIKUCHI and Shin-Ichiro OSAWA and Kazuo KAKINUMA and Shoko OTA and Kazuto KATSUSE and Kazushi UKISHIRO and Kazutaka JIN and Hidenori ENDO and Nobukazu NAKASATO and Kyoko SUZUKI},
  journal={NMC Case Report Journal},
  abstract={Hippocampectomy is effective for drug-resistant mesial temporal lobe epilepsy with hippocampal sclerosis. However, multiple studies have reported high risks associated with hippocampectomy in patients with mesial temporal lobe epilepsy without hippocampal sclerosis on magnetic resonance imaging and in those with preserved memory function. Verbal memory and language functions are believed to coexist in the same hemisphere. We present a case of left mesial temporal lobe epilepsy with atypical memory function lateralization revealed by super-selective infusion of propofol to the intracranial artery (super-selective Wada test). A 24-year-old right-handed man with drug-resistant focal impaired awareness seizures was diagnosed with left mesial temporal lobe epilepsy without hippocampal sclerosis, but he showed preserved verbal intelligence quotient and memory, suggesting a high risk of severe memory decline after hippocampectomy. We performed super-selective Wada test to the posterior cerebral artery to assess the lateralization of verbal and visual memory separately, and to the middle cerebral artery to assess language function. The results revealed right-sided dominance for both verbal and visual memory, although the language was left-dominant. Hippocampectomy was performed and resulted in freedom from seizures. Memory assessments 1 year postoperatively showed no decline in all subtests. In patients with drug-resistant epilepsy exhibiting atypical neuropsychological profiles, the memory-dominant, and language-dominant hemispheres may not align; detailed evaluations of function lateralization are necessary for tailored treatment.},
  volume={12},
  pages={65-71},
  year={2025},
  doi={10.2176/jns-nmc.2024-0217}
}""",
    
    # Fix 3: Simple test case
    """@article{test2025,
  title={Test Title},
  author={Test Author},
  journal={Test Journal},
  abstract={This is a test abstract.},
  year={2025}
}"""
]

def test_bibtex_variation(content, variation_name):
    """Test a specific BibTeX variation."""
    print(f"\nTesting {variation_name}:")
    print("=" * 50)
    
    try:
        parser = BibTexParser()
        parser.ignore_nonstandard_types = True
        parser.homogenize_fields = True
        parser.common_strings = True
        
        bib_database = bibtexparser.loads(content, parser=parser)
        print(f"Found {len(bib_database.entries)} entries")
        
        if bib_database.entries:
            entry = bib_database.entries[0]
            print(f"✅ SUCCESS!")
            print(f"  Entry ID: {entry.get('ID', 'N/A')}")
            print(f"  Entry type: {entry.get('ENTRYTYPE', 'N/A')}")
            print(f"  Title: {entry.get('title', 'N/A')[:50]}...")
            print(f"  Authors: {entry.get('author', 'N/A')[:50]}...")
            print(f"  Abstract length: {len(entry.get('abstract', ''))}")
            return True
        else:
            print("❌ No entries found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function."""
    print("BibTeX Parsing Debug - Testing Variations")
    print("=" * 70)
    
    variations = [
        ("Original (with spaces in key)", test_variations[0]),
        ("Fixed key (no spaces)", test_variations[1]),
        ("Fixed key + no empty number", test_variations[2]),
        ("Simple test case", test_variations[3])
    ]
    
    for name, content in variations:
        success = test_bibtex_variation(content, name)
        if success:
            print(f"\n🎉 Found working variation: {name}")
            break
    
    print("\n" + "=" * 70)
    print("Testing different parser configurations...")
    
    # Test with different parser configurations
    test_content = test_variations[2]  # The one without empty number field
    
    configs = [
        {"ignore_nonstandard_types": False, "homogenize_fields": False},
        {"ignore_nonstandard_types": True, "homogenize_fields": False},
        {"ignore_nonstandard_types": False, "homogenize_fields": True},
        {"ignore_nonstandard_types": True, "homogenize_fields": True},
    ]
    
    for i, config in enumerate(configs):
        print(f"\nConfig {i+1}: {config}")
        try:
            parser = BibTexParser()
            for key, value in config.items():
                setattr(parser, key, value)
            
            bib_database = bibtexparser.loads(test_content, parser=parser)
            print(f"  Found {len(bib_database.entries)} entries")
            
            if bib_database.entries:
                print(f"  ✅ SUCCESS with this config!")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    main()
