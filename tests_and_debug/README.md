
# Testing and Debugging Files

This directory contains all testing, debugging, and development utility files for the "Research made Readable" application. These files were created during the development and refactoring process to test specific functionality, debug issues, and validate the application's behavior.

## File Descriptions

### Main Testing Files

#### `test_app.py`
**Purpose:** Interactive Streamlit testing application for the BibTeX parser functionality  
**Description:** A standalone Streamlit app that provides a user interface for testing BibTeX parsing with the problematic test case that was encountered during development. It includes the full test BibTeX content and allows interactive testing of the parser.  
**Usage:** Run with `streamlit run test_app.py` from the project root directory

#### `test_bibtex.bib`
**Purpose:** BibTeX test data file  
**Description:** Contains the actual BibTeX entry that was causing parsing issues during development. This is a real research paper about verbal memory localization in epilepsy patients.  
**Usage:** Used as input data for various testing scripts

### Debug Scripts

#### `debug_bibtex_detailed.py`
**Purpose:** Comprehensive BibTeX parsing debug script  
**Description:** A detailed debugging script that tests multiple variations of BibTeX content to identify specific parsing issues. It includes various fixes and workarounds for common BibTeX formatting problems.  
**Key Features:**
- Tests multiple BibTeX format variations
- Identifies key/value parsing issues
- Tests special character handling
- Validates different formatting approaches
**Usage:** Run with `python debug_bibtex_detailed.py` from the project root directory

#### `debug_standalone.py`
**Purpose:** Standalone parser logic replication  
**Description:** A minimal script that replicates the exact parser logic to isolate and test specific parsing functionality without the full application overhead.  
**Key Features:**
- Preprocessing function testing
- BibTeX content normalization
- Isolated parser testing
**Usage:** Run with `python debug_standalone.py` from the project root directory

#### `debug_validation.py`
**Purpose:** Validation step debugging  
**Description:** Specifically designed to debug the validation step of the BibTeX parsing process. Helps identify where validation failures occur and why.  
**Key Features:**
- Step-by-step validation process
- Error identification and logging
- Validation rule testing
**Usage:** Run with `python debug_validation.py` from the project root directory

### Parser Testing Files

#### `test_bibtex_debug.py`
**Purpose:** BibTeX parser unit testing  
**Description:** Direct testing of the BibTeX parser with various input scenarios and edge cases.  
**Usage:** Run with `python test_bibtex_debug.py` from the project root directory

#### `test_fixed_parser.py`
**Purpose:** Testing of the fixed/improved parser implementation  
**Description:** Tests the corrected version of the BibTeX parser after bugs were identified and fixed.  
**Usage:** Run with `python test_fixed_parser.py` from the project root directory

## How to Run Tests

### Prerequisites
Ensure you have the application dependencies installed:
```bash
cd /home/ubuntu/research_summary_app
pip install -r requirements.txt
```

### Running Individual Tests

1. **Interactive BibTeX Testing:**
   ```bash
   streamlit run tests_and_debug/test_app.py
   ```

2. **Debug Scripts:**
   ```bash
   python tests_and_debug/debug_bibtex_detailed.py
   python tests_and_debug/debug_standalone.py
   python tests_and_debug/debug_validation.py
   ```

3. **Parser Tests:**
   ```bash
   python tests_and_debug/test_bibtex_debug.py
   python tests_and_debug/test_fixed_parser.py
   ```

### Running All Tests
To run all debugging scripts in sequence:
```bash
cd /home/ubuntu/research_summary_app
for file in tests_and_debug/debug_*.py tests_and_debug/test_*.py; do
    echo "Running $file..."
    python "$file"
    echo "---"
done
```

## Common Issues and Solutions

### BibTeX Parsing Issues
The main issues identified during testing were:
1. **Spaces in BibTeX keys** - Keys with spaces cause parsing failures
2. **Special characters in abstracts** - Long abstracts with special characters need preprocessing
3. **Empty fields** - Fields with empty values need proper handling
4. **Formatting inconsistencies** - Different BibTeX formatting styles need normalization

### Solutions Implemented
- **Key preprocessing** - Automatic removal of spaces and special characters from keys
- **Content normalization** - Consistent formatting of BibTeX entries
- **Error handling** - Graceful handling of parsing failures
- **Validation improvements** - Better validation of parsed content

## Development Notes

### Migration Context
These files were created during the migration from PostgreSQL to DuckDB/Parquet storage. The BibTeX parsing functionality was extensively tested to ensure it continued working properly after the database migration.

### Test Data
The test BibTeX entry (`test_bibtex.bib`) is a real research paper:
- **Title:** "Verbal Memory Localized in Non-language-dominant Hemisphere: Atypical Lateralization Revealed by Material-specific Memory Evaluation Using Super-selective Wada Test"
- **Journal:** NMC Case Report Journal
- **Year:** 2025
- **DOI:** 10.2176/jns-nmc.2024-0217

This particular entry was chosen because it contains:
- Spaces in the citation key
- Multiple authors with complex names
- A very long abstract with medical terminology
- Various special characters and formatting challenges

## Future Testing
When adding new features or making changes to the BibTeX parser:
1. Run all existing tests to ensure no regression
2. Add new test cases for new functionality
3. Update the test data if needed
4. Document any new debugging procedures

## Contributing
If you add new test files:
1. Follow the naming convention (`test_*.py` for tests, `debug_*.py` for debugging)
2. Add comprehensive docstrings and comments
3. Update this README with descriptions of new files
4. Ensure tests can be run independently

---
*This testing suite ensures the reliability and robustness of the "Research made Readable" application's BibTeX parsing functionality.*
