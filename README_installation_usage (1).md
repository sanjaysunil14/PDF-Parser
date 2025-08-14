# USB PD Specification Parsing & Validation System

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/sanjaysunil14/PDF-Parser.git
   cd PDF-Parser
   ```

2. **Create a Virtual Environment** 
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate    # For Windows
   ```

3. **Install Dependencies**
   Make sure you have **Python 3.8+** installed.
   ```bash
   pip install -r requirements.txt
   ```

4. **Place the PDF File**
   Put your USB Power Delivery specification PDF in the project directory *(or update the script path to your PDF)*.

---

## 🚀 Usage

### Run the Table of Contents Parser
Extracts structured TOC, content, and metadata.
```bash
python TOC_PDF_Parser/comprehensive_usb_parser.py --input USB.pdf --output Output_File/
```

### Run Validation
Validates extracted content against predefined rules.
```bash
python TOC_PDF_Parser/validation_report_generator.py --input Output_File/spec.json --report Output_File/usb_pd_validation_report.xlsx
```

### Example Workflow
```bash

python TOC_PDF_Parser/comprehensive_usb_parser.py --input USB.pdf --output Output_File/


python TOC_PDF_Parser/validation_report_generator.py --input Output_File/spec.json --report Output_File/usb_pd_validation_report.xlsx
```

✅ **After running, you will find:**
- Parsed data in `Output_File/`
- Excel validation report in `Output_File/validation_report.xlsx`
