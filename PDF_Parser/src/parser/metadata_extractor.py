from pathlib import Path
import pdfplumber
import logging
import re
import json

class MetadataExtractor:
    """
    Extracts metadata information from the first page of a USB_PD_specification PDF.
    Attributes:
        pdf_path (Path): Path to the PDF file.
        doc_title (str): Title of the document.
    """

    REQUIRED_FIELDS = ["doc_title", "revision", "version", "release_date", "publisher", "raw_header"]

    def __init__(self, pdf_path: Path, doc_title: str):
        """
        Initialize the extractor with PDF path and document title.
        Arguments:
            pdf_path (Path): The path to the PDF file.
            doc_title (str): The title of the document.
        """
        self.pdf_path = pdf_path
        self.doc_title = doc_title

        # Configure logger
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    def extract(self) -> dict:
        """
        Extract metadata information from the first page of the PDF.
        Returns:
            dict: Metadata details including title, revision, version,
                  release date, publisher, and raw header text.
        """
        first_page_text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                if pdf.pages:
                    first_page_text = pdf.pages[0].extract_text() or ""
                else:
                    logging.warning("PDF has no pages to extract metadata from.")
        except FileNotFoundError as e:
            logging.error(f"File not found: {self.pdf_path} - {e}")
            return {
                "doc_title": self.doc_title,
                "revision": "Unknown",
                "version": "Unknown",
                "release_date": "Unknown",
                "publisher": "USB-IF",
                "raw_header": ""
            }

        except Exception as e:
            logging.error(f"Unexpected error extracting metadata: {e}")
            return {}

        # Extract metadata dynamically using regex
        revision = self._find_pattern(first_page_text, r"Revision\s*:?\s*([\d.]+)", default="Unknown")
        version = self._find_pattern(first_page_text, r"Version\s*:?\s*([\d.]+)", default="Unknown")
        release_date = self._find_pattern(first_page_text, r"Release\s*Date\s*:?\s*([\d\-]+)", default="Unknown")
        metadata = {
            "doc_title": self.doc_title,
            "revision": revision,
            "version": version,
            "release_date": release_date,
            "publisher": "USB-IF",
            "raw_header": first_page_text.strip()
        }

        # Validate schema
        self._validate_metadata(metadata)

        return metadata

    def _find_pattern(self, text: str, pattern: str, default: str = "Unknown") -> str:
        """Utility to find regex pattern in text, returns default if not found."""
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else default

    def _validate_metadata(self, metadata: dict) -> None:
        """Ensure all required fields exist in metadata."""
        missing = [field for field in self.REQUIRED_FIELDS if field not in metadata or not metadata[field]]
        if missing:
            logging.warning(f"Metadata is missing fields: {missing}")

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
    PDF_PATH = PROJECT_ROOT / "data" / "USB_PD_R3_2 V1_1_2024_10.pdf"
    OUTPUT_FILE = PROJECT_ROOT / "output" / "usb_pd_metadata.json"

    extractor = MetadataExtractor(PDF_PATH, "USB Power Delivery Specification Rev 3.2 V1.1 2024-10")
    metadata = extractor.extract()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print("Metadata extraction complete.")
