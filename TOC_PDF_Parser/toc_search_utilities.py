import json
from typing import List, Dict, Optional

class TOCSearchEngine:
    def __init__(self, jsonl_file: str):
        """Initialize search engine with JSONL file"""
        self.entries = []
        self.load_entries(jsonl_file)
        
    def load_entries(self, jsonl_file: str):
        """Load TOC entries from JSONL file"""
        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.entries.append(json.loads(line))
            print(f"Loaded {len(self.entries)} TOC entries")
        except FileNotFoundError:
            print(f"File {jsonl_file} not found")
        except Exception as e:
            print(f"Error loading entries: {e}")
    
    def search_by_keyword(self, keyword: str, fields: List[str] = None) -> List[Dict]:
        """Search entries by keyword in specified fields"""
        if fields is None:
            fields = ["title", "tags", "section_id", "full_path"]
        
        keyword_lower = keyword.lower()
        results = []
        
        for entry in self.entries:
            match_found = False
            match_details = []
            
            for field in fields:
                if field == "tags":
                    matching_tags = [tag for tag in entry["tags"] if keyword_lower in tag.lower()]
                    if matching_tags:
                        match_found = True
                        match_details.append(f"tags: {matching_tags}")
                elif field in entry:
                    if keyword_lower in str(entry[field]).lower():
                        match_found = True
                        match_details.append(f"{field}: {entry[field]}")
            
            if match_found:
                result = entry.copy()
                result["match_details"] = match_details
                results.append(result)
        
        return results
    
    def search_by_level(self, level: int) -> List[Dict]:
        """Get all entries at a specific level"""
        return [entry for entry in self.entries if entry["level"] == level]
    
    def search_by_page_range(self, start_page: int, end_page: int) -> List[Dict]:
        """Get entries within a page range"""
        return [entry for entry in self.entries if start_page <= entry["page"] <= end_page]
    
    def get_children(self, section_id: str) -> List[Dict]:
        """Get direct children of a section"""
        return [entry for entry in self.entries if entry["parent_id"] == section_id]
    
    def get_all_descendants(self, section_id: str) -> List[Dict]:
        """Get all descendants (children, grandchildren, etc.) of a section"""
        descendants = []
        
        def collect_descendants(parent_id):
            children = self.get_children(parent_id)
            for child in children:
                descendants.append(child)
                collect_descendants(child["section_id"])
        
        collect_descendants(section_id)
        return descendants
    
    def get_path_to_root(self, section_id: str) -> List[Dict]:
        """Get the path from a section to the root"""
        path = []
        current_entry = next((entry for entry in self.entries if entry["section_id"] == section_id), None)
        
        while current_entry:
            path.insert(0, current_entry)
            if current_entry["parent_id"]:
                current_entry = next((entry for entry in self.entries if entry["section_id"] == current_entry["parent_id"]), None)
            else:
                break
        
        return path
    
    def get_section_by_id(self, section_id: str) -> Optional[Dict]:
        """Get a specific section by its ID"""
        return next((entry for entry in self.entries if entry["section_id"] == section_id), None)

def demo_search():
    """Demonstrate search functionality"""
    print("\n=== TOC Search Demo ===")
    
    # Initialize search engine
    engine = TOCSearchEngine("usb_pd_toc.jsonl")
    
    if not engine.entries:
        print("No entries loaded. Make sure to run comprehensive_usb_parser.py first!")
        return
    
    # 1. Keyword search
    print("\n1. Search for 'Power':")
    results = engine.search_by_keyword("Power")
    for result in results[:5]:  # Show first 5 results
        print(f"   {result['section_id']} - {result['title']} (Page {result['page']})")
    
    # 2. Level-based search
    print("\n2. All Level 2 Sections:")
    level2_sections = engine.search_by_level(2)
    for section in level2_sections[:5]:  # Show first 5
        print(f"   {section['full_path']}")
    
    # 3. Page range search
    print("\n3. Sections on Pages 50-60:")
    page_results = engine.search_by_page_range(50, 60)
    for section in page_results:
        print(f"   {section['full_path']}")
    
    # 4. Hierarchical navigation
    print("\n4. Children of Section '2':")
    children = engine.get_children("2")
    for child in children:
        print(f"   {child['section_id']} - {child['title']} (Page {child['page']})")
    
    # 5. Path to root
    if engine.entries:
        sample_section = "2.1.1" if any(e["section_id"] == "2.1.1" for e in engine.entries) else engine.entries[0]["section_id"]
        print(f"\n5. Path to Root for Section '{sample_section}':")
        path = engine.get_path_to_root(sample_section)
        for i, section in enumerate(path):
            indent = "   " + "  " * i
            print(f"{indent}{section['section_id']} - {section['title']}")

if __name__ == "__main__":
    demo_search()
