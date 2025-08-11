# **USB PD Specification Parsing & Validation System**

## **Overview**
This project is a prototype system that parses a USB Power Delivery (USB PD) specification PDF file and outputs the content in structured JSONL format, along with a validation Excel report.  
It is designed to:
- Extract the Table of Contents (ToC)
- Extract all document sections (hierarchical structure, figures, tables)
- Generate document metadata
- Validate parsed content against the ToC
- Allow keyword and hierarchy searches in the ToC



## **Project Structure**

├── comprehensive_usb_parser.py      # Main parser – extracts TOC, content, metadata
├── validation_report_generator.py    # Compares TOC & parsed content, generates XLS report
├── toc_search_engine.py              # Search tool for TOC entries
├── usb_pd_toc.jsonl                  # Generated TOC entries
├── usb_pd_spec.jsonl                 # Generated parsed content
├── usb_pd_metadata.jsonl             # Generated document metadata
├── usb_pd_validation_report.xlsx     # Generated validation report
└── README.md                         # This file



## **Requirements**
-Python 3.8+  
-Install dependencies:
--bash
--pdfplumber 
--openpyxl


## **Usage**

### **1. Parse the USB PD PDF**
Run the parser to extract ToC, content, and metadata:

-python comprehensive_usb_parser.py


**Outputs:**
- `usb_pd_toc.jsonl` → Table of Contents entries
- `usb_pd_spec.jsonl` → Parsed sections with text, figures, tables
- `usb_pd_metadata.jsonl` → Document statistics



### **2. Generate Validation Report**
Compare the extracted ToC and parsed content:

-python validation_report_generator.py

**Output:**
- `usb_pd_validation_report.xlsx` → Summary of matches, mismatches, order errors, and counts.



Sample search features:
- Keyword search (`Power`, `Cable`, etc.)
- Filter by section level
- Filter by page range
- View children or full hierarchy path



## **File Formats**
### **JSONL Example – TOC Entry (`usb_pd_toc.jsonl`):**

{"doc_title": "USB Power Delivery Specification Rev X", "section_id": "2.1.2", "title": "Power Delivery Contract Negotiation", "page": 53, "level": 3, "parent_id": "2.1", "full_path": "2.1.2 Power Delivery Contract Negotiation", "tags": ["contracts", "negotiation"]}


### **JSONL Example – Section Entry (`usb_pd_spec.jsonl`):**

{"section_id": "2.1.2", "title": "Power Delivery Contract Negotiation", "content": "Section text...", "page_start": 53, "page_end": 54, "content_type": "text", "tables": [], "figures": [], "subsections": [], "word_count": 245, "tags": ["contracts", "negotiation"]}




## **Validation Report Metrics**
- **Total Sections** – TOC vs Parsed
- **Matched Sections**
- **Missing in Content**
- **Extra in Content**
- **Order Errors** – Page mismatches
- **Tables / Figures Count** – TOC vs Parsed



## **Error Handling**
- Skips empty or non-text pages.
- Warns if required files are missing.
- Handles file path errors.



## **Future Enhancements**
- Gap detection in section numbering (e.g., missing `2.1.3` between `2.1.2` and `2.1.4`).
- OCR support for scanned PDFs.
- Search in content as well as TOC.
