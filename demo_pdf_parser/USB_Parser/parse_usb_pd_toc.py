import pdfplumber
import re
import json
import os

# Path to your PDF file
PDF_FILE = r"C:\Users\SRUDHI\Desktop\toc assement\USB_Parser\USB.pdf"
# Adjust page indices for your PDF (0-based index)
TOC_FIRST_PAGE_IDX = 12
TOC_LAST_PAGE_IDX = 15

# Document title
DOC_TITLE = "Universal Serial Bus Power Delivery Specification"

# Regex pattern for parsing TOC lines (more forgiving)
toc_line_re = re.compile(
    r"^(\d+(?:\.\d+)*?)\s+(.*?)\s+\.{2,}\s+(\d+)$"
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

def parse_toc_lines(toc_lines):
    """
    Parse raw lines, including handling multi-line entries.
    Returns list of parsed entries, and list of unmatched lines.
    """
    entries = []
    unmatched = []

    buffer_line = ""
    for line in toc_lines:
        # Clean line
        line = line.strip()

        # Check if line looks like a new TOC entry
        match = toc_line_re.match(line)
        if match:
            # If buffer has previous incomplete entry, save or handle accordingly
            if buffer_line:
                # Try parsing previous buffer
                parsed = parse_single_line(buffer_line)
                if parsed:
                    entries.append(parsed)
                else:
                    unmatched.append(buffer_line)
            buffer_line = line
        else:
            # Not matching regex: assume part of previous entry (multi-line)
            buffer_line += " " + line

    # Parse last buffered line
    if buffer_line:
        parsed = parse_single_line(buffer_line)
        if parsed:
            entries.append(parsed)
        else:
            unmatched.append(buffer_line)

    return entries, unmatched

def parse_single_line(line):
    """
    Parse a single TOC line with regex.
    """
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
    """
    Extracts raw lines from specified pages
    """
    toc_lines = []
    with pdfplumber.open(pdf_file) as pdf:
        for i in range(first_page_idx, last_page_idx + 1):
            if i >= len(pdf.pages):
                continue
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                lines = [re.sub(r'\s+', ' ', line.strip()) for line in text.split('\n')]
                toc_lines.extend(lines)
    return toc_lines

def save_unmatched_lines(unmatched_lines, filename="unmatched_lines.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(unmatched_lines))
    print(f"Saved unmatched lines to {filename}")

def main():
    # Check if PDF exists
    if not os.path.isfile(PDF_FILE):
        print(f"Missing PDF file: {PDF_FILE}\nPlease download it and save it as '{PDF_FILE}'.")
        return

    # Extract raw TOC lines
    toc_lines = extract_toc(PDF_FILE, TOC_FIRST_PAGE_IDX, TOC_LAST_PAGE_IDX)
    print(f"Extracted {len(toc_lines)} raw lines from pages {TOC_FIRST_PAGE_IDX}-{TOC_LAST_PAGE_IDX}.")

    # Optional: print first few lines for debugging
    print("Sample extracted lines:")
    for line in toc_lines[:10]:
        print(repr(line))
    print("---")

    # Parse lines, handle multi-line entries
    entries, unmatched = parse_toc_lines(toc_lines)
    print(f"Parsed {len(entries)} TOC entries.")
    if unmatched:
        print(f"{len(unmatched)} lines could not be parsed. Saving for review.")
        save_unmatched_lines(unmatched)

    # Save entries to JSONL
    output_filename = "usb_pd_spec2.jsonl"
    with open(output_filename, "w", encoding="utf-8") as f:
        for e in entries:
            json.dump(e, f, ensure_ascii=False)
            f.write("\n")
    print(f"Saved {len(entries)} entries to {output_filename}.")


if __name__ == "__main__":
    main()
