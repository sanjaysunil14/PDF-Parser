# Parsing USB PD Specification

## Overview  
This project delivers a **Python-based automated system** for extracting, organizing, and validating content from the **USB Power Delivery (USB PD) Specification** document.  
It converts the dense technical PDF into **structured, machine-readable formats (JSONL/Excel)**, enabling easy validation of the Table of Contents (ToC), metadata generation, and efficient downstream usage.

---

## Key Goals  
- Automate extraction of structured information from large technical specifications.  
- Transform unstructured PDF text into **JSONL datasets** suitable for search, analysis, and reference.  
- Cross-check consistency between the Table of Contents and actual parsed sections.  
- Generate metadata for quick reference, revision tracking, and section indexing.  
- Build **modular, reusable, and error-tolerant scripts** for document parsing.  

---

## Features  
- **Table of Contents Extraction** – Captures hierarchy, section IDs, and page references.  
- **Section Parsing** – Converts all major document sections into JSONL format while preserving numbering and nesting.  
- **Metadata Generation** – Automatically records document title, revision, and section statistics.  
- **Validation Reports** – Identifies missing sections, ordering issues, and page discrepancies by comparing ToC with parsed output.  
- **Multi-format Export** – Outputs structured data in JSON, JSONL, and Excel formats.  

---

## Installation & Usage  

### 1. Setup  
```bash
# Clone the repository
git clone <your-repo-link>
cd <project-folder>

# Place the USB PD Specification PDF into the data/ directory
```

### 2. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 3. Run the Parser & Validator  
```bash
python app.py
```

### 4. Run Tests  
```bash
python -m unittest discover tests
```

### 5. Check Output  
- `usb_pd_toc.jsonl` – Extracted Table of Contents  
- `usb_pd_spec.jsonl` – Parsed sections  
- `usb_pd_metadata.json` – Document metadata  
- `validation_report.xlsx` – Validation results  

All outputs are available in the `output/` folder.  

---

## Tech Stack & Requirements  
- **Language:** Python 3.x  
- **Libraries:** pdfplumber, openpyxl, spaCy  

---

## Project Modules  

### 📌 Parser  
- **extract_toc.py** – Extracts ToC entries (IDs, titles, levels, pages) using regex; outputs `usb_pd_toc.jsonl`.  
- **section_extractor.py** – Extracts structured section content; exports `usb_pd_spec.jsonl`.  
- **metadata_extractor.py** – Captures metadata (title, revision, section count); outputs `usb_pd_metadata.json`.  

### 📌 Validator  
- **section_validate.py** – Compares parsed sections with ToC, flags missing/misordered sections, and generates `validation_report.xlsx`.  


