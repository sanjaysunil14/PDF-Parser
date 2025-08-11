import pdfplumber
import re
import json
import os

PDF_FILE = r"C:\Users\SRUDHI\Desktop\toc assement\USB_Parser\USB.pdf"
DOC_TITLE = "Universal Serial Bus Power Delivery Specification"

# --- Multiple regex patterns for robustness ---
TOC_PATTERNS = [
    re.compile(r"^(\d+(?:\.\d+)*?)\s+(.+?)\s+\.{2,}\s*(\d+)$"),  # with TOC dots
    re.compile(r"^(\d+(?:\.\d+)*?)\s+(.+?)\s+(\d+)$")            # without dots
]

def suggest_tags(title: str):
    keywords = {
        "contract": "contracts",
        "negotiation": "negotiation",
        "device": "devices",
        "communication": "communication",
        "avoidance": "avoidance",
        "cable": "cable",
        "message": "messages",
        "partner": "partners",
        "policy": "policy",
        "power": "power",
        "voltage": "voltage",
        "source": "source",
        "sink": "sink"
    }
    t_l = title.lower()
    return [tag for k, tag in keywords.items() if k in t_l]

def parse_toc_line(line: str):
    for pattern in TOC_PATTERNS:
        m = pattern.match(line)
        if m:
            section_id, title, page = m.groups()
            title = title.rstrip('. ').strip()
            level = section_id.count('.') + 1
            parent_id = '.'.join(section_id.split('.')[:-1]) if '.' in section_id else None
            return {
                "doc_title": DOC_TITLE,
                "section_id": section_id,
                "title": title,
                "page": int(page),
                "level": level,
                "parent_id": parent_id,
                "full_path": f"{section_id} {title}",
                "tags": suggest_tags(title)
            }
    return None

def extract_toc(pdf_file):
    toc_lines = []
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            if "Table of Contents" in text:
                # Get next few pages until TOC ends
                for j in range(i, min(i + 10, len(pdf.pages))):
                    pg_text = pdf.pages[j].extract_text()
                    for raw in pg_text.split('\n'):
                        line = re.sub(r'\s+', ' ', raw.strip())
                        toc_lines.append(line)
                break
    return toc_lines

def main():
    if not os.path.isfile(PDF_FILE):
        print(f"PDF not found: {PDF_FILE}")
        return

    toc_lines = extract_toc(PDF_FILE)
    entries, unmatched = [], []

    buffer = ""
    for line in toc_lines:
        if re.search(r"\d+$", line):  # ends with page number
            combined = (buffer + " " + line).strip() if buffer else line
            entry = parse_toc_line(combined)
            if entry:
                entries.append(entry)
            else:
                unmatched.append(combined)
            buffer = ""
        else:
            buffer += " " + line

    with open("usb_pd_spec.jsonl", "w", encoding="utf-8") as f:
        for e in entries:
            json.dump(e, f, ensure_ascii=False)
            f.write("\n")

    with open("unmatched_lines.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unmatched))

    print(f"✅ Parsed {len(entries)} TOC entries. Unmatched: {len(unmatched)}")

if __name__ == "__main__":
    main()
