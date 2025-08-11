import json

class TOCSearchEngine:
    def __init__(self, jsonl_file):
        with open(jsonl_file, encoding="utf-8") as f:
            self.entries = [json.loads(line) for line in f]

    def search_by_keyword(self, keyword):
        keyword = keyword.lower()
        return [e for e in self.entries if keyword in e["title"].lower()]

    def filter_by_level(self, level):
        return [e for e in self.entries if e["level"] == level]

    def filter_by_page_range(self, start, end):
        return [e for e in self.entries if start <= e["page"] <= end]

    def get_children(self, section_id):
        return [e for e in self.entries if e["parent_id"] == section_id]

    def get_path_to_root(self, section_id):
        path = []
        current_id = section_id
        lookup = {e["section_id"]: e for e in self.entries}
        while current_id:
            entry = lookup.get(current_id)
            if entry:
                path.insert(0, entry)
                current_id = entry["parent_id"]
            else:
                break
        return path
