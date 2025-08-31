import unittest
from unittest.mock import mock_open, patch
from pathlib import Path
from src.validator.section_validator import SectionValidator
import logging


class TestSectionValidatorSimple(unittest.TestCase):
    def setUp(self):
        self.validator = SectionValidator(Path("dummy_toc.jsonl"), Path("dummy_spec.jsonl"), Path("dummy.xlsx"))

    @patch("pathlib.Path.open", new_callable=mock_open, read_data='{"section_id": "1", "title": "Intro"}\n{"section_id": "2", "title": "Details"}\n')
    def test_load_jsonl_success(self, mock_file):
        result = self.validator.load_jsonl(self.validator.toc_file)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["section_id"], "1")

    @patch("pathlib.Path.open", new_callable=mock_open, read_data='invalid json\n')
    def test_load_jsonl_failure(self, mock_file):
        with patch("logging.error") as mock_log_error:
            result = self.validator.load_jsonl(self.validator.toc_file)
            self.assertEqual(result, [])
            mock_log_error.assert_called()


if __name__ == "__main__":
    unittest.main()
