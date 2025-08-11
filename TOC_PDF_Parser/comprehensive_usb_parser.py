import pdfplumber
import re
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class ComprehensiveUSBPDParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc_title = "Universal Serial Bus Power Delivery Specification"
        self.toc_entries = []
        self.content_sections = []
        self.metadata = {}
        self.tables = []
        self.figures = []
        
    def extract_toc(self) -> List[Dict]:
        """Extract Table of Contents"""
        toc_entries = []
        toc_patterns = [
            re.compile(r"^(\d+(?:\.\d+)*?)\s+(.+?)\s+\.{2,}\s*(\d+)$"),
            re.compile(r"^(\d+(?:\.\d+)*?)\s+(.+?)\s+(\d+)$")
        ]
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                    
                if "Table of Contents" in text or "Contents" in text:
                    # Extract TOC from this and next few pages
                    for j in range(i, min(i + 10, len(pdf.pages))):
                        pg_text = pdf.pages[j].extract_text()
                        if not pg_text:
                            continue
                            
                        lines = pg_text.split('\n')
                        for line in lines:
                            clean_line = re.sub(r'\s+', ' ', line.strip())
                            if len(clean_line) < 5:
                                continue
                                
                            for pattern in toc_patterns:
                                match = pattern.match(clean_line)
                                if match:
                                    section_id, title, page_num = match.groups()
                                    title = title.rstrip('. ').strip()
                                    level = section_id.count('.') + 1
                                    parent_id = '.'.join(section_id.split('.')[:-1]) if '.' in section_id else None
                                    
                                    entry = {
                                        "section_id": section_id,
                                        "title": title,
                                        "page": int(page_num),
                                        "level": level,
                                        "parent_id": parent_id,
                                        "full_path": f"{section_id} {title}",
                                        "doc_title": self.doc_title,
                                        "tags": self.generate_tags(title)
                                    }
                                    toc_entries.append(entry)
                                    break
                    break
        
        self.toc_entries = toc_entries
        return toc_entries
    
    def extract_all_sections(self) -> List[Dict]:
        """Extract content from all sections in the PDF"""
        content_sections = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            current_section = None
            current_content = ""
            section_pattern = re.compile(r"^(\d+(?:\.\d+)*?)\s+(.+?)$")
            
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if not text:
                    continue
                    
                lines = text.split('\n')
                for line in lines:
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    
                    # Check if this line starts a new section
                    match = section_pattern.match(clean_line)
                    if match and len(clean_line) < 100:  # Likely a section header
                        # Save previous section if exists
                        if current_section:
                            current_section["content"] = current_content.strip()
                            current_section["page_end"] = page_num - 1
                            current_section["word_count"] = len(current_content.split())
                            content_sections.append(current_section)
                        
                        # Start new section
                        section_id, title = match.groups()
                        current_section = {
                            "section_id": section_id,
                            "title": title.strip(),
                            "content": "",
                            "page_start": page_num,
                            "page_end": page_num,
                            "content_type": "text",
                            "tables": [],
                            "figures": [],
                            "subsections": [],
                            "word_count": 0,
                            "tags": self.generate_tags(title)
                        }
                        current_content = ""
                    else:
                        # Add to current section content
                        if current_section:
                            current_content += " " + clean_line
                        
                        # Check for tables
                        if "Table" in clean_line and any(c.isdigit() for c in clean_line):
                            if current_section:
                                table_info = {
                                    "table_id": clean_line,
                                    "caption": clean_line,
                                    "page": page_num,
                                    "data": []
                                }
                                current_section["tables"].append(table_info)
                                self.tables.append(table_info)
                        
                        # Check for figures
                        if "Figure" in clean_line and any(c.isdigit() for c in clean_line):
                            if current_section:
                                figure_info = {
                                    "figure_id": clean_line,
                                    "caption": clean_line,
                                    "page": page_num
                                }
                                current_section["figures"].append(figure_info)
                                self.figures.append(figure_info)
            
            # Don't forget the last section
            if current_section:
                current_section["content"] = current_content.strip()
                current_section["word_count"] = len(current_content.split())
                content_sections.append(current_section)
        
        self.content_sections = content_sections
        return content_sections
    
    def generate_metadata(self) -> Dict:
        """Generate document metadata"""
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
        
        metadata = {
            "document_id": "usb_pd_spec_v1",
            "document_title": self.doc_title,
            "document_version": "1.0",
            "total_pages": total_pages,
            "total_sections": len(self.content_sections),
            "total_tables": len(self.tables),
            "total_figures": len(self.figures),
            "extraction_date": datetime.now().isoformat(),
            "processing_stats": {
                "sections_parsed": len(self.content_sections),
                "sections_failed": 0,
                "tables_extracted": len(self.tables),
                "figures_extracted": len(self.figures)
            },
            "document_structure": {
                "max_depth": max([entry["level"] for entry in self.toc_entries]) if self.toc_entries else 0,
                "level_distribution": self.get_level_distribution(),
                "page_distribution": self.get_page_distribution()
            }
        }
        
        self.metadata = metadata
        return metadata
    
    def generate_tags(self, title: str) -> List[str]:
        """Generate semantic tags from title"""
        keywords = {
            "contract": "contracts", "negotiation": "negotiation", "device": "devices",
            "communication": "communication", "avoidance": "avoidance", "cable": "cable",
            "message": "messages", "partner": "partners", "policy": "policy",
            "power": "power", "voltage": "voltage", "source": "source", "sink": "sink",
            "protocol": "protocol", "data": "data", "control": "control"
        }
        title_lower = title.lower()
        return [tag for keyword, tag in keywords.items() if keyword in title_lower]
    
    def get_level_distribution(self) -> Dict:
        """Get distribution of sections by level"""
        distribution = {}
        for entry in self.toc_entries:
            level = str(entry["level"])
            distribution[level] = distribution.get(level, 0) + 1
        return distribution
    
    def get_page_distribution(self) -> Dict:
        """Get distribution of sections by page ranges"""
        if not self.content_sections:
            return {}
        
        page_ranges = {"1-50": 0, "51-100": 0, "101-200": 0, "201+": 0}
        for section in self.content_sections:
            page = section["page_start"]
            if page <= 50:
                page_ranges["1-50"] += 1
            elif page <= 100:
                page_ranges["51-100"] += 1
            elif page <= 200:
                page_ranges["101-200"] += 1
            else:
                page_ranges["201+"] += 1
        return page_ranges
    
    def save_all_outputs(self):
        """Save all required JSONL files"""
        # 1. usb_pd_toc.jsonl (Table of Contents)
        with open("usb_pd_toc.jsonl", "w", encoding="utf-8") as f:
            for entry in self.toc_entries:
                json.dump(entry, f, ensure_ascii=False)
                f.write("\n")
        
        # 2. usb_pd_spec.jsonl (All content sections)
        with open("usb_pd_spec.jsonl", "w", encoding="utf-8") as f:
            for section in self.content_sections:
                json.dump(section, f, ensure_ascii=False)
                f.write("\n")
        
        # 3. usb_pd_metadata.jsonl (Document metadata)
        with open("usb_pd_metadata.jsonl", "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {len(self.toc_entries)} TOC entries to usb_pd_toc.jsonl")
        print(f"Saved {len(self.content_sections)} content sections to usb_pd_spec.jsonl")
        print(f"Saved metadata to usb_pd_metadata.jsonl")

def main():
    # UPDATE THIS PATH TO YOUR PDF FILE
    pdf_file = r"C:\Users\SRUDHI\Desktop\toc assement\USB_Parser\USB.pdf"
    
    if not os.path.isfile(pdf_file):
        print(f"PDF not found: {pdf_file}")
        return
    
    parser = ComprehensiveUSBPDParser(pdf_file)
    
    print("Extracting Table of Contents...")
    toc_entries = parser.extract_toc()
    
    print("Extracting all content sections...")
    content_sections = parser.extract_all_sections()
    
    print("Generating metadata...")
    metadata = parser.generate_metadata()
    
    print("Saving all outputs...")
    parser.save_all_outputs()
    
    print(f"\nExtraction complete!")
    print(f"- TOC entries: {len(toc_entries)}")
    print(f"- Content sections: {len(content_sections)}")
    print(f"- Tables found: {len(parser.tables)}")
    print(f"- Figures found: {len(parser.figures)}")

if __name__ == "__main__":
    main()
