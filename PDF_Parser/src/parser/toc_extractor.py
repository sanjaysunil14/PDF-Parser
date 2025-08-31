import re
import json
from pathlib import Path
from PyPDF2 import PdfReader


class TOCExtractor:
    """
    Extract Table of Contents (TOC) sections from a PDF file.
    """

    TOC_REGEX = re.compile(r"^(\d+(?:\.\d+)*)(?:\s+)(.+?)\s*(\d+)?$")

    def __init__(self, pdf_path, start_page, end_page,
                 doc_title="USB PD Specification Rev X"):
        """
        Initialize TOCExtractor.

        Arguments:
            pdf_path: Path to the PDF file.
            start_page: Starting page number (1-based).
            end_page: Ending page number (inclusive).
            doc_title: Document title metadata.
        """
        self.pdf_path = Path(pdf_path)
        self.start_page = start_page
        self.end_page = end_page
        self.doc_title = doc_title
        self.toc_sections = []

    def extract(self):
        """
        Extract TOC sections from the PDF file.

        Returns:
            list[dict]: Extracted TOC section entries.
        """
        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

        reader = PdfReader(str(self.pdf_path))
        num_pages = len(reader.pages)

        if self.start_page < 1 or self.end_page > num_pages:
            raise ValueError(
                f"Page range ({self.start_page}-{self.end_page}) "
                f"out of bounds for {num_pages} pages."
            )

        for page_num in range(self.start_page - 1, self.end_page):
            page = reader.pages[page_num]
            text = page.extract_text() or ""
            for line in text.splitlines():
                self._process_line(line.strip())

        self._sort_toc_sections()
        return self.toc_sections

    def _process_line(self, line):
        """Process a single line of text to extract TOC info."""
        if not line:
            return

        match = self.TOC_REGEX.match(line)
        if not match:
            return

        section_id = match.group(1)
        title = match.group(2).strip()
        title = re.sub(r'(\s*\.\s*)+$', '', title)
        if title.strip('.') == '':
            title = ''

        page_number = int(match.group(3)) if match.group(3) else -1
        level = section_id.count('.') + 1
        parent_id = '.'.join(section_id.split('.')[:-1]) if level > 1 else None
        full_path = f"{section_id} {title}".strip()
        full_path = re.sub(r'(\s*\.\s*)+$', '', full_path)

        self.toc_sections.append(
            {
                "doc_title": self.doc_title,
                "section_id": section_id,
                "title": title,
                "page": page_number,
                "level": level,
                "parent_id": parent_id,
                "full_path": full_path,
            }
        )

    def _sort_toc_sections(self):
        """Sort TOC sections by hierarchical section IDs."""

        def section_id_key(sid):
            return [int(x) for x in sid.split('.')]

        self.toc_sections.sort(key=lambda x: section_id_key(x['section_id']))

    def save_jsonl(self, output_path):
        """
        Save extracted TOC sections to a JSONL file.

        Arguments:
            output_path: Output file path.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding="utf-8") as f:
            for item in self.toc_sections:
                f.write(json.dumps(item) + '\n')

        print(f"TOC extraction completed")


if __name__ == "__main__":
    pdf_file_path = (
        r"D:\.@PLACEMENT\usb_pd_parsers\data\USB_PD_R3_2 V1_1_2024_10.pdf"
    )
    start_page = 13
    end_page = 18

    extractor = TOCExtractor(pdf_file_path, start_page, end_page)

    try:
        toc = extractor.extract()
        extractor.save_jsonl("output/usb_pd_toc.jsonl")
    except (FileNotFoundError, ValueError) as err:
        print(f"Error: {err}")
