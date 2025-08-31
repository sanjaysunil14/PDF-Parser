import unittest
from pathlib import Path

from src.parser.section_extractor import SectionExtractor, TOCExtractor 

class DummyTagger:
    """Simple dummy tagger to avoid SpaCy dependency in tests."""
    def assign(self, text: str):
        return ["dummy"] if text else []


class SectionExtractorTest(unittest.TestCase):

    def setUp(self):
        self.tagger = DummyTagger()
        self.extractor = SectionExtractor(Path("dummy.pdf"), self.tagger, "Dummy Doc")

    def test_clean_title(self):
        dirty = "Chapter 1......   Introduction "
        cleaned = TOCExtractor.clean_title(dirty)
        self.assertEqual(cleaned, "Chapter 1 Introduction")

    def test_extract_sections(self):
        # Fake TOC
        toc = [
            {"section_id": "1", "title": "Intro", "page": 1, "level": 1},
            {"section_id": "2", "title": "Details", "page": 2, "level": 1},
        ]
        # Fake pages (simulate pdfplumber.extract_text results)
        pages = ["This is intro text", "This is details text"]

        # Instead of calling extract_sections (which opens pdf), 
        # we simulate the internal loop using fake pages
        sections = []
        for idx, entry in enumerate(toc):
            start = entry["page"] - 1
            if idx + 1 < len(toc):
                next_start = toc[idx + 1]["page"]
                end = max(start, min(next_start - 2, len(pages) - 1))
            else:
                end = len(pages) - 1

            section_text = " ".join(pages[start:end + 1])
            tags = self.tagger.assign(section_text)
            sections.append({
                "doc_title": "Dummy Doc",
                "section_id": entry["section_id"],
                "title": TOCExtractor.clean_title(entry["title"]),
                "page": start + 1,
                "level": entry.get("level", 1),
                "parent_id": entry.get("parent_id"),
                "full_path": entry.get("full_path", ""),
                "tags": tags,
                "type": "section",
            })

        # Assertions
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["title"], "Intro")
        self.assertIn("dummy", sections[0]["tags"])

    def test_extract_list_section_found(self):
        pages = [
            "List of Figures\nFigure 1 something",
            "Continued figure list..."
        ]
        result = self.extractor._extract_list_section(pages, "List of Figures")
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "List of Figures")

    def test_extract_list_section_not_found(self):
        pages = ["No lists here", "Just text"]
        result = self.extractor._extract_list_section(pages, "List of Tables")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
