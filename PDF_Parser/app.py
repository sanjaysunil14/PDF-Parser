import json
from pathlib import Path

from src.parser.metadata_extractor import MetadataExtractor
from src.parser.toc_extractor import TOCExtractor
from src.parser.section_extractor import SectionExtractor
from src.validator.section_validator import SectionValidator  # The OOP validator class with XLSX output


def main():
    PROJECT_ROOT = Path(__file__).parent.resolve()
    PDF_PATH = PROJECT_ROOT / "data" / "USB_PD_R3_2 V1_1_2024_10.pdf"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    OUTPUT_DIR.mkdir(exist_ok=True)

    tag_map = {
        "power_delivery": ["power delivery", "pd"],
        "protocol": ["protocol", "message", "communication"],
        "physical_layer": ["physical layer", "phy"],
        "source_sink": ["source", "sink"],
        # Add further tags and keywords as needed
    }

    DOC_TITLE = "USB Power Delivery Specification Rev 3.2 V1.1 2024-10"

    # Step 1: Extract Metadata
    meta_extractor = MetadataExtractor(PDF_PATH, DOC_TITLE)
    metadata = meta_extractor.extract()
    with open(OUTPUT_DIR / "usb_pd_metadata.jsonl", "w", encoding="utf-8") as f:
        f.write(json.dumps(metadata) + "\n")

    # Step 2: Extract TOC (adjust page range as needed)
    toc_extractor = TOCExtractor(PDF_PATH, DOC_TITLE)
    toc_entries = toc_extractor.extract(start_page=13, end_page=18)
    with open(OUTPUT_DIR / "usb_pd_toc.jsonl", "w", encoding="utf-8") as f:
        for entry in toc_entries:
            f.write(json.dumps(entry) + "\n")

    # Step 3: Extract Spec Sections based on TOC entries
    section_extractor = SectionExtractor(PDF_PATH, tag_map)
    spec_sections = section_extractor.extract(toc_entries)
    with open(OUTPUT_DIR / "usb_pd_spec.jsonl", "w", encoding="utf-8") as f:
        for section in spec_sections:
            f.write(json.dumps(section) + "\n")

    print("Metadata, TOC, and Section extraction completed.")

    # Step 4: Validate and generate XLSX report
    toc_file = OUTPUT_DIR / "usb_pd_toc.jsonl"
    spec_file = OUTPUT_DIR / "usb_pd_spec.jsonl"
    validation_report = OUTPUT_DIR / "validation_report.xlsx"

    validator = SectionValidator(toc_file, spec_file, validation_report)
    validator.run()
    print(f"Validation report generated: {validation_report}")


if __name__ == "__main__":
    main()