import pdfplumber
import re
import json
import os

PDF_FILE = r"C:\Users\SRUDHI\Desktop\toc assement\USB_Parser\USB.pdf"  
TOC_FIRST_PAGE_IDX = 12
TOC_LAST_PAGE_IDX = 15

DOC_TITLE = "Universal Serial Bus Power Delivery Specification"


toc_line_re = re.compile(
    r"^(\d+(?:\.\d+)*?)\s+(.+?)\s+\.{0,}\s*(\d+)$"
)

def suggest_tags(title):
    title = title.lower()
    tags = []
    if "contract" in title: tags.append("contracts")
    if "negotiation" in title: tags.append("negotiation")
    if "device" in title: tags.append("devices")
    if "communication" in title: tags.append("communication")
    if "avoidance" in title: tags.append("avoidance")
    if "cable" in title: tags.append("cable")
    if "message" in title: tags.append("messages")
    if "partner" in title: tags.append("partners")
    if "policy" in title: tags.append("policy")
    return tags

def parse_toc_line(line):
    m = toc_line_re.match(line)
    if not m:
        return None
    section_id, title, page = m.groups()
    
    title = title.rstrip('. ').strip()
    level = section_id.count('.') + 1
    parent_id = '.'.join(section_id.split('.')[:-1]) if '.' in section_id else None
    full_path = f"{section_id} {title}"
    return {
        "doc_title": DOC_TITLE,
        "section_id": section_id,
        "title": title,
        "page": int(page),
        "level": level,
        "parent_id": parent_id,
        "full_path": full_path,
        "tags": suggest_tags(title),
    }

def extract_toc(pdf_file, first_page_idx, last_page_idx):
    toc_lines = []
    with pdfplumber.open(pdf_file) as pdf:
        for i in range(first_page_idx, last_page_idx + 1):
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                
                lines = [re.sub(r'\s+', ' ', line.strip()) for line in text.split('\n')]
                toc_lines.extend(lines)
    return toc_lines

def main():
    if not os.path.isfile(PDF_FILE):
        print(f"Missing PDF file: {PDF_FILE}\nPlease download it and save it as '{PDF_FILE}'.")
        return

    toc_lines = extract_toc(PDF_FILE, TOC_FIRST_PAGE_IDX, TOC_LAST_PAGE_IDX)
    entries = []
    unmatched = []
    for line in toc_lines:
        entry = parse_toc_line(line)
        if entry:
            entries.append(entry)
        else:
            
            unmatched.append(line)

    with open("usb_pd_spec1.jsonl", "w", encoding="utf-8") as f:
        for entry in entries:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')

    print(f"Done. Parsed {len(entries)} ToC entries.")
    if unmatched:
        print(f"{len(unmatched)} lines could not be parsed ")

if __name__ == "__main__":
    main()

