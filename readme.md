# Intelligent Parsing & Structuring of USB PD Document

## Project Overview
A Python-based system to parse, structure, and validate the USB Power Delivery Specification PDF.  
It extracts the Table of Contents (ToC), processes all document sections into structured JSONL files, generates document metadata, and produces validation report comparing the ToC with parsed sections.

## Objectives
- Automate the extraction of structured content from complex technical PDFs.
- Convert unstructured PDF text into machine-readable formats (JSONL).
- Validate consistency between Table of Contents and actual document sections.
- Generate metadata for easier reference and search.
- Provide reusable, modular, and error-handled parsing scripts.

## Features
- Extracts Table of Contents with hierarchy, section IDs, and page numbers.
- Parses all sections of the document into JSONL format.
- Generates document metadata (title, revision, section count).
- Validates parsed data against the ToC for missing/mismatched sections, order errors, and page discrepancies.
- Exports results in JSONL, JSON, and Excel formats.

## Installation & Setup
1. Clone the repository and navigate to the project folder.
2. Place the USB PD Specification PDF in the `data/` directory.
3. Create and activate a Python virtual environment. (If needed)
4. Install dependencies:  " pip install -r requirements.txt "
5. Run the parser and validator: " python app.py "
6. Run unit test to verify parser and validator: 
        "python -m unittest discover tests"
7. Check the output/ folder for generated files

## Requirements
- Python 3.x
- pdfplumber
- openpyxl
- spacy

## Project Description
This project is divided into modular components for clarity and maintainability:
- Parser Module:
    1. extract_toc.py
    - Extracts the Table of Contents from the PDF.
    - Identifies section numbers, titles, hierarchy (level), and page numbers using regex patterns.
    - Exports structured output to usb_pd_toc.jsonl.
    2. section_extractor.py
    - Parses all main content sections from the PDF body.
    - Preserves section numbering, titles, and hierarchy structure.
    - Saves extracted sections to usb_pd_spec.jsonl.
    3. metadata_extractor.py
    - Extracts and stores document metadata (e.g. title, revision, total section count).
    - Outputs usb_pd_metadata.json.
- Validator Module
    1. section_validate.py
    - Compares parsed section data against the ToC.
    - Detects missing sections, ordering errors, and page mismatches.
    - Generates validation_report.xlsx for detailed analysis.

## Author
Dhana Varshini S  
Final Year B.Tech Artificial Intelligence & Data Science  
@ Sri Shakthi Institute of Engineering and Technology  
