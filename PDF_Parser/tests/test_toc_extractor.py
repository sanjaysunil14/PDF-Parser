import unittest
from src.parser.toc_extractor import TOCExtractor
class TOCExtractorSimpleTest(unittest.TestCase):
    def setUp(self):
        self.extractor = TOCExtractor("dummy.pdf", 1, 1, "DocTitle")

    def test_process_line_simple(self):
        line = "1.2 Section Name 5"
        self.extractor._process_line(line)
        self.assertEqual(len(self.extractor.toc_sections), 1)
        entry = self.extractor.toc_sections[0]
        self.assertEqual(entry['section_id'], "1.2")
        self.assertEqual(entry['title'], "Section Name")
        self.assertEqual(entry['page'], 5)
        self.assertEqual(entry['level'], 2)
        self.assertEqual(entry['parent_id'], "1")

    def test_sort_toc_sections_simple(self):
        self.extractor.toc_sections = [
            {"section_id": "2.1"},
            {"section_id": "1"},
            {"section_id": "1.1"},
        ]
        self.extractor._sort_toc_sections()
        sorted_ids = [s['section_id'] for s in self.extractor.toc_sections]
        self.assertEqual(sorted_ids, ["1", "1.1", "2.1"])


if __name__ == "__main__":
    unittest.main()
